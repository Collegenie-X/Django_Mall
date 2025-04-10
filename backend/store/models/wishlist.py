from django.db import models
from accounts.models import User
from .problem import Problem


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlists")
    problem = models.ForeignKey(
        Problem, on_delete=models.CASCADE, related_name="wishlisted_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "problem")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.problem.title}"
