# -*- coding:utf8 -*- ＃
# ==========================
# Name          MainTask.py
# Description:  爬取 http://www.jisudhw.com 的电影
# Author:       hayes
# Date:         2019/8/25 11:15
# ==========================

import GyUtils
import sys

reload(sys)
sys.setdefaultencoding('utf8')
logging = GyUtils.logger("log_movies.log")

if __name__ == '__main__':

    cursor = GyUtils.mysql_connect_cursor()
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
        data = GyUtils.action_step_one(url,dat)
        for href, name in data:
            filmInfo = GyUtils.action_step_two(href)
            bof_urls = filmInfo["film_url"].split("#")
            filmInfo.pop("film_url")
            filmInfo["film_column"] = type[i-5]
            sql = GyUtils.dict_2_insert_sql(filmInfo,"t_movies")
            # logging.info(sql)
            cursor.execute(sql)

            for bof_url in bof_urls :
                sql_url = "insert into t_movies_url (uuid,film_name,film_url)values ('%s' , '%s' , '%s' )" \
                          % (filmInfo["uuid"],filmInfo["film_name"], bof_url)
                # logging.info(sql_url)
                cursor.execute(sql_url)
            cursor.execute("commit")
            logging.info("<<{}>>{}集   save done".format(filmInfo["film_name"], len(bof_urls)))
        logging.info(url+">>>>> success")





















