# @Time : 2020/12/13 1:55 PM 
# @Author : LinXiaofei
# @File : parseSentence.py


from backend.graphSearch.graphSearch import graphSearch
import configparser
config = configparser.ConfigParser()
config.read("../backend/config.ini")
subject = config['DEFAULT']['subject']
from backend.nlu.LTPUtil import *
from backend.data.data_process import read_file,read_template
from backend.sentence_similarity import SentenceSimilarity


class ParseSentence(object):
    def __init__(self):
        self.graph_util = graphSearch()
        self.nlu_util = SentenceSimilarity()

        instanceArray = list(set(read_file("../backend/data/"+subject+"/entity.csv")))
        self.instanceArray = sorted(instanceArray, key=lambda i: len(i), reverse=True)

        proArray = read_file("../backend/data/"+subject+"/cleanpro.csv")
        self.proArray = sorted(proArray, key=lambda i: len(i), reverse=True)

        relArray = read_file("../backend/data/"+subject+"/cleanrel.csv")
        self.relArray = sorted(relArray, key=lambda i: len(i), reverse=True)

        etype = list(set(read_file("../backend/data/" + subject + "/etype.csv")))
        self.typeArray = sorted(etype, key=lambda i: len(i), reverse=True)
        """

        jieba.load_userdict(self.instanceArray)
        jieba.load_userdict(self.proArray)
        jieba.load_userdict(self.relArray)
        jieba.load_userdict(self.typeArray)
        """

    """
    def getCutWords(self, words):
        return list(jieba.cut(words))
    """

    def getEntity(self,words):
        entity = []
        for word in words:

            if word in self.instanceArray:
                entity.append(word)

        return entity



    def getEtype(self,words):
        etype = []

        for word in words:
            if word in self.typeArray:
                etype.append(word)

        return etype

    def getCount(self,index,dep):

        if dep[index][2] == 'SBV':
            return 5
        if dep[index][2] == 'ATT':
            att_obeject = dep[index][1]-1

            if dep[att_obeject][2] == 'SBV':
                return 4
            if dep[att_obeject][2] == 'VOB':
                return 2
        if dep[index][2] == 'VOB':
            return 3

        return 0


    def extractBestEnt(self,words,dep):
        entity = self.getEntity(words)
        etype = self.getEtype(words)

        if len(entity) == 0 and len(etype)==0:
            return None,"false"
        if len(entity)==1 and len(etype)==0:
            return entity[0],"entity"
        if len(entity)==0 and len(etype)==1:
            return etype[0],"etype"

        ent_count = []
        type_count = []
        for e in entity:
            e_index = words.index(e)
            ent_count.append(self.getCount(e_index,dep))

        for t in etype:
            t_index = words.index(t)
            c = self.getCount(t_index,dep)
            if c in self.proArray:
                c = c-4
            type_count.append(c)

        ent_index = -1
        ent_c = 0

        type_c = 0
        type_index = -1
        print(dep)
        print(entity)
        print(ent_count)
        print(etype)
        print(type_count)

        for c_i in range(len(ent_count)):


            if ent_count[c_i] > ent_c:
                ent_c = ent_count[c_i]
                ent_index = c_i

        for c_i in range(len(type_count)):


            if type_count[c_i] > type_c:
                type_c = type_count[c_i]
                type_index = c_i

        if ent_c >= type_c:
            return entity[ent_index],"entity"
        else:
            return etype[type_index],"etype"


    def getConcept(self, entity):

        type_list = self.graph_util.getFather(entity)

        best_father = ""
        max_count = 0

        for father in type_list:
            son_count = len(self.graph_util.getEntityByType(father))
            if son_count > max_count:
                max_count = son_count
                best_father = father

        return best_father

    def getStandard(self,entity,best_father,words):
        return words.replace(entity, best_father)


    def getSimilar(self, words, templates):

        self.nlu_util.set_sentences(templates)
        self.nlu_util.TfidfModel()
        return self.nlu_util.similarity_top_k(words,5)

    def getSimilarByLsi(self, words, templates):
        self.nlu_util.set_sentences(templates)
        self.nlu_util.LsiModel()
        return self.nlu_util.similarity_top_k(words,5)[0]


    def getSimilarPro(self, words, pros):
        print(words,"words")

        self.nlu_util.set_sentences(list(pros))
        self.nlu_util.LsiModel()

        return self.nlu_util.similarity_top_k(words,1)[0]


    def matchTemplate(self, father, words):
        raw_template = list(read_file("../backend/template_library/"+subject+"/"+father+".csv"))
        template_arr = []
        for template in raw_template:

            if template != "==========":
                template_arr.append(template)
            else:
                if words in template_arr:
                    #print(template_arr)
                    return [template_arr[0],template_arr[1]]
                else:
                    template_arr = []
        return None


    def getMatchResult(self, templates, words):

        if words in templates:
            return [1,templates.index(words)]
        else:
            similar_tempalte = self.getSimilar(words, templates)
            print(similar_tempalte)
            similar_tempalte_index = []
            for tem in similar_tempalte:
                similar_tempalte_index.append(templates.index(tem[0]))
            if similar_tempalte[0][1] >= 0.6:
                return [2,similar_tempalte_index]
        return [0,"无法回答"]

