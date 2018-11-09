#-*- encoding:utf-8 -*-
import requests
import bs4
import re
import json
import openpyxl
import sys
import time
import random

'''此脚本为爬取网易云音乐15个歌手分类中的热门歌手中的热门歌曲的评论排行榜'''

def get_songers(page): #获取所有分类的热门歌手 返回dict
    songers={}
    headers={
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Cache-Control':'no-cache',
        'Connection':'keep-alive',
        'Cookie':'mail_psc_fingerprint=3717713c98660b8885cd78c8f7cb7af4; __gads=ID=d94d974e5f9dc0c5:T=1506045311:S=ALNI_MaEWN6i8X52dDZdYPjqSCSA1oVWOA; vjuids=a5e6341df.15ea74c0e75.0.941115a82a253; usertrack=ezq0pVoKgNdhb/v1BeoIAg==; _ga=GA1.2.1122557775.1510637788; nts_mail_user=bym_fish@163.com:-1:1; NTES_CMT_USER_INFO=127961435%7C%E6%9C%89%E6%80%81%E5%BA%A6%E7%BD%91%E5%8F%8B07E8Br%7C%7Cfalse%7CYnltX2Zpc2hAMTYzLmNvbQ%3D%3D; P_INFO=bym_fish@163.com|1533093116|2|study|00&99|sic&1532486568&other#sic&510100#10#0#0|&0||bym_fish@163.com; vjlast=1506045333.1534913055.12; vinfo_n_f_l_n3=7c5ee84b19f99a57.1.11.1506045333265.1534749967500.1534913058714; _ntes_nnid=77859a8fd70b848c2e5fdea7a8ec1565,1537943241451; _ntes_nuid=77859a8fd70b848c2e5fdea7a8ec1565; WM_NI=yzJg4j12ryOjRvfva4ZmgN0UJu8h%2FTAZTUn8ZXhXeLHBKMdCeUhDk8xGonESGXKFy6Jk%2BzvyAfyZKBPvHTb1nwt1a2NgZJ4Ifn0kL933qYbqUsSsXTq%2Fb2M32ZYmsbzBdVQ%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eeabe26fb6ace58ff56d8b928fa3d14a928b8baef36f8fed82b4f24689b0a0bacb2af0fea7c3b92abba68688b762f3eebe9ace6292aaaa97e4409ab3a9afb35f8aabf889ae6083869cb6ed349a88a8b9e8488c9e85aee749a78ba8a5ea34bc99a18fc859858885a7fc3e8ab5e59bf57383bab7bbca4a94aa88b5e13baea9bcd2e43a8eb996abb743a6b2008ccf33f1edbfbae17b97ad9d94db60b3f1aed3d039f286978ef26aba9eacb7d437e2a3; WM_TID=%2FpNEMn3K7dpAQRAQVFZ4LRIkhO7GGB%2FE; JSESSIONID-WYYY=laVqq0NF67bfPWkD%2FEz5uR%2B9v2g45bIcMXu4zjZ6ZncOG0SCvft7x1KveZw%2FC%2BaxfMWKl%5CNFJKYJAzj09OJxNCb28VYCwyzyMdux%2FxaDJJ5CAtsfd83nS45o97sFpHIfyk8eq3pOVxW9P%2F%5CHJjua92RO2gjcs3mYo%2B1lfnsPe%2BGnzi7n%3A1540457392076; _iuqxldmzr_=32; __utma=94650624.1651417532.1507777869.1540450004.1540455849.20; __utmb=94650624.16.10.1540455849; __utmc=94650624; __utmz=94650624.1540432962.17.8.utmcsr=baidu|utmccn=(organic)|utmcmd=organic',
        'Host':'music.163.com',
        'Pragma':'no-cache',
        'Referer':'https://music.163.com/',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
    }
    for id in page:
        url = 'https://music.163.com/discover/artist/cat?id={}'.format(str(id))
        res = requests.get(url,headers=headers)
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        for songer in soup.find_all('a',attrs={'class': 'nm nm-icn f-thide s-fc0'}):
            name = songer.string
            id = songer['href'].replace('/artist?id=', '').strip()
            songers[id] = name
    return songers

