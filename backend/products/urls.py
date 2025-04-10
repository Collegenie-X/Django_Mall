from django.urls import path
from .views import ProductListCreateAPIView, ProductRetrieveUpdateDeleteAPIView

urlpatterns = [
    path(
        "", ProductListCreateAPIView.as_view(), name="product-list-create"
    ),  # 상품 목록 조회 및 생성
    path(
        "<int:pk>/",
        ProductRetrieveUpdateDeleteAPIView.as_view(),
        name="product-detail",
    ),  # 상품 상세 조회, 수정 및 삭제
]
