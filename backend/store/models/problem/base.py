from django.db import models
from django.core.files.storage import FileSystemStorage
from multiselectfield import MultiSelectField
from accounts.models import User
from ..base import *
from ..unit_section import UnitType, SectionType
from .validators import ProblemValidators
from .meta import ProblemMeta

file_storage = FileSystemStorage(location="media/")


class Problem(models.Model):
    # 기본 필드
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="* required")
    title = models.CharField(
        max_length=100, db_index=True, help_text="* 100글자 이내 작성해 주세요."
    )
    description = models.TextField(
        db_index=True, help_text="* 300글자 이내로 작성해 주세요."
    )

    # 분류 관련 필드
    subject = models.CharField(
        max_length=50, help_text="* required", choices=SUBJECT_CHOICES, db_index=True
    )
    problem_type = models.CharField(
        max_length=20, choices=PROBLEM_TYPE, blank=True, null=True, default="Normal"
    )
    type = MultiSelectField(
        choices=TYPE_CHOICES,
        default="Short Answer",
        help_text="* select one or more types",
    )
    grade = models.CharField(
        max_length=100, choices=GRADE_CHOICES, blank=True, null=True, default=None
    )

    # 단위 및 섹션
    unit = models.ManyToManyField(UnitType, related_name="problems", blank=True)
    detailed_section = models.ManyToManyField(
        SectionType, related_name="DetailSection", blank=True
    )

    # 난이도
    difficulty = models.IntegerField(
        choices=DIFFICULTY_CHOICES,
        default=1,
        help_text="* 상 중 하 등급으로 구분됩니다.",
    )

    # 가격 관련 필드
    discounted_price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        blank=True,
        null=True,
        default=0,
        help_text="*달러 기준이며, $1 ~ $100 사이에서 입력해야 합니다.",
    )
    price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=5.00,
        help_text="*달러 기준이며, $1 ~ $100 사이에서 입력해야 합니다.",
    )
    is_free = models.BooleanField(
        default=False, help_text="공짜일 경우에는 선택해 주세요."
    )

    # 표시 관련 필드
    is_view = models.BooleanField(
        default=True, help_text="비공개일때는 체크를 제거해 주세요.", db_index=True
    )

    # PDF 관련 필드
    pages = models.PositiveSmallIntegerField(help_text="* PDF (Pages number)")
    problems = models.PositiveSmallIntegerField(help_text="* PDF (Problem Numbers)")
    file = models.FileField(
        upload_to=get_file_upload_path, storage=file_storage, null=True, blank=True
    )

    # 시간 관련 필드
    updated_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def clean(self):
        ProblemValidators.validate_price(self)
        ProblemValidators.validate_discounted_price(self)

    def total_reviews_score(self):
        """문제의 총 리뷰 점수를 반환합니다."""
        from reviews.models import Review

        reviews = Review.objects.filter(problem=self)
        if not reviews.exists():
            return 0
        total_score = sum(review.rating for review in reviews)
        return round(total_score / reviews.count(), 1)

    def total_comments(self):
        """문제의 총 댓글 수를 반환합니다."""
        from reviews.models import Comment

        return Comment.objects.filter(review__problem=self).count()

    class Meta:
        verbose_name = "Problem"
        verbose_name_plural = "Problems"
        ordering = ["-created_date"]
