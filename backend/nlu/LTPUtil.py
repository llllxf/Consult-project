# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import jieba
import configparser
from pyltp import Postagger, Parser, Segmentor

class LTPUtil(object):


    def __init__(self):

        """
        词性标注
        """
        config = configparser.ConfigParser()
        config.read("../backend/config.ini")
        subject = config['DEFAULT']['subject']
        self.postagger = Postagger()
        self.postagger.load("../../ltp_data_v3.4.0/pos.model")
        self.segmentor = Segmentor()
        self.segmentor.load("../../ltp_data_v3.4.0/cws.model")

        self.cut_tool = jieba
        self.cut_tool.load_userdict("../backend/data/" + subject + "/entforcut.csv")

        """
        句法依存分析
        """
        self.parser = Parser()
        self.parser.load("../../ltp_data_v3.4.0/parser.model")


        """
        疑问代词
        """
        self.Interrogative_pronouns = ['哪里', '什么', '怎么', '哪', '为什么', '啥','谁']
        self.noun_for_pedia = ['n', 'nh', 'ni', 'nl', 'ns', 'nz', 'nt','i']
        self.clear_word = ['嗯','噫','啊','哦']


    """
    :describe 词性分析
    :arg 分词列表
    """



    def get_normal_seg(self,words):

        return list(self.segmentor.segment(words))


    def get_postag(self, words):
        postags = self.postagger.postag(words)
        return postags

    """
    :describe 句法依存
    :arg 分词列表, 词性列表
    """

    def get_seg(self,words):
        return list(self.cut_tool.cut(words))


    def get_parse(self, words, postags):
        parse = self.parser.parse(words, postags)
        return parse

    """
    :describe 
    得到问题对应的模版
    1.先对问题分词
    2.得到每个分词对应的词性
    3.得到句法依存分析树

    :arg 句子
    """


    def get_sentence_data(self, words):

        cut_words = self.get_seg(words)
        postags = self.get_postag(cut_words)
        arcs = self.parser.parse(cut_words, postags)

        #arcs_dict,reverse_arcs_dict = self._build_sub_dicts(cut_words, arcs)
        dep = []
        revers_dep={}
        count = 1
        for i in range(len(cut_words)):

            sub_arc = arcs[i]
            dep.append((i+1,sub_arc.head,sub_arc.relation))
            #if sub_arc.relation == 'COO':
            #    sub_arc = arcs[sub_arc.head-1]
            if sub_arc.head in revers_dep.keys():
                revers_dep[sub_arc.head].append([i+1,sub_arc.relation])
            else:
                revers_dep[sub_arc.head]=[[i+1,sub_arc.relation]]
            #print(sub_arc.relation,sub_arc.head)
            """
            if sub_arc.head == 'HED':
                dep.append((count,0,'HED'))
            for sub_dict in reverse_arcs_dict:
                keys = sub_dict.keys()
                for k in keys:
                    if i in sub_dict[k]:
                        dep.append((count,i+1,k))
                        break
            count=count+1
            """
        print(dep)
        return cut_words,list(postags),dep,revers_dep


    """
    :decription: 为句子中的每个词语维护一个保存句法依存儿子节点的字典
    :args:
    words: 分词列表
    postags: 词性列表
    arcs: 句法依存列表
    """


    def _build_sub_dicts(self, words, arcs):
        sub_dicts = []
        sub_dicts2 = []
        for idx in range(len(words)):
            sub_dict = dict()
            for arc_idx in range(len(arcs)):
                """
                如果这个依存关系的头节点是该单词
                """
                if arcs[arc_idx].head == idx + 1:
                    if arcs[arc_idx].relation in sub_dict:
                        sub_dict[arcs[arc_idx].relation].append(arc_idx)
                    else:
                        sub_dict[arcs[arc_idx].relation] = []
                        sub_dict[arcs[arc_idx].relation].append(arc_idx)
            sub_dicts.append(sub_dict)
        for i in range(len(words)):
            sub_dicts2.append({})
        for idx in range(len(words)):
            for arc_idx in range(len(arcs)):
                """
                如果这个依存关系的头节点是该单词
                """
                if arcs[arc_idx].head == idx + 1:
                    if arcs[arc_idx].relation in sub_dicts2[arc_idx].keys():
                        sub_dicts2[arc_idx][arcs[arc_idx].relation].append(idx)
                    else:
                        sub_dicts2[arc_idx][arcs[arc_idx].relation] = []
                        sub_dicts2[arc_idx][arcs[arc_idx].relation].append(idx)
        #print("sub_dicts2",sub_dicts2)

        return sub_dicts,sub_dicts2

    """
    :decription:完善识别的部分实体
    """

    def _fill_ent(self, words, postags, sub_dicts, word_idx):
        sub_dict = sub_dicts[word_idx]
        prefix = ''
        if 'ATT' in sub_dict:
            for i in range(len(sub_dict['ATT'])):
                prefix += self._fill_ent(words, postags, sub_dicts, sub_dict['ATT'][i])

        postfix = ''
        if postags[word_idx] == 'v':
            if 'VOB' in sub_dict:
                postfix += self._fill_ent(words, postags, sub_dicts, sub_dict['VOB'][0])
            if 'SBV' in sub_dict:
                prefix = self._fill_ent(words, postags, sub_dicts, sub_dict['SBV'][0]) + prefix

        return prefix + words[word_idx] + postfix


if __name__=='__main__':
    s = input()
    LTPUtil()
    words, pattern, arcs_dict, postags, hed_index = LTPUtil.get_sentence_pattern(['中国','最大','淡水湖'])
    print(words, pattern, arcs_dict, list(postags), hed_index)
