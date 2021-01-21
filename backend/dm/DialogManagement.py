# @Time : 2020/12/13 11:11 AM 
# @Author : LinXiaofei
# @File : DialogManagement.py
import configparser
import numpy as np
config = configparser.ConfigParser()
config.read("../backend/config.ini")
from backend.nlu.processNLU import processNLU
from backend.graphSearch import normalBussiness


class DialogManagement(object):
    def __init__(self):
        self.nlu_util = processNLU()
        self.normal_bussiness = normalBussiness()


    def getProValue(self,entity,nlu_results):
        """
        :param entity:
        :param nlu_results:
        :return:
        """
        if nlu_results[1] == 0:
            return nlu_results
        if nlu_results[1] == 1:
            ans = self.normal_bussiness.doNormal([entity],nlu_results[0])
            return [ans[2],1,ans[0]]

        if nlu_results[1] == 2:
            ans = self.normal_bussiness.doNormal([entity], nlu_results[0])
            return [ans[2],2,nlu_results[2],ans[0]]

    def getEntName(self,entity,nlu_results):

        pro_list = self.normal_bussiness.searchEnt(entity,nlu_results[0])
        pro_value = np.array(pro_list)[:,1]
        similarPro = self.nlu_util.parse_util.getSimilarPro(nlu_results[1],pro_value)

        ind = list(pro_value).index(similarPro[0])

        return [pro_list[ind][0]+"的"+nlu_results[0]+":"+pro_list[ind][1],1,pro_list[ind][0]]

    def doNLU(self, words):

        """
        :param words: 句子
        :return:
        标识 答案 反问 实体
        无法回答：0
        可以回答：1
        确认问题：2
        """

        entity, nlu_results = self.nlu_util.process(words)

        if int(nlu_results[0]) == 0:
            return [0,"无法回答"+entity+"相关的问题。"]
        elif int(nlu_results[0]) == 1:
            ans = self.normal_bussiness.doNormal([entity], nlu_results[1])
            return [1, ans[2], ans[0]]
        elif int(nlu_results[0]) == 2:
            ans = self.normal_bussiness.doNormal([entity], nlu_results[1])

            return [2, ans[2], nlu_results[2],entity]


        """
        entity,nlu_results,task = self.nlu_util.process(words)
        if task == "proValue":
            return self.getProValue(entity,nlu_results)
        if task == "entName":
            return self.getEntName(entity,nlu_results)
        if task is None:
            return ['无法回答',0,None]
        """

    def AEntityInformation(self,entity):
        ans = self.normal_bussiness.getOneEntity(entity)
        print(ans)
        return ans