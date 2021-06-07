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
from backend.data.data_process import read_file
from backend.nlu.LTPUtil import LTPUtil
import numpy as np
import configparser

class ConProStrict(object):
    def __init__(self):
        self.ltp_util = LTPUtil()
        config = configparser.ConfigParser()
        config.read("../backend/config.ini")
        subject = config['DEFAULT']['subject']
        self.wether_rel = (config[subject]['wether_rel'] == 'True')
        if self.wether_rel:
            config.read("../backend/data/" + subject + "/relconfig.ini")
            self.rel_config = config
            print("self.rel_config", self.rel_config)
        config.read("../backend/data/" + subject + "/proconfig.ini")
        self.pro_config = config
        self.graph_util = graphSearch()

        etype = list(set(read_file("../backend/data/" + subject + "/etype.csv")))
        self.typeArray = sorted(etype, key=lambda i: len(i), reverse=True)

    def checkSPNumPro(self,words,num_pro):



        for num in num_pro:
            keys = self.pro_config[num].keys()
            if num in words:

                return num,words.index(num)
            if 'alias' in keys:
                a_array = self.pro_config[num]['alias'].split(",")
                for a in a_array:
                    if a in words:

                        return num,words.index(a)
        return None,None


    def getNumpro(self, ent,words,pos):
        pro_list = self.graph_util.getProList(ent)
        num_list = self.getNumPro(pro_list)
        print(ent,num_list)
        if len(num_list)>0:
            pro,_ = self.checkNumberPro(num_list,words,pos)
            if pro:
                return pro
        return None


    def getNumPro(self, pro_list):
        numpro = []
        for pro in pro_list:
            """
            if pro not in list(self.pro_config.keys()):
                continue
            """
            if pro in ['示例', '图片', '降水位置图', '出处', '河流','湖泊',
                       '干湿状况', '天气图', '符号图', '最低值', '最高值', '分类编号', '气候']:
                continue

            if self.pro_config[pro]['type'] == 'numpro':
                numpro.append(pro)
        return numpro

    def checkVOB(self,dep,ent_index,verb_index):

        if dep[ent_index][2] == 'VOB' and dep[ent_index][1]==verb_index+1:
            return True

        if dep[ent_index][2] == 'ATT' and dep[dep[ent_index][1]-1][2]=='VOB' and  dep[dep[ent_index][1]-1][1]==verb_index+1:
            return True

        if dep[verb_index][2] == 'HED':
            return True

    def checkRelationWithR(self, words,reverse_dep,end_ent,hed_index):

        check_list = reverse_dep[hed_index]

        for cw in check_list:
            print(cw,words[cw[0]-1],end_ent)
            if (words[cw[0]-1] in end_ent or end_ent in words[cw[0]-1]) and cw[1]=='SBV':
                return True
        return False


    def checkSBV(self,dep,ent_index,verb_index):

        if dep[ent_index][2] == 'SBV' and dep[ent_index][1]==verb_index+1:
            return True

        if dep[ent_index][2] == 'ATT' and dep[dep[ent_index][1]-1][2]=='SBV' and  dep[dep[ent_index][1]-1][1]==verb_index+1:
            return True

        if dep[verb_index][2] == 'HED':
            return True

        return False

    def checkVerbRel(self, entity,check_rel,ask_type):
        flag = False

        """
        如果没有约束类型，就不做约束
        """
        if ask_type is None:
            flag = True


        rel_list = self.graph_util.getRelList(entity)
        if rel_list is None or len(rel_list)==0:
            return None,None,False
        for rel in rel_list:

            rtype = self.rel_config[rel]['type']
            if rtype != 'verbnormal':
                continue

            if 'ask_type' in self.rel_config[rel].keys() and ask_type:
                first_type = self.rel_config[rel]['ask_type'].split("|")
                for ft in first_type:
                    at_array = ft.split(",")
                    print("at_array",at_array,ask_type)
                    for at in at_array:
                        if at == ask_type:
                            ask_type = at_array[0]
                            flag = True
                            break
            else:

                ask_type = None
                flag = True

            print("===============ask_type", flag)

            if rel == check_rel:
                print("rel,ask_type", rel, ask_type)
                if flag:
                    return rel, ask_type, True
                else:
                    return rel, None, False

            if 'alias' in self.rel_config[rel].keys():
                a_list = self.rel_config[rel]['alias'].split(",")
                for a in a_list:
                    if a == check_rel:
                        print("rel,ask_type",rel,ask_type)
                        if flag:
                            return rel,ask_type, True
                        else:
                            return rel, None, False
        return None,None,False

    def checkPVerbRel(self, entity, check_rel):
        rel_list = self.graph_util.getPRelList(entity)
        if rel_list is None or len(rel_list)==0:
            return None
        for rel in rel_list:

            rtype = self.rel_config[rel]['type']

            if rtype != 'verbnormal':
                continue
            #print(rel,"asdasdasdasdasd===",check_rel)
            """
            if 'ask_type' in self.rel_config[rel].keys() and ask_type:
                first_type = self.rel_config[rel]['ask_type'].split("|")
                for ft in first_type:
                    at_array = ft.split(",")
                    print("at_array", at_array, ask_type)
                    for at in at_array:
                        if at == ask_type:
                            ask_type = at_array[0]
                            break
            """
            if rel == check_rel:
                return rel
            if 'alias' in self.rel_config[rel].keys():
                a_list = self.rel_config[rel]['alias'].split(",")
                for a in a_list:
                    if a == check_rel:
                        return rel
        return None

    def checkSBVorVOB(self,dep,ent_index,verb_index,pro_index):

        if dep[ent_index][2] == 'VOB' and dep[ent_index][1]==verb_index+1:
            return True

        if dep[ent_index][2] == 'ATT' and dep[dep[ent_index][1]-1][2]=='VOB' and  dep[dep[ent_index][1]-1][1]==verb_index+1:
            return True

        if dep[verb_index][2] == 'HED':
            return True

        if dep[ent_index][2] == 'SBV' and dep[ent_index][1]==verb_index+1:
            return True

        if dep[ent_index][2] == 'ATT' and dep[dep[ent_index][1]-1][2]=='SBV' and  dep[dep[ent_index][1]-1][1]==verb_index+1:
            return True

        if dep[verb_index][2] == 'ATT' and dep[verb_index][1] == pro_index+1:
            return True

    def getRel(self,words,dep,reverse_dep,ent, ent_index):
        rel_list = self.graph_util.getRelList(ent)
        if rel_list is None or len(rel_list)==0:
            return None,None

        nonenormal = []
        verbnormal = []
        sepverb = []
        for rel in rel_list:

            rtype = self.rel_config[rel]['type']

            if rtype == 'nonenormal':
                nonenormal.append(rel)
            #elif rtype == 'verbnormal':
            #    verbnormal.append(rel)
            elif rtype == 'sepverbrel':
                sepverb.append(rel)

        print("nonenormal",nonenormal)
        #print("verbnormal",verbnormal)
        print("sepverbrel",sepverb)

        if len(sepverb) > 0:
            best_rel, key_word = self.getSepVerbPro(sepverb, words, ent_index, dep,reverse_dep)

            if best_rel:
                print("best_rel, key_word", best_rel, key_word)
                return best_rel, key_word

        if len(verbnormal) > 0:
            best_rel, key_word = self.getVerbNormalRel(verbnormal, words,dep,ent_index)

            if best_rel:
                print("best_rel, key_word", best_rel, key_word)
                return best_rel, key_word
        if len(nonenormal)>0:
            best_rel, key_word = self.getNoneNormalRel(nonenormal, words, dep, reverse_dep)
            if best_rel:
                print("best_rel, key_word", best_rel, key_word)
                return best_rel, key_word

        return None,None



    def getpro(self, words, pos, dep, reverse_dep,ent, ent_index):

        print("getpro",ent)

        pro_list = self.graph_util.getProList(ent)

        normal = []
        sepnone = []
        sepverb = []
        seppverb = []
        sephow = []
        reason = []
        default = []

        for pro in pro_list:

            if pro in ['示例', '图片', '降水位置图', '出处', '河流','湖泊',
                       '干湿状况', '天气图', '符号图', '最低值', '最高值', '分类编号', '气候']:
                continue
            """
            print("self.pro_config.keys()",list(self.pro_config.keys()))

            if pro not in self.pro_config.keys():
                continue
            """
            if 'sepnone' in self.pro_config[pro]['type']:
                sepnone.append(pro)
            elif 'sepverb' in self.pro_config[pro]['type']:
                sepverb.append(pro)
            elif 'seppverb' in self.pro_config[pro]['type']:
                seppverb.append(pro)
            elif 'reason' in self.pro_config[pro]['type']:
                reason.append(pro)
            elif 'default' in self.pro_config[pro]['type']:
                default.append(pro)
            elif 'sephow' in self.pro_config[pro]['type']:
                sephow.append(pro)
            elif self.pro_config[pro]['type'] != 'numpro':
                normal.append(pro)

        print("normal:", normal)
        print("sepnone:", sepnone)
        print("sepverb:", sepverb)
        print("seppverb:", seppverb)
        print("sephow:", sephow)
        print("reason:", reason)
        print("default:", default)
        if len(reason) > 0:
            best_pro, key_word = self.getReasonPro(reason, words, dep,reverse_dep, ent_index)
            print(best_pro, key_word)
            if best_pro:
                return best_pro, key_word
        if len(sepnone) > 0:
            best_pro, key_word = self.getSepNonePro(sepnone, words, ent_index, dep,reverse_dep)
            print(best_pro, key_word)
            if best_pro:
                return best_pro, key_word
        if len(sepverb) > 0:
            best_pro, key_word = self.getSepVerbPro(sepverb, words, ent_index, dep,reverse_dep)
            print(best_pro, key_word)
            if best_pro:
                return best_pro, key_word
        if len(seppverb) > 0:
            best_pro, key_word = self.getSepPVerbPro(seppverb, words, ent_index, dep,reverse_dep)
            print(best_pro, key_word)
            if best_pro:
                return best_pro, key_word
        if len(sephow) > 0:
            best_pro, key_word = self.getSepHowPro(sephow, words, ent_index, dep, reverse_dep)
            print(best_pro, key_word)
            if best_pro:
                return best_pro, key_word
        if len(normal) > 0:
            best_pro, key_word = self.getNormalPro(normal, words, pos, dep, reverse_dep,ent_index)
            print(best_pro, key_word)
            if best_pro:
                return best_pro, key_word
        if len(default) > 0:
            best_pro = self.getDefaultPro(default, words, pos, dep, reverse_dep,ent)
            if best_pro:
                return best_pro, words[ent_index]

        return None, None

    def checkNumberPro(self,pro_list,words,pos):

        for pro in pro_list:
            key = list(self.pro_config[pro])
            if pro in words and ('多少' in words or '几' in "".join(words)):
            #if pro in words and self.checkAskingPro(words,dep,reverse_dep,pro):
                print("addpro", pro)
                return pro,pro


            if 'alias' in key:
                alias = self.pro_config[pro]['alias'].split(",")

                for a in alias :
                    if a in words and ('多少' in words or '几' in "".join(words)):
                        return pro,a
        for pro in pro_list:
            print(pro,words,"？===========================================")
            key = list(self.pro_config[pro])
            print(key)
            if 'unit' in key:
                none = self.pro_config[pro]['unit'].split(",")
                for a in none:
                    #print(words,words.index(a),len(pos),"words.index(a) ")
                    if (a in words and pos[words.index(a) - 1] == 'r') or ("几"+a in "".join(words)):
                        print("addnoun", a)
                        return pro,a

            if 'adj' in key:
                adj = self.pro_config[pro]['adj'].split(",")
                for a in adj:
                    if (a in words and words[words.index(a) - 1] == '多') or ('多'+a in words):
                        return pro, a
        return None,None

    def checkNumberProForCompare(self,pro_list,words,pos):
        for pro in pro_list:
            key = list(self.pro_config[pro])
            if pro in words:

                if 'adj' in key:
                    adj_array = self.pro_config[pro]['adj'].split(",")
                    if '更'+adj_array[0] in "".join(words):
                        return pro,adj_array[0],"positive"
                    if '更'+adj_array[1] in "".join(words):
                        return pro,adj_array[1],"negative"
                    if '较'+adj_array[0] in "".join(words):
                        return pro,adj_array[0],"positive"
                    if '较'+adj_array[1] in "".join(words):
                        return pro,adj_array[1],"negative"
                    if pro+adj_array[0] in "".join(words):
                        return pro,adj_array[0],"positive"
                    if pro+adj_array[1] in "".join(words):
                        return pro,adj_array[1],"negative"

            if 'alias' in key:
                alias = self.pro_config[pro]['alias'].split(",")

                for a in alias:
                    if a in words:
                        if 'adj' in key:
                            adj_array = self.pro_config[pro]['adj'].split(",")
                            if '更' + adj_array[0] in "".join(words):
                                return pro, adj_array[0], "positive"
                            if '更' + adj_array[1] in "".join(words):
                                return pro, adj_array[1], "negative"
                            if '较' + adj_array[0] in "".join(words):
                                return pro, adj_array[0], "positive"
                            if '较' + adj_array[1] in words:
                                return pro, adj_array[1], "negative"
                            if a + adj_array[0] in "".join(words):
                                return pro, adj_array[0], "positive"
                            if a + adj_array[1] in "".join(words):
                                return pro, adj_array[1], "negative"

            if 'adj' in key:
                adj_array = self.pro_config[pro]['adj'].split(",")
                print(pro,adj_array)

                if '更' + adj_array[0] in "".join(words):
                    return pro, adj_array[0], "positive"
                if '更' + adj_array[1] in "".join(words):
                    return pro, adj_array[1], "negative"
                if '较' + adj_array[0] in "".join(words):
                    return pro, adj_array[0], "positive"
                if '较' + adj_array[1] in "".join(words):
                    return pro, adj_array[1], "negative"

                if adj_array[0] in words and pos[words.index(adj_array[0])-1]=='r':
                    return pro,adj_array[0], "positive"
                if len(adj_array) == 2 and adj_array[1] in words and pos[words.index(adj_array[1])-1]=='r':
                    return pro, adj_array[1], "negative"


        return None,None,None

    def getNormalPro(self,pro_list, words, pos, dep, reverse_dep,ent_index):

        best_pro = []
        key_word = []
        pro_index = []
        numpro = []

        for pro in pro_list:
            print(pro)

            key = list(self.pro_config[pro])
            if pro in words and self.checkAskingPro(words,dep,reverse_dep,pro):
                print("addpro", pro)
                best_pro.append(pro)
                key_word.append(pro)
                pro_index.append(words.index(pro))
                #break

            if "主要" in pro:
                main_pro = pro.replace("主要", "")
                if main_pro in words and self.checkAskingPro(words,dep,reverse_dep,main_pro):
                    best_pro.append(pro)
                    key_word.append(main_pro)
                    pro_index.append(words.index(main_pro))
                    #break

            if "split_alias" in key:
                split_alias = self.pro_config[pro]['split_alias'].split(",")
                alias_index = self.pro_config[pro]['alias_index'].split(",")
                print(split_alias)
                print(alias_index)
                for a_index in range(len(split_alias)):
                    sa = split_alias[a_index]
                    sa_first = sa[:int(alias_index[a_index])]
                    sa_end = sa[int(alias_index[a_index]):]
                    if sa_first in words and sa_end in words:

                        begin_index = words.index(sa_first)+1
                        end_index = words.index(sa_end)
                        print(sa_first, begin_index,sa_end,end_index)
                        flag = False
                        for i in range(begin_index,end_index):
                            print("i",i,begin_index,end_index)
                            if pos[i] == 'r':
                                flag = True
                                break
                        if flag:
                            best_pro.append(pro)
                            key_word.append(sa_end)
                            pro_index.append(words.index(sa_end))
                            break

            if 'alias' in key:
                alias = self.pro_config[pro]['alias'].split(",")
                for a in alias:
                    if a in words and self.checkAskingPro(words,dep,reverse_dep,a):
                        best_pro.append(pro)
                        key_word.append(a)
                        pro_index.append(words.index(a))
                        #break

            if 'r_alias' in key:
                alias = self.pro_config[pro]['r_alias'].split(",")
                for a in alias:
                    if a in words:
                        best_pro.append(pro)
                        key_word.append(a)
                        pro_index.append(words.index(a))
                        #break


            if 'verb' in key:
                verb = self.pro_config[pro]['verb'].split(",")

                for a in verb:

                    if a in words and self.checkSBV(dep,ent_index,words.index(a)):

                        if 'verb_limit' in key:
                            verb_limit_list = self.pro_config[pro]['verb_limit'].split(",")
                            for vl in verb_limit_list:
                                if vl in words and pos[words.index(vl)-1]=='r':
                                    best_pro.append(pro)
                                    key_word.append(a)
                                    pro_index.append(words.index(a))
                                    break
                                elif vl=='none' and pos[-1]=='r':
                                    best_pro.append(pro)
                                    key_word.append(a)
                                    pro_index.append(words.index(a))
                                    break
                        else:
                            best_pro.append(pro)
                            key_word.append(a)
                            pro_index.append(words.index(a))
                            #break

            if 'passive_verb' in key:
                verb = self.pro_config[pro]['passive_verb'].split(",")

                for a in verb:

                    if a in words and self.checkVOB(dep,ent_index,words.index(a)):
                        print("addpassive_verb", a)
                        best_pro.append(pro)
                        key_word.append(a)
                        pro_index.append(words.index(a))
                        continue

            if self.pro_config[pro]['type'] == "numpro":
                numpro.append(pro)

        print("best_pro",best_pro)

        if len(best_pro) == 1:
            return best_pro[0], key_word[0]

        elif len(best_pro) > 1:
            count = []
            for i in range(len(best_pro)):
                if dep[pro_index[i]][2] == 'HED':
                    count.append(4)
                elif dep[pro_index[i]][2] == 'VOB' and dep[dep[pro_index[i]][1] - 1][2] == 'HED':
                    if words[pro_index[i]] == '特征':
                        count.append(1)
                    else:
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

    def getSepVerbPro(self,pro_list, words, ent_index, dep,reverse_dep):

        for pro in pro_list:
            key = list(self.pro_config[pro])
            if pro in words and self.checkAskingPro(words,dep,reverse_dep,pro):
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
                if front_pro in words and end_pro in words and self.checkSBV(dep,ent_index,words.index(front_pro)) and self.checkAskingPro(words,dep,reverse_dep,end_pro):

                    best_pro = pro
                    key_word = front_pro
                    return best_pro, key_word
            front_pro = pro[:-2]
            end_pro = pro[-2:]
            if front_pro in words and end_pro in words and self.checkSBV(dep,ent_index,words.index(front_pro)) and self.checkAskingPro(words,dep,reverse_dep,end_pro):
                best_pro = pro
                key_word = front_pro
                return best_pro, key_word
            if 'alias' in key:

                alias = self.pro_config[pro]['alias'].split(",")

                count = 0
                for a in alias:
                    if a in words and self.checkAskingPro(words,dep,reverse_dep,a):
                        print("addalias", a)
                        best_pro = pro
                        key_word = a
                        return best_pro, key_word
                    if 'split_index' in key:

                        split_index = self.pro_config[pro]['split_index'].split(",")


                        front_pro = a[:int(split_index[count])]
                        end_pro = a[int(split_index[count]):]
                    else:
                        front_pro = a[:-2]
                        end_pro = a[-2:]
                    print(front_pro,end_pro)
                    count = count+1

                    if front_pro in words and end_pro in words and self.checkSBV(dep,ent_index,words.index(front_pro))  and self.checkAskingPro(words,dep,reverse_dep,end_pro):
                        print("add sepverbpro alias", a)
                        best_pro = pro
                        key_word = front_pro
                        return best_pro, key_word

            if 'r_alias' in key:

                alias = self.pro_config[pro]['r_alias'].split(",")
                for a in alias:
                    front_pro = a[:2]
                    end_pro = a[2:]

                    if end_pro in words and front_pro in words and self.checkSBVorVOB(dep, ent_index, words.index(
                            front_pro),words.index(end_pro)):
                        print("add sepverbpro r_alias", a)
                        best_pro = pro
                        key_word = front_pro
                        return best_pro, key_word

            if 'verb' in key:
                verb = self.pro_config[pro]['verb'].split(",")

                for a in verb:

                    if a in words and self.checkSBV(dep,ent_index,verb_index = words.index(a)):
                        print("addverb", a)
                        best_pro = pro
                        key_word = a
                        return best_pro, key_word

            if 'passive_verb' in key:
                verb = self.pro_config[pro]['passive_verb'].split(",")
                for a in verb:
                    if a in words and self.checkVOB(dep,ent_index,verb_index = words.index(a)):
                        print("addpassive_verb", a)
                        best_pro = pro
                        key_word = a
                        return best_pro, key_word
        """
        for pro in pro_list:
            if '特征' in pro:
                continue
            if pro[-2:] in words and self.checkAskingPro(words,dep,reverse_dep,pro[-2:]):
                best_pro = pro
                key_word = pro[-2:]
                return best_pro, key_word
        """

        return None, None


    def getSepPVerbPro(self,pro_list, words, ent_index, dep,reverse_dep):

        for pro in pro_list:
            key = list(self.pro_config[pro])
            if pro in words and self.checkAskingPro(words,dep,reverse_dep,pro):
                best_pro = pro
                key_word = pro
                return best_pro, key_word

            if "主要" in pro:
                main_pro = pro.replace("主要", "")
                if main_pro in words and self.checkAskingPro(words,dep,reverse_dep,pro):
                    best_pro = pro
                    key_word = main_pro
                    return best_pro, key_word
                front_pro = main_pro[:2]
                end_pro = main_pro[2:]
                if end_pro in words and self.checkAskingPro(words,dep,reverse_dep,end_pro) and front_pro in words and self.checkSBVorVOB(dep,ent_index,words.index(front_pro)):
                    best_pro = pro
                    key_word = front_pro
                    return best_pro, key_word
            front_pro = pro[:2]
            end_pro = pro[2:]
            if end_pro in words and front_pro in words and self.checkSBVorVOB(dep,ent_index,words.index(front_pro),words.index(end_pro)) and self.checkAskingPro(words,dep,reverse_dep,end_pro) :
                best_pro = pro
                key_word = front_pro
                print("add add add")
                return best_pro, key_word
            if 'alias' in key:
                alias = self.pro_config[pro]['alias'].split(",")
                count = 0
                for a in alias:
                    if a in words  and self.checkAskingPro(words,dep,reverse_dep,a):
                        print("addalias", a)
                        best_pro = pro
                        key_word = a
                        return best_pro, key_word
                    if 'split_index' in key:
                        split_index = self.pro_config[pro]['split_index'].split(",")
                        front_pro = a[:int(split_index[count])]
                        end_pro = a[int(split_index[count]):]
                    else:
                        front_pro = a[:2]
                        end_pro = a[2:]
                    if end_pro in words and front_pro in words and self.checkSBVorVOB(dep,ent_index,words.index(front_pro),words.index(end_pro)) and self.checkAskingPro(words,dep,reverse_dep,end_pro):
                        print("add sepverbpro alias", a)
                        best_pro = pro
                        key_word = front_pro
                        return best_pro, key_word
            if 'r_alias' in key:

                alias = self.pro_config[pro]['r_alias'].split(",")
                for a in alias:

                    front_pro = a[:2]
                    end_pro = a[2:]

                    if end_pro in words and front_pro in words and self.checkSBVorVOB(dep, ent_index, words.index(
                            front_pro),words.index(end_pro)):
                        print("add sepverbpro r_alias", a)
                        best_pro = pro
                        key_word = front_pro
                        return best_pro, key_word

            if 'verb' in key:
                verb = self.pro_config[pro]['verb'].split(",")

                for a in verb:

                    if a in words and self.checkSBV(dep,ent_index,verb_index = words.index(a)):
                        print("addverb", a)
                        best_pro = pro
                        key_word = a
                        return best_pro, key_word
            if 'passive_verb' in key:
                verb = self.pro_config[pro]['passive_verb'].split(",")
                for a in verb:
                    if a in words and self.checkVOB(dep,ent_index,verb_index = words.index(a)):
                        print("addpassive_verb", a)
                        best_pro = pro
                        key_word = a
                        return best_pro, key_word


        return None, None


    def getSepHowPro(self,pro_list, words, ent_index, dep,reverse_dep):
        print("getSepHowPro================")

        for pro in pro_list:
            key = list(self.pro_config[pro])
            if pro in words and self.checkAskingPro(words,dep,reverse_dep,pro):
                best_pro = pro
                key_word = pro
                return best_pro, key_word

            end_pro = pro[:2]
            front_pro = pro[2:]
            print(end_pro,front_pro,words)


            if end_pro in words and front_pro in words and ('怎么' in words or '如何' in words):
                end_index = words.index(end_pro)
                front_index = words.index(front_pro)
                if dep[end_index][1] == front_index+1 or dep[front_index][1] == end_index+1:
                    best_pro = pro
                    key_word = front_pro
                    print("add add add")
                    return best_pro, key_word

            if 'alias' in key:
                alias = self.pro_config[pro]['alias'].split(",")
                count = 0
                for a in alias:
                    if a in words  and self.checkAskingPro(words,dep,reverse_dep,a):
                        print("addalias", a)
                        best_pro = pro
                        key_word = a
                        return best_pro, key_word
                    if 'split_index' in key:
                        split_index = self.pro_config[pro]['split_index'].split(",")

                        end_pro = a[:int(split_index[count])]
                        front_pro = a[int(split_index[count]):]
                    else:
                        end_pro = a[:2]

                        front_pro = a[2:]
                    if end_pro in words and front_pro in words and ('怎么' in words or '如何' in words):
                        end_index = words.index(end_pro)
                        front_index = words.index(front_pro)
                        if dep[end_index][1] == front_index+1 or dep[front_index][1] == end_index+1:
                            best_pro = pro
                            key_word = front_pro
                            print("add add add",a)
                            return best_pro, key_word

            if 'verb' in key:
                verb = self.pro_config[pro]['verb'].split(",")

                for a in verb:

                    if a in words and self.checkSBV(dep,ent_index,verb_index = words.index(a)):
                        print("addverb", a)
                        best_pro = pro
                        key_word = a
                        return best_pro, key_word
            if 'passive_verb' in key:
                verb = self.pro_config[pro]['passive_verb'].split(",")
                for a in verb:
                    if a in words and self.checkVOB(dep,ent_index,verb_index = words.index(a)):
                        print("addpassive_verb", a)
                        best_pro = pro
                        key_word = a
                        return best_pro, key_word

        return None, None

    def getSepNonePro(self,pro_list, words, ent_index, dep,reverse_dep):

        for pro in pro_list:
            key = list(self.pro_config[pro])
            if pro in words and self.checkAskingPro(words,dep,reverse_dep,pro):
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
                if front_pro in "".join(words) and end_pro in words and (
                        words.index(front_pro) < words.index(end_pro) or dep[words.index(front_pro)][2] == 'HED'):
                    best_pro = pro
                    key_word = front_pro
                    return best_pro, key_word
            front_pro = pro[:-2]
            end_pro = pro[-2:]
            if front_pro in "".join(words) and end_pro in words and (
                            "".join(words).index(front_pro) < "".join(words).index(end_pro) or dep[words.index(front_pro)][2] == 'HED'):
                best_pro = pro
                key_word = front_pro
                return best_pro, key_word
            if 'alias' in key:

                alias = self.pro_config[pro]['alias'].split(",")


                for a in alias:
                    if a in words:
                        print("addalias", a)
                        best_pro = pro
                        key_word = a
                        return best_pro, key_word
                    front_pro = a[:-2]
                    end_pro = a[-2:]
                    if front_pro in "".join(words) and end_pro in words and (
                                    "".join(words).index(front_pro) < "".join(words).index(end_pro) or dep[words.index(front_pro)][2] == 'HED'):
                        print("add sepverbpro alias", a)
                        best_pro = pro
                        key_word = front_pro
                        return best_pro, key_word
            if 'verb' in key:
                verb = self.pro_config[pro]['verb'].split(",")

                for a in verb:
                    if a in words and self.checkSBV(dep,ent_index,words.index(a)):
                        print("addverb", a)
                        best_pro = pro
                        key_word = a
                        return best_pro, key_word
            if 'passive_verb' in key:
                verb = self.pro_config[pro]['passive_verb'].split(",")
                for a in verb:
                    if a in words and self.checkVOB(dep,ent_index,words.index(a)):
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

    def getReasonPro(self,pro_list, words, dep, reverse_dep, ent_index):
        print("getReasonPro=====================")
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
            key = list(self.pro_config[pro])
            if 'alias' in key:
                alias = self.pro_config[pro]['alias'].split(",")

                for a in alias:
                    if a in words:
                        print("addalias", a)
                        best_pro = pro
                        key_word = a
                        return best_pro, key_word
                    front_pro = a[:-2]
                    end_pro = a[-2:]
                    print(front_pro,end_pro,"==========================")
                    if front_pro in words and end_pro in words and (self.checkAskingPro(words,dep,reverse_dep,front_pro) or self.checkAskingPro(words,dep,reverse_dep,end_pro)):
                        best_pro = pro
                        key_word = a
                        return best_pro, key_word

            if 'passive_verb' in key:
                verb = self.pro_config[pro]['passive_verb'].split(",")
                for a in verb:
                    if a in words and self.checkVOB(dep,ent_index,words.index(a)):
                        print("addpassive_verb", a)
                        best_pro = pro
                        key_word = a
                        return best_pro, key_word

        return None, None

    def getDefaultPro(self,pro_list, words, pos ,dep, reverse_dep, ent):

        print("getDefaultPro",words)

        for pro in pro_list:
            if pro in words:
                return pro
            key = list(self.pro_config[pro])
            if 'alias' in key:
                alias = self.pro_config[pro]['alias'].split(",")

                for a in alias:
                    if a in words:
                        print("addalias", a)
                        best_pro = pro
                        return best_pro

        r_flag = False
        v_flag = False

        if len(words) == 3 or  (len(words) == 4 and (words[3] in ["?", "？"] or words[3] not in self.typeArray)):

            for w_index in range(len(words)):
                if words[w_index] in ['什么','何','哪些','如何']:
                    r_flag = True
                if words[w_index] in ['是', '有', '在', '为', '包括' , '含', '含有','涵盖']:
                    v_flag = True
        if r_flag and v_flag:
            return pro_list[0]

        end_ent = self.ltp_util.get_normal_seg(ent)[-1]

        if ent not in words:
            r_arr = ['什么', '何', '哪些', '多少', '哪', '哪里', '为什么', '为何', '哪个', "什么样", '哪样', '何样', '如何']
            for r_word in r_arr:
                if r_word in words:
                    r_index = words.index(r_word)
                    if dep[r_index][2]=='VOB':
                        hed_index = dep[r_index][1]
                        if self.checkRelationWithR(words,reverse_dep,end_ent,hed_index):
                            return pro_list[0]
                    #if dep[r_index][2] ==
                    if dep[r_index][2] in ['ATT','ADV'] and (words[dep[r_index][1]-1] in end_ent or end_ent in words[dep[r_index][1]-1]):
                        return pro_list[0]


        return None

        #if ent not in words:
        #    r_arr = ['什么', '何', '哪些']

    def checkAskingPro(self,words,dep,reverse_dep, check_pro):
        print("checkAskingPro====================")
        print(reverse_dep)
        print(dep)
        print(check_pro)
        print("========================================")
        flag = False
        r_arr = ['什么', '何', '哪些','多少','哪','哪里','为什么','为何','哪个',"什么样",'哪样','何样','如何','怎么']
        pro_index = words.index(check_pro)
        print(pro_index,dep[pro_index][2])
        print("========================================")

        for r_word in r_arr:

            if r_word in words:
                flag = False
                r_index = words.index(r_word)

                if dep[r_index][1] == pro_index+1 or dep[pro_index][1] == r_index+1:
                    return True


                if dep[r_index][2] in ['VOB','POB','FOB']:
                    hed_index = dep[r_index][1]

                    check_list = reverse_dep[hed_index]
                    for cw in check_list:
                        if words[cw[0]-1] == check_pro and cw[1]=='SBV':
                            print("=======================================1")
                            return True
                    """
                    疑问代词两跳之后和属性指向一个地方
                    """
                    temp_index = dep[r_index][1]
                    pro_index = words.index(check_pro)
                    if dep[temp_index-1][1] == dep[pro_index][1]:
                        print("=======================================2")
                        return True


                elif dep[r_index][2] == 'ATT':

                    if words[dep[r_index][1]-1] == check_pro:
                        print("=======================================3")
                        return True

                    if dep[dep[r_index][1]-1][2] in ['VOB','POB','FOB']:

                        vob_index = dep[r_index][1]-1
                        hed_index = dep[vob_index][1]
                        check_list = reverse_dep[hed_index]
                        print(check_list,dep[hed_index-1])
                        for cw in check_list:
                            if words[cw[0] - 1] == check_pro and cw[1] == 'SBV':
                                return True
                    if dep[dep[r_index][1]-1][2] == 'ATT':

                        check_index = dep[r_index][1]-1
                        while(dep[check_index][2]=='ATT'):
                            next_index = dep[check_index][1]-1
                            if words[next_index] == check_pro:
                                return True
                            check_index = next_index

                    if dep[pro_index][2] == 'ATT':
                        c_i = pro_index
                        while (dep[c_i][2] == 'ATT'):
                            print(words[dep[c_i][1] - 1])
                            if c_i == r_index:
                                return True
                            if dep[dep[c_i][1] - 1][2] in ['VOB','FOB','POB'] and dep[r_index][1]==dep[c_i][1]:
                                return True
                            c_i = dep[c_i][1] - 1

        if flag:
            return True
        return False

    def getVerbNormalRel(self,pro_list, words, dep,ent_index):

        best_pro = []
        key_word = []
        pro_index = []


        for pro in pro_list:
            print(pro)
            key = list(self.pro_config[pro])
            if pro in words and self.checkSBV(dep,ent_index,words.index(pro)):
                print("addpro", pro)
                best_pro.append(pro)
                key_word.append(pro)
                pro_index.append(words.index(pro))
                break


            if 'alias' in key:
                alias = self.pro_config[pro]['alias'].split(",")
                for a in alias:
                    if a in words and self.checkSBV(dep,ent_index,words.index(a)):
                        best_pro.append(pro)
                        key_word.append(a)
                        pro_index.append(words.index(a))
                        break

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


    def getNoneNormalRel(self,pro_list, words, dep,reverse_dep):

        best_pro = []
        key_word = []
        pro_index = []


        for pro in pro_list:
            print(pro)

            key = list(self.pro_config[pro])
            if pro in words and self.checkAskingPro(words,dep,reverse_dep, pro):
                print("addpro", pro)
                best_pro.append(pro)
                key_word.append(pro)
                pro_index.append(words.index(pro))
                break


            if 'alias' in key:
                alias = self.pro_config[pro]['alias'].split(",")
                for a in alias:
                    if a in words and self.checkAskingPro(words,dep,reverse_dep, pro):
                        best_pro.append(pro)
                        key_word.append(a)
                        pro_index.append(words.index(a))
                        break

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
