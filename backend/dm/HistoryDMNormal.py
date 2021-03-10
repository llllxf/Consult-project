# @Time : 2021/2/9 11:55 AM 
# @Author : LinXiaofei
# @File : HistoryDM.py

from backend.dm.DialogManagementNormal import DialogManagementNormal
from backend.subject.history_business import *
from backend.data.data_process import read_file

import configparser

class HistoryDMNormal(object):

    def __init__(self):
        config = configparser.ConfigParser()
        content = config.read("../backend/config.ini")

        config['DEFAULT']['subject'] = '历史'

        with open('../backend/config.ini', 'w') as file:
            config.write(file)
        self.dm = DialogManagementNormal()
        year_pro = read_file("../backend/data/历史/year_pro.csv")
        self.dm.setConpro(year_pro)
        self.history_business = HistoryBussiness()


    def doNLU(self,words):
        entity, book_ans, task_type = self.history_business.dealBookSBV(words)
        print(entity, book_ans, task_type,"entity, ans, task_type")
        ans = []
        if '谁' in words or '哪位' in words or '哪个人' in words or '哪一个人' in words or '哪一位' in words:
            nluresult = self.history_business.dealWho(words)
            ans = self.dm.dealContent('单人',nluresult)
        elif '哪年' in words or '哪一年' in words or '几年' in words or '多少年' in words:
            ans = self.history_business.dealYear(words)
        elif entity:
            ans = self.dm.dealNormal(entity, book_ans)
        elif self.history_business.checkSplitEnt(words):
            ans = self.history_business.dealCombineEntForCon(words)

        if len(ans)==0 or ans[0] == 0:
            ans = self.dm.doNLU(words)

        return ans


