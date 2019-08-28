# -*- coding:utf8 -*- ＃
# ==========================
# Name          MainTask.py
# Description:  爬取 http://www.jisudhw.com 的电影
# Author:       hayes
# Date:         2019/8/25 11:15
# ==========================

import GyUtils
import sys
import time
import datetime

reload(sys)
sys.setdefaultencoding('utf8')
logging = GyUtils.logger("log_movies.log")

class MainTask():
    def __init__(self):
        self.referer = 'http://www.jisudhw.com'

    def to_date(self, dateStr):

        return datetime.datetime.strptime(dateStr.strip(), "%Y-%m-%d %H:%M:%S")

    def action_step_one(self, url,last_date):
        soup = GyUtils.request_get(url)
        # soup = GyUtils.readText("html.txt")
        data = []
        if soup:
            tt = soup.find_all(name="span", attrs={"class": "tt"})
            for span in tt:

                li =  span.parent
                vb4 = li.find(name="span", attrs={"class": "xing_vb4"})
                update_date = li.find(name="span", attrs={"class": "xing_vb7"}).text
                name = vb4.text
                href = self.referer + vb4.find("a").get("href")
                if self.to_date(update_date) > self.to_date(last_date):
                    data.append((href, name))
        return data

    def action_step_two(self, url):
        soup = GyUtils.request_get(url)
        # soup = GyUtils.readText("html2.txt")
        filmInfo = {}
        if soup:
            vodBox = soup.find(name="div", attrs={"class": "vodBox"})
            filmInfo["uuid"] = int(time.time() * 1000000)
            filmInfo["film_pic"] = vodBox.find("img").get("src")
            filmInfo["film_name"] = vodBox.find("h2").text.replace("'", "`")
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
            filmInfo["film_nr"] = soup.find_all(name="div", attrs={"class": "vodplayinfo"})[1].text.replace("'","`")
            inputs = soup.find_all(name="input", attrs={"name": "copy_sel"})
            film_url = ""
            for input in inputs:
                bof_url = input.parent.text
                if not (str(bof_url).endswith("m3u8")) and not (str(bof_url).endswith("mp4")):
                    film_url = film_url + bof_url + "#"
            filmInfo["film_url"] = film_url[0:-1]
            return filmInfo

if __name__ == '__main1111__':
    task = MainTask()
    data = task.action_step_one("http://www.jisudhw.com/?m=vod-type-id-5.html","1997-01-02 12:12:12")
    for d in data :
        print d


if __name__ == '__main__':

    cursor = GyUtils.mysql_connect_cursor()
    task = MainTask()
    type = ['动作片', '喜剧片', '爱情片', '科幻片', '恐怖片', '剧情片', '战争片']
    for i in range(5, 12):
        url = 'http://www.jisudhw.com/?m=vod-type-id-{}.html'.format(i)
        sql = r"select max(film_update_time) dat from t_movies where film_column like '%"+type[i-5]+"%'"
        cursor.execute(sql)
        dat = cursor.fetchone()['dat']
        if dat:
            dat = dat[3:]
        if not dat:
            dat = "1970-01-01 00:00:00"
        logging.info("<<{}>>的上次爬取时间是{}".format(type[i-5],dat))
        data = task.action_step_one(url,dat)
        for href, name in data:
            filmInfo = task.action_step_two(href)
            bof_urls = filmInfo["film_url"].split("#")
            filmInfo.pop("film_url")
            sql = GyUtils.dict_2_insert_sql(filmInfo,"t_movies")
            logging.info(sql)
            cursor.execute(sql)

            for bof_url in bof_urls :
                sql_url = "insert into t_movies_url (uuid,film_name,film_url)values ('%s' , '%s' , '%s' )" \
                          % (filmInfo["uuid"],filmInfo["film_name"], bof_url)
                logging.info(sql_url)
                cursor.execute(sql_url)
            cursor.execute("commit")
            logging.info("<<{}>>  save done".format(filmInfo["film_name"]))
        logging.info(url+">>>>> success")





















