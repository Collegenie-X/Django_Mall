# admin.py
from django.contrib import admin
from .models import Product

admin.site.register(Product)  # ✅ 모델을 관리자 페이지에 등록


# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'price')               # 리스트 페이지에 보일 컬럼들
#     search_fields = ('name',)                            # 검색 필드
#     list_filter = ('price',)                             # 필터 사이드바
#     ordering = ('-id',)
