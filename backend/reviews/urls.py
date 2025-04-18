# reviews/urls.py

from django.urls import path
from .views import ReviewListCreateAPIView, ReviewDetailAPIView ,CommentListCreateAPIView,CommentRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('<int:problem_id>/problem/', ReviewListCreateAPIView.as_view(), name='review-list-create'),
    path('<int:pk>/', ReviewDetailAPIView.as_view(), name='review-detail'),
   
    
]
