from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Product
from .serializers import ProductSerializer

from django.core.cache import cache


class ProductListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer

    def get_queryset(self):
        cached_products = cache.get('product_list')

        if cached_products is None:
            products = Product.objects.all()
            serializer = self.serializer_class(products, many=True)
            cache.set('product_list', serializer.data)
            return products

        return cached_products

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
