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
## 返回HTML文件
- 在templates目录下创建index.html文件
- 更改views.py
```python
from django.shortcuts import render #一般会自动导入
def index(request):
    return render(request, 'index.heml') #render方法使用数据字典和请求元数据,渲染一个指定的html模板,第一个参数必须是request,第二个是模板
```
- 修改settings文件中的DIRS，让django知道我们的html文件在哪里
```python
#在settings.py中找到以下列表并添加
TEMPLATES = [
    'DIRS':[os.path.join(BASE_DIR), 'templates'] #templates为本地html所在文件夹
]
```
## 使用静态文件
- 在django中 一般静态文件放在static目录下，如无此文件夹,在project_name目录下 新建static目录
- 将插件放入static目录,然后修改settings.py
```python
STATIC_URL = '/static/'  #这个'static'指你在浏览器中直接访问静态文件需要添加的前缀

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  #这里的static是指项目目录中的static目录名
]
```
## 接收用户发送的数据
`username = request.POST.get('username')` # 接收用户输入的username内容,其他类似
## 返回动态页面
- 在views中编辑要返回的动态数据,已字典形式返回,例如:
```python
user_list = []
def hello(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        temp = {'username':username,'pwd':password} # 把用户输入的数据构建字典
        user_list.append(temp)
    return render(request,'index.html',{'data':user_list} # return data
```
- 编辑index.py 展示views返回的data

## 使用数据库
- 先要在settings.py 中注册app：
```python
#在settings.py 中找到INSTALLED_APPS列表 添加
INSTALLED_APPS = [
    'APP_NAME'
]
DATABASES = {  #这个字典内是数据库的一些信息,不用更改
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  #这个是指定使用的数据库类型
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'), #默认轻量级sqlite3
    }
}
```
- 编写models.py 
```python
from django.db import models
class UserInfo(models.Model):
    user = models.CharField(max_length=32) #创建字段，设置最大长度32,类型为char
    pwd = models.CharField(max_length=32)
```
- pycharm 创建数据库的表
   
   - `python manage.py makemigrations` 
   - `python manage.py migrate` #这步操作后会创建成果db.sqlite3

- 修改views.py
```python
def hello(request):  #用户名和密码例子
     if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        models.UserInfo.objects.create(username=username,pwd=password)
    user_list = models.UserInfo.objects.all()
    return render(request,'index.html',{'data':user_list})
```
### 数据库常用操作命令
- 获取所有数据行,相当于SELECT * FROM 
`models.UserInfo.object.all()`
- 设置过滤条件
`models.UserInfo.object.filter(id=1)`  #括号中为过滤条件
- 获取单个对象
`models.UserInfo.object.get(id=1)`
- 限制返回数据  相当于 LIMIT 0, 2
`models.UserInfo.object.order_by('name')[0:2]`  #name为排序条件,[0:2]设置过滤条数
- 数据排序
`models.UserInfo.object.odery_by('id')`
- 连锁使用
`models.UserInfo.object.filter(name='').order_by('id')`
- update数据
```sqlite3
test1 = models.UserInfo.object.get(id=1)
test1.name = 'test'
test1.save       #保存更改
``` 
`models.UserInfo.object.filter(id=1).update(name='test')` #一步到位
`models.UserInfo.object.all().update(name='test')`        #修改所有的列
- 删除数据
```sqlite3
test1 = .object.get(id=1)
test1.delete()    #删除
```
`models.UserInfo.object.filter(id=1).delete()`             #一步到位
`models.UserInfo.object.all().delete()`                    #删除所有数据
# ** over **



