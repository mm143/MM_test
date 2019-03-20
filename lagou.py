#*_*coding: utf-8
'''本爬虫脚本为爬取拉勾网招聘信息,可设置爬去的职位, 爬去的页数,爬去的信息保存再当前目录下job.txt'''
import requests
from bs4 import BeautifulSoup
import json,time
from random import randint

def main(page,job_name):
    url_data='https://www.lagou.com/jobs/positionAjax.json?city=%E6%88%90%E9%83%BD&needAddtionalResult=false'
    url_start='https://www.lagou.com/jobs/list_%E5%89%8D%E7%AB%AF?labelWords=&fromSearch=true&suginput='
    header = {
        'Host':'www.lagou.com',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
        'X-Anit-Forge-Code':'0',
        'X-Anit-Forge-Token': None,
        'X-Requested-With':'XMLHttpRequest',
        'Referer':'https://www.lagou.com/jobs/list_%E5%89%8D%E7%AB%AF?labelWords=&fromSearch=true&suginput='
    }
    header2 = {
        'Upgrade-Insecure-Requests':'1',
        'Host': 'www.lagou.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
        'Referer': 'https://www.lagou.com/jobs/list_%E5%89%8D%E7%AB%AF?labelWords=&fromSearch=true&suginput='

    }
    s = requests.Session()
    s.get(url=url_start,headers=header)
    cookies = s.cookies
    for p in range(1,page+1):
        data = {
            'first': 'true',
            'pn': str(p),
            'kd': job_name
        }
        response = s.post(url=url_data,headers=header,data=data,cookies=cookies,timeout=5)
        response.encoding = response.apparent_encoding
        r = json.loads(response.text)
        result = r['content']['positionResult']['result']
        for i in result:
            try:
                url = 'https://www.lagou.com/jobs/%s.html'%i['positionId']
                response_job = s.get(url=url,headers=header2,timeout=5)
                content = response_job.text
                soup = BeautifulSoup(content,'lxml')
                b = soup.find('div',class_='job-detail')
                if b == None:
                    job = '职位名称: %s\n' \
                          '公司名称: %s\n' \
                          '工资: %s\n' \
                          '工作经验: %s\n' \
                          '学历要求: %s\n' \
                          '职位详情: https://www.lagou.com/jobs/%s.html\n' \
                          '%s\n' % (i['positionName'], i['companyFullName'], i['salary'], i['workYear'], i['education'],
                                    i['positionId'], '-' * 200)
                    with open('job.txt', 'a', encoding='utf-8') as f:
                        f.write(job)
                    continue
                job_detail = b.text
                job_addr = (soup.find('div',class_='work_addr').text).split()
                job_addr.pop()
                work_addr = ''.join(job_addr)
                job = '职位名称: %s\n' \
                      '公司名称: %s\n' \
                      '工资: %s\n' \
                      '工作经验: %s\n' \
                      '学历要求: %s\n' \
                      '职位详情: https://www.lagou.com/jobs/%s.html\n' \
                      '%s\n' \
                      '工作地址: %s\n' \
                      '%s\n' % (i['positionName'], i['companyFullName'], i['salary'], i['workYear'], i['education'], i['positionId'],job_detail, work_addr, '-' * 200)
                with open('job.txt','a',encoding='utf-8') as f:
                    f.write(job)
                time.sleep(randint(3,6))
            except Exception as e:
                print(e)
                continue
if __name__ == '__main__':
    job_name = input('输入要爬去的职位(例如: java python 前端): ')
    page = int(input('输入要爬去的页数: '))
    main(page,job_name)
    print('已完成,保存至当前目录下 job.txt')