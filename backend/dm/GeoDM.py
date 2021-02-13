# @Time : 2021/2/8 3:57 PM 
# @Author : LinXiaofei
# @File : GeoDM.py
from backend.dm.DialogManagement import DialogManagement
from backend.subject.geoBussiness import *


class GeoDM(object):

    def __init__(self):
        self.dm = DialogManagement()
        self.dm.setConpro(['作用','特征','影响','简介','定义','河流','湖泊','内容'])


    def doNLU(self,words):
        if '最' in  words:
            #print("geo-dm=======================")
            ans = doMost(words)
            if ans[0] == 1:
                #print("this work")
                return ans
        ans = self.dm.doNLU(words)
        return ans

