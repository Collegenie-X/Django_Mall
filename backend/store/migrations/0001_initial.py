# Generated by Django 5.2 on 2025-04-10 02:37

import django.core.files.storage
import django.db.models.deletion
import multiselectfield.db.fields
import store.models.base
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="SectionType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(blank=True, default="", max_length=50, null=True),
                ),
                (
                    "subject",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Math", "Math"),
                            ("Science", "Science"),
                            ("Liberal Arts", "Liberal Arts"),
                            ("English", "English"),
                            ("STEM", "STEM"),
                            ("SAT", "SAT"),
                        ],
                        help_text="* required",
                        max_length=50,
                        null=True,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UnitType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(blank=True, default="", max_length=50, null=True),
                ),
                (
                    "subject",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Math", "Math"),
                            ("Science", "Science"),
                            ("Liberal Arts", "Liberal Arts"),
                            ("English", "English"),
                            ("STEM", "STEM"),
                            ("SAT", "SAT"),
                        ],
                        help_text="* required",
                        max_length=50,
                        null=True,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Problem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        db_index=True,
                        help_text="* 100글자 이내 작성해 주세요.",
                        max_length=100,
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        db_index=True, help_text="* 300글자 이내로 작성해 주세요."
                    ),
                ),
                (
                    "subject",
                    models.CharField(
                        choices=[
                            ("Math", "Math"),
                            ("Science", "Science"),
                            ("Liberal Arts", "Liberal Arts"),
                            ("English", "English"),
                            ("STEM", "STEM"),
                            ("SAT", "SAT"),
                        ],
                        db_index=True,
                        help_text="* required",
                        max_length=50,
                    ),
                ),
                (
                    "problem_type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Normal", "Normal"),
                            ("Premium", "Premium"),
                            ("Best", "Best"),
                        ],
                        default="Normal",
                        max_length=20,
                        null=True,
                    ),
                ),
                (
                    "type",
                    multiselectfield.db.fields.MultiSelectField(
                        choices=[
                            ("Multiple Choice", "Multiple Choice"),
                            ("Short Answer", "Short Answer"),
                            ("Mathematical Modeling", "Mathematical Modeling"),
                            (
                                "Learning Through Discussion",
                                "Learning Through Discussion",
                            ),
                            ("STEAM", "STEAM"),
                            ("Math Puzzle", "Math Puzzle"),
                            ("Math for Literacy", "Math for Literacy"),
                            ("Physics", "Physics"),
                            ("Chemistry", "Chemistry"),
                            ("Biology", "Biology"),
                            ("E.S.S", "E.S.S"),
                            ("Sentence Completion", "Sentence Completion"),
                            ("Text Completion", "Text Completion"),
                            ("Reading Comprehension", "Reading Comprehension"),
                            ("Homeschooling", "Homeschooling"),
                            ("School Classes", "School Classes"),
                            ("Math", "Math"),
                            ("English", "English"),
                        ],
                        default="Short Answer",
                        help_text="* select one or more types",
                        max_length=246,
                    ),
                ),
                (
                    "grade",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Kindergarten", "Kindergarten"),
                            ("USA grade 1", "USA grade 1"),
                            ("USA grade 2", "USA grade 2"),
                            ("USA grade 3", "USA grade 3"),
                            ("USA grade 4", "USA grade 4"),
                            ("USA grade 5", "USA grade 5"),
                            ("USA grade 6", "USA grade 6"),
                            ("USA grade 7", "USA grade 7"),
                            ("USA grade 8", "USA grade 8"),
                            ("Algebra 1", "Algebra 1"),
                            ("Geometry", "Geometry"),
                            ("Algebra 2", "Algebra 2"),
                            ("Trigonometry", "Trigonometry"),
                            ("Precalculus", "Precalculus"),
                            ("High school statistics", "High school statistics"),
                            (
                                "Statistics and probability",
                                "Statistics and probability",
                            ),
                            ("Linear algebra", "Linear algebra"),
                            ("Differential equations", "Differential equations"),
                            ("Multivariable calculus", "Multivariable calculus"),
                            ("AP Calculus BC", "AP Calculus BC"),
                            ("AP Calculus AB", "AP Calculus AB"),
                            ("AP Statistics", "AP Statistics"),
                        ],
                        default=None,
                        max_length=100,
                        null=True,
                    ),
                ),
                (
                    "difficulty",
                    models.IntegerField(
                        choices=[(3, "High"), (2, "Medium"), (1, "Low")],
                        default=1,
                        help_text="* 상 중 하 등급으로 구분됩니다.",
                    ),
                ),
                (
                    "discounted_price",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        default=0,
                        help_text="*달러 기준이며, $1 ~ $100 사이에서 입력해야 합니다.",
                        max_digits=7,
                        null=True,
                    ),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2,
                        default=5.0,
                        help_text="*달러 기준이며, $1 ~ $100 사이에서 입력해야 합니다.",
                        max_digits=7,
                    ),
                ),
                (
                    "is_free",
                    models.BooleanField(
                        default=False, help_text="공짜일 경우에는 선택해 주세요."
                    ),
                ),
                (
                    "is_view",
                    models.BooleanField(
                        db_index=True,
                        default=True,
                        help_text="비공개일때는 체크를 제거해 주세요.",
                    ),
                ),
                (
                    "pages",
                    models.PositiveSmallIntegerField(help_text="* PDF (Pages number)"),
                ),
                (
                    "problems",
                    models.PositiveSmallIntegerField(
                        help_text="* PDF (Problem Numbers)"
                    ),
                ),
                (
                    "file",
                    models.FileField(
                        blank=True,
                        null=True,
                        storage=django.core.files.storage.FileSystemStorage(
                            location="media/"
                        ),
                        upload_to=store.models.base.get_file_upload_path,
                    ),
                ),
                ("updated_date", models.DateTimeField(auto_now=True)),
                ("created_date", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        help_text="* required",
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "detailed_section",
                    models.ManyToManyField(
                        blank=True, related_name="DetailSection", to="store.sectiontype"
                    ),
                ),
                (
                    "unit",
                    models.ManyToManyField(
                        blank=True, related_name="problems", to="store.unittype"
                    ),
                ),
            ],
            options={
                "verbose_name": "Problem",
                "verbose_name_plural": "Problems",
                "ordering": ["-created_date"],
            },
        ),
        migrations.CreateModel(
            name="PreviewImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        help_text="600 X 800 jpg, png, SVG 이미지만 업로드 가능합니다.",
                        null=True,
                        upload_to="images/",
                    ),
                ),
                (
                    "image_url",
                    models.CharField(
                        blank=True,
                        help_text="이미지 URL을 입력하세요.",
                        max_length=200,
                        null=True,
                    ),
                ),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
                (
                    "problem",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="preview_images",
                        to="store.problem",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Wishlist",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "problem",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="wishlisted_by",
                        to="store.problem",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="wishlists",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
                "unique_together": {("user", "problem")},
            },
        ),
    ]
