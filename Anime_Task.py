#!/usr/bin/python
# -*- coding: utf-8 -*-
# ==========================================

# @Time    : 2019/9/6 3:12 PM
# @Author  : HayesLin
# @FileName: Media_Task.py
# @Software: PyCharm

# ==========================================

import GyUtils
import sys
reload(sys)
sys.setdefaultencoding('utf8')
logging = GyUtils.logger("log_Anime.log")


class doTask():

    def action(self, cursor):

        type = ['国产动漫', '日韩动漫', '欧美动漫', '港台动漫','海外动漫']
        for i, ttt in enumerate([23, 24, 25, 31, 32]):
            url = 'http://www.jisudhw.com/?m=vod-type-id-{}.html'.format(ttt)
            sql = r"select max(film_update_time) dat from t_anime where film_column like '%" + type[i] + "%'"
            cursor.execute(sql)
            dat = cursor.fetchone()['dat']
            if dat:
                dat = dat[3:]
            if not dat:
                dat = "1970-01-01 00:00:00"
            logging.info("<<{}>>的上次爬取时间是{}".format(type[i], dat))
            data = GyUtils.action_step_one(url, dat)
            for href, name in data:
                filmInfo = GyUtils.action_step_two(href)
                sql = "select count(1) ct from t_anime where film_name = '{}'".format(filmInfo["film_name"])
                cursor.execute(sql)
                has = cursor.fetchone()['ct']
                if has:
                    logging.info("<<" + filmInfo["film_name"] + ">> 已经存在!!")
                    continue
                bof_urls = filmInfo["film_url"].split("#")
                filmInfo.pop("film_url")
                filmInfo["film_column"] = type[i]
                sql = GyUtils.dict_2_insert_sql(filmInfo, "t_anime")
                # logging.info(sql)
                cursor.execute(sql)

                for bof_url in bof_urls:
                    sql_url = "insert into t_movies_url (uuid,film_name,film_url)values ('%s' , '%s' , '%s' )" \
                              % (filmInfo["uuid"], filmInfo["film_name"], bof_url)
                    # logging.info(sql_url)
                    cursor.execute(sql_url)
                cursor.execute("commit")
                logging.info("<<{}>>{}集   save done".format(filmInfo["film_name"],len(bof_urls)))
            logging.info(url + ">>>>> success")

    def updateDataBase(self, cursor):
        sql = r"SELECT * from t_anime where film_notes not like '%完结'"
        cursor.execute(sql)
        mysqlData = cursor.fetchall();
        for ddd in mysqlData:

            uuid = ddd['uuid']
            sql = r"SELECT count(1) ct from t_movies_url where uuid ='{}'".format(uuid)
            cursor.execute(sql)
            muchJi = cursor.fetchone()['ct']

            film_href = ddd['film_href']
            filmInfo = GyUtils.action_step_two(film_href)
            if not filmInfo:
                continue
            bof_urls = filmInfo["film_url"].split("#")
            if len(bof_urls) > muchJi:
                for index, bof_url in enumerate(bof_urls):
                    if (index + 1) > muchJi:
                        sql_url = "insert into t_movies_url (uuid,film_name,film_url)values ('%s' , '%s' , '%s' )" % (uuid, filmInfo["film_name"], bof_url)
                        logging.info(sql_url)
                        cursor.execute(sql_url)
                sql = r"update t_anime set film_notes='{}',film_update_time='{}'  where uuid='{}'".format(filmInfo["film_notes"],filmInfo["film_update_time"],uuid)
                cursor.execute(sql)
                cursor.execute("commit")
            else:
                logging.info("<<" + filmInfo["film_name"] + ">> 暂无更新")



if __name__ == '__main__':
    cursor = GyUtils.mysql_connect_cursor()

    dt = doTask()
    dt.updateDataBase(cursor)
    dt.action(cursor);
