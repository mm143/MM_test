## django 笔记 from 网易云课堂--知了
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
