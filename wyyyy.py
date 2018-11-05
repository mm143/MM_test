import requests
import json

def get_comments(url):
    name_id = url.split('=')[1]
    headers = {
        "Referer":"https://music.163.com/song?id={}".format(name_id),
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
        }
    params='IjSqIGfHeRILGQ4Q5RavWpY3CR8AtxC4PgD/Q/ptdV9ADtYnkqXVO7xbXksFzs8ZYrw/jwsxWjUHQdzJCDE1gYNCQEOyrvjFB4M54JyozNa+TJdGCYisXRdzh34pf7w7TMXtymLcm/5W2tJt5E3rjA1cHeMMjNvQcI3gf8vPp17lrVvzS3aFEdKIqrqweS1N'
    encSecKey='28b1edf3175456c216913c0b6dece6a378fb383b26bb6dd0bcd6e0161e793a9344f4ed2f65ab4c3f51e220f638561d3249c26b7069116553cc378c707e3649ab10a90e434a1336c5a1c3a497ca3792e7969f9a4bfff1ad22e97d0ad6f283996af584cb41cefff69c64b580634c6ddf1b2f61335c60bb22575463d869400a6e71'
    data = {
        'params':params,
        'encSecKey':encSecKey
        }
    comments_url = "https://music.163.com/weapi/v1/resource/comments/R_SO_4_{}?csrf_token=".format(name_id)
    res = requests.post(comments_url,headers=headers,data=data)
    return res
    

def main():
    url = input('请输入要爬取的歌曲url:')  #到网易云音乐网站获取歌曲url
    res = get_comments(url)
    
    comment = json.loads(res.text)
    with open('content.txt','w',encoding='utf-8') as f: # 保存评论到本目录下
        for i in comment['hotComments']:
            try:
                nickname = i['user']['nickname']
                content = i['content']
                likedCount = i['likedCount']
                f.write('网友==> '+ nickname + '\n')
                f.write('评论==> '+ content + '\n')
                f.write('点赞==> '+ str(likedCount) + '\n')
                f.write('----------------------------------------------------------------------------\n')
            except:
                continue

    
if __name__ == '__main__':    
    main()
