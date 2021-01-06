# @Time : 2020/12/28 3:07 PM
# @Author : LinXiaofei
# @File : templateManage.py
import os

from backend.template_library.NumPro import NumPro
from backend.template_library.ConPro import *
from backend.graphSearch.graphSearch import graphSearch
import configparser
config = configparser.ConfigParser()
config.read("../backend/pro_config.ini")
class TemplateManage(object):
    def __init__(self):
        self.graph_util = graphSearch()


    def templateManage(self,ent):
        template = []
        pro_list = self.graph_util.getProList(ent)


        template_pro = []
        template_index = []
        template_ask = []
        for p in pro_list:
            if p not in list(config.keys()):
                continue
            key = list(config[p])

            if config[p]['type'] == 'numpro':
                numpro = NumPro()
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
                template += temp
                template_pro.append(p)
                template_index.append(len(template))
                template_ask.append(temp[0])

            if config[p]['type'] == 'rangeconpro':
                rangeconpro = RangeConPro()
                rangeconpro.setEnt(ent)
                rangeconpro.setConPro(p)
                if 'alias' in key:
                    rangeconpro.setAlias(config[p]['alias'])
                if 'verb' in key:
                    rangeconpro.setVerb(config[p]['verb'])
                temp = rangeconpro.getTemplate()
                template += temp
                template_pro.append(p)
                template_index.append(len(template))
                template_ask.append(temp[0])
            if config[p]['type'] == 'desconpro':
                desconpro = DesConPro()
                desconpro.setEnt(ent)
                desconpro.setConPro(p)
                if 'alias' in key:
                    desconpro.setAlias(config[p]['alias'])
                temp = desconpro.getTemplate()
                template += temp
                template_pro.append(p)
                template_index.append(len(template))
                template_ask.append(temp[0])
            if config[p]['type'] == 'onlyconpro':
                onlyconpro = OnlyConPro()
                onlyconpro.setEnt(ent)
                onlyconpro.setConPro(p)
                if 'alias' in key:
                    onlyconpro.setAlias(config[p]['alias'])
                if 'verb' in key:
                    onlyconpro.setVerb(config[p]['verb'])
                temp = onlyconpro.getTemplate()
                template += temp
                template_pro.append(p)
                template_index.append(len(template))
                template_ask.append(temp[0])
        print("=================得到的模版===============",)
        for t in template:
            print(t)
        print("模版对应的属性: ", template_pro)
        print("属性对应的下标: ",template_index)
        print("模版对应的标准问法: ",template_ask)
        return template,template_pro,template_index,template_ask

    def getPro(self, index, template_index, template_pro, template_ask):

        for i in range(len(template_index)):

            if index < template_index[i]:
                pro = template_pro[i]
                ask = template_ask[i]
                return pro,ask

if __name__ == '__main__':
    t = TemplateManage()
    t.templateManage("日本")
