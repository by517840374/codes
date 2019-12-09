import random
import string
import json
import datetime
from django.shortcuts import render

# Create your views here.

from django.views.generic import View
from .models import Upload
from django.http import HttpResponsePermanentRedirect,HttpResponse



class HomeView(View):
    """用来显示主页的视图类"""

    def get(self, request):
        """专门用于处理get请求"""

        return render(request, 'base.html', {})

    def post(self, request):
        """专门处理post请求"""
        # 如果有文件，向下执行，没有文件的情况，前端已经处理好
        if request.FILES:
            # 获取文件
            file = request.FILES.get('file')
            # 获取文件名
            name = file.name
            # 获取文件大小
            size = int(file.size)
            # 写文件到static/files
            with open('static/file/'+name,'wb') as f:
                f.write(file.read())
            # 生成随机八位的 code
            code = ''.join(random.sample(string.digits, 8))
            u = Upload(
                path= 'static/file/'+name,
                name=name,
                Filesize=size,
                code=code,
                # 获取上传文件的用户ip
                PCIP=str(request.META['REMOTE_ADDR']),
            )
            # 存储数据库
            u.save()
            # 使用HttpResponsePermanentRedirect 重定向到展示文件的页面。这里的 code 唯一标示一个文件。
            return HttpResponsePermanentRedirect('/s/'+code)


class DisplayView(View):
    """展示文件的视图类"""

    def get(self, request, code):
        """支持get请求，并且可接受一个参数，这里的code需要和配置路由的code保持一致。"""
        # 通过ORM模型查找
        u = Upload.objects.filter(code=str(code))
        # 如果u有内容，u 的访问次数+1，否则返回给前端的内容也是空的
        if u:
            for i in u:
                # 每次访问 访问次数+1
                i.DownloadDocount += 1
                i.save()
            # 返回渲染的页面,其中 content 是我们传给 template/content.html 的内容
        return render(request, 'content.html', {'content': u})


class MyView(View):
    """定义一个MyView用于完成用户管理功能"""
    def get(self, request):
        # 获取用户的IP
        IP = request.META['REMOTE_ADDR']
        # 查找数据
        u = Upload.objects.filter(PCIP=str(IP))
        for i in u:
            # 访问量+1
            i.DownloadDocount += 1
            i.save()
        return render(request, 'content.html', {'content':u})


class SearchView(View):
    def get(self, request):
        # 获取get请求中的kw的值，即搜索的内容
        code = request.GET.get('kw')
        u = Upload.objects.filter(name=str(code))
        # 定义一个空字典,将查询的结果放入字典中
        data = {}
        if u:
            for i in range(len(u)):
                """将符合条件的数据放到data中"""
                u[i].DownloadDocount += 1
                u[i].save()
                data[i]={}
                data[i]['download'] = u[i].DownloadDocount
                data[i]['filename'] = u[i].name
                data[i]['id'] = u[i].id
                data[i]['ip'] = str(u[i].PCIP)
                data[i]['size'] = u[i].Filesize
                data[i]['time'] = str(u[i].Datatime.strftime('%Y-%m-%d %H:%M'))
                # 时间格式化
                data[i]['key'] = u[i].code
            # django 使用 HttpResponse 返回 json 的标准方式,content_type 是标准写法
        return HttpResponse(json.dumps(data), content_type='application/json')
