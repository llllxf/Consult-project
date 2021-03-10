# @Time : 2021/2/8 3:57 PM 
# @Author : LinXiaofei
# @File : GeoDM.py
from backend.dm.DialogManagement import DialogManagement
from backend.subject.geoBussiness import *
import configparser



class GeoDM(object):

    def __init__(self):
        config = configparser.ConfigParser()
        content = config.read("../backend/config.ini")

        config['DEFAULT']['subject'] = '地理'

        with open('../backend/config.ini', 'w') as file:
            config.write(file)

        self.dm = DialogManagement()
        self.geo_dm = GeoBussiness()
        self.dm.setConpro(['作用','特征','影响','简介','定义','河流','湖泊','内容','原理'])
        print("GeoDM????????????????????????????")


    def doNLU(self,words):

        if '最' in  words:
            #print("geo-dm=======================")
            ans = self.geo_dm.doMost(words)
            if ans[0] == 1:
                return ans

        ans = self.dm.doNLU(words)
        return ans

    def AEntityInformation(self, entity):
        return self.dm.AEntityInformation(entity)

