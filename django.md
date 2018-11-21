# django的语法笔记
## 1、安装django
`windows => pip3 install django`
`linux   => pip3 install django`
- windows安装完成后需要将django的安装路径添加到环境变量中,一般在python36/Scripts \n
* 升级pip3
`python -m pip install --upgrade pip`
## 2、查看django安装是否成功
`django-admin help`
`import django; django.get_version()`
## 3、创建django项目
`cmd => django-admin startproject project_name`
`pycharm => New Project => Django`
### 项目内文件说明
- project_name目录下
   
1. __init__.py  ==> 空文件
2. settings.py  ==> 主配置文件
3. urls.py      ==> 主路由文件
4. wsgi.py      ==> 网关接口
* templates     ==> HTML文件安置目录
+ manage.py     ==> 项目管理脚本

## 创建APP
- 打开pycharm的terminal 输入:
`python manage.py startapp app_name`

## 编写路由 urls.py
- 打开urls.py  添加路由
```python
from app_name import views #需要先导入对应app中的views文件

urlpatterns = [
    path('index/',views.index), #添加路由,重点是路由中的index函数
]
```
## 编写视图函数 views.py
```python
from django.shortcuts import HttpResponse  #导入这模块

def index(request): #第一个参数必须是requests,requests参数封装了用户请求的所有内容
    return HttpResponse('Hello World~')  #不能直接返回字符串,必须由HttpResponse这个类封装起来
```
## 运行web服务
- 命令行的方式是:
`python manage.py runserver 127.0.0.1:8000`
- pycharm中的方式是:
   
   1. 点击项目名称中的Edit Configuration
   2. 输入host 和 port
   3. 点击绿色Run 按钮
- 然后就可以在本地浏览器中输入127.0.0.1:8000/index 中访问了