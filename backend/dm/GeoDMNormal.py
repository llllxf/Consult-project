# @Time : 2021/2/8 3:57 PM 
# @Author : LinXiaofei
# @File : GeoDM.py
from backend.dm.DialogManagementNormal import DialogManagementNormal
from backend.subject.geoBussiness import *
import configparser


class GeoDMNormal(object):

    def __init__(self):
        config = configparser.ConfigParser()
        content = config.read("../backend/config.ini")

        config['DEFAULT']['subject'] = '地理'

        with open('../backend/config.ini', 'w') as file:
            config.write(file)
        self.dm = DialogManagementNormal()
        self.geo_dm = GeoBussiness()
        self.dm.setConpro(['作用','特征','影响','简介','定义','河流','湖泊','内容'])
        print("GeoDM????????????????????????????")


    def doNLU(self,words):
        flag, ans = self.geo_dm.getCompare(words)

        if flag:
            return ans
        if '最' in  words:
            #print("geo-dm=======================")
            ans = self.geo_dm.doMost(words)
            if ans[0] == 1:
                #print("this work")
                return ans


        ans = self.dm.doNLU(words)

        if int(ans[0]) == 0:
            ans = [0,'无法回答',ans[1]]

        if int(ans[0]) == 5:
            ans = self.geo_dm.searchBinaryRel(words,ans[1:])

        if int(ans[0]) == 6:
            ans = self.geo_dm.searchBinaryPRel(ans[1:])

        return ans


    def AEntityInformation(self, entity):
        return self.dm.AEntityInformation(entity)

