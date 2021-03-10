# @Time : 2021/2/8 7:21 PM
# @Author : LinXiaofei
# @File : geoBussiness.py

from backend.nlu.LTPUtil import *
from backend.nlu.parseSentence import *
from backend.graphSearch.graphSearch import graphSearch
import numpy as np




class GeoBussiness(object):
    def __init__(self):
        self.ltp_util = LTPUtil()
        self.graph_util = graphSearch()
        self.parseSen = ParseSentence()
        """
        self.dm = DialogManagement()
        year_pro = read_file("../backend/data/历史/year_pro.csv")
        self.dm.setConpro(year_pro)
        self.history_business = HistoryBussiness()
        print("HistoryDM????????????????????????????")
        """

    def dealMostType(self,etype,con,word_count,key_word):

        name = []
        content = []
        count = []

        tri_list = self.graph_util.fuzzySearchOne("?plabel", "特征", etype)
        for value in tri_list:
            print(value)
            temp = 0
            for c in range(len(con)):
                if con[c] in value[2]:
                    print(con[c], word_count[c], value[0])
                    temp += word_count[c]

            if (temp >= np.sum(word_count) / 2):
                flag = True
                for kw in key_word:
                    if kw not in value[2]:
                        flag = False
                if flag:
                    name.append(value[0])
                    content.append(value[2])
                    count.append(temp)

        most_pro = ['地位', '作用', '定义', '优点', '意义', '示例', '内容']
        for p in most_pro:
            result = self.graph_util.getValueByPro(etype, p)
            for value in result:
                print(value)
                temp = 0
                for c in range(len(con)):
                    if con[c] in value[1]:
                        print(con[c], word_count[c], value[0])
                        temp += word_count[c]

                if (temp >= np.sum(word_count) / 2):
                    flag = True
                    for kw in key_word:
                        if kw not in value[1]:
                            flag = False
                    if flag:
                        name.append(value[0])
                        content.append(value[1])
                        count.append(temp)

        if len(count) == 0:
            return [0]
        cal_value = []
        value_len = []
        cal_name = []
        max_count = np.max(count)
        for i in range(len(count)):
            if count[i] == max_count:
                cal_value.append(content[i])
                value_len.append(len(content[i]))
                cal_name.append(name[i])
        return [1, cal_name[np.argmin(value_len)] + ": " + cal_value[np.argmin(value_len)],
                cal_name[np.argmin(value_len)]]


    def dealMostEnt(self,entity,con,word_count,key_word):

        name = []
        content = []
        count = []

        pro_list, rel_list = self.graph_util.searchEntity(entity)


        for p in pro_list:
            temp = 0
            for c in range(len(con)):
                if con[c] in p[1]:
                    print(con[c], word_count[c], p[1])
                    temp += word_count[c]
            if (temp >= np.sum(word_count) / 2):
                flag = True
                for kw in key_word:
                    if kw not in p[1]:
                        flag = False
                if flag:

                    content.append(p[1])
                    count.append(temp)
        if len(count) == 0:
            return [0]
        cal_value = []
        value_len = []

        max_count = np.max(count)
        for i in range(len(count)):
            if count[i] == max_count:
                cal_value.append(content[i])
                value_len.append(len(content[i]))

        return [1, cal_value[np.argmin(value_len)],
                entity]


    def doMost(self,words):



        cut_word, pos, dep = self.ltp_util.get_sentence_data(words)
        key_word = []

        for w_index in range(len(cut_word)):
            if '最' == cut_word[w_index]:
                key_word.append(cut_word[w_index])
                key_word.append(cut_word[w_index+1])
            elif '最' in cut_word[w_index]:
                key_word.append(cut_word[w_index])

        con, word_count = self.parseSen.getValuableWords(cut_word, pos, dep)
        ent, parseType = self.parseSen.extractType(cut_word)

        print(parseType, "parseType")
        if parseType in ['split', 'split_end']:
            return self.dealMostType(ent,con,word_count,key_word)
        elif parseType== 'normal':
            ent,_,__ = self.parseSen.extractBestEnt(cut_word,dep)
            if ent:

                return self.dealMostEnt(ent,con,word_count,key_word)

        return [0]












    def doMost2(self,words):
        cut_word, pos, dep = self.ltp_util.get_sentence_data(words)


        #cut_word, hidden = self.ltp_util.getSEG(words)
        #dep = self.ltp_util.getDEP(hidden)[0]
        #pos = self.ltp_util.getPOS(hidden)[0]
        #print(pos)
        #cut_word = cut_word[0]

        ent, parseType = parseSen.extractType(cut_word)
        print(parseType, "parseType")
        if parseType in ['split', 'split_end']:
            etype = ent
        else:
            return [0]

        pos_entity = parseSen.getEntity(cut_word)
        print("===========================================")

        for w_idnex in range(len(cut_word)):

            print(cut_word[w_idnex])

            if '最' in cut_word[w_idnex]:

                if cut_word[w_idnex] == '最':
                    key_adj = "最" + cut_word[w_idnex + 1]
                else:
                    key_adj = cut_word[w_idnex]

                begin = w_idnex
                left = 1
                none_array = []
                while (begin >= left):

                    if '最' in cut_word[begin - left]:

                        none_array += pos_entity
                        none_array = list(set(none_array))
                        break

                    if pos[begin - left] in ['n', 'nl', 'ni', 'ns', 'nz'] and cut_word[begin - left] not in none_array:
                        none_array.append(cut_word[begin - left])
                    left = left + 1
                #key_adj = "最" + cut_word[w_idnex + 1]
                none_array.append(key_adj)
                print(none_array)

                ans,ent = self.dealMost(etype, none_array)

                if ans:
                    print("ajshdkajshdoaiuehdlud==============",ans)
                    return [1, ans, ent]

        return [0]

    def dealMost(self,etype, match):

        tri_list = self.graph_util.fuzzySearchOne("?plabel", "特征", etype)

        for i in range(len(tri_list)):
            flag = True
            for m in match:
                if m not in tri_list[i][2]:
                    flag = False
                    break
            if flag:
                print(tri_list[i][0],"dealMost")
                return tri_list[i][0]+":"+tri_list[i][2],tri_list[i][0]

        most_pro = ['地位', '作用', '定义', '优点', '意义', '示例', '内容']
        for p in most_pro:
            result = self.graph_util.getValueByPro(etype, p)
            for i in range(len(result)):
                flag = True
                for m in match:
                    if m not in result[i][1]:
                        flag = False
                        break
                if flag:
                    print(result[i][0], "dealMost")
                    return result[i][0]+":"+result[i][1],result[i][0]

        if '世界' in match or '地球' in match:
            for i in range(len(tri_list)):
                flag = True
                for m in match:
                    if m == '世界' or m == '地球':
                        continue
                    if m not in tri_list[i][2]:
                        flag = False
                        break
                if flag:
                    print(tri_list[i][0], "dealMost")
                    return tri_list[i][0]+":"+tri_list[i][2],tri_list[i][0]
            for i in range(len(result)):
                flag = True
                for m in match:
                    if m == '世界' or m == '地球':
                        continue
                    if m not in result[i][1]:
                        flag = False
                        break
                if flag:
                    print(result[i][0], "dealMost")
                    return result[i][0]+":"+result[i][1],result[i][0]

        return None

