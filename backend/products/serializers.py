# serializers.py
from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        # fields = ('id', 'name', 'price', 'description') 처럼 명시적으로 적을 수도 있습니다.

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("상품명은 최소 3글자 이상이어야 합니다.")
        return value

    def validate(self, attrs):
        # price가 0원 이하이면 에러 발생
        if attrs.get("price") is not None and attrs["price"] <= 0:
            raise serializers.ValidationError("상품 가격은 0원보다 커야 합니다.")
        return attrs
