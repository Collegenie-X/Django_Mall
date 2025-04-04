# store/views/wishlist.py

from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from store.model import Problem, Wishlist
from store.serializers import ProblemSerializer


class ToggleWishlistAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, problem_id):
        user = request.user
        problem = get_object_or_404(Problem, id=problem_id)

        wishlist_item, created = Wishlist.objects.get_or_create(
            user=user, problem=problem
        )

        if created:
            message = "Added to wishlist."
            is_wished = True
        else:
            wishlist_item.delete()
            message = "Removed from wishlist."
            is_wished = False

        return Response(
            {"message": message, "is_wished": is_wished}, status=status.HTTP_200_OK
        )


class UserWishlistListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        wishlists = Wishlist.objects.filter(user=user).select_related("problem")
        problems = [wishlist.problem for wishlist in wishlists]
        serializer = ProblemSerializer(
            problems, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
