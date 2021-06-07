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

        self.dm.setConpro(['内容', '概况', '定义', '简介', '定义', '发展', '过程', '历史意义', '意义'])
        self.history_business = HistoryBussiness()


    def doNLU(self,words):
        entity, book_ans, task_type = self.history_business.dealBookSBV(words)
        print(entity, book_ans, task_type,"entity, ans, task_type")
        ans = []
        if '谁' in words or '哪位' in words or '哪个人' in words or '哪一个人' in words or '哪一位' in words:
            nluresult = self.history_business.dealWho(words)
            ans = self.dm.dealContent('单人',nluresult)
        elif entity:
            ans = self.dm.dealNormal(entity, book_ans)
        elif self.history_business.checkSplitEnt(words):
            ans = self.history_business.dealCombineEntForCon(words)

        if len(ans)==0 or ans[0] == 0:
            ans = self.dm.doNLU(words)

        if ans[0] == 0:
            return [0,'无法回答']

        return ans


