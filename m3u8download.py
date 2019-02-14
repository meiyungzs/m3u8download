import requests
import threading
from urllib.parse import urljoin
import re
import os
import time

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

def download(url):
    try:
        name = url.split('/')[-1]
        data = requests.get(url,timeout=5).content
        with open(save_dir+name,'wb') as f:
            f.write(data)
        print(url)
    except Exception as e:
        download(url)

def hecheng():
    os.chdir(save_dir)
    file_list = os.listdir()
    for i in file_list:
        if not i.endswith('.ts'):
            file_list.remove(i)

    file_list.sort()  

    os.system('echo "file output1.mp4\nfile output2.mp4" > mp4list.txt')
    os.system('ffmpeg -i "concat:%s" -acodec copy -vcodec copy -absf aac_adtstoasc output1.mp4'%'|'.join(file_list[0:len(file_list)//2]))
    os.system('ffmpeg -i "concat:%s" -acodec copy -vcodec copy -absf aac_adtstoasc output2.mp4'%'|'.join(file_list[len(file_list)//2:]))
    os.system('ffmpeg -y -f concat -safe 0 -i mp4list.txt -c copy finsh.mp4')
    os.system('rm -f output1.mp4 output2.mp4 mp4list.txt %s' % ' '.join(file_list))
    print("完成！")

def down_finish():
    while True:
        time.sleep(1)
        print(threading.active_count())
        if threading.active_count() == 2:
            hecheng()
            break

def main(url_m3u8):
    response = requests.get(url_m3u8,headers=headers).text
    print(response)
    if '#EXT-X-STREAM-INF' in  response:
        url = re.findall('\n(.*?\.m3u8)',response)[0]
        url2 = urljoin(url_m3u8,url)
        text = requests.get(url2,headers=headers).text
        parse_m3u8(text,url2)
    else:
        # print(response)
        parse_m3u8(response,url_m3u8)

def parse_m3u8(text,url_m3u8):
    print(text)       
    url_list = []
    for i in text.split('\n'):
        if i.endswith('.ts'):
            url = urljoin(url_m3u8,i)
            url_list.append(url)
    
    # if url_list == []:
        # parse_m3u8(text,url_m3u8)

    thread_list = []
    for i in url_list:
        t = threading.Thread(target=download,args=(i,))
        thread_list.append(t)

    for i in thread_list:
        i.start()
        # i.join()
    deamon = threading.Thread(target=down_finish) 
    deamon.start()   

if __name__ == "__main__":
    # 保存路径
    save_dir = 'video/'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # 下载视频的URL
    url_m3u8 = 'http://v3.julyedu.com/video/73/667/2a70b0e95b.m3u8'
    main(url_m3u8)