def get_songs(songers):  #用所有歌手id 获取所有歌手的热门歌曲  返回歌曲id
    songs = {}
    headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
    }
    j = 1
    for songer_id in songers:
        url = 'https://music.163.com/artist?id={}'.format(songer_id)
        res = requests.get(url,headers=headers)
        songs_json = re.findall(r'textarea id="song-list-pre-data" style="display:none;">(.*?)</textarea>.*',res.text)
        sys.stdout.write('爬取到%s个歌手信息,正在处理第%s个......'%(len(songers),str(j))+' \r')
        sys.stdout.flush()
        try:
            if songs_json:
                songs_list = json.loads(songs_json[0])  #此处报错 out range  初步怀疑部分歌手没有歌曲内容造成
                for song in songs_list:
                    id = str(song['id'])
                    song_name = song['name']
                    songs[id] = song_name
                    #song_ = 'id:{} ==> {} \n'.format(str(song['id']),song['name'])
        except Exception as e:
            print('出错歌手id为 ==> %s'%songer_id)
            print(e)
        j += 1
    return songs
            

def get_comments(songs): #用歌曲id获取每首歌的评论数，评论大于30000时，写入数据库
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.append(['歌曲名','评论数'])
    j = 1
    for song_id in songs:
        time.sleep(random.ranint(3,9))
        try:
            sys.stdout.write('爬取到%s首歌曲,正在处理第%s首......'%(len(songs),str(j))+' \r')
            sys.stdout.flush()
            url = "https://music.163.com/weapi/v1/resource/comments/R_SO_4_{}?csrf_token=".format(song_id)
            headers = {
                "Accept":"*/*",
                "Accept-Encoding":"gzip, deflate, br",
                "Accept-Language":"zh-CN,zh;q=0.8",
                "Connection":"keep-alive",
                "Content-Length":"516",
                "Content-Type":"application/x-www-form-urlencoded",
                "Cookie":"mail_psc_fingerprint=3717713c98660b8885cd78c8f7cb7af4; __gads=ID=d94d974e5f9dc0c5:T=1506045311:S=ALNI_MaEWN6i8X52dDZdYPjqSCSA1oVWOA; vjuids=a5e6341df.15ea74c0e75.0.941115a82a253; usertrack=ezq0pVoKgNdhb/v1BeoIAg==; _ga=GA1.2.1122557775.1510637788; nts_mail_user=bym_fish@163.com:-1:1; NTES_CMT_USER_INFO=127961435%7C%E6%9C%89%E6%80%81%E5%BA%A6%E7%BD%91%E5%8F%8B07E8Br%7C%7Cfalse%7CYnltX2Zpc2hAMTYzLmNvbQ%3D%3D; P_INFO=bym_fish@163.com|1533093116|2|study|00&99|sic&1532486568&other#sic&510100#10#0#0|&0||bym_fish@163.com; vjlast=1506045333.1534913055.12; vinfo_n_f_l_n3=7c5ee84b19f99a57.1.11.1506045333265.1534749967500.1534913058714; _ntes_nnid=77859a8fd70b848c2e5fdea7a8ec1565,1537943241451; _ntes_nuid=77859a8fd70b848c2e5fdea7a8ec1565; WM_NI=poupJg3ekqazNJteNkBYXZE3CUer804X%2F4YLGcAXX0UMx2%2BdRIwOaQyYTjPM4Rfc1q8HHmfNR8AOCcdk2bq3QZXc06hN7XVvjFDmNx0dNzvu1lcpmungYL9H1okhxsytSWo%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eea6b47290ac8398d47c9b9e8fa3c15b928f9e84f345a68ff997eb66f1b48792d52af0fea7c3b92ab4b1bb91c96df1bba592e4728e96bc86cd61828798bbc839818bab93bb3cf888e1d5dc4885bd8fb9db3c9793b8d3aa709297b9b0e45bbb879c8bd347f88eaa84b47bfc98888ee54692e88fb0c269a8b5fe83f43993869884b33eac92f9b9d57eaa9a8c8ecd74f4bc829bf57ff3b4ad91f07faeb997adbc44f3b1a589fb79bbac9db8ee37e2a3; WM_TID=%2FpNEMn3K7dpAQRAQVFZ4LRIkhO7GGB%2FE; JSESSIONID-WYYY=IYJQGhbMhvYpNnF3f4iogiPNeGi8GsquRsTrIDWwK9K7Q%2Bh7lrli31qXlZy%2Bk%2FuCRyWYCfqMCXqJIOwAZxtu9nEYVOpCrVTuu65r5xe4C%5Cuuc38QEufvMjTIwTAPH%5CwhQRXN9xWUKFdKfOgb1WyYUPatUQEJrIsiMM8zJ4KYuzcA%5CyIM%3A1540956410507; _iuqxldmzr_=32; __utma=94650624.1651417532.1507777869.1540547393.1540952871.28; __utmb=94650624.15.10.1540952871; __utmc=94650624; __utmz=94650624.1540952871.28.12.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; MUSIC_U=9de0b492647e4661d0d11bc392fe83c4dfe007791dc6e29dc69d1ce280c1d9fd5b1322b5d7d05f61973d23dfe458bad1bff748db9e9cfbf8642a565388478f73305842396b5dfc01; __remember_me=true; __csrf=ffb8bec0672477b21e4ed7532296cfa7",
                "Host":"music.163.com",
                "Origin":"https://music.163.com",
                "Referer":"https://music.163.com/song?id={}".format(song_id),
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
                }
            params = 'ZIDK9Nv/D67iZW2GGf49SCAKLOIjH3gFjcT+pO7mK6GEzMGHfBTgpZdTDifpAptBjSSXJLIajcU28SPmL1IpdVHxyWyLgDYW0Tu2rcJBbZptosH9I1bKlajbn6zNBo7iRV0sa5ETl6DoPwzFZvZa3T6OvCAmYnGHMDoeH4lXugQdp7chtCt+aX5eV1qoGlFjLzNumFSfqDCCJ0lqjWvqqZ9WTYzZy1hphjl55cEdeD4='
            encSecKey = '55c149ec4ed08650753e8856c9d96d9df0e9ca4bfcd3a9ca219dd0b0da8e3b818dc64195f1889af0c738edfc31b68e26d89591bf537581b9984d25191e47f2d64bed45947db700a6647cc34c48312daec15b3a917d582208824090f044549702556e757c424a1fa06cf17cafec19422844f9a9ed31322e204d5a2edcb7270133'
            data = {
                'params':params,
                'encSecKey':encSecKey
                }
            res = requests.post(url,headers=headers,data=data)
            comment = json.loads(res.text)
            song_comment = comment['total']
            if song_comment > 30000:
                sheet.append([songs[song_id],song_comment])
                #print('%s 评论总计==> %s'%(songs[song_id],song_comment))
            else:
                pass
        except Exception as e:
            print('歌曲id ==> %s 报错,原因如下: %s'%(song_id,e))
            continue
        j += 1
    wb.save('wy_count_>1002.xlsx')


def main():
    print('正在执行中,请等待...')
    page = [1003,2001,2002,2003,6001,6002,6003,7001,7002,7003,4001,4002,4003] #所有歌手分类
    #page = [1002]
    songers = get_songers(page)
    songs = get_songs(songers)
    #songs = {'557583281':'哑巴','520458481':'背过手','27955656':'有没有','64443':'约定_mmmm','1293886117':'李荣浩的年少有为','1319908705':'贵姓' }
    get_comments(songs)
    print('执行完成,文件已保存至当前文件夹下==> wy_count.xlsx')

if __name__ == '__main__':
    main()
