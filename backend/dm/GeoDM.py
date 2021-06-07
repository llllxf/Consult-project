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
        self.dm.setConpro(['作用','特征','影响','简介','定义','湖泊','内容','原理'])
        print("GeoDM=========================================================")


    def doNLU(self,words):

        flag,ans = self.geo_dm.getCompare(words)

        if flag:
            return ans

        print("getCompar===================",flag,ans)
        #return [0,'无法回答']

        ans = self.geo_dm.getSum(words)

        print("====================2", ans)
        if ans:
            return ans

        if '最' in words:

            ans = self.geo_dm.doMost(words)
            if ans[0] == 1:
                return ans

        ans = self.dm.doNLU(words)
        if int(ans[0]) == 0:
            ans = [0,'无法回答',ans[1]]

        if int(ans[0]) == 5:
            ans = self.geo_dm.searchBinaryRel(words,ans[1:])

        if int(ans[0]) == 6:
            ans = self.geo_dm.searchBinaryPRel(ans[1:])

        return ans

    def getGeoType(self):
        type_list = read_file("../backend/data/地理/etype.csv")
        type_list = list(sorted(type_list, key=lambda i: len(i)))
        return type_list

    def getEntity(self,etype):
        ent_list = self.geo_dm.getEntity(etype)
        return ent_list

    def AEntityInformation(self, entity):
        return self.dm.AEntityInformation(entity)

    def AEntityRelation(self, entity):
        return self.geo_dm.getOneEntityRelation(entity)

