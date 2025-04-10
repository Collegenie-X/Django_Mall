from django.db import models
from accounts.models import User
from ..review import Review
from .meta import CommentMeta


class Comment(models.Model):
    # 관계 필드
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # 댓글 내용 필드
    content = models.TextField()

    # 시간 관련 필드
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.review}"

    class Meta(CommentMeta):
        pass
