# @Time : 2020/12/28 3:07 PM
# @Author : LinXiaofei
# @File : templateManage.py

import numpy as np
from backend.template_library.NumPro import NumPro
from backend.template_library.ConPro import *
from backend.graphSearch.graphSearch import graphSearch

import configparser
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

        numpro = NumPro()
        rangeconpro = RangeConPro()
        desconpro = DesConPro()

        for p in pro_list:
            if p in ['定义','示例','图片','内容','降水位置图','出处','河流',
                     '干湿状况','天气图','符号图','最低值','最高值','分类编号','内容','定义']:
                continue

            key = list(config[p])

            if config[p]['type'] == 'numpro':

                numpro.setEnt(ent)
                numpro.setPro(p)
                if 'alias' in key:
                    numpro.setAlias(config[p]['alias'])
                if 'adj' in key:
                    numpro.setAdj(config[p]['adj'])
                if 'unit' in key:
                    numpro.setUnit(config[p]['unit'])
                if 'noun' in key:
                    numpro.setNoun(config[p]['noun'])
                temp = numpro.getTemplate()
                none_template += temp
                none_template_pro.append(p)
                none_template_index.append(len(none_template))
                none_template_ask.append(temp[0])

            if config[p]['type'] == 'rangeconpro':

                rangeconpro.setEnt(ent)
                rangeconpro.setPro(p)
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
                desconpro.setPro(p)
                if 'alias' in key:
                    desconpro.setAlias(config[p]['alias'])

                temp = desconpro.getTemplate()
                none_template += temp
                none_template_pro.append(p)
                none_template_index.append(len(none_template))
                none_template_ask.append(temp[0])

            if config[p]['type'] == 'onlyconpro':

                onlyconpro = OnlyConPro()
                onlyconpro.setEnt(ent)
                onlyconpro.setPro(p)
                if 'alias' in key:
                    onlyconpro.setAlias(config[p]['alias'])
                if 'verb' in key:
                    onlyconpro.setVerb(config[p]['verb'])
                temp = onlyconpro.getTemplate()
                none_template += temp
                none_template_pro.append(p)
                none_template_index.append(len(none_template))
                none_template_ask.append(temp[0])

            if config[p]['type'] == 'sepnonepro':

                sepnonepro = SepNonePro()
                sepnonepro.setEnt(ent)
                sepnonepro.setPro(p)
                if 'alias' in key:
                    sepnonepro.setAlias(config[p]['alias'])
                    temp = sepnonepro.getTemplate()
                    none_template += temp
                    none_template_pro.append(p)
                    none_template_index.append(len(none_template))
                    none_template_ask.append(temp[0])

            if config[p]['type'] == 'sepverbpro':
                sepverbpro = SepVerbPro()
                sepverbpro.setEnt(ent)
                sepverbpro.setPro(p)
                if 'alias' in key:
                    sepverbpro.setAlias(config[p]['alias'])
                temp = sepverbpro.getTemplate()
                none_template += temp
                none_template_pro.append(p)
                none_template_index.append(len(none_template))
                none_template_ask.append(temp[0])

            if config[p]['type'] == 'reasonpro':
                reasonpro = ReasonPro()
                reasonpro.setEnt(ent)
                reasonpro.setPro(p)
                if 'alias' in key:
                    reasonpro.setAlias(config[p]['alias'])
                temp = reasonpro.getTemplate()
                none_template += temp
                none_template_pro.append(p)
                none_template_index.append(len(none_template))
                none_template_ask.append(temp[0])

            if  config[p]['type'] == 'sephowpro':

                sephowpro = SepHowPro()
                sephowpro.setEnt(ent)
                sephowpro.setPro(p)
                if 'alias' in key:
                    sephowpro.setAlias(config[p]['alias'])
                temp = sephowpro.getTemplate()
                none_template += temp
                none_template_pro.append(p)
                none_template_index.append(len(none_template))
                none_template_ask.append(temp[0])

            if  config[p]['type'] == 'howpro':

                howpro = HowPro()
                howpro.setEnt(ent)
                howpro.setPro(p)
                if 'alias' in key:
                    howpro.setAlias(config[p]['alias'])
                temp = howpro.getTemplate()
                none_template += temp
                none_template_pro.append(p)
                none_template_index.append(len(none_template))
                none_template_ask.append(temp[0])

        for n in none_template:
            print(n)

        #print("=================得到的模版===============",)
        #for t in none_template:
        #    print(t)
        #print("模版对应的属性: ", none_template)
        #print("属性对应的下标: ",none_template_index)
        #for ask in none_template_ask:
        #    print(ask)
        #print("模版对应的标准问法: ",none_template_ask)

        return none_template,none_template_pro,none_template_index,none_template_ask


    def getPro(self, index, template_index, template_pro, template_ask):

        for i in range(len(template_index)):

            if index < template_index[i]:
                pro = template_pro[i]
                ask = template_ask[i]

                return pro,ask

    def getBestPro(self,pro_list,words,pos):

        best_pro = []
        key_word = []
        for pro in pro_list:
            if pro in words:
                best_pro.append(pro)
                key_word.append(pro)

        for pro in pro_list:

            if 'alias' in list(config[pro]):
                alias = config[pro]['alias'].split(",")
                for a in alias:
                    if a in words:
                        best_pro.append(pro)
                        key_word.append(a)
                        #return pro
        for pro in pro_list:
            if 'verb' in list(config[pro]):
                verb = config[pro]['verb'].split(",")
                for a in verb:
                    if a in words:
                        best_pro.append(pro)
                        key_word.append(a)
        for pro in pro_list:
            if 'verb' in list(config[pro]):
                verb = config[pro]['verb'].split(",")
                for a in verb:
                    if a in words:
                        best_pro.append(pro)
                        key_word.append(a)

        for pro in pro_list:
            if 'verb' in list(config[pro]):
                verb = config[pro]['verb'].split(",")
                for a in verb:
                    if a in words:
                        best_pro.append(pro)
                        key_word.append(a)

        for pro in pro_list:
            if 'none' in list(config[pro]):
                none = config[pro]['none'].split(",")
                for a in none:
                    if a in words and pos[words.index(a)-1]=='r':
                        best_pro.append(pro)
                        key_word.append(a)

        for pro in pro_list:
            if 'adj' in list(config[pro]):
                adj = config[pro]['adj'].split(",")
                for a in adj:
                    if a in words and pos[words.index(a)-1]=='r':
                        best_pro.append(pro)
                        key_word.append(a)
        if len(best_pro)>0:
            return best_pro,key_word
        else:
            return [pro_list[0]],key_word

    def analysisPro(self,words,pro_list,key_list):


        best_pro = pro_list[0]

        if '什么' in words:
            r_index = words.index('什么')
        if '多少' in words:
            r_index = words.index('多少')
        if '怎么' in words:
            r_index = words.index('多少')


        dis = 1000000
        index = 0
        for k in key_list:
            p = pro_list[index]
            k_index = words.index(k)
            tem_dis = np.abs(k_index-r_index)
            if tem_dis < dis:
                dis = tem_dis
                best_pro = p
            index = index+1


        return best_pro


if __name__ == '__main__':
    t = TemplateManage()
    t.templateManage("俄罗斯有哪些农作物")
