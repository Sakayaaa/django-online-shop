from django.urls import path
from . import views

urlpatterns = [
    path('add-cart/<slug:slug>/', views.AddCart.as_view(), name='add-cart'),
    path('remove-cart/<slug:slug>/', views.RemoveCart.as_view(), name='remove-cart'),
    path('checkout/show-cart/', views.ShowCart.as_view(), name='show-cart'),
    path('checkout/increase-quantity<slug:slug>/', views.IncreaseQuantity.as_view(), name='increase-quantity'),
    path('checkout/decrease-quantity<slug:slug>/', views.DecreaseQuantity.as_view(), name='decrease-quantity'),
]
