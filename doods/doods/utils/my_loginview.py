from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

class MyView(LoginRequiredMixin, View):
    login_url = '/login/'  # 未登录跳转地址
    redirect_field_name = 'redirect_to'  # 查询参数记录来源页面