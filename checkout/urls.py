from django.urls import path
from . import views

urlpatterns = [
    path('add/<slug:slug>/', views.Add.as_view(), name='add'),
    # path('remove/<slug:slug>/', views.Remove.as_view(), name='remove'),
    path('cart-view/', views.CartView.as_view(), name='cart-view'),
    path('increase-quantity/<slug:slug>/', views.IncreaseQuantity.as_view(), name='increase-quantity'),
    path('decrease-quantity/<slug:slug>/', views.DecreaseQuantity.as_view(), name='decrease-quantity'),
]
