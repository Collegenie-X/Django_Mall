from django.conf import settings
from django.utils.safestring import mark_safe
from django.contrib import admin
from store.model import PreviewImage


class PreviewImageInline(admin.TabularInline):
    model = PreviewImage
    extra = 1
    fields = ("image", "image_url", "image_tag")
    readonly_fields = ("image_tag",)
    can_delete = True
    show_change_link = True

    def image_tag(self, obj):
        if obj.image and hasattr(obj.image, "url"):
            img_url = obj.image.url
        elif obj.image_url:
            img_url = settings.MEDIA_URL + obj.image_url
        else:
            img_url = None
        return (
            mark_safe(f'<img src="{img_url}" width="150" height="150" />')
            if img_url
            else "No Image"
        )
