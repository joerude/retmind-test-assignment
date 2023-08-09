from django.urls import path
from .views import ProductListView, ProductExportView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/export/', ProductExportView.as_view(), name='product-export-excel'),
]
