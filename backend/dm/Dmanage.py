# @Language: python3
# @File  : Dmanage.py
# @Author: LinXiaofei
# @Date  : 2020-05-01
"""

"""
import sys
import os

from backend.nlu.processNLU import processNLU
from backend.nlg.generateAns import generateAns



from backend.graphSearch.calculateBussiness import calculateBussiness
from backend.graphSearch.compareBussiness import compareBussiness
from backend.graphSearch.normalBussiness import normalBussiness

import configparser

config = configparser.ConfigParser()
config.read("../backend/config.ini")
"""
问答引擎
"""

class DialogManagement(object):
    def __init__(self):

        self.nlu_util = processNLU()

        self.nlg_util = generateAns()

        self.normal_bussiness = normalBussiness()
        self.compare_bussiness = compareBussiness()
        self.calculate_bussiness = calculateBussiness()

        self.last_sentence = []
        self.wether = []

        self.repertoryDict = {'地理':'geo4'}




    def doNLU(self,words):

        ans_str = ""
        ans_dict = self.nlu_util.process(words,self.last_sentence)
        ask_words = ans_dict['ask_words']
        entity_array = ans_dict['entity_array']
        property_array = ans_dict['property_array']
        keywords_array = ans_dict['keywords_array']
        task_type_array = ans_dict['task_type_array']

        i = 0
        key_ent, ans_type, ans = self.normal_bussiness.doNormal(ask_words, task_type_array[i], entity_array[i],
                                                                property_array[i],
                                                                keywords_array[i])
        if ans != None and ans != "":
            ans_str = ans_str + self.doNLG(key_ent, ans_type, ans, self.wether)
            return ans_str
        else:
            return "无法回答"



    def doNLG(self,entity,ans_type,ans,wether):

        ans_str = self.nlg_util.getAns(entity, ans_type, ans,wether)
        return ans_str

if __name__ == '__main__':
    a = DialogManagement()
    a.setSubject('地理')

    while(1):
        s = input("user: ")
        if s == "":
            continue
        ans = a.doNLU(s)
        print(ans[0])