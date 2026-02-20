from django.urls import path
from . import views

urlpatterns = [
    path('show-cart/', views.ShowCart.as_view(), name='show-cart'),
    path('add-to-cart/<>', views)
]
