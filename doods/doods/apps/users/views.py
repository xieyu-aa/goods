import json

from django.shortcuts import render,redirect
from django.views import View
from django.http import HttpResponseForbidden, JsonResponse, HttpResponse
import re
from users.models import User,Address
from django_redis import get_redis_connection

# 功能：注册
# 请求路径：/user/register/
# 请求方式： get，post
# 参数： post请求携带
# 响应：get返回模板，post重定向到首页
from doods.utils.my_loginview import MyView
from doods.utils.response_code import RET


class RegisteView(View):
    # get请求
    def get(self, request):
        # 返回注册页面
        return render(request,'register.html')
    # post请求
    def post(self, request):
        # 取参数
        user_name = request.POST.get('user_name')
        pwd = request.POST.get('pwd')
        cpwd = request.POST.get('cpwd')
        phone = request.POST.get('phone')
        smg_code = request.POST.get('msg_code')
        allow = request.POST.get('allow')
        # 校验参数
        if not all([user_name,pwd,cpwd,phone,smg_code,allow]):
            return JsonResponse({'code':RET.PARAMERR, 'errmsg':'参数不全'})
        if pwd != cpwd:
            return JsonResponse({'code':RET.DATAERR, 'errmsg':'密码不相同'})
        if not re.match(r'^1[3-9]\d{9}$',phone):
            return JsonResponse({'code':RET.DATAERR, 'errmsg':'手机格式不对'})
        if allow != 'on':
            return JsonResponse({'code':RET.NODATA, 'errmsg':'请勾选协议'})
        redis_con = get_redis_connection('ver')
        redis_sms_code = redis_con.get('sms_code%s'%phone)
        if not redis_sms_code:
            return JsonResponse({'code':RET.NODATA, 'errmsg':'短信验证吗过期了'})
        if smg_code != redis_sms_code.decode():
            return JsonResponse({'code':RET.DATAERR, 'errmsg':'短信验证码错误'})
        user = User.objects.create_user(username=user_name, password=pwd, mobile=phone)
        # 保存到数据库
        # 返回响应
        return redirect('/login')


# 判断用户名存在
class CheckUsername(View):
    def get(self, request,username):
        count = User.objects.filter(username=username).count()

        return JsonResponse({'count':count,'code':RET.OK})

# 判断手机号
class CheckMobile(View):
    def get(self, request,mobile):
        count = User.objects.filter(mobile=mobile).count()

        return JsonResponse({'count':count,'code':RET.OK})

# 返回个人信息
class UserInfoView(MyView):
    # get请求
    def get(self, request):
        data = {
            'username':request.user.username,
            'mobile':request.user.mobile,
            'email':request.user.email
        }
        return render(request,'user_center_info.html', data)

# 返回个人收货地址
class AddressesView(MyView):
    # get请求
    def get(self, request):
        addressess = Address.objects.filter(user_id=request.user.id).all()
        addresses = []
        for address in addressess:
            data = {
                'title': address.title,
                'receiver': address.receiver,
                'province': address.province.name,
                'city': address.city.name,
                'district': address.district.name,
                'place': address.place,
                'city_id': address.city_id,
                'district_id': address.district_id,
                'province_id': address.province_id,
                'mobile': address.mobile,
                'email': address.email,
                'tel': address.tel
            }
            addresses.append(data)
        data_dict = {'addresses':addresses}
        return render(request,'user_center_site.html', data_dict)

# 新增收货地址
class AddressesCreateViewView(MyView):
    # post请求
    def post(self, request):
        data_dict = json.loads(request.body.decode())
        title = data_dict.get('title')
        receiver = data_dict.get('receiver')
        province_id = data_dict.get('province_id')
        city_id = data_dict.get('city_id')
        district_id = data_dict.get('district_id')
        place = data_dict.get('place')
        mobile = data_dict.get('mobile')
        tel = data_dict.get('tel')
        email = data_dict.get('email')

        if not all([title,receiver,province_id,city_id,district_id,place,mobile,tel,email]):
            return JsonResponse({'code':RET.PARAMERR,'errmsg':'参数不全'})
        data_dict['user_id'] = request.user.id
        address = Address.objects.create(**data_dict)
        data = {
            'title': address.title,
            'receiver': address.receiver,
            'province': address.province.name,
            'city': address.city.name,
            'district': address.district.name,
            'place': address.place,
            'city_id': address.city_id,
            'district_id': address.district_id,
            'province_id': address.province_id,
            'mobile': address.mobile,
            'email': address.email,
            'tel': address.tel
        }

        return JsonResponse({'code':RET.OK,'address':data})


# 修改地址
class AddressesUpView(MyView):
    # post请求
    def put(self, request,adress_id):
        data_dict = json.loads(request.body.decode())
        title = data_dict.get('title')
        receiver = data_dict.get('receiver')
        province_id = data_dict.get('province_id')
        city_id = data_dict.get('city_id')
        district_id = data_dict.get('district_id')
        place = data_dict.get('place')
        mobile = data_dict.get('mobile')
        tel = data_dict.get('tel')
        email = data_dict.get('email')

        if not all([title,receiver,province_id,city_id,district_id,place,mobile,tel,email]):
            return JsonResponse({'code':RET.PARAMERR,'errmsg':'参数不全'})
        del data_dict['id']
        del data_dict['district']
        del data_dict['city']
        del data_dict['province']
        ret = Address.objects.filter(id=adress_id).update(**data_dict)
        address = Address.objects.filter(id=adress_id)
        data = {
            'title': address.title,
            'receiver': address.receiver,
            'province': address.province.name,
            'city': address.city.name,
            'district': address.district.name,
            'place': address.place,
            'city_id': address.city_id,
            'district_id': address.district_id,
            'province_id': address.province_id,
            'mobile': address.mobile,
            'email': address.email,
            'tel': address.tel
        }

        return JsonResponse({'code':RET.OK,'address':data})


