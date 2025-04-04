from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from store.model import UnitType


class UnitTypeAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "subject", "problem_subject", "problem_title"]
    list_filter = ["subject"]
    search_fields = ["name"]
    ordering = ["name", "subject"]

    def problem_subject(self, obj):
        subjects = set(p.subject for p in obj.problems.all())
        return ", ".join(subjects) if subjects else "No related subjects"

    def problem_title(self, obj):
        return (
            mark_safe(
                "  ----(title): ".join(
                    [
                        f'<a href="/admin/store/problem/{p.id}/change/" target="_blank">{p.title}</a>'
                        for p in obj.problems.all()
                    ]
                )
            )
            or "No related titles"
        )

    @admin.action(description="Update Unit subject by related Problems")
    def update_unit_subject_by_problems(self, request, queryset):
        updated, skipped = 0, 0
        for unit in queryset:
            problems = unit.problems.all()
            if problems.exists():
                unit.subject = problems.first().subject
                unit.save()
                updated += 1
            else:
                skipped += 1
                self.message_user(
                    request, f"Unit '{unit.name}' 건너뜀", messages.WARNING
                )
        msg = f"{updated}개 업데이트 / {skipped}개 건너뜀"
        self.message_user(request, msg, messages.SUCCESS)

    actions = [update_unit_subject_by_problems]
    fieldsets = ((None, {"fields": ("name", "subject", "problem_subject")}),)
    readonly_fields = ["problem_subject"]
