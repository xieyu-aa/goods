from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('register/', views.RegisteView.as_view()),
    re_path('usernames/(?P<username>\w{5,20})/count/', views.CheckUsername.as_view()),
    re_path('mobiles/(?P<mobile>1[3-9]\d{9})/count/', views.CheckMobile.as_view()),
    path('info/', views.UserInfoView.as_view()),
    path('addresses/', views.AddressesView.as_view()),
    path('addresses/create/', views.AddressesCreateViewView.as_view()),
    re_path('addresses/(?P<adress_id>\d+)/', views.AddressesUpView.as_view()),
]