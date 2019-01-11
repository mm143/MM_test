# django 笔记 from 网易云课堂--知了
## 1、virtualenv 虚拟环境
- `pip install virtualenv` #安装虚拟环境
- `virtualenv [虚拟环境的名字]`  #创建虚拟环境
- windows进入虚拟环境
`cd 虚拟环境目录/Scripts 执行 activates`
- 退出虚拟环境 `deactivate`
- 创建环境的时候指定python解释器
`virtualenv -p python_path`
## 2、virtualenvwrapper包
- 安装 `pip install virtualenvwrapper`
- 创建虚拟环境 `mkvirtualenv [虚拟环境的名字] `   # 在当前登陆用户的目录下创建一个Envs文件夹
- 进入虚拟环境 `workon [虚拟环境名字]` 
- 退出虚拟环境 `deactivate`
- 删除某个虚拟环境 `rmvirtualenv [虚拟环境的名字]`
- 列出所有虚拟环境 `lsvirtualenv`
- 进入到某个虚拟环境目录 `cdvirtualenv [虚拟环境的名字]`
- 修改 mkvirtualenv 的默认路径 
在'我的电脑'==>右键==>属性==>环境变量 中添加一个参数 WORKON_HOME, 将这个参数的值设置为你需要的路径
- 创建虚拟环控的时候指定python的版本 `mkvirtualenv --python==python_path [虚拟环境名字]`
## 3、开始项目
### 创建项目
- 命令行 `django-admin startproject project_name`
- pychram  `New Project => Django`
### 启动项目
- 命令行 `python manage.py runserver 127.0.0.1:8000` 
- pycharm 
点击项目名称中的Edit Configuration => 输入host 和 port => 点击绿色Run 按钮
*如果要局域网内其他设备访问此项目, 运行服务是IP设置为 0.0.0.0 ,然后在settings文件的ALLOWED_HOSTS 列表中添加主机IP地址,其他设备输入主机ip:port 即可访问*
*提醒 注意防火墙*
- urls 中变量的使用
变量添加在 <> 内, 例如: path('index/<device_id>',views.index) 中 device_id就是变量,views的函数拿到这个变量后可以进行操作，views中对应函数的参数中必须包含这个变量 def index(request,device_id)
- urls中查询字符串的使用
直接在views的函数中调用 request.GET.get('id') => id即为path中的查询的字符串, 例如: 127.0.0.1:8000/index/?id=test 
- 给url 命名 (url是经常变化的,如果在代码中写死可能会经常改代码)
在path函数中,传递一个'name'的参数就可以命名
- 应用命名空间, 防止多个app出现同名url_name
在对应app的urls.py 中添加一个 app_name=NAME 变量  NAME就是应用的名称, 在需要反转的时候使用 app_name:url_name 的方式进行反转

## 4、模板
- render 模块
```python
from django.shortcuts import render
def index(request):
    return render(request, 'index.html')   #index.html 即为模板
```
- 项目查找模板的路径
1. 在settings.py 的TEMPLATES的列表中的DIRS 项中添加模板所在路径 (BASE_DIR 指定当前项目所在的path)
2. settings.py中的APP_DIRS 设置为True 时为如果在DIRS 中没有找到对应模板,会去各APP的templates目录中寻找
3. 寻找顺序DIRS > 当前APP的templates目录 > 其他已经安装APP的templates

## 变量
1. html文件中 用{{ }}包围变量名
2. 访问变量的属性名  {{ variable.name or variable.1 }}
3. 如果变量是一个dict 遍历变量的key  {{ variable.keys}}  遍历values {{ variable.values }} 遍历key-values {{ variable.items }}

