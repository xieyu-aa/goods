from django.shortcuts import render,redirect
from django.views import View
from django.http import HttpResponseForbidden, JsonResponse, HttpResponse
from .models import Area
from doods.utils.response_code import RET


class AreaView(View):
    # get请求
    def get(self, request):
        area_id = request.GET.get('area_id')
        if not area_id:
            areas = Area.objects.filter(parent=None).all()
            area_lisrt = []
            for area in areas:
                area_lisrt.append({'id':area.id, 'name':area.name})
            return JsonResponse({'code':RET.OK, 'province_list':area_lisrt})

        cities = Area.objects.filter(parent_id=area_id).all()
        city_list = []
        for area in cities:
            city_list.append({'id': area.id, 'name': area.name})
        return JsonResponse({'code': RET.OK, 'sub_data':{'subs': city_list}})

