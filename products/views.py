import openpyxl

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from django.core.cache import cache
from django.http import HttpResponse

from .models import Product
from .serializers import ProductSerializer


class ProductListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer

    def get_queryset(self):
        cached_products = cache.get('product_list')

        if cached_products is None:
            print("Fetching products from the database")
            products = Product.objects.order_by('-created_at')
            serializer = self.serializer_class(products, many=True)
            cache.set('product_list', serializer.data)
            return products
        else:
            print("Fetching products from the cache")

        return cached_products

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductExportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)

        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Product List"
        sheet.append(["ID", "Name", "Price", "Created At"])

        for product_data in serializer.data:
            sheet.append(
                [
                    product_data['id'], product_data['name'],
                    product_data['price'], product_data['created_at']
                ]
            )

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=product_list.xlsx'
        workbook.save(response)
        workbook.close()

        return response
