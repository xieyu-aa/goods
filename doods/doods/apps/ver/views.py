from django.shortcuts import render,redirect
from django.views import View
from django.http import HttpResponseForbidden, JsonResponse, HttpResponse
import re
from doods.libs.captcha.captcha import captcha
from django_redis import get_redis_connection
import random
from doods.utils import constanse
from doods.utils.response_code import RET

# 图片验证码
class ImageCode(View):
    def get(self, request, uuid):
        _,text,image_data = captcha.generate_captcha()
        print(text)
        redis_con = get_redis_connection('ver')
        redis_con.set('image%s'%uuid,text,constanse.REDIS_IMAGE_CODE_EXPIRES)
        return HttpResponse(image_data,content_type='image/png')

# 短信验证码
class MsgCode(View):
    def get(self, request, mobile):

        image_code_id = request.GET.get('image_code_id')
        image_code = request.GET.get('image_code')
        if not all([image_code,image_code_id]):
            return JsonResponse({'code':RET.PARAMERR, 'errmsg':'参数错误'})
        if not re.match('1[3-9]\d{9}',mobile):
            return JsonResponse({'code':RET.DATAERR, 'errmsg':'手机格式错误'})
        redis_con = get_redis_connection('ver')
        redis_sms_code = redis_con.get('sms_code%s'%mobile)
        if redis_sms_code:
            return JsonResponse({'code':RET.DBERR, 'errmsg':'不要访问频繁'})
        image_code_t = redis_con.get('image%s'%image_code_id)
        if not image_code_t:
            return JsonResponse({'code':RET.NODATA, 'errmsg':'图片验证码已过期'})
        if image_code.upper() != image_code_t.decode().upper():
            return JsonResponse({'code':RET.DATAERR, 'errmsg':'图片验证码错误'})
        sms_code = '%06d' % random.randint(0, constanse.SMS_CODE_MAX)
        redis_con.set('sms_code%s' % mobile, sms_code, constanse.REDIS_SMS_CODE_EXPIRES)
        from celery_tasks.sms.tasks import send_sms
        send_sms_relust = send_sms.delay(mobile)
        print(type(send_sms_relust))
        print(send_sms_relust.get())
        print(send_sms_relust.result)
        return JsonResponse({'code':RET.OK,'errmsg':'已发送，请接受'})