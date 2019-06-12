#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import json
import os
import regex as re
import browser_cookie3
import numpy as np

mobile_headers = {
    'Accept': 'application/json, text/plain, */*',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
'Connection': 'keep-alive',
"Content-Type": "application/json",
'Content-Length': '0',
'Cookie': '_ga=GA1.2.966311996.1559739092; GCID=7beecdb-ca03875-7887861-c789959; _gid=GA1.2.1269686349.1560245138; GCESS=BAcEbtgv0QQEAC8NAAYE1iedlQkBAQMEFE0AXQwBAQIEFE0AXQgBAwsCBAAFBAAAAAAKBAAAAAABBCVwFgA-; Hm_lvt_022f847c4e3acd44d4a2481d9187f1e6=1559804304,1560245138,1560245160,1560300821; SERVERID=3431a294a18c59fc8f5805662e2bd51e|1560300886|1560300810; _gat=1; Hm_lpvt_022f847c4e3acd44d4a2481d9187f1e6=1560300887',
'Host': 'time.geekbang.org',
'Origin': 'https://account.geekbang.org',
'Referer': 'https://account.geekbang.org/dashboard/buy?category=1&sort=1&order=sort',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
}

# 专栏
my_column_url = "https://time.geekbang.org/serv/v1/my/columns"

# 视频专栏
video_url = "https://time.geekbang.org/serv/v1/column/articles"

# 音频专栏
audio_url = "https://time.geekbang.org/serv/v1/column/audios"

# 所有专栏
all_column_url = "https://time.geekbang.org/serv/v1/columns"

# 获取 Chrome cookie
cj = browser_cookie3.chrome()

JSON_PATH = os.path.join(os.getcwd(), 'json/')
AUDIO_PATH = os.path.join(os.getcwd(), 'audio/')
VIDEO_PATH = os.path.join(os.getcwd(), 'video/')

# mkdir
def make_dir(path):
    try:
        os.mkdir(path)
    except:
        pass

make_dir(JSON_PATH)
make_dir(VIDEO_PATH)
make_dir(AUDIO_PATH)

# 所有专栏
def fetch_all_column():
    payload = "{}"
    response = requests.request("POST", all_column_url, data=payload, headers=mobile_headers)
    json_data = json.loads(response.content.decode('utf-8'))

    print(json_data)
    data = json_data.get('code')
    if data != 0:
        return

    list = json_data.get('data').get('list')
    my_column = []

    for item in list:
        cid = item.get('id')
        column_unit = item.get('column_unit')
        column_title = item.get('column_title')
        had_sub = item.get('had_sub')
        is_include_audio = item.get('is_include_audio')

        message = "id = %s    has_audio = %s    column_unit = %s    column_title = %s" % (cid, is_include_audio, column_unit,  column_title)
        print(my_column)

        if had_sub:
            my_column.append(message)
    print("-" * 40)
    print("had sub:")
    print(my_column)

def column_type_string(column_type):
    return {
            1 : "audio",
            3 : "video",
            }.get(column_type, "other")

# 获取我的专栏
def fetch_my_column():
    payload = '{}'
    response = requests.request("POST", my_column_url, data=payload, headers=mobile_headers)
    json_data = json.loads(response.content.decode('utf-8'))

    print(json_data)
    data = json_data.get('code')
    if data != 0:
        return

    list = json_data.get('data').get('list')

    for item in list:
        id = item.get('id')
        column_type = item.get('column_type')
        column_title = item.get('column_title')
        print("id = %s  type = %s  column_title = %s" % (id, column_type_string(column_type), column_title))

# 根据专栏 id 获取视频
def download_video_by_cid(cid, size):
    payload = " {\"cid\":%s,\"size\":%d,\"prev\":%d,\"order\":\"earliest\"}" % (cid, size, 0)
    response = requests.request("POST", video_url, data=payload, cookies=cj, headers=mobile_headers)
    print(response.content.decode('utf-8'))
    download_videos(response, '')
def download_video_by_array (cid, numberArray, size):
    payload = " {\"cid\":%s,\"size\":%d,\"prev\":%d,\"order\":\"earliest\"}" % (cid, size, 0)
    response = requests.request("POST", video_url, data=payload, cookies=cj, headers=mobile_headers)
    download_videos(response, numberArray)
def download_videos(response, arrays):
    json_data = json.loads(response.content.decode('utf-8'))
    data = json_data.get('code')
    if data != 0:
        return

    list = json_data.get('data').get('list')
    index = 0
    # if arrays != '':
    #     arrays = np.array(arrays)
    print(arrays)
    for item in list:
        index = str(int(index) + 1)
        print(index)
        print(index not in arrays)
        if arrays != '' and index not in arrays:
            continue
        else:  
            video_media = item.get('video_media')
            article_title = item.get('article_title')

            pattern = ' |\|'
            article_title = re.sub(pattern, '_', article_title)
            print(article_title)
            print(video_media)
            if len(video_media) > 0:
                video = json.loads(video_media)
                video_path = VIDEO_PATH + article_title +'.mp4'
                m3u8 = video.get('hd').get('url')
                cmd = 'ffmpeg -y -i %s %s' % (m3u8, video_path)
                os.system(cmd.encode('utf-8'))

# 根据专栏 id 获取音频
def download_audio_by_cid(cid, size):
    payload = " {\"cid\":%d,\"size\":%d,\"prev\":%d,\"order\":\"newest\"}" % (cid, size, 0)
    response = requests.request("POST", audio_url, data=payload, headers=mobile_headers)
    download_audio(response)

def download_json(json_data, file_name):
    json_path = JSON_PATH + file_name + '.json'

    # save json file
    with open(json_path, 'wt') as f:
        # unicode
        json_string = json.dumps(json_data, sort_keys=False, ensure_ascii=False, indent=4)
        f.write(json_string)
        print("save : {}.json".format(file_name))
        f.close()

def download_one_audio(audio_download_url, article_sharetitle):
    if len(audio_download_url) > 0:
        print(audio_download_url)
        mp3_path = AUDIO_PATH + article_sharetitle +'.mp3'
        cmd = "wget -c %s -O %s" % (audio_download_url, mp3_path)
        os.system(cmd.encode('utf-8'))

def download_audio(response):
    json_data = json.loads(response.content.decode('utf-8'))
    print(json_data)
    data = json_data.get('code')
    if data != 0:
        return

    list = json_data.get('data').get('list')

    for item in list:
        audio_download_url = item.get('audio_download_url')
        article_sharetitle = item.get('article_sharetitle')

        pattern = ' |\|'
        article_sharetitle = re.sub(pattern, '_', article_sharetitle)
        print(article_sharetitle)

        download_one_audio(audio_download_url, article_sharetitle)

def exec_audio():
    cid = int(input("input audio column id:\n> "))
    download_audio_by_cid(cid, default_size)


def exec_video():
    cid = int(input("input video column id:\n> "))
    download_video_by_cid(cid, default_size)

print("login 'http://geekbang.org' from chrome first")

if __name__ == "__main__":
    """ 下载音频
    cid = 50
    size = 100
    download_audio_by_cid(cid, size)
    fetch_my_column()
    """

    """ 下载视频
    cid = 77
    size = 100
    download_video_by_cid(cid, size)
    """

    """ 查看所有专栏
    """
    fetch_all_column()

    """ 查看我的专栏
    fetch_my_column()
    """
