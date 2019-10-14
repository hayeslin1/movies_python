# -*- coding:utf-8 -*- ＃
# ==========================
# Name          Gyutils
# Description:  OK资源网爬虫 公共类
# Author:       hayes
# Date:         8/24/19
# ==========================

import logging
import requests
import random
from bs4 import BeautifulSoup
import pymysql
import time
import datetime


referer = 'http://www.jisudhw.com'


# 记录日志
def logger(log_name):
    logging.basicConfig(level=logging.INFO,  # 控制台打印的日志级别
                        # when='D',  #when是间隔的时间单位，单位有以下几种：S 秒 M 分 H 小时、 D 天、 W 每星期（interval==0时代表星期一） midnight 每天凌晨
                        filename=log_name,
                        filemode='a',  ##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志  # a是追加模式，默认如果不写的话，就是追加模式
                        format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'  # 日志格式
                        )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
    console.setFormatter(formatter)
    logging.getLogger("").addHandler(console)
    return logging


def request_get(url):
    r = requests.get(url, headers=header, timeout=10)
    if r.status_code is 200:
        # logging.info("数据加载完成........")
        soup = BeautifulSoup(r.content, 'lxml')
        return soup
    else:
        return None


def request_post(url, data):
    r = requests.post(url, headers=header, data=data, timeout=10)
    if r.status_code is 200:
        # logging.info("数据加载完成........")
        soup = BeautifulSoup(r.content, 'lxml')
        return soup
    else:
        return None


def readText(path):
    txt = open(path).read()
    return BeautifulSoup(txt, 'lxml')


def dict_2_insert_sql(d, table):
    sql = "insert into %s set " % table
    tmplist = []
    for k, v in d.items():

        tmp = " %s = '%s' " % (str(k), str(v))
        tmplist.append('' + tmp + '')
    kkk = ",".join(tmplist)
    sql += kkk
    return sql


def mysql_connect_cursor(
    host = 'hayeslin.xyz',
    user = 'root',
    pasd = '1qaz!QAZ',
    db = 'movies'):
    try:
        conn = pymysql.connect(host=host, port=3306, user=user, password=pasd, db=db, charset='utf8',
                               cursorclass=pymysql.cursors.DictCursor)
        logging.info("mysql connection success..........")
    except Exception as e:
        logging.error(e.message)
        exit(3306)
    return conn.cursor()  # 获取一个游标


def to_date(dateStr):

        return datetime.datetime.strptime(dateStr.strip(), "%Y-%m-%d %H:%M:%S")

def action_step_one(url, last_date):
    soup = request_get(url)
    # soup = GyUtils.readText("html.txt")
    data = []
    if soup:
        tt = soup.find_all(name="span", attrs={"class": "tt"})
        for span in tt:

            li = span.parent
            vb4 = li.find(name="span", attrs={"class": "xing_vb4"})
            update_date = li.find(name="span", attrs={"class": "xing_vb6"}).text
            name = vb4.text
            href = referer + vb4.find("a").get("href")
            if to_date(update_date + " 00:00:00") > to_date(last_date):
                data.append((href, name))
    return data


def action_step_two(url):
    soup = request_get(url)
    # soup = GyUtils.readText("html2.txt")
    filmInfo = {}
    if soup:
        vodBox = soup.find(name="div", attrs={"class": "vodBox"})
        filmInfo["uuid"] = int(time.time() * 1000000)
        filmInfo["film_href"] = url
        filmInfo["film_pic"] = vodBox.find("img").get("src")
        filmInfo["film_name"] = vodBox.find("h2").text.replace("'", "`")
        filmInfo["film_notes"] = vodBox.find("span").text.replace("'", "`")
        vodinfobox = vodBox.find("div", attrs={"class": "vodinfobox"})
        lis = vodinfobox.find_all("li")
        filmInfo["film_alias"] = lis[0].text.replace("'", "`")
        filmInfo["film_director"] = lis[1].text.replace("'", "`")
        filmInfo["film_stars"] = lis[2].text.replace("'", "`")
        filmInfo["film_column"] = lis[3].text.replace("'", "`")
        filmInfo["film_area"] = lis[4].text.replace("'", "`")
        filmInfo["film_language"] = lis[5].text
        filmInfo["film_release_year"] = lis[6].text
        filmInfo["film_time_length"] = lis[7].text
        filmInfo["film_update_time"] = lis[8].text
        filmInfo["film_score"] = lis[11].text
        filmInfo["film_type"] = lis[14].text.replace("'", "`")
        filmInfo["film_nr"] = soup.find_all(name="div", attrs={"class": "vodplayinfo"})[1].text.replace("'", "`")
        inputs = soup.find_all(name="input", attrs={"name": "copy_sel"})
        film_url = ""
        for input in inputs:
            bof_url = input.parent.text
            if not (str(bof_url).endswith("m3u8")) and not (str(bof_url).endswith("mp4")):
                film_url = film_url + bof_url + "#"
        filmInfo["film_url"] = film_url[0:-1]
        return filmInfo


User_Agents = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52"]
header = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Referer': 'https://www.baidu.com',
    'User-Agent': random.choice(User_Agents)
}
