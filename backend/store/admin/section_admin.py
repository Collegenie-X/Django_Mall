from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from store.models import SectionType


class SectionTypeAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "subject",
        "problem_subject",
        "problem_units",
        "problem_title",
    ]
    list_filter = ["subject"]
    search_fields = ["name"]
    ordering = ["name", "subject"]

    def problem_subject(self, obj):
        subjects = set(p.subject for p in obj.DetailSection.all())
        return ", ".join(subjects) if subjects else "No related subjects"

    def problem_units(self, obj):
        units = set(unit.name for p in obj.DetailSection.all() for unit in p.unit.all())
        return ", ".join(units) if units else "No related units"

    def problem_title(self, obj):
        return (
            mark_safe(
                "  ----(title): ".join(
                    [
                        f'<a href="/admin/store/problem/{p.id}/change/" target="_blank">{p.title}</a>'
                        for p in obj.DetailSection.all()
                    ]
                )
            )
            or "No related titles"
        )

    @admin.action(description="Update Section subject by related Problems")
    def update_section_subject_by_problems(self, request, queryset):
        updated, skipped = 0, 0
        for section in queryset:
            problems = section.DetailSection.all()
            if problems.exists():
                section.subject = problems.first().subject
                section.save()
                updated += 1
            else:
                skipped += 1
        self.message_user(
            request,
            f"{updated}개 subject 업데이트, {skipped}개 건너뜀",
            messages.SUCCESS,
        )

        updated, skipped = 0, 0
        for section in queryset:
            problems = section.DetailSection.all()
            units = set(unit for p in problems for unit in p.unit.all())
            if units:
                section.unit.set(units)
                updated += 1
            else:
                skipped += 1
        self.message_user(
            request, f"{updated}개 unit 업데이트, {skipped}개 건너뜀", messages.SUCCESS
        )

    actions = [update_section_subject_by_problems]
    fieldsets = (
        (None, {"fields": ("name", "subject", "problem_subject", "problem_units")}),
    )
    readonly_fields = ["problem_subject", "problem_units"]
