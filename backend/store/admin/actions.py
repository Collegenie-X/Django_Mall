from django.contrib import messages
from store.models import PreviewImage
from django.conf import settings


# 문제 유형 설정
def make_best(modeladmin, request, queryset):
    updated = queryset.update(problem_type="Best")
    modeladmin.message_user(
        request, f"{updated} problem(s) marked as Best.", messages.SUCCESS
    )


make_best.short_description = "Mark selected problems as Best"


def make_premium(modeladmin, request, queryset):
    updated = queryset.update(problem_type="Premium")
    modeladmin.message_user(
        request, f"{updated} problem(s) marked as Premium.", messages.SUCCESS
    )


make_premium.short_description = "Mark selected problems as Premium"


def make_normal(modeladmin, request, queryset):
    updated = queryset.update(problem_type="Normal")
    modeladmin.message_user(
        request, f"{updated} problem(s) marked as Normal.", messages.SUCCESS
    )


make_normal.short_description = "Mark selected problems as Normal"


# 프리뷰 이미지 자동 지정
def update_preview_images_by_subject_static(modeladmin, request, queryset):
    subject_to_static_image = {
        "English": "images/English.jpg",
        "Liberal Arts": "images/Liberal_Art.jpg",
        "Math": "images/Math.jpg",
        "SAT_English": "images/SAT_English.jpg",
        "SAT_Math": "images/SAT_Math.jpg",
        "Science": "images/Science.jpg",
        "STEM": "images/STEM.jpg",
    }
    updated_count = 0
    skipped_count = 0

    for problem in queryset:
        subject = problem.subject
        if subject == "SAT":
            image_path = subject_to_static_image.get(
                "SAT_Math" if "Math" in problem.type else "SAT_English"
            )
        else:
            image_path = subject_to_static_image.get(subject)

        if image_path:
            problem.preview_images.all().delete()
            PreviewImage.objects.create(problem=problem, image_url=image_path)
            updated_count += 1
        else:
            skipped_count += 1
            modeladmin.message_user(
                request,
                f"'{problem}'의 주제 '{subject}'에 매핑된 이미지가 없습니다.",
                messages.WARNING,
            )

    message = f"{updated_count}개 문제 업데이트 완료."
    if skipped_count:
        message += f" {skipped_count}개 문제는 매핑 실패."
    modeladmin.message_user(request, message, messages.SUCCESS)


update_preview_images_by_subject_static.short_description = (
    "Static preview image 자동 지정"
)


# 프리뷰 이미지 삭제
def delete_preview_images(modeladmin, request, queryset):
    deleted_count = 0
    for problem in queryset:
        deleted_count += problem.preview_images.count()
        problem.preview_images.all().delete()
    modeladmin.message_user(
        request, f"{deleted_count} preview images deleted.", messages.SUCCESS
    )


delete_preview_images.short_description = "선택된 문제의 preview 이미지 삭제"


# is_free 토글
def toggle_is_free(modeladmin, request, queryset):
    updated = 0
    for problem in queryset:
        problem.is_free = not problem.is_free
        problem.save()
        updated += 1
    modeladmin.message_user(
        request, f"{updated}개 문제의 무료 여부를 변경했습니다.", messages.SUCCESS
    )


toggle_is_free.short_description = "Toggle is_free status"


# is_view 토글
def toggle_is_view(modeladmin, request, queryset):
    updated = 0
    for problem in queryset:
        problem.is_view = not problem.is_view
        problem.save()
        updated += 1
    modeladmin.message_user(
        request, f"{updated}개 문제의 visibility를 변경했습니다.", messages.SUCCESS
    )


toggle_is_view.short_description = "Toggle is_view status"