## if else
1. 格式
```html
{%  if condition %}
    ...display
{% elif condition %}
    ...display
{% else %}
    ...display
{% endif %}
```
2. if 标签 支持 and, or, not, <, >, <=, >=, !=, not in, in.....
## for...in...
1. 格式
```html
<ul>
{% for athlete in athlete_list%}
    <li>{{ athlete }}</li>
{% endfor %}
</ul>
```
2. 给标签增加一个 reversed 使列表反向迭代
```html
<ul>
{% for athlete in athlete_list reversed %}
    <li>{{ athlete }}</li>
{% endfor %}
</ul>
```
3. 模板中的for in 不支持continue 和 break
4. forloop常用参数
- forloop.counter => 显示当前是第几层循环，位数从1开始
- forloop.counter0 => 显示当前是第几层循环,位数从0开始
- forloop.revcounter => 显示当前是倒数第几层循环,从1开始
- forloop.revcounter0 => 显示当前是倒数第几层循环,从0开始
- forloop.frist => 条件式 当前是第一次循环时
- forloop.last => 当前是最后一次循环时
5. 一个示例代码
```html
<table border="1">
    <tbody>
        <tr>
            <th>id</th>
            <th>书名</th>
            <th>作者</th>
            <th>售价</th>
        </tr>
        {% for book in books %}
            {% if forloop.first %}
                <tr style="background: red;>"
            {% elif forloop.last %}
                <tr style="background: skyblue;>"
            {% else %}
                <tr style="background: aqua;>"
            {% endif %}
            <tr>
                <td>{{ forloop.revcounter }}</td>
                <td>{{ book.name }}</td>
                <td>{{ book.author }}</td>
                <td>{{ book.price }}</td>
            </tr>
        {% endfor %}
    </tbody>
</table>
```

## url 标签
1. 格式
- 普通网址 `<a href="https:www.baidu.com">百度一下</a>` 
- 同系统url `<a href="{% url 'url_name' %}">title</a>`
- 带参数的url `<a href="{% url 'url_name' arg=' ' %}">title</a>`   arg => 变量名 ' '内为变量的值, 多个参数用空格分隔
- 带查询字符串的url `<a href="{% url 'url_name' %}?arg=' ' ">title</a>` arg => 变量名 ' '内为变量的值
2. 

