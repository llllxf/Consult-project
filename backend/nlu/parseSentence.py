# @Time : 2020/12/13 1:55 PM 
# @Author : LinXiaofei
# @File : parseSentence.py


from backend.graphSearch.graphSearch import graphSearch
import configparser
config = configparser.ConfigParser()
config.read("../backend/config.ini")
subject = config['DEFAULT']['subject']
from backend.data.data_process import read_file,read_template
from backend.sentence_similarity import SentenceSimilarity
import jieba

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

        jieba.load_userdict(self.instanceArray)
        jieba.load_userdict(self.proArray)
        jieba.load_userdict(self.relArray)
        jieba.load_userdict(self.typeArray)

        #self.template_transfer = {'国家':'日本','河流':'长江'}


    def getCutWords(self, words):
        return list(jieba.cut(words))

    def getEntity(self,words):
        entity = ""
        cut_words = self.getCutWords(words)
        for word in cut_words:
            if word in self.instanceArray:
                entity = word
                return entity
        return None

    def getType(self,words):
        etype = ""
        cut_words = self.getCutWords(words)
        for word in cut_words:
            if word in self.typeArray:
                etype = word
                return etype
        return None

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
        #return words.replace(entity,self.template_transfer[best_father])
        return words.replace(entity, best_father)



    def getSimilar(self, words, templates):

        self.nlu_util.set_sentences(templates)
        self.nlu_util.TfidfModel()
        return self.nlu_util.similarity_top_k(words,1)[0]

    def getSimilarByLsi(self, words, templates):
        self.nlu_util.set_sentences(templates)
        self.nlu_util.LsiModel()
        return self.nlu_util.similarity_top_k(words,1)[0]


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
            if similar_tempalte[1] >= 0.85:
                return [2,templates.index(similar_tempalte[0])]
        return [0,"无法回答"]

