# @Time : 2020/12/28 3:07 PM
# @Author : LinXiaofei
# @File : templateManage.py
import os

from backend.template_library.NumPro import NumPro
from backend.template_library.ConPro import *
from backend.graphSearch.graphSearch import graphSearch
from backend.nlu.LTPUtil import *
from backend.data.data_process import *
import configparser
import jieba
config = configparser.ConfigParser()
config.read("../backend/proconfig.ini")



class TemplateManage(object):
    def __init__(self):
        self.graph_util = graphSearch()

    def templateManage(self,ent):

        pro_list = self.graph_util.getProList(ent)

        none_template = []
        none_template_pro = []
        none_template_index = []
        none_template_ask = []

        num_template = []
        num_template_pro = []
        num_template_index = []
        num_template_ask = []

        numpro = NumPro()
        rangeconpro = RangeConPro()
        desconpro = DesConPro()

        for p in pro_list:
            if p not in list(config.keys()):
                continue
            key = list(config[p])


            if config[p]['type'] == 'numpro':

                numpro.setEnt(ent)
                numpro.setNumPro(p)
                if 'alias' in key:
                    numpro.setAlias(config[p]['alias'])
                if 'adj' in key:
                    numpro.setAdj(config[p]['adj'])
                if 'unit' in key:
                    numpro.setAdj(config[p]['unit'])
                if 'noun' in key:
                    numpro.setNoun(config[p]['noun'])
                temp = numpro.getTemplate()
                num_template += temp
                num_template_pro.append(p)
                num_template_index.append(len(num_template))
                num_template_ask.append(temp[0])

            if config[p]['type'] == 'rangeconpro':

                rangeconpro.setEnt(ent)
                rangeconpro.setConPro(p)
                if 'alias' in key:
                    rangeconpro.setAlias(config[p]['alias'])
                if 'verb' in key:
                    rangeconpro.setVerb(config[p]['verb'])
                temp = rangeconpro.getTemplate()
                none_template += temp
                none_template_pro.append(p)
                none_template_index.append(len(none_template))
                none_template_ask.append(temp[0])

            if config[p]['type'] == 'desconpro':

                desconpro.setEnt(ent)
                desconpro.setConPro(p)
                if 'alias' in key:
                    desconpro.setAlias(config[p]['alias'])

                temp = desconpro.getTemplate()
                print(temp)
                none_template += temp
                none_template_pro.append(p)
                none_template_index.append(len(none_template))
                none_template_ask.append(temp[0])

            if config[p]['type'] == 'onlyconpro':

                onlyconpro = OnlyConPro()
                onlyconpro.setEnt(ent)
                onlyconpro.setConPro(p)
                if 'alias' in key:
                    onlyconpro.setAlias(config[p]['alias'])
                if 'verb' in key:
                    onlyconpro.setVerb(config[p]['verb'])
                temp = onlyconpro.getTemplate()
                none_template += temp
                none_template_pro.append(p)
                none_template_index.append(len(none_template))
                none_template_ask.append(temp[0])

        for ask in none_template_ask:
            print(ask)
        #print("模版对应的标准问法: ",none_template_ask)

        return none_template,none_template_pro,none_template_index,none_template_ask


    def getPro(self, index, template_index, template_pro, template_ask):

        for i in range(len(template_index)):

            if index < template_index[i]:
                pro = template_pro[i]
                ask = template_ask[i]

                return pro,ask

    def writepro(self):
        tri_list = self.graph_util.getAll()
        clean_tri = []
        pro_list = []
        for tri in tri_list:
            if tri[1] in pro_list or tri[1] in ['定义','示例','图片','内容']:
                continue
            pro_list.append(tri[1])
            clean_tri.append(tri)
        wf = open("clean_tri.txt","w")
        for tri in clean_tri:
            wf.writelines(tri[0]+"\t"+tri[1]+"\t"+tri[2]+"\n")
            wf.writelines("\n")
            wf.writelines("\n")



if __name__ == '__main__':

    #jieba.load_userdict(['三大原始居民'])
    #word = list(jieba.cut("三大原始居民是一个实体吗"))
    ltp_util = LTPUtil()
    #postags = ltp_util.get_postag(word)
    #arcs = ltp_util.get_parse(word,postags)
    cut_words, postags, dep = ltp_util.get_sentence_data("三大原始居民是一个实体吗")
    print(cut_words)
    print(postags)
    print(dep)






