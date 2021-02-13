# @Time : 2020/12/27 12:28 PM 
# @Author : LinXiaofei
# @File : ConPro.py
"""
    原因型
    形成 + ent + 的原因是什么
    形成 + ent + 的 + conpro.split("原因")[0]/alias_conpro + "因素是什么"
    造成 + ent + 的 + conpro.split("原因")[0]/alias_conpro + "因素是什么"

    n+n
    名词分离型
    ent + "的" + sepnonepro + "是什么"
    ent + "主要的" + sepnonepro + "是什么"
    ent + "的" + front_pro + "是什么" + end_pro
    ent + "的" + front_pro + "以" + end_pro + "为主"

    v+n
    动词分离型
    ent + "的" + sepverbpro + "是什么"
    ent + front_pro + "的" + end_pro + "是什么"

    描述型
    ent + conpro/alias_conpro + 的概况 + 是什么
    ent + conpro/alias_conpro + 的情况 + 是什么
    ent + conpro/alias_conpro + 有 + 什么/哪些 + 特征
    ent + conpro/alias_conpro + 的特征 + 是/有 + 什么/哪些

    范围型
    ent + conpro/alias_conpro + 是/有 + 什么/哪些
    ent + 以 + 什么/哪些 + conpro/alias_conpro 为主
    ent + 有 + 哪些/什么 + conpro/alias_conpro
    ent + 主要的 + conpro/alias_conpro 是/有 + 什么/哪些
    ent + v + 的 + conpro/alias_conpro + 有哪些/有什么

    唯一型
    ent + 的 + conpro/alias_conpro + 是什么
    ent + v + 什么

    如何型
    ent + 是怎么 + howpro + 的
    怎么 + howpro + ent

    如何分解型
    ent + 的 + sephowpro + 是什么
    ent + 的 + front_none + 是怎么 + end_verb + 的

    默认型
    作为实体没有属性是的默认情况


"""

from backend.graphSearch.graphSearch import graphSearch

import numpy as np
import configparser
config = configparser.ConfigParser()
config.read("../backend/config.ini")
subject = config['DEFAULT']['subject']
config.read("../backend/data/"+subject+"/proconfig.ini")


def getpro(words, pos, dep, ent, ent_list,ent_index):

    graph_util = graphSearch()
    pro_list = graph_util.getProList(ent)

    print(pro_list,ent,"???????")

    normal = []
    sep = []
    reason = []
    default = []
    for pro in pro_list:
        if pro in ['示例', '图片','降水位置图', '出处', '河流',
                 '干湿状况', '天气图', '符号图', '最低值', '最高值', '分类编号', '气候']:
            continue
        if 'sep' in config[pro]['type']:
            sep.append(pro)
        elif 'reason' in config[pro]['type']:
            reason.append(pro)
        elif 'default' in config[pro]['type']:
            default.append(pro)
        else:
            normal.append(pro)

    print(normal)
    print(sep)
    print(reason)
    print(default)
    if len(reason) > 0:
        best_pro,key_word = getReasonPro(reason,words,ent_index)
        print(best_pro, key_word)
        if best_pro:
           return ent,best_pro,key_word
    if len(sep) > 0:
        best_pro, key_word = getSepPro(sep, words, ent_index, dep)
        print(best_pro, key_word)
        if best_pro:
            return ent, best_pro, key_word

    if len(normal) > 0:
        best_pro, key_word = getNormalPro(normal, words, pos, dep, ent_index)
        print(best_pro, key_word)
        if best_pro:
            return ent, best_pro, key_word
    if len(default) > 0:
        best_pro = getDefaultPro(default, words, pos)
        if best_pro:
            return ent,best_pro,words[ent_index]





    stop_pro = pro_list+['定义', '示例', '图片', '内容', '降水位置图', '出处', '河流',
                 '干湿状况', '天气图', '符号图', '最低值', '最高值', '分类编号', '内容', '定义', '气候']
    for e in ent_list:
        uncertain = graph_util.getProList(e)
        print(e, uncertain)

        for pro in uncertain:
            if pro in stop_pro:
                continue

            stop_pro.append(pro)

            if 'sep' in config[pro]['type']:
                best_pro, key_word = getSepPro([pro], words, ent_index, dep)
                if best_pro:
                    return e,best_pro, key_word
            elif 'reason' in config[pro]['type']:
                best_pro, key_word = getReasonPro([pro], words,ent_index)
                if best_pro:
                    return e,best_pro, key_word
            else:
                best_pro, key_word = getNormalPro(normal,words, pos, dep, ent_index)
                if best_pro:
                    return e,best_pro, key_word

    return None,None, None


