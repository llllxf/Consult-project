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


    def dealNormal(self, entity, cut_words, pos):

        flag, template_mode = self.analysis_util.getTemplateMode(cut_words)

        template, template_pro, template_index, template_ask = self.template_util.templateManage(entity)
        match_result = self.parse_util.getMatchResult(template, template_mode)
        if match_result[0] == 1:
            pro, ask = self.template_util.getPro(match_result[1], template_index, template_pro, template_ask)
            return entity, [1, pro, ask],"normal"
        if match_result[0] == 2:
            pro_array = []
            ask_array = []
            for temp in match_result[1]:
                pro, ask = self.template_util.getPro(temp, template_index, template_pro, template_ask)
                pro_array.append(pro)
                ask_array.append(ask)

            best_pro, key_words = self.template_util.getBestPro(pro_array, cut_words, pos)
            if len(best_pro) == 1:
                return entity, [2, best_pro[0], ask_array[pro_array.index(best_pro[0])]],"normal"
            elif len(best_pro) > 1:
                final_pro = self.template_util.analysisPro(cut_words, best_pro, key_words)
                return entity, [2, final_pro, ask_array[pro_array.index(final_pro)]],"normal"

        if match_result[0] == 0:
            return entity, [0, "无法回答。"],"normal"









        return entity, [0, "无法回答。"],"normal"

    def process(self, words):

        seg,hidden = getSEG(words)
        pos = getPOS(hidden)[0]
        dep = getDEP(hidden)[0]
        cut_words = list(seg)[0]

        entity,ent_type = self.parse_util.extractBestEnt(cut_words,dep)
        print(entity,ent_type,"entity=============")

        if ent_type=="false":
            return None,[0, "无法回答。"],"normal"

        elif ent_type=="entity":
            return self.dealNormal(entity,cut_words,pos)

        elif ent_type == "etype" and '最' in cut_words:
            left = 1
            begin = cut_words.index('最')

            while(begin>=left):

                if pos[begin-left] in ['n','nl','ni','ns','nz']:
                    cut_words[begin-left]
                    break
                left = left+1
            key_adj = cut_words[cut_words.index('最') + 1]
            if left > begin:

                return entity,[key_adj],"most"
            else:
                key_pro = cut_words[begin-left]
                return entity,[key_pro,key_adj],"most"

        elif ent_type == "etype" and cut_words.index(entity):

            procon = []

            dep_list = dep
            for i in range(len(cut_words)):
                if dep_list[i][2] == 'HED':
                    hed_index = i
                    break
            type_index = cut_words.index(entity)
            if type_index > hed_index and pos[type_index-1]=='r':
                procon = cut_words[:hed_index]
            else:
                procon = cut_words[:type_index]

            return entity,procon,"content"

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



