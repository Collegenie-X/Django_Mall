from django.forms import ValidationError
from django.shortcuts import get_object_or_404


from store.models import Problem, UnitType, SectionType

from django_filters import rest_framework as filters

import csv
import re
from math import ceil
from django.db.models import Count, Avg, Q, F, Value, IntegerField, Case, When, Sum
from django.core.exceptions import ValidationError
from django_filters import rest_framework as filters


from functools import reduce
from operator import add


from rest_framework.decorators import api_view, permission_classes


class ProblemFilter(filters.FilterSet):
    problem_type = filters.CharFilter(
        field_name="problem_type", lookup_expr="icontains"
    )
    type = filters.CharFilter(field_name="type", lookup_expr="icontains")
    subject = filters.CharFilter(field_name="subject", lookup_expr="icontains")
    grade = filters.CharFilter(field_name="grade", lookup_expr="icontains")
    search = filters.CharFilter(method="filter_search")
    unit = filters.CharFilter(method="filter_unit")
    detailed_section = filters.CharFilter(method="filter_detailed_section")
    difficulty = filters.CharFilter(method="filter_difficulty")

    # Add the is_free filter
    is_free = filters.BooleanFilter(field_name="is_free")

    class Meta:
        model = Problem
        fields = [
            "problem_type",
            "type",
            "subject",
            "grade",
            "search",
            "unit",
            "detailed_section",
            "difficulty",
            "is_free",
        ]

    def filter_search(self, queryset, name, value):
        words = value.split()
        self.words = words  # Store the list of words in the filter_set instance

        if not words:
            return queryset

        # OR 조건으로 각 단어가 title 또는 description에 포함되는지 필터링
        filter_conditions = Q()
        for word in words:
            filter_conditions |= Q(title__icontains=word)
        queryset = queryset.filter(filter_conditions)

        # 각 단어에 대한 일치 여부를 어노테이션으로 추가
        annotations = {}
        for i, word in enumerate(words):
            annotations[f"match_word_{i}"] = Case(
                When(Q(title__icontains=word), then=Value(1)),
                default=Value(0),
                output_field=IntegerField(),
            )
        queryset = queryset.annotate(**annotations)

        # 일치하는 단어의 수를 합산하여 search_rank 계산
        if len(words) > 0:
            search_rank_expression = reduce(
                add, [F(f"match_word_{i}") for i in range(len(words))], Value(0)
            )
            queryset = queryset.annotate(search_rank=search_rank_expression).order_by(
                "-search_rank"
            )

            # 전체 단어의 50% 이상 일치해야 함
            min_matches = ceil(len(words) / 2)
            queryset = queryset.filter(search_rank__gte=min_matches)

        return queryset

    def filter_unit(self, queryset, name, value):
        # 콤마와 공백을 모두 구분자로 사용하여 유닛 리스트 생성
        unit_list = [u.strip() for u in re.split(r"[,\s]+", value) if u.strip()]
        unit_list = list(set(unit_list))  # 중복 제거

        if not unit_list:
            raise ValidationError("유효한 unit 값을 입력해 주세요.")

        # 유사한 유닛 찾기 (부분 일치)
        similar_units = UnitType.objects.none()
        for unit_name in unit_list:
            similar_units |= UnitType.objects.filter(name__icontains=unit_name)
        similar_units = similar_units.distinct()
        similar_unit_names = similar_units.values_list("name", flat=True)

        if not similar_unit_names:
            raise ValidationError(
                f"유사한 unit 값을 찾을 수 없습니다: {', '.join(unit_list)}"
            )

        # 모든 지정된 유닛을 가진 문제만 필터링 (AND 조건)
        for unit_name in unit_list:
            queryset = queryset.filter(Q(unit__name__icontains=unit_name))

        return queryset

    def filter_detailed_section(self, queryset, name, value):
        # 콤마와 공백을 모두 구분자로 사용하여 상세 섹션 리스트 생성
        section_list = [s.strip() for s in re.split(r"[,\s]+", value) if s.strip()]
        section_list = list(set(section_list))  # 중복 제거

        if not section_list:
            raise ValidationError("유효한 detailed_section 값을 입력해 주세요.")

        # 유사한 상세 섹션 찾기 (부분 일치)
        similar_sections = SectionType.objects.none()
        for section in section_list:
            similar_sections |= SectionType.objects.filter(name__icontains=section)
        similar_sections = similar_sections.distinct()
        similar_section_names = similar_sections.values_list("name", flat=True)

        if not similar_section_names:
            raise ValidationError(
                f"유사한 detailed_section 값을 찾을 수 없습니다: {', '.join(section_list)}"
            )

        # 모든 지정된 상세 섹션을 가진 문제만 필터링 (AND 조건)
        for section_name in section_list:
            queryset = queryset.filter(
                Q(detailed_section__name__icontains=section_name)
            )

        return queryset

    def filter_difficulty(self, queryset, name, value):
        try:
            # 콤마와 공백을 모두 구분자로 사용하여 난이도 리스트 생성
            difficulty_list = [
                int(d.strip())
                for d in re.split(r"[,\s]+", value)
                if d.strip().isdigit()
            ]
            if not difficulty_list:
                raise ValueError
            return queryset.filter(difficulty__in=difficulty_list)
        except ValueError:
            raise ValidationError(
                "유효하지 않은 difficulty 값이 있습니다. 숫자 형태로 입력해 주세요."
            )
