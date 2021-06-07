# @Time : 2021/2/9 11:16 AM 
# @Author : LinXiaofei
# @File : history_business.py
from backend.nlu.LTPUtil import LTPUtil
from backend.nlu.parseSentence import ParseSentence
from backend.data.data_process import read_file
from backend.graphSearch.graphSearch import graphSearch
from backend.graphSearch.normalBussiness import normalBussiness
from backend.nlu.processNLU import processNLU
from backend.numUtil.numUtil import getDateNum

import numpy as np
import configparser

class HistoryBussiness(object):

    def __init__(self):

        config = configparser.ConfigParser()
        config.read("../backend/data/历史/combine_ent3.ini")
        self.config = config
        self.parseSentence = ParseSentence()
        self.normal_bussiness = normalBussiness()
        self.process_nlu = processNLU()
        self.ltp_util = LTPUtil()
        self.graph_util = graphSearch()

    def getEntitybyType(self,entity):
        entity_list = self.normal_bussiness.graph_util.getEntityByTypeAddType(entity)

        return entity_list


    def askWho(self,words):

        if '哪个' in words and '人' in words:
            words.replace("人", "单人")
        elif '谁' in words:
            words.replace("谁", '哪个单人')
        return words

    def dealYear(self,words):

        cut_words, pos, dep,reverse_dep = self.ltp_util.get_sentence_data(words)
        print(cut_words)
        """
        seg, hidden = self.ltp_util.getSEG(words)
        cut_words = seg[0]
        pos = self.ltp_util.getPOS(hidden)[0]
        dep = self.ltp_util.getDEP(hidden)[0]
        """

        #ent_list = self.parseSentence.getEntity(cut_words)

        ent, array, extractType = self.parseSentence.extractBestEnt(cut_words, dep)
        year_pro = read_file("../backend/data/历史/year_pro.csv")

        con, con_count = self.parseSentence.getValuableWords(cut_words, pos, dep)
        print(ent,con, con_count)
        print("=================================")

        if extractType == 'entity':

            ans = self.normal_bussiness.compareContentYear([ent], [con, con_count], year_pro)
            if ans:
                if '年' in ans or '世纪' in ans:
                    return [1, ans, ent]
            ans = self.normal_bussiness.doNormalForFalseYear(ent, [con, con_count])
            if ans:
                if '年' in ans or '世纪' in ans:
                    return [1, ans, ent]

        con_index = list(np.argsort(con_count))
        con_count_sort = np.array(con_count)[con_index]
        con_sort = np.array(con)[con_index]

        for c in con_sort:
            if '年' in c:
                continue
            best_word = c
            break

        ans = self.normal_bussiness.doNormalForFalseYear(best_word, [con_sort, con_count_sort])
        if ans:
            if '年' in ans or '世纪' in ans:
                return [1, ans, ent]
        return [0, "无法回答", None]

    def dealWho(self,words):
        #ltp = LTPUtil()

        cut_words, pos, dep,reverse_dep = self.ltp_util.get_sentence_data(words)
        con, con_count = self.parseSentence.getValuableWords(cut_words, pos, dep)
        key_ent = self.parseSentence.getSimpleEntity(cut_words)


        return [con, con_count,key_ent]

    def compareTime(self,words):

        ask_type = None

        posi_array = ['早','近']
        nega_array = ['晚','迟']

        if '哪' in words:
            for p in posi_array:
                if p in words and words.index(p) > words.index('哪'):
                    ask_type = "positive"
                    break
            for n in nega_array:
                if n in words and words.index(n) > words.index('哪'):
                    ask_type = "negative"
                    break
        if ask_type is None:
            return False,None

        cut_words, pos, dep, reverse_dep = self.ltp_util.get_sentence_data(words)

        ent_list = self.parseSentence.getEntityTwo(cut_words)

        if ent_list is None:
            return False,None


        value_list = self.graph_util.fuzzySearchForSAP("?plabel","时间",ent_list[0])
        if len(value_list) == 0:
            return False,None

        date_num_1 = 100000000000000000000000000000000000

        for v in value_list:
            temp_date_num_1 = getDateNum(v)
            if temp_date_num_1 and temp_date_num_1<date_num_1:
                date_num_1 = temp_date_num_1


        value_list = self.graph_util.fuzzySearchForSAP("?plabel", "时间", ent_list[1])

        if len(value_list) == 0:
            return False,None

        date_num_2 = 100000000000000000000000000000000000
        for v in value_list:
            temp_date_num_2 = getDateNum(v)
            if temp_date_num_2 and temp_date_num_2<date_num_2:
                date_num_2 = temp_date_num_2

        if date_num_2 == 100000000000000000000000000000000000 or date_num_1==100000000000000000000000000000000000:
            return True, [0, "无法回答", ent_list[0]]

        if ask_type == 'positive':
            if date_num_1 < date_num_2:
                return True,[1,ent_list[0]+"比"+ent_list[1]+"早",ent_list[0]]
            else:
                return True,[1, ent_list[1] + "比" + ent_list[0] + "早", ent_list[1]]
        else:
            if date_num_1 < date_num_2:
                return True, [1, ent_list[1] + "比" + ent_list[0] + "晚", ent_list[1]]
            else:
                return True, [1, ent_list[0] + "比" + ent_list[1] + "晚", ent_list[0]]


    def dealBookSBV(self,words):
        print(words,"dealBookSBV")
        #ltp = LTPUtil()


        cut_words, pos, dep, reverse_dep = self.ltp_util.get_sentence_data(words)

        """排除从句"""

        _, task_type = self.parseSentence.getWordsExtractType(cut_words, dep, pos)
        #print("task_type",task_type)


        if task_type in ['split', 'split_end']:
            return None, None, None

        ent, array, extractType = self.parseSentence.extractBestEnt(cut_words, dep)
        bookent = read_file("../backend/data/历史/bookent.csv")

        if ent in bookent and "《" in words:
            cut_words[cut_words.index(ent)] = "《" + ent + "》"
            entity, ans, task_type = self.process_nlu.dealNormal("《" + ent + "》", ["《" + ent + "》"], cut_words, pos, dep,reverse_dep)

            return entity, ans, task_type

        return None, None, None

    def dealCombineEntForCon(self,words):
        ent_array = self.config.sections()

        for ent in ent_array:
            key_words = self.config[ent]['keyword'].split(",")
            match_words = self.config[ent]['matchword'].split(",")

            flag = False
            for kw in key_words:
                if kw in words:
                    flag = True
                    for mw in match_words:
                        print(mw, words, ent)
                        if mw not in words:
                            flag = False
                            break
                    if flag:
                        break
                if flag:
                    break
            if flag:
                graph_util = graphSearch()
                pro_list, rel_list = graph_util.searchEntity(ent)
                for pro in pro_list:
                    if pro[0] in ['内容', '定义']:
                        return [1, pro[1], ent]

        return [0, '无法回答', None]

    def checkSplitEnt(self,words):
        check_arr = ['不同', '比较', '相同', '关系', '异同','影响','时间', '意义', '原因', '缘由', '理由', '方针', '政策',
                     '认识', '评价','启示']

        for ca in check_arr:
            if ca in words:
                return True
        return False

    def ansAgain(self, entity, nlu_result):
        print(type(entity).__name__,entity,"???")

        if type(entity).__name__ == 'str':
            print("type(entity).__name__ is 'str'")

            con = nlu_result[0]
            count = nlu_result[1]
            print(con)
            print(count)
            sort_index = np.argsort(count)[::-1]
            con = list(np.array(con)[sort_index])
            count = list(np.array(count)[sort_index])
            print("type(entity).__name__ is 'str'")
            print(con)
            print(count)
            for c_index in range(len(con)):
                if entity != con[c_index]:
                    best_value, best_name = self.normal_bussiness.doNormalForFalse(con[c_index],nlu_result)
                    if best_value:
                        return [1,best_value,best_name]
        elif type(entity).__name__ == 'list':

            con = nlu_result[0]
            count = nlu_result[1]
            print("type(entity).__name__ is 'list'")
            print(con)
            print(count)
            sort_index = np.argsort(count)[::-1]
            con = list(np.array(con)[sort_index])
            count = list(np.array(count)[sort_index])
            print("type(entity).__name__ is 'list'")
            print(count)
            print(con)



            for c_index in range(len(con)):
                if count[c_index] not in entity:
                    best_value, best_name = self.normal_bussiness.doNormalForFalse(con[c_index], nlu_result)
                    if best_value:
                        return [1, best_value, best_name]

        return [0,"无法回答"]





