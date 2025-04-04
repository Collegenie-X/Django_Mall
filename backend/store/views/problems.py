# store/views/problems.py

import logging
import re
from math import ceil
from functools import reduce
from operator import add

from django.db.models import Count, Avg, Q, F, Value, IntegerField, Case, When, Sum
from django.db.models import Prefetch
from django.core.exceptions import ValidationError
from django.forms import ValidationError as DjangoFormValidationError

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters

from store.serializers import ProblemSerializer
from store.model import Problem
from store.views.filters import ProblemFilter  # (※ Filter 클래스를 별도 파일로 빼도 됨)

logger = logging.getLogger(__name__)


# ----------------------------------------
# (A) 필터 & 페이지네이션
# ----------------------------------------
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


# ----------------------------------------
# (B) ProblemListCreate 뷰
# ----------------------------------------
class ProblemListCreate(generics.ListAPIView):
    serializer_class = ProblemSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ProblemFilter
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = Problem.objects.filter(is_view=True)

        problem_type = self.request.query_params.get("problem_type")
        if problem_type in ["Best", "Premium"]:
            # 랜덤 정렬
            return queryset.filter(problem_type=problem_type).order_by("?")
        else:
            return queryset.order_by("-created_date")

    def get_permissions(self):
        # GET/PUT 이외에는 인증 필요하게 할 수도 있음
        if self.request.method in ["GET", "PUT"]:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def list(self, request, *args, **kwargs):
        try:
            # 필터 파라미터가 하나라도 있는지 확인
            filter_params = [
                "problem_type",
                "subject",
                "grade",
                "search",
                "unit",
                "detailed_section",
                "difficulty",
                "is_free",
                "type",
            ]
            filter_present = any(
                request.query_params.get(param) for param in filter_params
            )

            page = request.query_params.get("page")
            page_size = request.query_params.get("page_size")

            # 필터/페이징이 없으면 전체 반환 (페이징 X)
            if not filter_present and not page and not page_size:
                queryset = self.get_queryset()
                serializer = self.get_serializer(queryset, many=True)
                serialized_data = serializer.data

                # search_rank가 있는 경우 추가
                search = request.query_params.get("search")
                if search:
                    for idx, problem in enumerate(queryset):
                        serialized_data[idx]["search_rank"] = getattr(
                            problem, "search_rank", None
                        )

                response_data = {"count": queryset.count(), "results": serialized_data}
                return Response(response_data, status=status.HTTP_200_OK)

            # 필터 파라미터나 페이지네이션이 있으면 페이징 처리
            queryset = self.filter_queryset(self.get_queryset())
            page_qs = self.paginate_queryset(queryset)
            if page_qs is not None:
                serializer = self.get_serializer(page_qs, many=True)
                serialized_data = serializer.data

                # search_rank가 있는 경우 matched_words 추가
                search = request.GET.get("search")
                if search:
                    words = search.split()
                    for idx, problem in enumerate(page_qs):
                        serialized_data[idx]["matched_words"] = [
                            word
                            for i, word in enumerate(words)
                            if getattr(problem, f"match_word_{i}", 0)
                        ]

                return self.get_paginated_response(serialized_data)

            # 페이징 필요 없으면 일반 응답
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        except ValidationError as ve:
            logger.error(f"Validation 오류: {ve}")
            return Response({"detail": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except DjangoFormValidationError as form_ve:
            logger.error(f"Form Validation 오류: {form_ve}")
            return Response(
                {"detail": str(form_ve)}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"예상치 못한 오류: {e}")
            return Response(
                {"detail": "데이터 처리 중 오류가 발생했습니다."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get_paginated_response(self, data):
        return Response(
            {
                "parameters": {
                    "problem_type": self.request.GET.get("problem_type"),
                    "subject": self.request.GET.get("subject"),
                    "grade": self.request.GET.get("grade"),
                    "search": self.request.GET.get("search"),
                    "unit": self.request.GET.get("unit"),
                    "is_free": self.request.GET.get("is_free"),
                    "detailed_section": self.request.GET.get("detailed_section"),
                    "difficulty": self.request.GET.get("difficulty"),
                    "type": self.request.GET.get("type"),
                },
                "count": self.paginator.page.paginator.count,
                "num_pages": self.paginator.page.paginator.num_pages,
                "current_page": self.paginator.page.number,
                "page_size": len(data),  # 실제 페이지 내 항목 수
                "results": data,
            }
        )


# ----------------------------------------
# (C) ProblemDetail 뷰
# ----------------------------------------
class ProblemDetail(APIView):
    def get_permissions(self):
        if self.request.method in ["PUT", "DELETE"]:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_object(self, pk):
        return get_object_or_404(Problem, pk=pk)

    def get(self, request, pk, format=None):
        problem = self.get_object(pk)
        serializer = ProblemSerializer(problem, context={"request": request})
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        problem = self.get_object(pk)
        if problem.user != request.user:
            return Response(
                {"detail": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN
            )
        serializer = ProblemSerializer(
            problem, data=request.data, partial=True, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
