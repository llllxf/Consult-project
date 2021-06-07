# @Time : 2020/12/27 12:28 PM 
# @Author : LinXiaofei
# @File : ConPro.py
"""
没有用

"""

from backend.graphSearch.graphSearch import graphSearch
from backend.data.data_process import read_file
import numpy as np
import configparser
"""
config = configparser.ConfigParser()
config.read("../backend/config.ini")
subject = config['DEFAULT']['subject']
config.read("../backend/data/"+subject+"/proconfig.ini")
"""

class ConPro(object):
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("../backend/config.ini")
        subject = config['DEFAULT']['subject']
        config.read("../backend/data/" + subject + "/proconfig.ini")
        self.config = config
        self.graph_util = graphSearch()

        etype = list(set(read_file("../backend/data/" + subject + "/etype.csv")))
        self.typeArray = sorted(etype, key=lambda i: len(i), reverse=True)
    """
    def getNumPro(self, words, pos,ent):
        pro_list = self.graph_util.getProList(ent)
    """



    def getpro(self, words, pos, dep, ent, ent_index):

        pro_list = self.graph_util.getProList(ent)

        normal = []
        sep = []
        reason = []
        default = []
        for pro in pro_list:
            if pro in ['示例', '图片', '降水位置图', '出处', '河流',
                       '干湿状况', '天气图', '符号图', '最低值', '最高值', '分类编号', '气候']:
                continue
            if 'sep' in self.config[pro]['type']:
                sep.append(pro)
            elif 'reason' in self.config[pro]['type']:
                reason.append(pro)
            elif 'default' in self.config[pro]['type']:
                default.append(pro)
            else:
                normal.append(pro)

        print("normal:", normal)
        print("sep:", sep)
        print("reason:", reason)
        print("default:", default)
        if len(reason) > 0:
            best_pro, key_word = self.getReasonPro(reason, words, ent_index)
            print(best_pro, key_word)
            if best_pro:
                return best_pro, key_word
        if len(sep) > 0:
            best_pro, key_word = self.getSepPro(sep, words, ent_index, dep)
            print(best_pro, key_word)
            if best_pro:
                return best_pro, key_word

        if len(normal) > 0:
            best_pro, key_word = self.getNormalPro(normal, words, pos, dep, ent_index)
            print(best_pro, key_word)
            if best_pro:
                return best_pro, key_word
        if len(default) > 0:
            best_pro = self.getDefaultPro(default, words, pos)
            if best_pro:
                return best_pro, words[ent_index]
        """
        stop_pro = pro_list + ['示例', '图片', '降水位置图', '出处', '河流',
                               '干湿状况', '天气图', '符号图', '最低值', '最高值', '分类编号', '气候']
        for e in ent_list:
            uncertain = graph_util.getProList(e)
            print("uncertain:", e, uncertain)

            for pro in uncertain:
                if pro in stop_pro:
                    continue
                print("pro:", pro)

                stop_pro.append(pro)

                if 'sep' in self.config[pro]['type']:
                    best_pro, key_word = self.getSepPro([pro], words, ent_index, dep)
                    if best_pro:
                        return e, best_pro, key_word
                elif 'reason' in self.config[pro]['type']:
                    best_pro, key_word = self.getReasonPro([pro], words, ent_index)
                    if best_pro:
                        return e, best_pro, key_word
                else:
                    best_pro, key_word = self.getNormalPro([pro], words, pos, dep, ent_index)
                    if best_pro:
                        return e, best_pro, key_word
        """

        return None, None

    def getNormalPro(self,pro_list, words, pos, dep, ent_index):

        best_pro = []
        key_word = []
        pro_index = []

        for pro in pro_list:
            print(pro)

            key = list(self.config[pro])
            if pro in words:
                print("addpro", pro)
                best_pro.append(pro)
                key_word.append(pro)
                pro_index.append(words.index(pro))
                continue

            if "主要" in pro:
                main_pro = pro.replace("主要", "")
                if main_pro in words:
                    best_pro.append(pro)
                    key_word.append(main_pro)
                    pro_index.append(words.index(main_pro))
                    continue

            if 'alias' in key:
                alias = self.config[pro]['alias'].split(",")

                for a in alias:
                    if a in words:
                        best_pro.append(pro)
                        key_word.append(a)
                        pro_index.append(words.index(a))
                        continue

            if 'verb' in key:
                verb = self.config[pro]['verb'].split(",")

                for a in verb:
                    if a in words and ent_index < words.index(a):
                        best_pro.append(pro)
                        key_word.append(a)
                        pro_index.append(words.index(a))
                        continue
            if 'passive_verb' in key:
                verb = self.config[pro]['passive_verb'].split(",")
                for a in verb:
                    if a in words and ent_index > words.index(a):
                        print("addpassive_verb", a)
                        best_pro.append(pro)
                        key_word.append(a)
                        pro_index.append(words.index(a))
                        continue
            """
            if self.config[pro]['type'] == "numpro":

                if 'unit' in key:

                    none = self.config[pro]['unit'].split(",")
                    for a in none:
                        print()
                        if a in words and pos[words.index(a) - 1] == 'r':
                            print("addnoun", a)
                            best_pro.append(pro)
                            key_word.append(a)
                            pro_index.append(words.index(a))
                            continue

                if 'adj' in key:
                    adj = self.config[pro]['adj'].split(",")
                    for a in adj:
                        if a in words and words[words.index(a) - 1] == '多':
                            print("addadj", a)
                            best_pro.append(pro)
                            key_word.append(a)
                            pro_index.append(words.index(a))
                            continue
                """
        print(dep)
        if len(best_pro) == 1:
            return best_pro[0], key_word[0]

        elif len(best_pro) > 1:
            count = []
            for i in range(len(best_pro)):
                if dep[pro_index[i]][2] == 'HED':
                    count.append(4)
                elif dep[pro_index[i]][2] == 'VOB' and dep[dep[pro_index[i]][1] - 1][2] == 'HED':
                    count.append(3)
                elif dep[pro_index[i]][2] == 'SBV' and dep[dep[pro_index[i]][1] - 1][2] == 'HED':

                    if words[dep[pro_index[i]][1] - 1] == '是':
                        count.append(5)
                    else:
                        count.append(2)
                else:
                    count.append(0)
            max_count = np.argmax(count)
            return best_pro[max_count], key_word[max_count]

        return None, None

    def getSepPro(self,pro_list, words, ent_index, dep):

        for pro in pro_list:
            key = list(self.config[pro])
            if pro in words:
                best_pro = pro
                key_word = pro
                return best_pro, key_word

            if "主要" in pro:
                main_pro = pro.replace("主要", "")
                if main_pro in words:
                    best_pro = pro
                    key_word = main_pro
                    return best_pro, key_word
                front_pro = main_pro[:-2]
                end_pro = main_pro[-2:]
                if front_pro in words and end_pro in words and (
                        words.index(front_pro) < words.index(end_pro) or dep[words.index(front_pro)][2] == 'HED'):
                    best_pro = pro
                    key_word = front_pro
                    return best_pro, key_word
            front_pro = pro[:-2]
            end_pro = pro[-2:]
            # print("北极黄河站什么时候建立的",front_pro,end_pro,dep[words.index(front_pro)][2])
            if front_pro in words and end_pro in words and (
                    words.index(front_pro) < words.index(end_pro) or dep[words.index(front_pro)][2] == 'HED'):
                best_pro = pro
                key_word = front_pro
                return best_pro, key_word
            if 'alias' in key:

                alias = self.config[pro]['alias'].split(",")
                print("北极的代表动物是什么", alias, words)

                for a in alias:
                    if a in words:
                        print("addalias", a)
                        best_pro = pro
                        key_word = a
                        return best_pro, key_word
                    front_pro = a[:-2]
                    end_pro = a[-2:]
                    if front_pro in words and end_pro in words and (
                            words.index(front_pro) < words.index(end_pro) or dep[words.index(front_pro)][2] == 'HED'):
                        print("add sepverbpro alias", a)
                        best_pro = pro
                        key_word = front_pro
                        return best_pro, key_word
            if 'verb' in key:
                verb = self.config[pro]['verb'].split(",")

                for a in verb:
                    if a in words and ent_index < words.index(a):
                        print("addverb", a)
                        best_pro = pro
                        key_word = a
                        return best_pro, key_word
            if 'passive_verb' in key:
                verb = self.config[pro]['passive_verb'].split(",")
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

        return None, None

    def getReasonPro(self,pro_list, words, ent_index):
        for pro in pro_list:
            if pro in words:
                return pro, pro

            if '原因' in pro:
                reason_pro = pro.replace("原因", "")
                if reason_pro in words and ("原因" in words or "因素" in words):
                    return pro, reason_pro
            if '因素' in pro:
                reason_pro = pro.replace("因素", "")
                if reason_pro in words and ("原因" in words or "因素" in words):
                    return pro, reason_pro

            if "主要" in pro:
                main_pro = pro.replace("主要", "")
                if main_pro in words:
                    return pro, main_pro
                if '原因' in main_pro:
                    reason_pro = main_pro.replace("原因", "")
                    if reason_pro in words and ("原因" in words or "因素" in words):
                        return pro, reason_pro
                if '因素' in main_pro:
                    reason_pro = main_pro.replace("因素", "")
                    if reason_pro in words and ("原因" in words or "因素" in words):
                        return pro, reason_pro
            key = list(self.config[pro])
            if 'alias' in key:
                alias = self.config[pro]['alias'].split(",")

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
                    verb = self.config[pro]['passive_verb'].split(",")
                    for a in verb:
                        if a in words and ent_index > words.index(a):
                            print("addpassive_verb", a)
                            best_pro = pro
                            key_word = a
                            return best_pro, key_word

        return None, None

    def getDefaultPro(self,pro_list, words, pos):

        

        for pro in pro_list:
            if pro in words:
                return pro
            key = list(self.config[pro])
            if 'alias' in key:
                alias = self.config[pro]['alias'].split(",")

                for a in alias:
                    if a in words:
                        print("addalias", a)
                        best_pro = pro

                        return best_pro

        r_flag = False
        v_flag = False

        if len(words) == 3 or  (len(words) == 4 and (words[3] in ["?", "？"] or words[3] not in self.typeArray)):
            for w_index in range(len(words)):
                if pos[w_index] == 'r':
                    r_flag = True
                if words[w_index] in ['是', '有', '在', '为', '包括' , '含', '含有','涵盖']:
                    v_flag = True
        if r_flag and v_flag:
            return pro_list[0]












