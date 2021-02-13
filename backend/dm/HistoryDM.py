# @Time : 2021/2/9 11:55 AM 
# @Author : LinXiaofei
# @File : HistoryDM.py

from backend.dm.DialogManagement import DialogManagement
from backend.subject.history_business import *
from backend.data.data_process import read_file

class HistoryDM(object):

    def __init__(self):
        self.dm = DialogManagement()
        year_pro = read_file("../backend/data/历史/year_pro.csv")
        self.dm.setConpro(year_pro)

    def doNLU(self,words):
        entity, ans, task_type = dealBookSBV(words)
        print(entity, ans, task_type,"entity, ans, task_type")
        if '谁' in words or '哪位' in words or '哪个人' in words or '哪一个人' in words or '哪一位' in words:
            nluresult = dealWho(words)
            ans = self.dm.dealContent('单人',nluresult)
        elif '哪年' in words or '哪一年' in words or '几年' in words or '多少年' in words:
            ans = dealYear(words)
        elif entity:

            return self.dm.dealNormal(entity, ans)
        else:
            ans = self.dm.doNLU(words)
        return ans


