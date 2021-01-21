# @Language: python3
# @File  : processNLU.py
# @Author: LinXiaofei
# @Date  : 2020-04-27
"""
nlu总控，负责问句理解
PatternMatch 得到问句模版，包括句法结构，词性分析
parsehWords 解析句子
formWords 得到句子的标准形式
"""



from backend.nlu.matchWords import parsehWords
from backend.nlu.analysisPattern import PatternMatch
import configparser
import numpy as np

config = configparser.ConfigParser()
config.read("../backend/config.ini")
subject = config['DEFAULT']['subject']

class processNLU(object):
    def __init__(self):
        self.words_util = parsehWords()
        self.pattern_util = PatternMatch()

        self.task_sort = ['task_son_kw_match','task_normal_pro','task_normal_rel','task_son_match','task_limit_sub','task_singal_entity']


    def process(self,words,last_sentence):
        """
        问句有不同的类型，不同的类型有不同的处理方式来达到对问句的理解

        该函数是自然语言理解的总控函数
        :param words:
        :return: 不同类型的问句统一的抽象形式，即抽取实体、属性/关系
        """

        ask_words, entity_array, coo, coo_index, property_array, keywords_array, task_type_array, ask_ent = self.dealWithNormal(
            words)

        ans_dict = {'ask_words': ask_words, 'entity_array': entity_array, 'coo': coo, 'coo_index': coo_index,
                    'property_array': property_array, 'keywords_array': keywords_array,
                    'task_type_array': task_type_array,  'ask_ent': ask_ent}
        return ans_dict


    def dealWithNormal(self,ask_words):
        """
        处理普通类型的问句，通过抽象出实体、属性/关系、疑问代词和谓语来匹配模版，模版的匹配涉及到句法依存、词性分析
        :param words: 问句
        :return:处理后的句子信息
        """

        cut_words = self.words_util.cutWords(ask_words)
        ask_ent, father, template_word = self.words_util.getEnt(cut_words)
        stander_words = self.words_util.getStandard(template_word,father)
        cut_words = self.words_util.cutWords(stander_words)
        cut_words[cut_words.index(self.words_util.getTemplateEnt(father))] = ask_ent
        pattern, pattern_index, coo, coo_index, arcs_dict, reverse_arcs_dict, postags, hed_index = self.words_util.getWordsPattern(
            cut_words)
        entity_array_temp = []
        property_array_temp = []
        keywords_array_temp = []
        task_type_array_temp = []
        task_num = []
        for p in pattern:
            entity, property, keywords, task_type = self.pattern_util.matchPattern(p, pattern_index, cut_words)
            entity_array_temp.append(entity)
            property_array_temp.append(property)
            if len(keywords) > 0:
                keywords_array_temp.append(keywords)
            else:
                keywords_array_temp.append(None)
            task_type_array_temp.append(task_type)
            if task_type in self.task_sort:
                task_num.append(self.task_sort.index(task_type))
            else:
                task_num.append(6)
        sort_index = np.argsort(task_num)
        entity_array = np.array(entity_array_temp)[sort_index]
        property_array = np.array(property_array_temp)[sort_index]
        keywords_array = np.array(keywords_array_temp)[sort_index]
        task_type_array = np.array(task_type_array_temp)[sort_index]

        return ask_words, entity_array, coo, coo_index, property_array, keywords_array, task_type_array, ask_ent

    def dealWithCalculate(self,ask_type,ask_ent):
        """
        处理计算类问题
        1.最值处理 最值的信息提取直接放在了calculate_util里面
        :param ask_ent:
        :return:
        """

        if ('most' in ask_type) or ('least' in ask_type) :

            ask_ent['task_type']=ask_type
            ask_ent['words_type'] = 'task_calculate'
            return ask_ent
        if 'dist' in ask_type:
            ask_ent['task_type'] = ask_type
            ask_ent['words_type'] = 'task_calculate'
            return ask_ent


if __name__ == '__main__':
    a = processNLU()
    while(1):
        s = input("user: ")
        if s == "":
            continue
        a.dealWithAsking(s)
