from django.urls import path, include

urlpatterns = [
    path('accounts/', include('accounts.urls')),
    path('checkout/', include('checkout.urls')),
    path('orders/', include('orders.urls')),
    path('products/', include('products.urls')),
]
