from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from django.db import models
from django.forms import SelectMultiple
from django.conf import settings
from store.model import Problem, PreviewImage
from .inlines import PreviewImageInline


from .actions import (
    make_best,
    make_premium,
    make_normal,
    update_preview_images_by_subject_static,
    delete_preview_images,
    toggle_is_free,
    toggle_is_view,
)


class ProblemAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {"widget": SelectMultiple(attrs={"size": "15"})},
    }
    inlines = [PreviewImageInline]

    def display_preview_images(self, obj):
        images = obj.preview_images.all()
        tags = []
        for i in images:
            url = (
                i.image.url
                if i.image and hasattr(i.image, "url")
                else settings.MEDIA_URL + i.image_url if i.image_url else None
            )
            tags.append(
                f'<img src="{url}" width="60" height="80" />' if url else "No Image"
            )
        return mark_safe(" ".join(tags)) if tags else "No Images"

    def display_units(self, obj):
        return ", ".join([f"{u.name} ({u.subject})" for u in obj.unit.order_by("name")])

    def display_detailed_sections(self, obj):
        return ", ".join(
            [f"{s.name} ({s.subject})" for s in obj.detailed_section.order_by("name")]
        )

    display_units.short_description = "Units"
    display_detailed_sections.short_description = "Sections"

    # actions 생략 → 기존 코드 그대로 붙여넣기 가능

    list_display = [
        "id",
        "display_preview_images",
        "is_free",
        "is_view",
        "problem_type",
        "subject",
        "price",
        "discounted_price",
        "user",
        "title",
        "grade",
        "type",
        "display_units",
        "display_detailed_sections",
        "pages",
        "problems",
        "created_date",
        "updated_date",
        "file",
    ]
    fieldsets = (
        ("User Info", {"fields": ("user", "is_view")}),
        ("Problem Info", {"fields": ("problem_type",)}),
        ("Subject", {"fields": ("subject", "type", "grade")}),
        ("Category", {"fields": ("unit", "detailed_section")}),
        ("Difficulty", {"fields": ("difficulty",)}),
        ("Contents", {"fields": ("title", "description")}),
        (
            "Etc",
            {"fields": ("price", "discounted_price", "is_free", "pages", "problems")},
        ),
        ("Files", {"fields": ("file",)}),
    )
    search_fields = ["user__username", "title", "description"]
    list_filter = [
        "is_view",
        "grade",
        "subject",
        "problem_type",
        "price",
        "discounted_price",
        "type",
        "unit",
        "detailed_section",
        "difficulty",
        "pages",
        "problems",
    ]
    ordering = ["-created_date", "-updated_date"]

    actions = [
        make_best,
        make_premium,
        make_normal,
        update_preview_images_by_subject_static,
        delete_preview_images,
        toggle_is_free,
        toggle_is_view,
    ]
    # readonly_fields = [
    #     "display_preview_images",
    #     "created_date",
    #     "updated_date",
    #     "display_units",
    #     "display_detailed_sections",
    # ]
