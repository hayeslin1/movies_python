#!/usr/bin/python
# -*- coding: utf-8 -*-
# ==========================================

# @Time    : 2019/9/6 3:12 PM
# @Author  : HayesLin
# @FileName: TV_Media_Task.py
# @Software: PyCharm

# ==========================================

from MainTask import *


class doTask():
    def __init__(self):
        self.referer = 'http://www.jisudhw.com'

    def action(self):
        pass









if __name__ == '__main__':

    mt = MainTask()
    url = 'http://jisudhw.com/?m=vod-type-id-12.html'

    soup = mt.action_step_one(url,last_date='1991-01-01 00:00:00')

    print soup
