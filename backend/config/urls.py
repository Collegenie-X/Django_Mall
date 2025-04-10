from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static  # 추가

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/accounts/", include("accounts.urls")),
    path("api/v1/store/", include("store.urls")),
    path("api/v1/products/", include("products.urls")),
    path("api/v1/reviews/", include("reviews.urls")),
]

# DEBUG 모드에서 정적/미디어 파일 서빙
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Static도 직접 local에서 서빙하려면 아래도 사용(필요 시)
    # urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(settings.BASE_DIR, "static"))
