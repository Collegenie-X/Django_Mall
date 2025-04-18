from django.db import models
from accounts.models import User
from store.models import Problem
from .choices import RATING_CHOICES
from .meta import ReviewMeta


class Review(models.Model):
    # 관계 필드
    user = models.ForeignKey(User, 
                             on_delete=models.CASCADE, 
                             related_name="reviews")
    problem = models.ForeignKey(
                        Problem, 
                        on_delete=models.CASCADE, 
                        related_name="reviews"
    )

    # 리뷰 내용 필드
    rating = models.IntegerField(choices=RATING_CHOICES, default=0)
    comment = models.TextField(blank=True, null=True)

    # 시간 관련 필드
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} /(title): {self.problem.title} /(rating):{self.rating}"

    class Meta(ReviewMeta):
        pass
