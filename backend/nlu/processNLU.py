# @Time : 2020/12/13 3:33 PM 
# @Author : LinXiaofei
# @File : processNLU.py


from backend.nlu.parseSentence import ParseSentence
#from backend.nlu.LTPUtil import LTPUtil
from backend.template_library.templateManage import TemplateManage

class processNLU(object):
    def __init__(self):
        self.parse_util = ParseSentence()
        #self.ltp_util = LTPUtil()
        self.template_util = TemplateManage()

    def process(self, words):

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
    """
    def ansEntName(self, etype, words):

        pro_value = ""
        pro = ""
        template = self.parse_util.getSimilarByLsi(words,etype)[0]
        pro = self.parse_util.matchTemplate(etype,template)[0]
        print(pro,"pro",template)

        cut_template = self.parse_util.getCutWords(template)
        cut_words = self.parse_util.getCutWords(words)


        t_pattern, t_arcs_dict, t_reverse_arcs_dict, t_postags, t_hed_index = self.ltp_util.get_sentence_pattern(cut_template)
        pattern, arcs_dict, reverse_arcs_dict, postags, hed_index = self.ltp_util.get_sentence_pattern(
            cut_words)
        if cut_template[t_hed_index] in ['是', '为', '有', '在']:

            if t_postags[t_hed_index - 1] == 'n' and cut_template[t_hed_index - 1] in cut_words[:hed_index] and cut_template[t_hed_index - 1] != etype:
                pro_value = "".join(cut_words[hed_index + 1])
        elif cut_template[t_hed_index] == cut_words[hed_index] and t_postags[t_hed_index] == 'v':
            #print(cut_template[t_hed_index],"...")

            pro_value = "".join(cut_words[hed_index + 1:])



        return pro,pro_value
    """

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



