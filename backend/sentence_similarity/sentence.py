#encoding=utf-8


from backend.nlu.LTPUtil import *
from backend.sentence_similarity.zhcnSegment import zhcnSeg

class Sentence(object):

    def __init__(self,sentence,id = 0):
        self.id = id
        self.origin_sentence = sentence
        self.cuted_sentence = self.cut()
        #print(self.cuted_sentence)

    # 对句子分词
    def cut(self):
        seg,hidden = getSEG(self.origin_sentence)
        return seg[0]

    # 获取切词后的词列表
    def get_cuted_sentence(self):
        return self.cuted_sentence

    # 获取原句子
    def get_origin_sentence(self):
        return self.origin_sentence

    # 设置该句子得分
    def set_score(self,score):
        self.score = score