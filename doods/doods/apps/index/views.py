from django.shortcuts import render,redirect
from django.views import View
from django.http import HttpResponseForbidden, JsonResponse, HttpResponse

from users.models import User


class IndexView(View):
    # get请求
    def get(self, request):
        # 返回首页
        return render(request,'index.html')
    # post请求