def getNormalPro(pro_list, words, pos, dep, ent_index):


    best_pro = []
    key_word = []
    pro_index = []

    for pro in pro_list:
        print(pro)

        key = list(config[pro])
        if pro in words:
            print("addpro", pro)
            best_pro.append(pro)
            key_word.append(pro)
            pro_index.append(words.index(pro))
            continue

        if "主要" in pro:
            main_pro = pro.replace("主要","")
            if main_pro in words:
                best_pro.append(pro)
                key_word.append(main_pro)
                pro_index.append(words.index(main_pro))
                continue

        if 'alias' in key:
            alias = config[pro]['alias'].split(",")

            for a in alias:
                if a in words:
                    best_pro.append(pro)
                    key_word.append(a)
                    pro_index.append(words.index(a))
                    continue

        if 'verb' in key:
            verb = config[pro]['verb'].split(",")

            for a in verb:
                if a in words and ent_index < words.index(a):
                    best_pro.append(pro)
                    key_word.append(a)
                    pro_index.append(words.index(a))
                    continue
        if 'passive_verb' in key:
            verb = config[pro]['passive_verb'].split(",")
            for a in verb:
                if a in words and ent_index > words.index(a):
                    print("addpassive_verb", a)
                    best_pro.append(pro)
                    key_word.append(a)
                    pro_index.append(words.index(a))
                    continue

        if config[pro]['type'] == "numpro":

            if 'noun' in key:

                none = config[pro]['noun'].split(",")
                for a in none:
                    print()
                    if a in words and pos[words.index(a) - 1] == 'r':
                        print("addnoun", a)
                        best_pro.append(pro)
                        key_word.append(a)
                        pro_index.append(words.index(a))
                        continue

            if 'adj' in key:
                adj = config[pro]['adj'].split(",")
                for a in adj:
                    if a in words and words[words.index(a)-1]=='多':
                        print("addadj", a)
                        best_pro.append(pro)
                        key_word.append(a)
                        pro_index.append(words.index(a))
                        continue
    print(dep)
    if len(best_pro) == 1:
        return best_pro[0],key_word[0]

    elif len(best_pro) > 1:
        count = []
        for i in range(len(best_pro)):
            if dep[pro_index[i]][2] == 'HED':
                count.append(4)
            elif dep[pro_index[i]][2] == 'VOB' and dep[dep[pro_index[i]][1]-1][2]=='HED':
                count.append(3)
            elif dep[pro_index[i]][2] == 'SBV' and dep[dep[pro_index[i]][1]-1][2]=='HED':

                if words[dep[pro_index[i]][1]-1] == '是':
                    count.append(5)
                else:
                    count.append(2)

            else:
                count.append(0)
        max_count = np.argmax(count)
        return best_pro[max_count],key_word[max_count]

    return None,None

