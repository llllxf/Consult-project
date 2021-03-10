# @Time : 2021/3/5 12:07 PM 
# @Author : LinXiaofei
# @File : extractEntity.py

from backend.nlu.LTPUtil import LTPUtil
from backend.template_library.ConPro import *

class ExtractEntity(object):



    def __init__(self):

        self.pro_util = ConPro()
        self.seg_util = LTPUtil()

    def getEligibleEnt(self,words,ent_list):
        eligible_ent = []

        #seg,hidden = self.ltp_util.seg([words])
        #e_cut_list,hidden = self.ltp_util.seg(ent_list)
        cut_words = self.seg_util.get_normal_seg(words)
        print(cut_words)
        #e_cut_list = jieba.cut(ent_list)
        for e_index in range(len(ent_list)):
            #e_cut = e_cut_list[e_index]
            e_cut = list(self.seg_util.get_normal_seg(ent_list[e_index]))
            print(ent_list[e_index],e_cut)
            count = 0
            for e in e_cut:
                if e in cut_words:
                    count = count+1

            if count >= len(e_cut)-1:
                eligible_ent.append(ent_list[e_index])
        return eligible_ent

    def getBestEntPro(self,cut_words,pos,dep,entity_list,entity_index):
        words = "".join(cut_words)

        eligible_ent = self.getEligibleEnt(words,entity_list)
        print(eligible_ent,"eligible_ent")

        ent_list = []
        pro_list = []

        for ent in eligible_ent:
            best_pro,key_words = self.pro_util.getpro(cut_words, pos, dep, ent, entity_index)
            if best_pro:

                pro_list.append(best_pro)
                ent_list.append(ent)
        if len(pro_list)>0:
            return ent_list[-1],pro_list[-1]

        return None,None









    def extractBestEnt(self,words,dep):

        entity = self.getEntity(words)
        etype = self.getEtype(words)

        if len(entity) == 0 and len(etype)==0:

            return None,[],"false"
        if len(entity)==1 and len(etype)==0:
            array = self.getExpandEnt(entity[0])
            return entity[0],array,"entity"
        if len(entity)==0 and len(etype)==1:
            return etype[0],[],"etype"

        ent_count = []
        type_count = []
        for e in entity:

            e_index = words.index(e)
            print("====================e",e, words,e_index)
            ent_count.append(self.getCount(e_index,dep))

        for t in etype:
            t_index = words.index(t)
            print("====================t", t, words, t_index)
            c = self.getCount(t_index,dep)
            if t in self.proArray:
                c = c-4

            type_count.append(c)

        ent_index = -1
        ent_c = 0

        type_c = 0
        type_index = -1


        for c_i in range(len(ent_count)):


            if ent_count[c_i] >= ent_c:
                ent_c = ent_count[c_i]
                ent_index = c_i

        for c_i in range(len(type_count)):


            if type_count[c_i] > type_c:
                type_c = type_count[c_i]
                type_index = c_i
        print(entity,ent_count)
        print(etype, type_count)

        if ent_index == -1 and type_index == -1:
            return None, [], "false"
        print(ent_c,type_c)



        if ent_index != -1 and ent_c >= type_c:

            for i in range(len(words)):

                if ent_index > -1 and dep[i][2] == 'COO' and words[dep[i][1]-1] == entity[ent_index]:
                    coo_entity = self.checkCombineEnt(entity[ent_index],words[i])
                    if coo_entity:
                        array = self.getExpandEnt(coo_entity)
                        print("============================1")
                        return [coo_entity,dep[i][1]-1],array,"coo_entity"
            print("============================2")
            array = self.getExpandEnt(entity[ent_index])
            return entity[ent_index],array,"entity"

        else:
            print(words)
            for i in range(len(words)):
                print(type_index,dep[i][1],dep[i][2])
                if type_index > -1 and dep[i][2] == 'COO' and words[dep[i][1]-1] == etype[type_index]:
                    coo_entity = self.checkCombineEnt(etype[type_index],words[i])
                    if coo_entity:
                        array = self.getExpandEnt(coo_entity)
                        print("============================5")
                        return [coo_entity,dep[i][1]-1],array,"coo_entity"
            print("============================3")
            return etype[type_index],[],"etype"
        print("============================4")


    def getWordsExtractType(self, words, dep):

        SBV = 0
        VOB = 0

        FOB = 0

        for i in range(len(words)):

            if dep[i][2] == 'SBV':
                SBV = SBV+1
            if dep[i][2] == 'VOB':
                VOB = VOB+1
            if dep[i][2] == 'FOB':
                FOB = FOB + 1
        if (VOB+FOB) >=2 or SBV >=2:

            de_index = -1
            r_index = -1
            for i in range(len(words)):

                if words[i] in self.r:
                    r_index = i

                if i == 0 and words[i + 1] in self.typeArray and words[i] in self.r:
                    """
                    什么+type
                    """
                    split_index = i + 1
                    end_words = words[split_index + 1:]
                    ent = words[split_index]
                    return [end_words, split_index, ent], "split_end"

                if len(words) > i + 3 and words[i + 1] in ['是','有','在']:
                    """
                    是/有/在+什么+type
                    """
                    if words[i + 2] in self.r and words[i + 3] in self.typeArray:
                        split_index = i
                        front_words = words[:split_index]
                        end_words = words[split_index + 1:]
                        ent = words[split_index + 3]
                        return [front_words, split_index, ent], "split"

                if words[i] == '的' and len(words)>i+1:
                    """
                    的+type
                    """

                    de_index = i
                    if words[i+1] in self.typeArray:
                        split_index = i
                        front_words = words[:split_index]
                        end_words = words[split_index + 1:]
                        ent = words[split_index+1]
                        print([front_words, split_index, ent],"split")
                        return  [front_words, split_index, ent],"split"

        return None,"normal"






