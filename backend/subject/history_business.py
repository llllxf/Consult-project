# @Time : 2021/2/9 11:16 AM 
# @Author : LinXiaofei
# @File : history_business.py
from backend.nlu.LTPUtil import LTPUtil
from backend.nlu.parseSentence import ParseSentence
from backend.data.data_process import read_file
from backend.graphSearch.graphSearch import graphSearch
from backend.graphSearch.normalBussiness import normalBussiness
from backend.nlu.processNLU import processNLU

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




    def askWho(self,words):

        if '哪个' in words and '人' in words:
            words.replace("人", "单人")
        elif '谁' in words:
            words.replace("谁", '哪个单人')
        return words

    def dealYear(self,words):

        cut_words, pos, dep = self.ltp_util.get_sentence_data(words)
        """
        seg, hidden = self.ltp_util.getSEG(words)
        cut_words = seg[0]
        pos = self.ltp_util.getPOS(hidden)[0]
        dep = self.ltp_util.getDEP(hidden)[0]
        """

        ent, array, extractType = self.parseSentence.extractBestEnt(cut_words, dep)
        year_pro = read_file("../backend/data/历史/year_pro.csv")

        con, con_count = self.parseSentence.getValuableWords(cut_words, pos, dep)

        if extractType == 'entity':
            ans = self.normal_bussiness.doNormalbyCon([ent], [con, con_count], year_pro)
            if ans:
                if '年' in ans:
                    return [1, ans, ent]

        best_word = con[np.argmax(con_count)]
        ans = self.normal_bussiness.doNormalForFalse(best_word, [con, con_count])
        if ans:
            if '年' in ans:
                return [1, ans, ent]

        return [0, "无法回答", None]

    def dealWho(self,words):
        #ltp = LTPUtil()

        cut_words, pos, dep = self.ltp_util.get_sentence_data(words)
        """
        seg, hidden = self.ltp_util.getSEG(words)
        cut_words = seg[0]
        pos = self.ltp_util.getPOS(hidden)[0]
        dep = self.ltp_util.getDEP(hidden)[0]
        """

        con, con_count = self.parseSentence.getValuableWords(cut_words, pos, dep)

        key_ent = self.parseSentence.getEntity(cut_words)
        print([con, con_count] + key_ent)

        return [con, con_count] + key_ent

    def dealBookSBV(self,words):
        #ltp = LTPUtil()

        cut_words, pos, dep = self.ltp_util.get_sentence_data(words)
        """
        seg, hidden = self.ltp_util.getSEG(words)
        cut_words = seg[0]
        pos = self.ltp_util.getPOS(hidden)[0]
        dep = self.ltp_util.getDEP(hidden)[0]
        """

        _, task_type = self.parseSentence.getWordsExtractType(cut_words, dep, pos)

        if task_type in ['split', 'split_end']:
            return None, None, None

        ent, array, extractType = self.parseSentence.extractBestEnt(cut_words, dep)
        bookent = read_file("../backend/data/历史/bookent.csv")

        if ent in bookent:
            cut_words[cut_words.index(ent)] = "《" + ent + "》"
            entity, ans, task_type = self.process_nlu.dealNormal("《" + ent + "》", array, cut_words, pos, dep)

            return entity, ans, task_type

        return None, None, None

    def dealCombineEntForCon(self,words):
        ent_array = self.config.sections()

        for ent in ent_array:
            key_words = self.config[ent]['keyword'].split(",")
            match_words = self.config[ent]['matchword'].split(",")
            # print(ent)
            # print(key_words)
            # print(match_words)
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
        check_arr = ['不同', '比较', '相同', '关系', '异同', '特点', '影响', '性', '条件', '时间', '意义', '原因', '缘由', '理由', '方针', '政策',
                     '认识', '评价']

        for ca in check_arr:
            if ca in words:
                return True
        return False