def getSepPro(pro_list, words, ent_index, dep):


    for pro in pro_list:
        key = list(config[pro])
        if pro in words:
            best_pro = pro
            key_word = pro
            return best_pro,key_word

        if "主要" in pro:
            main_pro = pro.replace("主要","")
            if main_pro in words:
                best_pro = pro
                key_word = main_pro
                return best_pro, key_word
            front_pro = main_pro[:-2]
            end_pro = main_pro[-2:]
            if front_pro in words and end_pro in words and (words.index(front_pro) < words.index(end_pro) or dep[words.index(front_pro)]=='HED'):
                best_pro = pro
                key_word = front_pro
                return best_pro, key_word
        front_pro = pro[:-2]
        end_pro = pro[-2:]
        if front_pro in words and end_pro in words and (words.index(front_pro) < words.index(end_pro) or dep[words.index(front_pro)]=='HED'):
            best_pro = pro
            key_word = front_pro
            return best_pro, key_word
        if 'alias' in key:
            alias = config[pro]['alias'].split(",")

            for a in alias:
                if a in words:
                    print("addalias", a)
                    best_pro = pro
                    key_word = a
                    return best_pro, key_word
                front_pro = a[:-2]
                end_pro = a[-2:]
                if front_pro in words and end_pro in words and (words.index(front_pro) < words.index(end_pro) or dep[words.index(front_pro)]=='HED'):
                    print("add sepverbpro alias", a)
                    best_pro = pro
                    key_word = front_pro
                    return best_pro, key_word
        if 'verb' in key:
            verb = config[pro]['verb'].split(",")
            for a in verb:
                if a in words and ent_index < words.index(a):
                    print("addverb", a)
                    best_pro = pro
                    key_word = a
                    return best_pro, key_word
        if 'passive_verb' in key:
            verb = config[pro]['passive_verb'].split(",")
            for a in verb:
                if a in words and ent_index > words.index(a):
                    print("addpassive_verb", a)
                    best_pro = pro
                    key_word = a
                    return best_pro, key_word
    for pro in pro_list:
        if '特征' in pro:
            continue
        if pro[-2:] in words:
            best_pro = pro
            key_word = pro[-2:]
            return best_pro, key_word

    return None,None

def getReasonPro(pro_list, words, ent_index):
    for pro in pro_list:
        if pro in words:
            return pro,pro

        if '原因' in pro:
            reason_pro = pro.replace("原因","")
            if reason_pro in words and ("原因" in words or "因素" in words):
                return pro,reason_pro
        if '因素' in pro:
            reason_pro = pro.replace("因素","")
            if reason_pro in words and ("原因" in words or "因素" in words):
                return pro,reason_pro

        if "主要" in pro:
            main_pro = pro.replace("主要","")
            if main_pro in words:
                return pro,main_pro
            if '原因' in main_pro:
                reason_pro = main_pro.replace("原因", "")
                if reason_pro in words and ("原因" in words or "因素" in words):
                    return pro, reason_pro
            if '因素' in main_pro:
                reason_pro = main_pro.replace("因素", "")
                if reason_pro in words and ("原因" in words or "因素" in words):
                    return pro, reason_pro
        key = list(config[pro])
        if 'alias' in key:
            alias = config[pro]['alias'].split(",")

            for a in alias:
                if a in words:
                    print("addalias", a)
                    best_pro = pro
                    key_word = a
                    return best_pro, key_word
                front_pro = a[:-2]
                end_pro = a[-2:]
                if front_pro in words and end_pro in words and words.index(front_pro) > words.index(end_pro):
                    print("add sepverbpro alias", a)
                    best_pro = pro
                    key_word = a
                    return best_pro, key_word
            if 'passive_verb' in key:
                verb = config[pro]['passive_verb'].split(",")
                for a in verb:
                    if a in words and ent_index > words.index(a):
                        print("addpassive_verb", a)
                        best_pro = pro
                        key_word = a
                        return best_pro, key_word
        """
        for pro in pro_list:
            if pro[-2:] in words:
                best_pro = pro
                key_word = pro[-2:]
                return best_pro, key_word

        """

    return None,None

def getDefaultPro(pro_list, words, pos):
    r_flag = False
    v_flag = False
    if len(words)==3 or (len(words)==4 and words[3] in ["?","？"]):
        for w_index in range(len(words)):
            if pos[w_index] == 'r':
                r_flag = True
            if words[w_index] in ['是','有']:
                v_flag = True
    if r_flag and v_flag:

        return pro_list[0]


