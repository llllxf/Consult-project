# @Time : 2020/12/13 3:33 PM 
# @Author : LinXiaofei
# @File : processNLU.py


from backend.nlu.parseSentence import ParseSentence

from backend.nlu.LTPUtil import LTPUtil
#from backend.template_library.ConPro import *
from backend.nlu.extractEntity import ExtractEntity
import numpy as np
class processNLU(object):

    def __init__(self):
        self.parse_util = ParseSentence()
        self.ent_util = ExtractEntity()
        self.ltp_util = LTPUtil()


    def dealNormalFalse(self, entity, cut_words, pos, dep):
        print(entity, cut_words, pos,dep,"split_false")

        valuable_words,word_count = self.parse_util.getValuableWords(cut_words, pos, dep)
        return entity, [4, valuable_words,word_count], "normal"
    """
    def dealNormalCoo(self, entity_arg, ent_list, cut_words, pos, dep):
        entity = entity_arg[0]
        entity_index = entity_arg[1]
        ent,best_pro, key_word = self.pro_util.getpro(cut_words,pos,dep,entity,ent_list,entity_index)
        if best_pro:
            if ent == entity:
                return entity,[1,best_pro],"normal"
            else:
                return ent, [2, best_pro,ent+"的"+best_pro], "normal"
        else:
            valuable_words,word_count = self.parse_util.getValuableWords(cut_words, pos, dep)
            return entity, [3, valuable_words,word_count], "normal"
    """

    def dealNormalCoo(self, entity_arg, ent_list,  cut_words, pos, dep):
        entity = entity_arg[0]
        entity_index = entity_arg[1]

        ent,best_pro = self.ent_util.getBestEntPro(cut_words,pos,dep,ent_list,entity_index)

        #ent,best_pro, key_word = self.pro_util.getpro(cut_words,pos,dep,entity,entity_index)
        if best_pro:

            if ent == entity:
                return entity,[1,best_pro],"normal"
            else:
                return ent, [2, best_pro,ent+"的"+best_pro], "normal"
        else:
            valuable_words,word_count = self.parse_util.getValuableWords(cut_words, pos,dep)
            return entity, [3, valuable_words,word_count], "normal"

    def dealNormal(self, entity, ent_list,  cut_words, pos, dep):
        #entity = entity_arg[0]
        entity_index = cut_words.index(entity)

        ent,best_pro = self.ent_util.getBestEntPro(cut_words,pos,dep,ent_list,entity_index)

        #ent,best_pro, key_word = self.pro_util.getpro(cut_words,pos,dep,entity,entity_index)
        if best_pro:

            if ent == entity:
                return entity,[1,best_pro],"normal"
            else:
                return ent, [2, best_pro,ent+"的"+best_pro], "normal"
        else:
            valuable_words,word_count = self.parse_util.getValuableWords(cut_words, pos,dep)
            return entity, [3, valuable_words,word_count], "normal"
    """
    def getValuableWords(self, words,dep):
        seg, hidden = self.ltp_util.getSEG(words)
        pos = self.ltp_util.getPOS(hidden)[0]
        con,word_count = self.parse_util.getValuableWords(words,pos,dep)
        return [con,word_count]
    """

    def process(self, words):

        cut_words,pos,dep = self.ltp_util.get_sentence_data(words)
        """
        seg,hidden = self.ltp_util.getSEG(words)
        pos = self.ltp_util.getPOS(hidden)[0]
        dep = self.ltp_util.getDEP(hidden)[0]
        cut_words = list(seg)[0]
        """
        print("分词: ",cut_words)
        print("依存句法：",dep)
        print("词性分析",pos)

        extract_words,extract_type= self.parse_util.getWordsExtractType(cut_words,dep,pos)

        if extract_type in ["normal","split_false"]:

            entity,array,ent_type = self.parse_util.extractBestEnt(cut_words,dep)
            print("======================================")
            print("抽取的实体: ",entity)
            print("扩充的实体: ",array)
            print("结果类型: ",ent_type)

        if extract_type in ["split","split_end"]:
            split_con = extract_words[0]
            split_index = extract_words[1]
            entity = extract_words[2]
            ent_type = "etype"
        """
        if extract_type == "split_false":
            split_con = extract_words[0]
            split_index = extract_words[1]

            ent_type = "entity"
        """

        print("抽取的实体: ",entity)
        print("实体的类型: ", ent_type)
        print("结果类型: ", extract_type)



        if ent_type=="false":

            con,con_count = self.parse_util.getValuableWords(cut_words,pos,dep)


            for i in range(len(cut_words)):
                print(dep[i][2])
                if dep[i][2] == 'HED' and pos[i] in ['n','nd','ni','nl','ns','nt','nz','i']:
                    print("HED=============", cut_words[i], [con, con_count], "false")
                    return cut_words[i],[con,con_count],"false"
            for i in range(len(cut_words)):

                if dep[i][2] == 'SBV' and pos[i] in ['n','nd','ni','nl','ns','nt','nz','i']:
                    print("SBV=============", cut_words[i], [con, con_count], "false")
                    return cut_words[i], [con,con_count], "false"
            for i in range(len(cut_words)):
                if dep[i][2] == 'VOB' and pos[i] in ['n', 'nd', 'ni', 'nl', 'ns', 'nt', 'nz','i']:
                    return cut_words[i], [con,con_count], "false"
            for i in range(len(cut_words)):
                if dep[i][2] == 'POB' and pos[i] in ['n', 'nd', 'ni', 'nl', 'ns', 'nt', 'nz','i']:
                    return cut_words[i], [con,con_count], "false"
            for i in range(len(cut_words)):
                if dep[i][2] == 'ATT' and pos[i] in ['n', 'nd', 'ni', 'nl', 'ns', 'nt', 'nz','i']:
                    return cut_words[i], [con,con_count], "false"
            return con[np.argmax(con_count)],[con,con_count], "false"

        elif ent_type=="entity":
            #if extract_type == "split_false":
            #   return self.dealNormalFalse(entity,split_con,pos[:split_index],dep[:split_index])
            entity, ans,task_type = self.dealNormal(entity,array,cut_words,pos,dep)
            if ans[0] <= 2:
                return entity, ans,task_type


            return entity, ans,task_type

        elif ent_type=="coo_entity":
            return self.dealNormalCoo(entity,array,cut_words,pos,dep)

        elif ent_type == "etype":
            key_entity = self.parse_util.getEntity(cut_words)
            print(key_entity,"============================???")
            for i in range(len(cut_words)):
                if dep[i][2] == 'HED':
                    hed_index = i
                    break
            type_index = cut_words.index(entity)
            print(type_index)
            print(hed_index)
            print(pos[type_index-1])
            if extract_type == "split":
                procon, con_count = self.parse_util.getValuableWords(split_con,pos[:split_index],dep[:split_index])

            elif type_index == 0:

                temp = cut_words[type_index+1:]
                temp_pos = pos[type_index+1:]
                temp_dep = dep[type_index+1:]
                procon, con_count = self.parse_util.getValuableWords(temp, temp_pos,temp_dep)

            elif type_index > hed_index and pos[type_index-1]=='r':


                temp = cut_words[:hed_index]
                temp_pos = pos[:hed_index]
                temp_dep = dep[:hed_index]
                procon, con_count = self.parse_util.getValuableWords(temp,temp_pos,temp_dep)
            elif type_index < hed_index and pos[type_index-1] == "r":

                temp = cut_words[type_index+1:]
                temp_pos = pos[type_index+1:]
                temp_dep = dep[type_index+1:]
                procon, con_count = self.parse_util.getValuableWords(temp, temp_pos, temp_dep)

            else:

                procon, con_count = self.parse_util.getValuableWords(cut_words, pos, dep)
            print(procon, con_count,"procon===============")

            if len(key_entity)==0:

                for i in range(len(cut_words)):
                    if dep[i][2] == 'HED' and pos[i] in ['n', 'nd', 'ni', 'nl', 'ns', 'nt', 'nz']:
                        key_entity.append(cut_words[i])
                for i in range(len(cut_words)):
                    if dep[i][2] == 'SBV' and pos[i] in ['n', 'nd', 'ni', 'nl', 'ns', 'nt', 'nz']:
                        key_entity.append(cut_words[i])
                for i in range(len(cut_words)):
                    if dep[i][2] == 'VOB' and pos[i] in ['n', 'nd', 'ni', 'nl', 'ns', 'nt', 'nz']:
                        key_entity.append(cut_words[i])

            """

            elif ent_type == "etype" and '最' in cut_words:
                con, con_count = self.parse_util.getValuableWords(cut_words, pos, dep)
                left = 1
                begin = cut_words.index('最')
                none_array = []
                while (begin >= left):

                    if pos[begin - left] in ['n', 'nl', 'ni', 'ns', 'nz']:
                        none_array.append(cut_words[begin - left])

                    left = left + 1

                key_adj = "最" + cut_words[cut_words.index('最') + 1]
                none_array.append(key_adj)

                return entity, [none_array, con, con_count], "most"
            """

            return entity,[procon,con_count,key_entity],"content"











