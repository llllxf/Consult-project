# @Time : 2021/3/5 12:07 PM 
# @Author : LinXiaofei
# @File : extractEntity.py

from backend.nlu.LTPUtil import LTPUtil
from backend.template_library.ConPro import *
from backend.template_library.ConProStrict import *

class ExtractEntity(object):

    def __init__(self):

        self.pro_normal_util = ConPro()
        self.pro_strict_util = ConProStrict()
        self.seg_util = LTPUtil()
        self.r = ['哪里','什么','哪个','哪一个','哪些','哪']
        self.rel_limit = {'洲':['洲','大洲'],'国家':['国','国家'],'省':['省','省份'],'河流':['河','大河','河流'],'海洋':['海洋','海','大洋','洋'],'城市':['城市','市'],'湖泊':['湖','湖泊'],'发达国家':['发达国家'],'发展中国家':['发展中国家'],'社会主义国家':['社会主义国家']}

    def checkVerbRel(self, words, dep, reverse_dep, verb_index):
        print("verb_index",verb_index)
        print(dep[verb_index][2])


        if dep[dep[verb_index][1] - 1][2] in ['SBV', 'HED']:
            return True
        if dep[verb_index][2] == 'HED':
            return True
        if words[dep[verb_index][1] - 1] in self.r:
            return True

        if dep[dep[verb_index][1] - 1][2] in ['FOB', 'POB', 'VOB'] and dep[verb_index][1] in reverse_dep.keys():
            v_list = reverse_dep[dep[verb_index][1]]
            for v in v_list:
                if words[v[0] - 1] in self.r:
                    return True

    def extractBestEntForRel(self, entity_list,words, dep, reverse_dep,pos):

        if len(entity_list) == 0:
            return None, None, None, None

        ask_type = None
        ask_ent = None

        for w_index in range(len(words)):
            if words[w_index] in self.r and w_index<len(words)-1:
                if dep[w_index][2] in ['VOB','POB','FOB']:
                    break
                if dep[w_index][2] == 'ATT':
                    vob_index = dep[w_index][1]-1
                    while(dep[vob_index][2] == 'ATT'):
                        vob_index = dep[vob_index][1]-1
                    ask_type = words[vob_index]
                    break
        #print("=======================1",ask_type,vob_index)

        """
        vob_type = None
        for etype in type_list:
            t_index = words.index(etype)
            if dep[t_index][2] in ['VOB', 'POB', 'FOB', 'SBV']:
                vob_type = etype
                break
        """

        for e in entity_list:
            e_index = words.index(e)
            if dep[e_index][2] == 'SBV' and pos[dep[e_index][1] - 1] in ['v','p'] and self.checkVerbRel(words, dep, reverse_dep, dep[e_index][1] - 1):

                print("==================================checkVerbRel",words[dep[e_index][1] - 1])

                rel,vob_type,flag = self.pro_strict_util.checkVerbRel(e,words[dep[e_index][1] - 1],ask_type)
                print(rel,vob_type,"rel,vob_type")
                if flag:
                    return 'SBV_REL_Normal',e,rel, vob_type

        for w_index in range(len(words)):
            if words[w_index] in self.r:
                if dep[w_index][2] in ['VOB','POB','FOB'] and dep[dep[w_index][1]-1][2] == 'HED':
                    check_list = reverse_dep[dep[w_index][1]]
                    print("check_list",check_list)
                    for c in check_list:
                        if c[1] == 'SBV':
                            ask_ent = words[c[0]-1]
                            break
                if ask_ent:
                    break
                if dep[w_index][2] == 'ATT':
                    vob_index = dep[w_index][1]-1
                    while(dep[vob_index][2] == 'ATT'):
                        vob_index = dep[vob_index][1]-1
                    if dep[vob_index][2] == 'SBV':
                        ask_ent = words[vob_index]
                        break
                if ask_ent:
                    break

        ask_ent_flag = True
        for e in self.rel_limit.keys():
            if ask_ent in self.rel_limit[e]:

                ask_ent = e
                ask_ent_flag = False
                break

        if ask_ent_flag:
            return None, None, None,None

        print(ask_ent,"ask_ent")

        for e in entity_list:
            e_index = words.index(e)
            if dep[e_index][2] in ['VOB', 'POB', 'FOB'] and pos[dep[e_index][1] - 1] == 'v':
                rel = self.pro_strict_util.checkPVerbRel(e,words[dep[e_index][1] - 1])
                if rel:
                    return 'VOB_REL_Normal', e, rel, ask_ent

        return None, None, None,None

    def getEligibleEnt(self,words,ent_list):

        eligible_ent = []
        eligible_ent_lack = []
        eligible_ent.append(ent_list[0])

        cut_words = self.seg_util.get_normal_seg(words)

        for e_index in range(1,len(ent_list)):

            e_cut = list(self.seg_util.get_normal_seg(ent_list[e_index]))

            count = 0
            print("e_cut",e_cut,cut_words)
            if e_cut[0] not in words:
                continue

            for e in e_cut:
                if e in ['的','与','和','、',',','，']:
                    count = count+1
                    continue

                if e in cut_words:
                    count = count+1
                if len(e) >= 4 and e not in cut_words:
                    count = count-1

            if count == len(e_cut)-1:
                eligible_ent_lack.append(ent_list[e_index])
            elif count == len(e_cut):
                eligible_ent.append(ent_list[e_index])

        return eligible_ent,eligible_ent_lack



    def getRel(self,cut_words,dep, reverse_dep, ent, entity_index):
        best_rel, key_words = self.pro_strict_util.getRel(cut_words, dep, reverse_dep, ent, entity_index)
        return best_rel

    def getBestEntProStrict(self,cut_words,pos,dep,reverse_dep,entity_list,entity_index):
        words = "".join(cut_words)

        eligible_ent,eligible_ent_lack = self.getEligibleEnt(words,entity_list)
        print(eligible_ent)
        print(eligible_ent_lack)

        ent_list = []
        pro_list = []
        pro_list_lack = []
        ent_list_lack = []

        for ent in eligible_ent:
            best_pro,key_words = self.pro_strict_util.getpro(cut_words, pos, dep, reverse_dep,ent, entity_index)
            if best_pro:
                pro_list.append(best_pro)
                ent_list.append(ent)
        print("pro_list",pro_list)
        print("ent_list",ent_list)
        if len(ent_list) > 1 or (len(ent_list)==1 and ent_list[0] not in cut_words):
            return ent_list[-1], pro_list[-1]
        if len(ent_list) == 1 and pro_list[-1] not in ['特征']:
            return ent_list[-1], pro_list[-1]
        for ent in eligible_ent_lack:
            best_pro, key_words = self.pro_strict_util.getpro(cut_words, pos, dep, reverse_dep, ent, entity_index)
            if best_pro:
                pro_list_lack.append(best_pro)
                ent_list_lack.append(ent)
        if len(ent_list_lack) > 0:
            return ent_list_lack[-1], pro_list_lack[-1]
        if len(ent_list) > 0:
            return ent_list[-1],pro_list[-1]

        for ent in eligible_ent:
            print("进入数值型属性")
            pro = self.pro_strict_util.getNumpro(ent,cut_words,pos)
            if pro:
                return ent,pro
        for ent in eligible_ent_lack:
            print("进入缺失型数值型属性")
            pro = self.pro_strict_util.getNumpro(ent,cut_words,pos)
            if pro:
                return ent,pro

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






