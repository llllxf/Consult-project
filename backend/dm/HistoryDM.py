# @Time : 2021/2/9 11:55 AM 
# @Author : LinXiaofei
# @File : HistoryDM.py

from backend.dm.DialogManagement import DialogManagement
from backend.subject.history_business import *
from backend.data.data_process import read_file
import configparser


class HistoryDM(object):

    def __init__(self):
        config = configparser.ConfigParser()
        content = config.read("../backend/config.ini")

        config['DEFAULT']['subject'] = '历史'

        with open('../backend/config.ini', 'w') as file:
            config.write(file)
        self.dm = DialogManagement()
        year_pro = read_file("../backend/data/历史/year_pro.csv")
        self.dm.setConpro(['内容','概况','定义','简介','定义'])
        self.history_business = HistoryBussiness()
        print("HistoryDM????????????????????????????")

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

    def AEntityInformation(self, entity):
        return self.dm.AEntityInformation(entity)