## 过滤器
1. add 
- 语法
`{ value|add:value2 } ` 如果value都为数字, 返回 两个数字的结果, 反之 返回两个字符串的拼接结果 两个列表 返回一个拼接后的列表
- 示例
`{ '1'|add:'2'} => 3` `{ '1'|add:'2abc'} => '12abc'` `{'[1,2]'|add:['3','4']} => [1,2,'3','4']`
2. cut
- 语法
`{ value|cut:value2 }` 从value中去除 value2 
- 示例
`{ '1ss2ss3sssss'|cut:'s'} => '123'`
3. date
- 语法
`{ time|date:'Y-m-d H:i:s'}` time 为views中(datetime.datetime.now())传过来的参数 
部分date过滤器参数参考 [DTL常用过滤器](https://blog.csdn.net/xujin0/article/details/83385065)
- 示例
```python
views.py 代码如下:
from django.shortcuts import render
from datetime import datetime
def time(request):
    context = {'time':datetime.now()}
    return render(request,'index.html',context=context)
indwx.html 代码如下:
    { time|date:'Y-m-d H:i:s'} => 2018-12-07 15:04:12
```

## 模板继承
1. 语法
`{% extends '模板的path' %}`
extends标签必须放在模板开始的位置
2. block 语法
```html
{% extends 'index.html'}
{% block block_mm %}
    内容
    {{ block.super }}   # 用block.super显示父模板中的内容
{% endblock %}
```
## 静态文件
1. 确保django.contrib.staticfiles 已经添加到settings.py 的 INSTALL_APPS 中
2. 添加static路径
- settings.py 中的 STATIC_URL 设置为 STATIC_URL = '/static/' 此类设置可在各app中的static目录下查找静态文件
- 在settings.py 中添加 STATICFILES_DIRS = [ os.path.join(BASE_DIR, 'static') ] 后在项目目录下添加static文件夹后就可以在此static目录下查找静态文件
3. 模板中加载静态文件使用 load 加载 static标签 比如要加载static下的style.css 示例:
```html
{% load static %}
<link rel="stylesheet" href="{% static 'style.css' %}">
``` 
4. 加载不同app下的同名静态文件时,先在static目录下创建与app名相同文件夹,将静态文件丢进此文件夹,在加载此文件时 前加上文件夹名 例如: {% static 'front/logo.jpg' %} {% ststic 'cms/logo.jpg' %}
5. 如果不想每次在模板中加载静态文件时都使用load加载,可在 settings.py 中的TEMPLATES/OPTIONS 添加
'builins':['django.templatetags.static'],以后在模板中可以直接使用static 标签,不用手动load
6. 

### 不使用缓存加载页面 `ctrl + shift + r`

## 数据库
django中 我们使用mysqlclient 来连接MySQL
1. 配置settings.py 
```python
DATABASES = {
    'default':{
        'ENGINE':'django.db.backends.mysql', #配置django使用的数据库引擎
        'NAME':'name',      # mysql数据库名
        'USER':'user',      # 登陆用户名
        'PASSWORD':'password',  # 密码
        'HOST':'localhost | 127.0.0.1',    #地址 localhost或127.0.0.1 都代表本机
        'PORT':'3306'       # 端口 默认3306
    }
}
```
2. 使用navicat 连接MySQL出现 2059的报错时, 进入mysql 输入以下命令:
`ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password'` #password为你想使用的验证密码
3. 操作mysql
```python
from django.db import connection #导入connection
def index(request):
    cursor = connection.cursor() #建立 cursor
    sql = "select * from table_name" #sql语句
    cursor.execute(sql)  #执行
    rows = cursor.fetchall()  #接受select 返回的结果 有三种用法 fetchall =>查所有  fetchone => 查一条数据 fetchmany(num) => 查指定条数  update和insert 不需要接受返回结果
```
4. 



## 杂七杂八笔记
1. 在views反转到某个网页
```python
from django.shortcuts import render,redirect, reverse
def index(request):
    return redirect(reverse('url_name'))  #url_name 为urls中url 的name 
```
2. html中的内容
```html
<form action="{% url 'sure_movie' %}" method="post"> #action中是提交到哪个网页  method中为提交方式
    <input type="text" name="name"></td>        #input 输入框 type为类型 text为文本  name为提交的参数名  value为参数值=输入框中的内容
    <td><input type="hidden" name="movie_id" value="{{ movie.0 }}"></td>    # hidden为隐藏  name为提交的参数名 value为参数的值
    <td><input type="submit" value="确认修改"></td>     #submit 为按钮   value为按钮显示的名称
</form>
```
3. views中判断网页的请求类型
```python
def index(request):
    if request.method == 'POST':  | if request.method == 'GET':
        return ... 
``` 

## ORM模型
1. 建立模板
```python
#在创建的app目录下的models.py 中建立模型
from django.db import models
class Model_name(models.Model):
    id = models.AutoField(primary_key=True)     #models中的AutoFiele为自增长类型 primary_key 设置为True 为 将此字段设置为主键
    name = models.CharField(max_length=100, null=False)     #models中的CharFiels 为字符串(sql中的varchar)  max_length为设置长度  null 设置为False 为不能为null
    author = models.CharField(max_length=100, null=False)   #
    price = models.FloatField(null=False, default=0)        #models中的FloatField 为浮点数类型(double) default 为设置默认值
    #models 中还有很多其他类型 此类中的 每一个变量 都会在数据库中创建一个字段
```
2. ORM模型映射数据库
- 第一步 => python manage.py makemigrations   此操作后会在app目录下创建一个migretions的文件夹 文件夹里会有创建的模型
- 第二步 => python manage.py migrate       此操作后会在数据库创建表
这两步操作之后在数据库中会出来一个新表 如果没指定表名 默认为 app_name_model_names  例如: front_book front为创建的app名字 book为models.py中的类名

3. ORM基本操作
- 增
```python
from .models import Model_name
model_name = Model_name(name='', author='', price='')
model_name.save()
```
- 查     所有的查询工作都是用ORM上的objects的属性  也可以自定义查询对象
```python   #用主键查询
from .models import Model_name
models_name = Model_name.objects.get(pk=1)  #.get()方法为获取一条数据 pk为 primary key 主键查询
print(models_name)
```
```python   #用其他条件查询
from .models import Model_name
models_name = Model_name.objects.filter(name='三国演义').first()  #.object.filter() 为其他条件查询 filter内没有内容为 select * from  first方法为查返回的第一个数据
print(models_name)
```
- 删
```python
from .models import Model_name
models_name = Model_name.objects.filter(name='三国演义').first() 
models_name.delete()
```

- 改
```python
from .models import Model_name
models_name = Model_name.objects.get(pk=2)
models_name.name = '3国演义'
models_name.save()
```

4. ORM模型常用属性
- AutoField         数据库层面是int类型 并有自动增长的功能
- BigAutoField      64位的整形,类似于AutoField 范围更大
- BooleanField      模型层面接受的是 True/False 在数据层面接受tinyint, 如果没有指定默认值,默认为None
- CharField         数据库层面是varchar, python层面是普通字符串  这个类型必须指定最大长度 即max_length  CharField最大255字符
- DateField         
- EmailField        类似于CharField 默认最大254个字符(可以不传递max_length参数)  主要用于邮箱
- IntegerField      整形 范围为  -(2*31) —— 2*31
- BigIntegerField   大整形范围为   -(2*63) —— 2*63
- TextField         大量文本类型

5. 外键
- orm模型中建立外键实例
```python
from django.db import models
class Author(models.Model):
    name = models.CharField(max_length=100, null=False)
class Book(models.Model):
    name = models.CharField(max_length=100, null=False)
    content = models.TextField()
    author = models.ForeignKey("Author", on_delete=models.CASCADE)  #ForeignKey(to, on_delete, *args) to为引用的模型名 on_delete 为删除主数据时 这条数据要进行的操作
```
- 要引用其他app内的模型时使用 app.model_name 示例:
`author = models.ForeignKey("book.Author", on_delete=models.CASCADE)`   #book 为app名 Author为book下models.py 中的模型
6. 表关系 一对多
```python
from django.db import models
from front.models import Author     #author表

class Category(models.Model):   #创建category表
    category =models.CharField(max_length=100, null=False)

class Article(models.Model):    #创建article表     此表中有两个外键分别对应author和category表
    title = models.CharField(max_length=100, null=False)
    content = models.TextField()
    category = models.ForeignKey("Category", on_delete=models.CASCADE,related_name='tt')    #category_id 外键对应Category模型中的主键字段 relaed_name 为通过category查询全部文章时的方法名 默认为models_name_set(如:article_set)
    author = models.ForeignKey("front.Author", on_delete=models.CASCADE)                    #author_id 外键对应Author模型中的主键字段
```
- 查询某一分类的全部数据，示例:
```python
from .models import Category,Article,Author
from django.http import HttpResponse
def index(request):
    category = Category.object.first()
    article = category.article_set.all()    #默认是model_name_set方法查询 可自行设置(relaed_name参数)  此示例为查询所有分类为category中第一条数据类型的article数据
    return HttpResponse('success')
```
- 添加数据 示例:
```python
from .models import Category,Article,Author
from django.http import HttpResponse
def index(request):
    category = Category.object.first()  #获取第一条分类
    author = Author.object.filter()     #通过过滤器获取author
    article = Article(title='test',content='1234567890')
    article.category = category         #添加category_id
    article.author = author             #添加author
    article.save()
    return HttpResponse('success')
```

## ORM查询条件 
1. 精确查询exact 和iexact
- exact在翻译成sql语句是等同于 =,  
`book = Book.objects.filter(content__exact='啊啊啊')` #sql语句为: select * from book where content = '啊啊啊';
- iexact翻译成sql语句是等同于 LIKE
`book = Book.objects.get(content__exact='啊啊啊')` #sql语句为: select * from book where content like '啊啊啊'; 
*** filter查询返回的是一个query对象,可以调用query方法查看sql语句(book.query), get返回的是一个ORM模型 ***
2. 查询某个字符串是否在指定的字段中 
- contains 使用大小写敏感的判断  等同于mysql中的 LIKE BINARY
`book = Book.objects.filter(content__contains='啊啊啊')`   #sql语句: select * from book where content like binary '%啊啊啊%';
- icontains 使用大小写不敏感的判断   等同于mysql中的 LIKE
`book = Book.objects.filter(content__icontains='啊啊啊')`   #sql语句: select * from book where content like '%啊啊啊%';
3. in 查询条件是否在给定的范围内
`book = Book.objects.filter(id__in=(1,2,3))`     #sql语句: select * from book where id in (1,2,3);
4. gt   大于
`book = Book.objects.filter(id__gt=2)`      # select * from book where id > 5;
5. gte  大于等于
6. lt   小于
7. lte  小于等于
8. startswith   以指定某个字符串开始,大小写敏感
`book = Book.objects.filter(content__startswitj="Hello")`   # select * from book where content like "Hello%";
9. istartswith  以指定某个字符串开始,大小写不敏感
10. endswith    以指定字符串结束,大小写敏感
11. iendswith    以指定字符串结束,大小写不敏感
12. range       在某个范围内  相当于  between ... and  ...
`book = Book.objects.filter(id__range=(1,3)`    # select * from book where id between 1 and 3;
13. isnull      是否为空
`book = Book.objects.filter(content__isnull=False)` # select * from book where content is NOT null;
14. exclude     排除满足条件的
## ORM 聚合函数
 **所有的聚合函数都是放在 django.db.models 下**
 **聚合函数不能单独的执行, 需要放在一些可以执行聚合函数的方法下边, 比如 aggregate(Avr())**
 **aggregate返回的是一个字典,字典的key就是聚合函数的名字**
 1. Avg  求平均值 示例:
 ```python
from django.db.models import *
def index(request):
    result = Book.objects.aggregate(avg=Avg("price"))  #求price这一列的平均值  avg为给聚合函数取名(返回结果中的key) 默认为 字段__聚合函数 如: price_Avg
 ```
2. Count  统计指定字段的个数
```python
from django.db.models import *
def index(request):
    result = Book.objects.aggregate(count=Count("price"))  #统计price这字段的个数
```
3. Max和Min  获取指定字段的最大值和最小值
```python
from django.db.models import *
def index(request):
    result = Book.objects.aggregate(max=Max("price"))  #求price这字段的最大值 最小值为Min
```
4. Sum 求指定字段的总和
```python
from django.db.models import *
def index(request):
    result = Book.objects.aggregate(sum=Sum("price"))  #求price字段的总和
``` 

5. F查询和Q查询
- F查询 
```python
book = Book.objects.filter(id__exact=F('publisher_id')) #F()的实例可以在查询中引用字段，来比较同一个 model 实例中两个不同字段的值。
```
- Q查询   ~放Q查询前面 表示取反  | 代表or & 表示and
```python
book = Book.objects.filter(Q(id=1) | Q(id=2))           #查id=1 或者id=2 的数据
book = Book.objects.filter(~Q(id=1))                    #查id不为1 的数据
book = Book.objects.filter(~Q(id=1) & Q(author_id=1))    #查id不为1 和 author_id为1 的数据

```
## QuerySet
1. filter   提取满足条件的数据,返回一个新的QuerySet
2. exclude  排除满足条件的数据, 返回一个新的QuerySer   与filter相反
```python
book = Book.objects.exclude(id=2)   #排除id=2的数据
```
3. annotate 给QuerySet中的每个对象添加一个查询表达式(聚合函数,F表达书,Q表达式,Func表达式等)的新的字段
```python
book = Book.objects.annotate(author_name=F('author__author'))   #author_name 为用annotate添加的新字段 获取anthor表中的anthor字段
    for i in book:
        print("%s ==> %s"%(i.name, i.author_name))
```
4. order_by  排序(order by ) 在排序字段前加一个 '-' 表示 倒序(order by ... desc)
```python
book = Book.objects.order_by('price')   #按照price字段排序
book = Book.objects.order_by('-price')  #按照price字段反向排序
book = Book.objects.order_by('price','id') #按照price排序 如果有price相同数据 相同的部分按照id排序
book = Book.objects.order_by('price','id').order_by('id')   #如果有两个order_by 会按照后边的字段排序
book = Book.objects.filter(id__gt=2).order_by('price','-id')   #filter筛选后再order_by 
```
补充: 在Meta类里 创建一个 ordering 列表 会按照列表中的而字段先后顺序 排序  示例;
```python
class Meta():   #创建模型下的一个类
    db_table = 'book'
    ordering = ['price','id','name']      #先按照price排序 price相同的数据按照id排序
book = Book.objects.all()      #会按照定义好的ordering 来排序
```
5. all  获取全部数据
6. delete   删除数据 适用于all() filter() exclude() 后
```python
book = Book.objects.filter(id=2)
book.delete()
#以上两行等同于下边
Book.objects.filter(id=2).delete()
```
7. update   批量更新(危险操作)  适用于all() filter() exclude() 后
```python
Book.objects.all().update(price='30.01')
Book.objeces.filter(id__gte=2).update(price='30.02')
```
8. 更新单条数据
```python
book = Book.objects.get(id=1)       #filter貌似不支持此修改方法 待验证
book.price = '39.99'
book.save()
```
9. 切片   [:2]    切除前2  reverse()[:2] 切除后2
```python 
book = Book.objects.all()[:10]          #保留前10条
book = Book.objects.all()[10:]          #
book = Book.objecs.all().reverse()[:2]  #保留后两条  
book = Book.objecs.all().reverse()[0]  #保留最后一条 
book = Book.objects.order_by('-id')[:2] #保留id最大的2条
```

## 表单forms
### 表单使用方法
在app目录下新建forms.py 文件 文件内代码示例:
```python
from django import forms
class Login(forms.Form):    #类必须继承 forms.Form
    username = forms.CharField(min_length=11,max_length=11,label='用户名')     #定义表单参数
    password = forms.CharField(label='密码')
```
views.py 中示例代码
```python
from django.shortcuts import render
from django.views.generic import View
from .forms import Login    #导入表单
from django.http import HttpResponse
class IndexView(View):
    def get(self,request):
        form = Login()
        return render(request,'index.html',context={'form':form})
    def post(self,request):
        form = Login(request.POST)  #接受表单的数据 
        if form.is_valid():         # form.is_valid()  如果提交的数据合法
            username = form.cleaned_data.get('username')    #获取处理过的值 form.clean_data.get() 获取处理过的值
            password = form.cleaned_data.get('password')    #获取处理过的值
            return HttpResponse('success')
        else:
            print(form.errors)  #form.errors 输出错误信息
            return HttpResponse('faild')
```
html模板中代码示例:
```html
<form action="" method="post">  <!-- 指定访问方法为post -->
<table>
    {{ form.as_table }}         <!-- form.as_table 能将表单以table的形式展示出来 -->
    <tr>
        <td></td>
        <td><input type="submit" value="登陆"></td>
    </tr>
</table>
</form>
```
### 表单中常用Field
1. CharField
接收文本 参数:
- max_length  指定字段的最大长度
- min_length  指定字段的最小长度
- required    这个字段是否是必须的  默认是必须的
- error_messages  在某个条件验证失败的时候 给出错误信息
2. EmailField
用来接受邮件, 会自动验证邮件是否合法
错误信息的key: required  invalid
3. FloatField 
接收浮点类型,并且通过验证后 会将这个字段的值转换为浮点类型
参数:
- max_value  最大的值
- min_value  最小的值
错误信息的key: required  invalid  max_value  min_value
4. IntegerField
接收整形,并且通过验证后 会将这个字段的值转换为整形
参数:
- max_value  最大的值
- min_value  最小的值
错误信息的key: required  invalid  max_value  min_value
5. URLField
接受url格式的字符串
错误信息的key: required  invalid 
### 验证器
1. 常用验证器
- MaxValueValidator 验证最大值
- MinValueValidator 验证最小值
- MinLengthValidator    验证最小长度
- MaxLengthValidator    验证最大长度
- EmailValidator    验证是否是邮箱格式
- URLValidator      验证是否是URL格式
- RegexValidator    正则表达式的验证器  示例验证手机号是否合格代码如下:
```python
from django.core import validators
class Login(forms.Form):
    username = forms.CharField(validators=[validators.RegexValidator(r'1[35789]\d{9}', message='请输入正确的手机号码')],label='用户名')  #message参数是如果不满足条件是报错的提示内容
    password = forms.CharField(label='密码')
```
2. 自定义验证器
在表单类下 定义一个函数 函数名以 clean_fieldname 命名 示例:
```python
from django import forms
from django.core import validators
class Login(forms.Form):
    username = forms.CharField(validators=[validators.RegexValidator(r'1[35789]\d{9}', message='请输入正确的手机号码')],label='用户名')
    password = forms.CharField(label='密码')

    def clean_username(self):   #针对username字段定义的验证器 只对username有效 
        username = self.cleaned_data.get('username')
        if username != '18180001232':
            raise forms.ValidationError('手机号未注册')
        else:
            return username
```