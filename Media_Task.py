#!/usr/bin/python
# -*- coding: utf-8 -*-
# ==========================================

# @Time    : 2019/9/6 3:12 PM
# @Author  : HayesLin
# @FileName: Media_Task.py
# @Software: PyCharm

# ==========================================

from MainTask import *


class doTask():
    def __init__(self):
        self.referer = 'http://www.jisudhw.com'

    def action(self, cursor):

        task = MainTask()
        type = ['内地综艺', '港台综艺', '日韩综艺', '欧美综艺']
        for i in range(26, 30):
            url = 'http://www.jisudhw.com/?m=vod-type-id-{}.html'.format(i)
            sql = r"select max(film_update_time) dat from t_media where film_column like '%" + type[i - 26] + "%'"
            cursor.execute(sql)
            dat = cursor.fetchone()['dat']
            if dat:
                dat = dat[3:]
            if not dat:
                dat = "1970-01-01 00:00:00"
            logging.info("<<{}>>的上次爬取时间是{}".format(type[i - 26], dat))
            data = task.action_step_one(url, dat)
            for href, name in data:
                filmInfo = task.action_step_two(href)
                sql = "select count(1) ct from t_media where film_name = '{}'".format(filmInfo["film_name"])
                cursor.execute(sql)
                has = cursor.fetchone()['ct']
                if has:
                    logging.info("<<" + filmInfo["film_name"] + ">> 已经存在!!")
                    continue
                bof_urls = filmInfo["film_url"].split("#")
                filmInfo.pop("film_url")
                filmInfo["film_column"] = type[i - 26]
                sql = GyUtils.dict_2_insert_sql(filmInfo, "t_media")
                # logging.info(sql)
                cursor.execute(sql)

                for bof_url in bof_urls:
                    sql_url = "insert into t_movies_url (uuid,film_name,film_url)values ('%s' , '%s' , '%s' )" \
                              % (filmInfo["uuid"], filmInfo["film_name"], bof_url)
                    # logging.info(sql_url)
                    cursor.execute(sql_url)
                cursor.execute("commit")
                logging.info("<<{}>>{}集   save done".format(filmInfo["film_name"], len(bof_urls)))
            logging.info(url + ">>>>> success")

    def updateDataBase(self, cursor):
        mt = MainTask()
        sql = r"SELECT * from t_media where film_notes not like '%完结'"
        cursor.execute(sql)
        mysqlData = cursor.fetchall();
        for ddd in mysqlData:

            uuid = ddd['uuid']
            sql = r"SELECT count(1) ct from t_movies_url where uuid ='{}'".format(uuid)
            cursor.execute(sql)
            muchJi = cursor.fetchone()['ct']

            film_href = ddd['film_href']
            filmInfo = mt.action_step_two(film_href)
            if not filmInfo:
                continue
            bof_urls = filmInfo["film_url"].split("#")
            if len(bof_urls) > muchJi:
                for index, bof_url in enumerate(bof_urls):
                    if (index + 1) > muchJi:
                        sql_url = "insert into t_movies_url (uuid,film_name,film_url)values ('%s' , '%s' , '%s' )" \
                                  % (uuid, filmInfo["film_name"], bof_url)
                        logging.info(sql_url)
                        cursor.execute(sql_url)
                sql = r"update t_media set film_notes='{}'".format(filmInfo["film_notes"])
                cursor.execute(sql)
                cursor.execute("commit")
            else:
                logging.info("<<" + filmInfo["film_name"] + ">> 暂无更新")

    def getNavigation(self):
        url = 'http://jisudhw.com'
        soup = GyUtils.request_get(url)
        # soup = GyUtils.readText("html.txt")
        div = soup.find("div", attrs={'class': 'sddm'})
        asss = div.find_all("a")
        for a in asss:
            print a


if __name__ == '__main__':
    cursor = GyUtils.mysql_connect_cursor()

    dt = doTask()
    dt.updateDataBase(cursor)
    dt.action(cursor);
    # dt.getNavigation()