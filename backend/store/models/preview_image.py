from django.db import models
from django.core.exceptions import ValidationError
from .base import get_image_upload_path
import os


class PreviewImage(models.Model):
    problem = models.ForeignKey(
        "Problem", on_delete=models.CASCADE, related_name="preview_images"
    )
    image = models.ImageField(
        upload_to="images/",
        null=True,
        blank=True,
        help_text="600 X 800 jpg, png, SVG 이미지만 업로드 가능합니다.",
    )
    image_url = models.CharField(
        max_length=200, null=True, blank=True, help_text="이미지 URL을 입력하세요."
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Preview Image for {self.problem.title}"

    def clean(self):
        if not self.image and not self.image_url:
            raise ValidationError("이미지를 업로드하거나 이미지 URL을 입력해야 합니다.")
        if self.image and self.image_url:
            raise ValidationError(
                "이미지를 업로드하거나 이미지 URL 중 하나만 선택해야 합니다."
            )
        if self.image:
            ext = os.path.splitext(self.image.name)[1].lower()
            if ext not in [".jpg", ".jpeg", ".png", ".svg"]:
                raise ValidationError(
                    "지원되지 않는 파일 형식입니다. jpg, jpeg, png, svg만 가능합니다."
                )
        if self.image_url:
            ext = os.path.splitext(self.image_url)[1].lower()
            if ext not in [".jpg", ".jpeg", ".png", ".svg"]:
                raise ValidationError(
                    "지원되지 않는 파일 형식입니다. jpg, jpeg, png, svg만 가능합니다."
                )
