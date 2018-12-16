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
2. block 语法
```html
{% extends 'index.html'}
{% block block_mm %}
    内容
    {{ block.super }}   # 用block.super显示父模板中的内容
{% endblock %}
```
