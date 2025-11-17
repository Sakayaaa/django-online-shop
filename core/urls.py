from django.urls import path, include

urlpatterns = [
    path('accounts/', include('accounts.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('products/', include('products.urls')),
]
