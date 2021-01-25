from django.urls import path, re_path
from . import views

urlpatterns = [
    path('login/', views.UserLoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
]

