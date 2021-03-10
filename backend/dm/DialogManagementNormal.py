# @Time : 2020/12/13 11:11 AM 
# @Author : LinXiaofei
# @File : DialogManagement.py
import configparser
import numpy as np
config = configparser.ConfigParser()
config.read("../backend/config.ini")
from backend.nlu.processNLU import processNLU
from backend.graphSearch import normalBussiness


class DialogManagementNormal(object):

    def __init__(self):
        self.nlu_util = processNLU()
        self.normal_bussiness = normalBussiness()
        self.con_pro = []

    def setConpro(self, con_pro):
        self.con_pro = con_pro

    def dealContent(self,etype,nlu_results):
        print(nlu_results,"dealContent")

        content = nlu_results[:2]
        key_entity = nlu_results[2:]

        if len(content) == 2:
            return [0,"无法回答该问题"]
        ans,ent = self.normal_bussiness.doConStrict(etype,content)

        if ans:
            return [1,ans,ent]
        else:
            for e in key_entity:
                ans = self.normal_bussiness.doNormalForFalseStrict(e,content)
                if ans:
                    return [1,ans,e]
        return [0,"无法回答该问题"]


    def doNLU(self, words):

        """
        :param words: 句子
        :return:
        标识 答案 反问 实体
        无法回答：0
        可以回答：1
        确认问题：2
        """

        entity, nlu_results,task = self.nlu_util.process(words)
        print(entity, nlu_results,task,"entity, nlu_results,task")

        if task == "false":

            return [0, "对不起，无法回答该问题。"]

        if task == "normal":
            return self.dealNormal(entity,nlu_results)


        if task == "content":
            return self.dealContent(entity, nlu_results)


    def setConpro(self, con_pro):
        self.con_pro = con_pro

    def dealNormal(self,entity, nlu_results):
        if int(nlu_results[0]) == 0:
            return [0,"无法回答相关的问题。"]
        elif int(nlu_results[0]) == 1:
            ans = self.normal_bussiness.doNormal([entity], nlu_results[1])
            return [1, ans[2], ans[0]]
        elif int(nlu_results[0]) == 2:
            ans = self.normal_bussiness.doNormal([entity], nlu_results[1])
            return [2, ans[2], nlu_results[2],entity]
        elif int(nlu_results[0]) == 3:
            print(nlu_results,"doNormalbyCon")
            ans = self.normal_bussiness.doNormalbyConStrict([entity],nlu_results[1:],self.con_pro)
            if ans:
                return [1,ans,entity]
            else:
                print(nlu_results)
                print(nlu_results[1])
                ans = self.normal_bussiness.doNormalForFalseStrict(entity,nlu_results[1:])
                if ans:
                    return [1,ans,entity]
                return [0,"无法回答相关的问题。"]
        elif int(nlu_results[0]) == 4:
            ans = self.normal_bussiness.doNormalForFalseStrict(entity, nlu_results[1:])
            if ans:
                return [1, ans, entity]

            return [0, "无法回答相关的问题。"]





    def dealContent(self,etype,nlu_results):
        print(nlu_results,"dealContent")

        content = nlu_results[:2]
        key_entity = nlu_results[2:]

        print(content)
        ans = self.normal_bussiness.doConStrict(etype,content)

        if ans:
            return [1,ans,etype]
        else:
            for e in key_entity:
                ans = self.normal_bussiness.doNormalForFalseStrict(e,content)
                if ans:
                    return [1,ans,e]
        return [0,"无法回答该问题"]


    def doNLU(self, words):

        """
        :param words: 句子
        :return:
        标识 答案 反问 实体
        无法回答：0
        可以回答：1
        确认问题：2
        """

        entity, nlu_results,task = self.nlu_util.process(words)
        print(entity, nlu_results,task,"??????")

        if task == "false":
            print(nlu_results,"false")
            ans = self.normal_bussiness.doNormalForFalseStrict(entity, nlu_results)
            if ans:
                return [1, ans, None]

            return [0, "对不起，无法回答该问题。"]

        if task == "normal":
            return self.dealNormal(entity,nlu_results)

        if task == "content":
            return self.dealContent(entity, nlu_results)