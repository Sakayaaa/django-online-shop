from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('register/', views.Register.as_view(), name='register'),
    path('profile/', views.ViewProfile.as_view(), name='view-profile'),
    path('edit-profile/', views.EditProfile.as_view(), name='edit-profile'),
]
