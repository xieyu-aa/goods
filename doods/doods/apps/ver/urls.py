from django.urls import path, include, re_path
from . import views

urlpatterns = [
    re_path('image_codes/(?P<uuid>.+)/', views.ImageCode.as_view()),
    re_path('sms_codes/(?P<mobile>\d+)/', views.MsgCode.as_view())
]