from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    tags = serializers.StringRelatedField(many=True, allow_empty=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'category_name', 'price', 'created_at', 'tags']
