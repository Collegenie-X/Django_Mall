# store/urls.py

from django.urls import path

# Problem 관련
from store.views.problems import ProblemListCreate, ProblemDetail

# Wishlist 관련
from store.views.wishlist import ToggleWishlistAPIView, UserWishlistListAPIView

# Unit/Section 관련
from store.views.unit_sections import unit_type_list, section_type_list

urlpatterns = [
    # Problem
    path("problems/", ProblemListCreate.as_view(), name="problem-list-create"),
    path("problems/<int:pk>/", ProblemDetail.as_view(), name="problem-detail"),
    # Wishlist
    path(
        "wishlist/toggle/<int:problem_id>/",
        ToggleWishlistAPIView.as_view(),
        name="wishlist-toggle",
    ),
    path("wishlist/", UserWishlistListAPIView.as_view(), name="user-wishlist-list"),
    # Unit / Section
    path("unit-types/", unit_type_list, name="unit_type_list"),
    path("section-types/", section_type_list, name="section_type_list"),
]
