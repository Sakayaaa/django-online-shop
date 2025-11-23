from django.urls import path
from . import views

app_name = 'products'  # namespace: همون اسم اپ

urlpatterns = [
    # Category URLs
    path('categories/', views.Categories.as_view(), name='category_list'),
    path('categories/<slug:slug>/', views.Categories.as_view(), name='category_children'),

    # Product URLs
    path('products/', views.ProductList.as_view(), name='product_list'),
    path('products/<int:pk>/', views.ProductDetail.as_view(), name='product_detail'),
]