"""
def getpro(words, pos, dep, ent, ent_list,ent_index,config):



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

    print("normal:",normal)
    print("sep:",sep)
    print("reason:",reason)
    print("default:",default)
    if len(reason) > 0:
        best_pro,key_word = getReasonPro(reason,words,ent_index,config)
        print(best_pro, key_word)
        if best_pro:
           return ent,best_pro,key_word
    if len(sep) > 0:
        best_pro, key_word = getSepPro(sep, words, ent_index, dep,config)
        print(best_pro, key_word)
        if best_pro:
            return ent, best_pro, key_word

    if len(normal) > 0:
        best_pro, key_word = getNormalPro(normal, words, pos, dep, ent_index,config)
        print(best_pro, key_word)
        if best_pro:
            return ent, best_pro, key_word
    if len(default) > 0:
        best_pro = getDefaultPro(default, words, pos,config)
        if best_pro:
            return ent,best_pro,words[ent_index]


    stop_pro = pro_list+['示例', '图片', '降水位置图', '出处', '河流',
                 '干湿状况', '天气图', '符号图', '最低值', '最高值', '分类编号','气候']
    for e in ent_list:
        uncertain = graph_util.getProList(e)
        print("uncertain:",e, uncertain)

        for pro in uncertain:
            if pro in stop_pro:
                continue
            print("pro:",pro)

            stop_pro.append(pro)

            if 'sep' in config[pro]['type']:
                best_pro, key_word = getSepPro([pro], words, ent_index, dep,config)
                if best_pro:
                    return e,best_pro, key_word
            elif 'reason' in config[pro]['type']:
                best_pro, key_word = getReasonPro([pro], words,ent_index,config)
                if best_pro:
                    return e,best_pro, key_word
            else:
                best_pro, key_word = getNormalPro([pro],words, pos, dep, ent_index,config)
                if best_pro:
                    return e,best_pro, key_word

    return None,None, None


def getNormalPro(pro_list, words, pos, dep, ent_index,config):


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

def getSepPro(pro_list, words, ent_index, dep,config):


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
            if front_pro in words and end_pro in words and (words.index(front_pro) < words.index(end_pro) or dep[words.index(front_pro)][2]=='HED'):
                best_pro = pro
                key_word = front_pro
                return best_pro, key_word
        front_pro = pro[:-2]
        end_pro = pro[-2:]
        #print("北极黄河站什么时候建立的",front_pro,end_pro,dep[words.index(front_pro)][2])
        if front_pro in words and end_pro in words and (words.index(front_pro) < words.index(end_pro) or dep[words.index(front_pro)][2]=='HED'):
            best_pro = pro
            key_word = front_pro
            return best_pro, key_word
        if 'alias' in key:

            alias = config[pro]['alias'].split(",")
            print("北极的代表动物是什么",alias,words)

            for a in alias:
                if a in words:
                    print("addalias", a)
                    best_pro = pro
                    key_word = a
                    return best_pro, key_word
                front_pro = a[:-2]
                end_pro = a[-2:]
                if front_pro in words and end_pro in words and (words.index(front_pro) < words.index(end_pro) or dep[words.index(front_pro)][2]=='HED'):
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

def getReasonPro(pro_list, words,ent_index,config):
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


    return None,None

def getDefaultPro(pro_list, words, pos,config):

    for pro in pro_list:
        if pro in words:
            return pro
        key = list(config[pro])
        if 'alias' in key:
            alias = config[pro]['alias'].split(",")

            for a in alias:
                if a in words:
                    print("addalias", a)
                    best_pro = pro

                    return best_pro

    r_flag = False
    v_flag = False

    if len(words)==3 or (len(words)==4 and words[3] in ["?","？"]):
        for w_index in range(len(words)):
            if pos[w_index] == 'r':
                r_flag = True
            if words[w_index] in ['是','有','在','为']:
                v_flag = True
    if r_flag and v_flag:

        return pro_list[0]
"""


