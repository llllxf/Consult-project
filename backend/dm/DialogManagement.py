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
        self.con_pro = []

    def setConpro(self, con_pro):
        self.con_pro = con_pro



    def dealNormal(self,entity, nlu_results):
        print("dealNormal,nlu_results",nlu_results)


        if int(nlu_results[0]) == 0:
            return [0,entity,nlu_results[1:]]
        elif int(nlu_results[0]) == 1:
            ans = self.normal_bussiness.doNormal([entity], nlu_results[1])
            return [1, ans[2], ans[0]]
        elif int(nlu_results[0]) == 2:
            ans = self.normal_bussiness.doNormal([entity], nlu_results[1])
            return [2, ans[2], nlu_results[2],entity]
        elif int(nlu_results[0]) == 3:
            print(nlu_results,"doNormalbyCon")
            ans = self.normal_bussiness.doNormalbyCon([entity],nlu_results[1:],self.con_pro)
            if ans:
                return [1,ans,entity]
            else:
                print(nlu_results)
                print(nlu_results[1])
                ans,ent = self.normal_bussiness.doNormalForFalse(entity,nlu_results[1:])
                if ans:
                    return [1,ans,ent]
                return [0,entity,nlu_results[1:]]
        elif int(nlu_results[0]) == 4:
            ans,ent = self.normal_bussiness.doNormalForFalse(entity, nlu_results[1:])
            if ans:
                return [1, ans, ent]

            return [0, entity,nlu_results[1:]]
        """
        elif int(nlu_results[0]) == 5:
             ans = self.normal_bussiness.searchBinaryRel([entity], nlu_results[1])
             return [1, ",".join(ans), entity]
        """

    def dealContent(self,etype,nlu_results):
        print(nlu_results,"dealContent")

        content = nlu_results[:2]
        key_entity = nlu_results[2:]

        print(content,"dealContent")
        ans,ent = self.normal_bussiness.doCon(etype,content)
        print(ans,ent, "dealContent")

        if ans:
            return [1,ans,ent]
        elif len(key_entity) >= 1:

            for e in key_entity[0]:
                print(key_entity,"key_entity")
                ans,ent = self.normal_bussiness.doNormalForFalse(e,content)
                if ans:
                    return [1,ans,ent]
        return [0,ent,content]


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
            ans,ent = self.normal_bussiness.doNormalForFalse(entity, nlu_results)
            if ans:
                return [1, ans,ent ]
            return [0, entity, nlu_results]
        if task == "normal":
            return self.dealNormal(entity,nlu_results)
        if task == "rel_normal":
            return [5,[nlu_results[1],None],entity]
        if task == "content":
            return self.dealContent(entity, nlu_results)
        if task == 'sbv_rel':
            print("sbv_rel===================",nlu_results,entity)
            return [5,nlu_results,entity]
        if task == 'vob_rel':
            return [6,nlu_results,entity]

    def getEntName(self,entity,nlu_results):

        pro_list = self.normal_bussiness.searchEnt(entity,nlu_results[0])
        pro_value = np.array(pro_list)[:,1]
        similarPro = self.nlu_util.parse_util.getSimilarPro(nlu_results[1],pro_value)

        ind = list(pro_value).index(similarPro[0])

        return [pro_list[ind][0]+"的"+nlu_results[0]+":"+pro_list[ind][1],1,pro_list[ind][0]]

    def AEntityInformation(self,entity):
        ans = self.normal_bussiness.getOneEntity(entity)
        print(ans)
        return ans

    def AEntityRelation(self,entity):
        ans = self.normal_bussiness.getOneEntityRelation(entity)
        print(ans)
        return ans

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
    def setConpro(self, con_pro):
        self.con_pro = con_pro


    def dealMost(self,etype,nlu_results):

        type_con = nlu_results[0]
        con = nlu_results[1:]
        ans = self.normal_bussiness.doMost(etype,type_con)

        if ans:
            return [1,ans,etype]
        else:
            ans = self.normal_bussiness.doNormalForFalse(etype,con)
            if ans:
                return [1, ans, etype]
        return [0,"对不起，无法回答该问题。"]

    def getEntName(self,entity,nlu_results):

        pro_list = self.normal_bussiness.searchEnt(entity,nlu_results[0])
        pro_value = np.array(pro_list)[:,1]
        similarPro = self.nlu_util.parse_util.getSimilarPro(nlu_results[1],pro_value)

        ind = list(pro_value).index(similarPro[0])

        return [pro_list[ind][0]+"的"+nlu_results[0]+":"+pro_list[ind][1],1,pro_list[ind][0]]

    def AEntityInformation(self,entity):
        ans = self.normal_bussiness.getOneEntity(entity)
        print(ans)
        return ans

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