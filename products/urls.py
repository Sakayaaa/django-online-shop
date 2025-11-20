from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.Categories.as_view(), name='categories'),
    path('categories/<slug:slug>/', views.Categories.as_view(), name='category_children'),
]
