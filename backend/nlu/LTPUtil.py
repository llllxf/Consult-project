# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from pyltp import Postagger, Parser

class LTPUtil(object):


    def __init__(self):

        """
        词性标注
        """
        self.postagger = Postagger()
        self.postagger.load("../../../ltp_data_v3.4.0/pos.model")


        """
        句法依存分析
        """
        self.parser = Parser()
        self.parser.load("../../../ltp_data_v3.4.0/parser.model")


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


    def get_postag(self, words):
        postags = self.postagger.postag(words)
        print(list(postags))
        return postags

    """
    :describe 句法依存
    :arg 分词列表, 词性列表
    """


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


    def get_sentence_pattern(self, words):

        postags = self.get_postag(words)
        arcs = self.parser.parse(words, postags)

        arcs_dict,reverse_arcs_dict = self._build_sub_dicts(words, arcs)
        hed_index = 0

        pattern = ""
        for i in range(len(arcs)):
            sub_arc = arcs[i]
            if sub_arc.relation == 'HED':
                hed_index = i

        for i in range(len(words)):
            if i == hed_index:
                pattern += 'HED-'
            for sub_dict in arcs_dict:
                keys = sub_dict.keys()
                for k in keys:
                    if i in sub_dict[k]:
                        pattern += k+"-"
                        break

        if pattern[-1] == '-':
            pattern = pattern[:-1]
        #print(pattern)
        #print(arcs_dict)
        #print(reverse_arcs_dict)
        #print(hed_index,words[hed_index])

        return pattern, arcs_dict, reverse_arcs_dict,postags, hed_index


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
