
import numpy as np
import jieba
import urllib.parse


from backend.data.data_process import read_file
from backend.nlu.LTPUtil import LTPUtil
from backend.graphSearch.graphSearch import graphSearch
from backend.dealNLU.compareNLU import compareNLU
from backend.dealNLU.calculateNLU import calculateNLU
import configparser

config = configparser.ConfigParser()
config.read("../backend/config.ini")
subject = config['DEFAULT']['subject']

class parsehWords(object):
    """
    """

    def __init__(self):
        """
        匹配类的初始化
        1. 从文件读取出图谱中的实体和属性
        2. 属性需要进一步出去，分离出图谱属性，统配属性，属性别称
        3. 实体个属性都按照长度排序
        4. 设定停用词和过滤符号

        """
        self.ltp_util = LTPUtil()
        self.compare_util = compareNLU()
        self.calculate_util = calculateNLU()
        self.graph_util = graphSearch()


        self.syntaxMatch = {'task_whether': [['是不是'], ['是', '吗'], ['有没有'], ['有', '吗'], ['是否'], ['是否是'],['会','吗']]}

        self.instanceArray = list(set(read_file(project_path + "/backend/data/allentity.csv")))
        self.instanceArray = sorted(self.instanceArray, key=lambda i: len(i), reverse=True)


        self.typeArray = list(set(read_file(project_path + "/backend/data/etype.csv")))
        self.typeArray = sorted(self.typeArray, key=lambda i: len(i), reverse=True)

        proArray = read_file(project_path + "/backend/data/cleanpro.csv")
        self.standardPro = sorted(proArray, key=lambda i: len(i), reverse=True)

        relArray = read_file(project_path + "/backend/data/cleanrel.csv")
        self.relArray = sorted(relArray, key=lambda i: len(i), reverse=True)


        self.template_ent = {'国家':'日本','湖泊':'洞庭湖','河流':'长江'}

        self.commonPro = []
        self.aliasArray = {}

        jieba.load_userdict(self.instanceArray)
        jieba.load_userdict(self.standardPro)
        jieba.load_userdict(self.relArray)


    def judgeSub(self, sub, ori_list):
        """
        :param sub: 被判断对象
        :param ori_list: 判断数组
        :return:
        """


        for ori in ori_list:

            if sub in ori:
                return True
        return False

    def cutWords(self,words):

        return list(jieba.cut(words))

    def dealWithLastSentence(self,words,last_sentence):
        sentence_array = last_sentence[0].split("最")
        ans = ""
        for pro in self.standardPro:
            if pro in words:
                ans += (sentence_array[0]+pro+"最"+sentence_array[1])
                return ans
        return words

    def classify(self,words,last_sentence):

        """
        得到句子的类型，不同类型的句子进行初步整理
        :param words:
        :return:
        对于是否问题，第一个返回值是问句类型，第二个返回值是问句本体，第三个值是问的实体
        对于比较问题，第一个返回值是问句类型，第二个值是模版匹配结果，第三个返回值是抽取的句子信息
            比较问题中如果返回的是反问句，那么匹配结果就是实际操作对象，也就是作用是正常比较问句的抽取信息，第三个值是反问标识
        """
        #目前暂时不再处理计算问题和比较问题
        if len(last_sentence)>0:
            words = self.dealWithLastSentence(words,last_sentence)


        compare_type,compare_inf,match_result = self.compare_util.checkCompare(words)

        if compare_type is not None:
            if compare_inf == 'task_compare_ask':
                return compare_type,match_result,compare_inf

            return compare_type,match_result,compare_inf

        calculate_type,calculate_inf,match_result = self.calculate_util.checkCalculateMost(words)
        if calculate_type is not None:
            if calculate_inf == 'task_calculate_ask':
                return calculate_type,match_result,calculate_inf


            return calculate_type,match_result,calculate_inf

        calculate_type, calculate_inf, match_result = self.calculate_util.checkCalculateDist(words)

        if calculate_type is not None:
            if calculate_inf == 'task_calculate_ask':
                return calculate_type, match_result, calculate_inf
            #print("任务类型: ", compare_type)
            #print("问题类型: ", match_result)
            #print("询问对象: ", calculate_inf)
            #print("===========================================")

            return calculate_type, match_result, calculate_inf


        return "task_normal",None,None

    def formAsking(self,words):
        """
        words_type, ask_ent, ask_words = self.classify(words)

        if words_type == 'task_compare':
            return ask_words,ask_ent,words_type
        elif words_type == 'task_normal':
            ask_words = words
        elif words_type == 'task_whether':
        """
        wether = False
        for pattern in self.syntaxMatch['task_whether']:
            count = 0
            for word in pattern:

                if word in words:
                    count = count+1
                if count == len(pattern):
                    pattern_array = words.split(pattern[0])
                    if len(pattern)>1:
                        ask_words = pattern_array[1][:-1]
                        ask_ent = pattern_array[0]
                    else:
                        ask_words = pattern_array[1]
                        ask_ent = pattern_array[0]
                    wether = True
        if wether is False:
            return None,None
        father_list = self.graph_util.getFather(ask_ent)
        father_list = sorted(father_list, key=lambda i: len(i), reverse=True)

        exist = False
        for father in father_list:
            if father in ask_words:
                exist = True
                break
        if exist == False:
            ask_words = ask_words + "的" + father_list[0] + "是什么"
        ask_words = self.checkR(ask_words)
        return ask_words,ask_ent

    def checkR(self,words):
        cut_words = list(jieba.cut(words))
        tlp_pattern, arcs_dict,reverse_arcs_dict,postags, hed_index = self.ltp_util.get_sentence_pattern(cut_words)
        postags = list(postags)

        if 'r' not in postags:
            words += "是什么"
            return words
        return words

    def aliasChange(self,cutwords):
        entity = []
        for word in cutwords:
            if word in self.instanceArray:
                entity.append(word)
        for ent in entity:
            pro_list = self.graph_util.getProList(ent)

            for pro in pro_list:
                if pro in self.aliasArray.keys():
                    for alias in self.aliasArray[pro]:
                        if alias in cutwords:
                            cutwords[cutwords.index(alias)] = pro
            return cutwords

        return cutwords


    def wordBywordAndCheck(self, cut_words,arcs_dict,reverse_arcs_dict,postags,hed_index):
        """
        1.分词
        2.得到图谱中的实体和属性，并标记下标，生成模版
        :param words: 句子
        :return: 抽取的实体，属性，关系
        """

        find_common_pro = []
        find_pro = []
        find_entity = []
        pro_index = {}
        com_index = {}
        ins_index = {}
        coo = []
        coo_index = []
        print(self.instanceArray)
        print(cut_words)


        words_mark = np.zeros(len(cut_words)) #每个分词的标记

        for c_index in range(len(cut_words)):

            cw = cut_words[c_index]
            if cw in self.instanceArray:
                if self.judgeSub(cw,find_entity):
                    continue
                if 'COO' in reverse_arcs_dict[c_index].keys():
                    coo.append(cut_words[c_index])
                    coo_index.append(c_index)
                    continue
                if cw in self.typeArray:
                    words_mark[c_index]=6
                else:
                    words_mark[c_index]=1
                ins_index[cw]=c_index
                find_entity.append(cw)

            if cw in self.standardPro:
                if self.judgeSub(cw,find_pro):
                    continue
                if words_mark[c_index] ==1 :
                    words_mark[c_index]=3
                    find_pro.append(cw)
                    pro_index[cw]=c_index
                elif words_mark[c_index]==6:
                    words_mark[c_index]=7
                    find_pro.append(cw)
                    pro_index[cw] = c_index
                elif words_mark[c_index]==0:
                    words_mark[c_index]=2
                    find_pro.append(cw)
                    pro_index[cw] = c_index

            if cw in self.relArray:
                if self.judgeSub(cw,find_pro):
                    continue
                if words_mark[c_index]>0:
                    continue
                else:
                    words_mark[c_index]=5
                    find_pro.append(cw)
                    pro_index[cw] = c_index
            if words_mark[c_index]>0:
                continue

            if cw in self.commonPro:
                if self.judgeSub(cw,find_pro):
                    continue
                if self.judgeSub(cw,find_common_pro):
                    continue
                find_common_pro.append(cw)
                com_index[cw]=c_index
                words_mark[c_index] = 4

        """
        形成模版
        """
        print("word_mark",words_mark)
        pattern_normal = ""
        pattern_pro = ""
        pattern_type = ""
        index = 0

        for wm in words_mark:
            if index >= len(postags):
                break

            if wm == 0:
                if postags[index] == 'r':
                    pattern_normal += 'R-'
                    pattern_pro += 'R-'
                    pattern_type += 'R-'


                elif index == hed_index and (postags[hed_index]=='v' or postags[hed_index]=='p'):
                    pattern_normal += 'V-'
                    pattern_pro += 'V-'
                    pattern_type += 'V-'

                else:
                    pattern_normal += cut_words[index]
                    pattern_pro += cut_words[index]
                    pattern_type += cut_words[index]
                    pattern_normal += '-'
                    pattern_pro += '-'
                    pattern_type += '-'
            if wm == 1:
                pattern_normal += 'ent-'
                pattern_pro += 'ent-'
                pattern_type += 'ent-'
            if wm == 2:
                if index == hed_index:
                    pattern_normal += 'hed&pro-'
                    pattern_pro += 'hed&pro-'
                    pattern_type += 'hed&pro-'
                else:
                    pattern_normal += 'pro-'
                    pattern_pro += 'pro-'
                    pattern_type += 'pro-'
            if wm == 3:
                pattern_normal += 'ent-'
                pattern_pro += 'pro-'
                pattern_type += 'ent-'
            """
            if wm == 4:
                pattern += "com"
                pattern += "-"
            """
            if wm == 5:
                if index == hed_index:
                    pattern_normal += 'hed&rel-'
                    pattern_pro += 'hed&rel-'
                    pattern_type += 'hed&rel-'
                else:
                    pattern_normal += 'rel-'
                    pattern_pro += 'rel-'
                    pattern_type += 'rel-'
            if wm == 6:
                pattern_normal += 'ent-'
                pattern_pro += 'ent-'
                pattern_type += 'type-'
            if wm == 7:
                pattern_normal += 'ent-'
                pattern_pro += 'pro-'
                pattern_type += 'type-'
            index = index+1

        if pattern_normal[len(pattern_normal)-1] == '-':
            pattern_normal = pattern_normal[:len(pattern_normal)-1]
        if pattern_pro[len(pattern_normal)-1] == '-':
            pattern_pro = pattern_pro[:len(pattern_normal)-1]
        if pattern_type[len(pattern_normal)-1] == '-':
            pattern_type = pattern_type[:len(pattern_normal)-1]



        form_pattern = []


        sub_pattern, sub_index = self.formPattern(pattern_type)
        form_pattern.append(sub_pattern)
        pattern_index = sub_index

        sub_pattern, sub_index = self.formPattern(pattern_normal)
        form_pattern.append(sub_pattern)


        sub_pattern,sub_index = self.formPattern(pattern_pro)
        form_pattern.append(sub_pattern)

        return form_pattern,pattern_index,coo,coo_index

    def formPattern(self,pattern):
        form_pattern = ""
        pattern_index = []
        index = 0
        for p in pattern.split("-"):

            if p in ['R', 'ent', 'hed&pro', 'hed&rel', 'rel', 'pro','V','type']:
                form_pattern += p
                pattern_index.append(index)
                form_pattern += '-'
            index = index + 1

        if form_pattern[-1] == '-':
            form_pattern = form_pattern[:-1]


        return form_pattern, pattern_index

    def unifyProCon(self,att_entity,con):
        for a in att_entity:
            if a in self.synonymy.keys():
                for a_s in self.synonymy[a]:
                    if a_s in con:
                        con = con.replace(a_s,a)
        return con


    def getWordsPattern(self, cut_words):
        """
        :param words: 问句
        :return:
        """
        #cut_words = list(jieba.cut(words))

        tlp_pattern, arcs_dict, reverse_arcs_dict, postags, hed_index = self.ltp_util.get_sentence_pattern(cut_words)
        postags = list(postags)

        print("========================================================")
        print("分词: ", cut_words)


        pattern,pattern_index,coo,coo_index = self.wordBywordAndCheck(
            cut_words,arcs_dict,reverse_arcs_dict,postags,hed_index)
        print("得到的句子模版: ", pattern)
        print("模版中的元素在句子中的下标",pattern_index)
        #print("抽取的实体: ", find_entity, "\t实体及其在句子中的下标: ", entity_index)
        #print("抽取的属性或关系: ", find_pro, "\t属性及其在句子中的下标: ", pro_index)
        print("句法依存树: ", arcs_dict, hed_index)
        print("反向依存句法树:", reverse_arcs_dict)
        print("句法依存模版: ", tlp_pattern)
        print("词性分析: ", postags)

        return pattern,pattern_index,coo,coo_index,arcs_dict,reverse_arcs_dict,postags,hed_index

    def wordBywordAndCheckForARC(self, cut_words, arcs_dict, reverse_arcs_dict, postags, hed_index):
        """
        1.分词
        2.得到图谱中的实体和属性，并标记下标，生成模版
        :param words: 句子
        :return: 抽取的实体，属性，关系
        """

        find_common_pro = []
        find_pro = []
        find_entity = []
        pro_index = {}
        com_index = {}
        ins_index = {}
        coo = []
        coo_index = []

        words_mark = np.zeros(len(cut_words))  # 每个分词的标记

        for c_index in range(len(cut_words)):

            cw = cut_words[c_index]
            if cw in self.instanceArray:
                if self.judgeSub(cw, find_entity):
                    continue
                if 'COO' in reverse_arcs_dict[c_index].keys():
                    coo.append(cut_words[c_index])
                    coo_index.append(c_index)
                    continue

                words_mark[c_index] = 1
                ins_index[cw] = c_index
                find_entity.append(cw)

            if cw in self.standardPro:
                if self.judgeSub(cw, find_pro):
                    continue
                if words_mark[c_index] == 1:
                    words_mark[c_index] = 3
                    find_pro.append(cw)
                    pro_index[cw] = c_index
                elif words_mark[c_index] > 0:
                    continue
                else:
                    words_mark[c_index] = 2
                    find_pro.append(cw)
                    pro_index[cw] = c_index

            if cw in self.relArray:
                if self.judgeSub(cw, find_pro):
                    continue
                if words_mark[c_index] > 0:
                    continue
                else:
                    words_mark[c_index] = 5
                    find_pro.append(cw)
                    pro_index[cw] = c_index
            if words_mark[c_index] > 0:
                continue

            if cw in self.commonPro:
                if self.judgeSub(cw, find_pro):
                    continue
                if self.judgeSub(cw, find_common_pro):
                    continue
                find_common_pro.append(cw)
                com_index[cw] = c_index
                words_mark[c_index] = 4

        """
        形成模版
        """
        pattern = ""
        index = 0

        for wm in words_mark:

            if wm == 0:
                if postags[index] == 'r':
                    pattern += 'R'
                    pattern += "-"
                elif index == hed_index and (postags[hed_index] == 'v' or postags[hed_index] == 'p'):
                    pattern += "V"
                    pattern += "-"
                else:
                    pattern += cut_words[index]
                    pattern += "-"
            if wm == 1:
                pattern += "ent"
                pattern += "-"
            if wm == 2:
                if index == hed_index:
                    pattern += "hed&pro"
                else:
                    pattern += "pro"
                pattern += "-"
            if wm == 3:
                pattern += "ent&pro"

                pattern += "-"
            if wm == 4:
                pattern += "com"
                pattern += "-"
            if wm == 5:
                if index == hed_index:
                    pattern += "hed&rel"
                else:
                    pattern += "rel"
                pattern += "-"
            index = index + 1
        if pattern[-1] == '-':
            pattern = pattern[:-1]

        form_pattern = ""
        pattern_index = []
        index = 0
        for p in pattern.split("-"):

            if p in ['R', 'ent', 'hed&pro', 'hed&rel', 'rel', 'pro', 'ent&pro', 'V']:
                form_pattern += p
                pattern_index.append(index)
                form_pattern += '-'
            index = index + 1

        if form_pattern[-1] == '-':
            form_pattern = form_pattern[:-1]

        return form_pattern, pattern_index, find_entity, find_pro, ins_index, pro_index,coo, coo_index

    def getWordsPatternForARC(self, cut_words):
        """
        :param words: 问句
        :return:
        """
        #cut_words = list(jieba.cut(words))


        tlp_pattern, arcs_dict, reverse_arcs_dict, postags, hed_index = self.ltp_util.get_sentence_pattern(cut_words)
        postags = list(postags)
        print("========================================================")
        print("分词: ", cut_words)


        pattern, pattern_index, find_entity, find_pro,entity_index,pro_index,coo, coo_index = self.wordBywordAndCheckForARC(
            cut_words,arcs_dict,reverse_arcs_dict,postags,hed_index)
        print("得到的句子模版: ", pattern)
        print("模版中的元素在句子中的下标",pattern_index)
        print("抽取的实体: ", find_entity, "\t实体及其在句子中的下标: ", entity_index)
        print("抽取的属性或关系: ", find_pro, "\t属性及其在句子中的下标: ", pro_index)
        print("句法依存树: ", arcs_dict, hed_index)
        print("反向依存句法树:", reverse_arcs_dict)
        print("句法依存模版: ", tlp_pattern)
        print("词性分析: ", postags)

        return pattern,pattern_index,coo,coo_index,arcs_dict,reverse_arcs_dict,postags,hed_index,find_entity, find_pro
    def getEnt(self,cut_words):
        """
        根据用户抽取实体，得到模版问句，和询问的实体类型
        :param words: 用户问句
        :return:
        """
        ent = ""
        template_word = ""

        father = ""

        for word in cut_words:

            if word in self.instanceArray:

                ent = word
                father = self.graph_util.getFather(ent)[0]
                print(father,self.template_ent[father])
                cut_words[cut_words.index(word)] = self.template_ent[father]
                template_word = "".join(cut_words)
                break

        return ent,father,template_word

    def getTemplateEnt(self,father):
        return self.template_ent[father]
    def getStandard(self,words,father):
        """
        匹配模版库，得到标准问句
        :param words:
        :param type:
        :return:
        """

        template_questions = list(read_file(project_path + "/backend/template_library/"+subject+"/"+father+".csv"))

        template_arr = []
        for template in template_questions:

            if template != "==========":
                template_arr.append(template)
            else:
                if words in template_arr:
                    return template_arr[0]
                else:
                    template_arr = []


if __name__ == '__main__':
    a = matchWords()
    #ans = a.dealWithAsking("中国最大的淡水湖是鄱阳湖吗")
    #print(ans)



    while (1):

        #print("user:")
        s = input("user: ")
        if s == '':
            continue
        #ans = a.wordBywordAndCheck(s)

        #print(list(jieba.cut(s)))
        #jieba.load_userdict(project_path + '/data/allentity.csv')
        #print(list(jieba.cut(s)))
        #ans = a.dealWithAsking(s,False)
        #ans = a.classify(s)
        #print(ans)
    








