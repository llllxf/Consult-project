# @Time : 2020/12/13 3:33 PM 
# @Author : LinXiaofei
# @File : processNLU.py


from backend.nlu.parseSentence import ParseSentence
from backend.nlu.analysisWords import analysisWords
from backend.nlu.LTPUtil import *
from backend.template_library.templateManage import TemplateManage

class processNLU(object):
    def __init__(self):
        self.parse_util = ParseSentence()
        self.analysis_util = analysisWords()

        self.template_util = TemplateManage()


    def process(self, words):

        entity = self.parse_util.getEntity(words)
        cut_words = self.parse_util.getCutWords(words)
        flag, template_mode = self.analysis_util.getTemplateMode(cut_words)

        template, template_pro, template_index, template_ask = self.template_util.templateManage(entity)
        match_result = self.parse_util.getMatchResult(template,template_mode)
        if match_result[0] == 1:
            pro, ask = self.template_util.getPro(match_result[1],template_index, template_pro, template_ask)
            return entity, [1,pro, ask]
        if match_result[0] == 2:
            pro_array = []
            ask_array = []
            for temp in match_result[1]:

                pro, ask = self.template_util.getPro(temp, template_index, template_pro, template_ask)
                pro_array.append(pro)
                ask_array.append(ask)

            seg

            return entity, [2, pro, ask]
        if match_result[0] == 0:
            return entity, [0,"无法回答。"]
        return entity, [0,"无法回答。"]

    def process2(self, words):

        entity = self.parse_util.getEntity(words)
        template, template_pro, template_index, template_ask = self.template_util.templateManage(entity)
        match_result = self.parse_util.getMatchResult(template,words)
        if match_result[0] == 1:
            pro, ask = self.template_util.getPro(match_result[1],template_index, template_pro, template_ask)
            return entity, [1,pro, ask]
        if match_result[0] == 2:
            pro, ask = self.template_util.getPro(match_result[1], template_index, template_pro, template_ask)
            return entity, [2, pro, ask]
        if match_result[0] == 0:
            return entity, [0,"无法回答。"]
        return entity, [0,"无法回答。"]


    def ansProValue(self, entity,words):

        best_father = self.parse_util.getConcept(entity)
        standard_words = self.parse_util.getStandard(entity, best_father, words)
        print(standard_words, "standard_words")
        matchResults = self.parse_util.getMatchResult(best_father, standard_words, entity)
        print(matchResults, standard_words, best_father, entity)
        return entity, matchResults

    def ansEntName(self, etype, words):
        pass

    def processOLD(self, words):

        entity = self.parse_util.getEntity(words)

        if entity:
            entity, matchResults = self.ansProValue(entity,words)
            return entity, matchResults,"proValue"

        etype = self.parse_util.getType(words)


        if etype:
            pro,pro_value = self.ansEntName(etype,words)

            if pro_value != "":
                return etype, [pro,pro_value], "entName"

        return None,None,None



