import os
import urllib

import requests
from lxml import etree


def get_from_github(github_url):
    """
    从github网页获取歌曲列表配置
    :param github_url: github网址
    :return: 歌曲配置列表
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'}
    content = None
    for i in range(3):
        try:
            response = requests.get(github_url, headers=headers, timeout=10)
            content = response.content.decode("utf-8")
            break
        except Exception as e:
            print("请求失败[%s]准备重试第%s次..." % (github_url, str(i + 1)))
    if content is None:
        return None
    return _get_from_github_html_content(github_url, content)


def _get_from_github_html_content(github_url, content):
    """
    解析github网页内容来获取歌曲列表配置
    :param github_url: github地址
    :param content: 网页文件路径
    :return: 歌曲配置列表
    """
    document = etree.HTML(content)
    music_text_list = document.xpath("//main//a[contains(text(), '.mp3')]//text()")
    songs = []
    for music_text in music_text_list:
        song = {}
        song['name'] = music_text[:-4]
        song['url'] = github_url.replace('/tree/', '/blob/') + "/" + urllib.parse.quote(music_text) + "?raw=true"
        songs.append(song)
    return songs


def get_from_local_github_html_file(github_url, filepath):
    """
    从本地下载下来的github网页文件获取歌曲列表配置
    :param filepath: 网页文件路径
    :return: 歌曲配置列表
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    return _get_from_github_html_content(github_url, content)


def get_from_local_disk(basedir):
    """
    从本地获取歌曲列表配置
    :param basedir: 根路径，表示从哪个文件夹找mp3文件
    :return: 歌曲配置列表
    """
    filenames = os.listdir(basedir)
    songs = []
    for filename in filenames:
        if filename.endswith('.mp3'):
            songs.append({'name': filename[:-4], 'url': basedir + "\\" + filename})
    return songs


if __name__ == '__main__':
    songs = get_from_local_disk("D:\\upload_music")
    print("从本地硬盘加载：", songs)

    # github网页上歌曲文件夹打开后的地址
    github_url = "https://github.com/191059014/music/tree/main/songs"
    songs = get_from_github(github_url)
    print("从github网页加载：", songs)

    songs = get_from_local_github_html_file(github_url, "C:\\Users\\Administrator\\Desktop\\music.html")
    print("从本地下载下来的github网页文件加载：", songs)
