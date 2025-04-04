# store/views/unit_section.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from django.db.models import Prefetch
from store.model import Problem, UnitType, SectionType
from store.serializers import UnitTypeSerializer, SectionTypeSerializer


@api_view(["GET"])
@permission_classes([AllowAny])
def unit_type_list(request):
    """
    모든 UnitType 목록을 가져옵니다.
    """
    problems_prefetch = Prefetch(
        "problems",
        queryset=Problem.objects.filter(is_view=True).only("id", "is_view"),
        to_attr="filtered_problems",
    )

    unit_types = UnitType.objects.all().prefetch_related(problems_prefetch)
    serializer = UnitTypeSerializer(unit_types, many=True, context={"request": request})
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def section_type_list(request):
    """
    모든 SectionType 목록을 가져옵니다.
    """
    problems_prefetch = Prefetch(
        "DetailSection",
        queryset=Problem.objects.filter(is_view=True)
        .only("id", "is_view")
        .prefetch_related(
            Prefetch("unit", queryset=UnitType.objects.only("id", "name", "subject"))
        ),
        to_attr="filtered_problems",
    )

    section_types = SectionType.objects.all().prefetch_related(problems_prefetch)
    serializer = SectionTypeSerializer(
        section_types, many=True, context={"request": request}
    )
    return Response(serializer.data)
