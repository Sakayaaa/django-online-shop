from django.urls import path
from . import views

app_name = 'products'  # namespace: همون اسم اپ

urlpatterns = [
    path('category_list/', views.CategoryList.as_view(), name='category_list'),
    path('category_list/<slug:slug>/', views.CategoryList.as_view(), name='category_children'),

    path('product_list/', views.ProductList.as_view(), name='product_list'),
    path('product_list/<int:pk>/', views.ProductDetail.as_view(), name='product_detail'),
]
