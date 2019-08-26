# -*- coding: utf-8 -*-
# @Time    : 2019-08-26 18:55
# @Author  : Hayes Lin
# @File    : searchTask.py
# @Software: PyCharm

import GyUtils
import sys

reload(sys)
sys.setdefaultencoding('utf8')


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

    # your_input = str(raw_input('please input your want:'))

    your_input = "使徒行者"

    do = doTask(your_input);
    data = do.action();
    for name, column, href in data:
        print  name,"\t", column,"\t", href
