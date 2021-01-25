from django.shortcuts import render,redirect
from django.views import View
from django.http import HttpResponseForbidden, JsonResponse, HttpResponse
from django.contrib.auth import  authenticate, login, logout
from users.models import User

from doods.utils import constanse
from doods.utils.response_code import RET


class UserLoginView(View):
    # get请求
    def get(self, request):
        # 返回登录页面
        return render(request,'login.html')
    # post请求
    def post(self, request):
        # 取参数
        username = request.POST.get('username')
        pwd = request.POST.get('pwd')
        remembered = request.POST.get('remembered')
        if not all([username, pwd]):
            return JsonResponse({'code':RET.PARAMERR, 'errmsg':'参数不全'})
        user = authenticate(username=username,password=pwd)
        if not user:
            return JsonResponse({'code':RET.DBERR, 'errmsg':'用户名或密码错误'})
        login(request,user)

        if remembered == 'on':
            request.session.set_expiry(constanse.REDIS_SESSION_COOKIE_EXPIRES)
        else:
            request.session.set_expiry(0)
        response = redirect('/')
        response.set_cookie('username',username,max_age=constanse.REDIS_SESSION_COOKIE_EXPIRES)
        return response


class LogoutView(View):
    # post请求
    def get(self, request):
        # 删session
        logout(request)
        # 删cookie
        response = redirect('/')
        response.delete_cookie('username')
        return response


