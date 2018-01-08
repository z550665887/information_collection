
# coding=utf8
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render
from django.db import models
from django.utils.timezone import now, timedelta
import datetime
import time
from django.db.models import Q
from collections import OrderedDict
import random
from collections import deque
import json
import base64
import traceback
from .models import information
from .models import mysql
from ipware.ip import get_ip
import os
def show(request):
    message = information.objects.all()
    # message = information.objects.filter(IP  = '10.50.6.195')
    # print (message)
    message2 = []
    print (request.get_full_path())
    # for i in message:
    #     # message2.append(json.loads(i.information.replace('deque','').replace("'",'"').replace('(','').replace(')','')))
    #     # print(i.information.replace("can't",'can.t').replace("'",'"'))
    #     message2.append(json.loads(i.information.replace("can't",'can.t').replace("'",'"')))
    # f=render(request, 'index.html', {'message': message2})
    # return f
    message3 = []
    for i in message:
        message3.append([json.loads(i.information.replace("can't",'can.t').replace("'",'"'))['int_ip'],json.loads(i.information.replace("can't",'can.t').replace("'",'"'))['sn']])
    num = 0
    print (message3)
    # for i in message3:
    #     print (i)
    #     if 'VMWARE' in i[1]['model']:
    #         num+=1
    f=render(request, 'index2.html', {'message': message3,'num':num})
    return f
    # request.path_info = '/show/'
    # request.path = '/show/'
    # print (request.META)
    # print(request.content_type)
    # # print(request.COOKIES)
    # print(dir(f))
    # print(request.GET)
    # print(request.POST)
    # print(request.COOKIES)
    # print(request.META)
    # print(request.FILES)
    # print(request.path)
    # print(request.path_info)
    # print(request.method)
    # print(request.resolver_match)
    # print(request._post_parse_error)
    # print(request.content_type)
    # print(request.content_params)
    #
    # print(f._headers)
        # if i['server_product'] == "VMware" or i['server_product'] == "VMware, Inc.":
        #     if i['memory_size'] and i['server_sn'] and i ['server_product'] and i['server_type'] and i['cpu_rart'] and i ['cpu_size']\
        #         and i['cpu_name'] and i['physical_number'] and i['cpu_processor'] and i['system_node'] and i['system_sys_verson'] and i['system_machine']\
        #         and i['system_release'] and i['system_sys_name'] and i['system_sys_code'] and i['network_ip'] and i['network_name'] and i['network_mac']\
        #         and i['disk']:
        #         pass
        #     else:
        #         message2.append(i)
        # else:
        #     if i['memory_size'] and i['server_sn'] and i ['server_product'] and i['server_type'] and i['cpu_rart'] and i ['cpu_size']\
        #         and i['cpu_name'] and i['physical_number'] and i['cpu_processor'] and i['system_node'] and i['system_sys_verson'] and i['system_machine']\
        #         and i['system_release'] and i['system_sys_name'] and i['system_sys_code'] and i['network_ip'] and i['network_name'] and i['network_mac']\
        #         and i['disk'] and i['memory_sn'] and i['memory_type']:
        #         pass
        #     else:
        #         message2.append(i)

def setting(request):
    # if request.GET['ip']:
    #     # configs=FindHost(request.GET['ip'])
    #     return HttpResponse(configs[0].services[1])
    return HttpResponse()

def testapi(request):
    # if get_ip(request) == "10.90.3.182":
    #     print(get_ip(request))
    #     print(dir(request.POST))
    #     print(request.POST.keys())
    #     print(request.POST['information'])
    # print(request.body)
    if 'information' in request.POST:
        # print(get_ip(request))
        # print(request.POST['information'])
        IP = information.objects.filter(IP=get_ip(request))
        if get_ip(request) =="172.30.50.98":
            print(get_ip(request))
            print(request.POST['information'])
        if get_ip(request) =="10.21.8.38":
            print(get_ip(request))
            print(request.POST['information'])
        if not IP:
            m = json.loads(request.POST['information'].replace("'", '"'))['information']
            information.objects.create(timestamp = str(int(time.time())), information = request.POST['information'],\
                    IP = get_ip(request),version=m['version'])
        else:
            m = json.loads(request.POST['information'].replace("'", '"'))['information']
            IP.update(timestamp = str(int(time.time())),version=m['version'])
            # IP.update(information = request.POST['information'])
    return HttpResponse()

def testmysql(request):
    if 'mysql' in request.POST:
        mysql.objects.create(information = request.POST['information'],IP = get_ip(request))
    return HttpResponse()

	
def reset_api(request):
    try:
        if 'info' in request.POST:
            datas = json.loads(request.POST['info'].replace("'",'"'))
            result =[]
            for data in datas:
                if 'host' and 'user' and 'pwd'  in data:
                    try:
                        print(data['host'], data['user'], data['pwd'])
                        if 'type' in data and data['type']=='PXE':
                            commit = "time 2 ipmitool -H {0} -U {1} -P {2} chassis bootdev pxe".format(data['host'],data['user'],data['pwd'])
                            msg = os.popen(commit).read()
                            commit = "time 2 ipmitool -H {0} -U {1} -P {2} power status".format(data['host'],data['user'],data['pwd'])
                            msg = msg +os.popen(commit).read()
                            result.append({"host":data['host'],"msg":msg,"status":200})
                        else:
                            commit = "time 2 ipmitool -H {0} -U {1} -P {2} power status".format(data['host'],data['user'],data['pwd'])
                            msg = os.popen(commit).read()
                            result.append({"host":data['host'],"msg":msg,"status":200})
                    except:
                        result.append({"msg":"restart faild","status":400})
                result.append(parameter_wrong())
            return  handle_response(result)
        return handle_response(parameter_wrong())
    except:
        traceback.print_exc()
        handle_response(find_wrong())

def find_wrong():    ###查询失败
    result = {
        "data": [],
        "httpstatus": 400,
        "msg": '查找信息失败'
    }
    return result

def parameter_wrong():       ##参数错误
    result = {
        "data": [],
        "httpstatus": 400,
        "msg": '参数错误'
    }
    return result

def success_return():       ##参数错误
    result = {
        "data": [],
        "httpstatus": 200,
        "msg": 'success'
    }
    return result

def handle_response(result):
    response =HttpResponse(json.dumps(result), content_type='application/json')
    response["Access-Control-Allow-Origin"] =  "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response
