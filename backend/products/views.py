# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated


class ProductListCreateAPIView(APIView):
    """
    GET: 상품 목록 조회
    POST: 상품 생성
    """

    ## 전체 목록 조회
    def get(self, request):

        self.permission_classes = [AllowAny]
        self.check_permissions(request)

        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    ## 상품 생성
    def post(self, request):

        self.permission_classes = [IsAuthenticated]
        self.check_permissions(request)

        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={"result": "성공적으로 생성되었습니다."},
                status=201,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductRetrieveUpdateDeleteAPIView(APIView):
    """
    GET: 특정 상품 상세 조회
    PUT: 상품 전체 수정
    PATCH: 상품 일부 수정
    DELETE: 상품 삭제
    """

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    def get(self, request, pk):
        product = self.get_object(pk)  ### pk 검색에 따른 Product-DB 하나 선택
        if product is None:
            return Response({"detail": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):  ### 전체 수정 
        product = self.get_object(pk)
        if product is None:
            return Response({"detail": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):  ### 부분 수정 
        product = self.get_object(pk)
        if product is None:
            return Response({"detail": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = self.get_object(pk)
        if product is None:
            return Response({"detail": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response(
            {"detail": "Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT
        )
