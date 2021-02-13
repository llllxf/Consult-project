# @Time : 2021/2/8 7:21 PM 
# @Author : LinXiaofei
# @File : geoBussiness.py

from backend.nlu.LTPUtil import *
from backend.nlu.parseSentence import *
from backend.graphSearch.graphSearch import graphSearch

parseSen = ParseSentence()
graph_util = graphSearch()

def doMost(words):
    cut_word,hidden = getSEG(words)
    dep = getDEP(hidden)[0]
    pos = getPOS(hidden)[0]
    print(pos)
    cut_word = cut_word[0]

    ent,parseType = parseSen.extractType(cut_word)
    print(parseType,"parseType")
    if parseType in ['split','split_end']:
        etype = ent
    else:

        return [0]

    pos_entity = parseSen.getEntity(cut_word)


    for w_idnex in range(len(cut_word)):


        if cut_word[w_idnex] == '最':

            begin = w_idnex
            left = 1
            none_array = []
            while (begin >= left):

                if cut_word[begin-left] == '最':
                    none_array += pos_entity
                    break

                if pos[begin - left] in ['n', 'nl', 'ni', 'ns', 'nz']:
                    none_array.append(cut_word[begin - left])
                left = left + 1
            key_adj = "最" + cut_word[w_idnex+1]
            none_array.append(key_adj)
            print(none_array)

            ans = dealMost(etype,none_array)

            if ans:
                return [1, ans, etype]

    return [0]


def dealMost(etype, match):
    print("doMost", etype, match)

    tri_list = graph_util.fuzzySearchOne("?plabel", "特征", etype)
    for i in range(len(tri_list)):
        flag = True
        for m in match:
            if m not in tri_list[i][2]:
                flag = False
                break
        if flag:
            return tri_list[i][0]

    most_pro = ['地位', '作用', '定义', '优点','意义','示例','内容']
    for p in most_pro:
        result = graph_util.getValueByPro(etype, p)
        for i in range(len(result)):
            flag = True
            for m in match:
                if m not in result[i][1]:
                    flag = False
                    break
            if flag:
                return result[i][0]

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
                return tri_list[i][0]
        for i in range(len(result)):
            flag = True
            for m in match:
                if m == '世界' or m == '地球':
                    continue
                if m not in result[i][1]:
                    flag = False
                    break
            if flag:
                return result[i][0]

    return None







