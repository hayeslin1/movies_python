# -*- coding: utf-8 -*-
# @Time    : 2019-08-26 18:55
# @Author  : Hayes Lin
# @File    : searchTask.py
# @Software: PyCharm

import GyUtils
import sys

reload(sys)
sys.setdefaultencoding('utf8')
logging = GyUtils.logger("log_search.log")

class doTask():
    def __init__(self, data):
        self.data = {'wd': data}
        self.url = "http://www.jisudhw.com/index.php?m=vod-search"
        self.referer = 'http://www.jisudhw.com'

    def action(self):
        soup = GyUtils.request_post(self.url, self.data)
        data = []
        if soup:
            tt = soup.find_all(name="span", attrs={"class": "tt"})
            for span in tt:
                li = span.parent
                vb4 = li.find(name="span", attrs={"class": "xing_vb4"})
                vb5 = li.find(name="span", attrs={"class": "xing_vb5"})
                name = vb4.text
                column = vb5.text
                href = self.referer + vb4.find("a").get("href")
                data.append((name, column, href))
        return data




if __name__ == '__main__':

    href_film = ''

    your_input = str(raw_input('please input your want:'))
    if your_input:
        do = doTask(your_input);
        data = do.action();
        for i in range(len(data)):
            print "标号:", i+1 , "   >>> 资源 : ", data[i][0], data[i][1] ,data[i][2]

        row = raw_input('请输入前面的标号:(不选可直接回车)')
        if row:
            rowi = row.split(",")[::-1]
            for i in rowi :
                ri = int(i)
                href_film = data[ri-1][2]

                if href_film:
                    filmInfo = GyUtils.action_step_two(href_film)
                    if filmInfo:
                        bof_urls = filmInfo["film_url"].split("#")
                        filmInfo.pop("film_url")
                        sql = "" ;
                        if data[ri-1][1].endswith("片"):
                            sql = GyUtils.dict_2_insert_sql(filmInfo, "t_movies")
                        elif data[ri-1][1].endswith("剧"):
                            sql = GyUtils.dict_2_insert_sql(filmInfo, "t_television")
                        elif data[ri-1][1].endswith("动漫"):
                            sql = GyUtils.dict_2_insert_sql(filmInfo, "t_anime")
                        elif data[ri-1][1].endswith("综艺"):
                            sql = GyUtils.dict_2_insert_sql(filmInfo, "t_media")

                        # logging.info(sql)
                        cursor = GyUtils.mysql_connect_cursor()
                        cursor.execute(sql)

                        for bof_url in bof_urls:
                            sql_url = "insert into t_movies_url (uuid,film_name,film_url)values ('%s' , '%s' , '%s' )" \
                                      % (filmInfo["uuid"], filmInfo["film_name"], bof_url)
                            # logging.info(sql_url)
                            cursor.execute(sql_url)
                        cursor.execute("commit")
                        logging.info("<<{}>>{}集   save done".format(filmInfo["film_name"], len(bof_urls)))

