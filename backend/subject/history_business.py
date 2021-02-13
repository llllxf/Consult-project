# @Time : 2021/2/9 11:16 AM 
# @Author : LinXiaofei
# @File : history_business.py
from backend.nlu.LTPUtil import *
from backend.nlu.parseSentence import ParseSentence
from backend.data.data_process import read_file
from backend.graphSearch.graphSearch import graphSearch
from backend.graphSearch.normalBussiness import normalBussiness
from backend.nlu.processNLU import processNLU
from ltp import LTP
import numpy as np
parseSentence = ParseSentence()
graph_util = graphSearch()
normal_bussiness = normalBussiness()
process_nlu = processNLU()
ltp = LTP(path="base")
def askWho(words):

    if '哪个' in words and '人' in words:
        words.replace("人","单人")
    elif '谁' in words:
        words.replace("谁",'哪个单人')
    return words

def dealYear(words):


    seg,hidden = getSEG(words)
    cut_words = seg[0]
    pos = getPOS(hidden)[0]
    dep = getDEP(hidden)[0]

    ent, array, extractType = parseSentence.extractBestEnt(cut_words,dep)
    year_pro = read_file("../backend/data/历史/year_pro.csv")

    con,con_count = parseSentence.getValuableWords(cut_words,pos,dep)

    if extractType == 'entity':
        ans = normal_bussiness.doNormalbyCon([ent], [con, con_count], year_pro)
        if ans:
            if '年' in ans:
                return [1, ans, ent]

    best_word = con[np.argmax(con_count)]
    ans = normal_bussiness.doNormalForFalse(best_word,[con,con_count])
    if ans :
        if '年' in ans:
            return [1,ans,ent]

    return [0,"无法回答",None]

def dealWho(words):

    seg,hidden = getSEG(words)
    cut_words = seg[0]
    pos = getPOS(hidden)[0]
    dep = getDEP(hidden)[0]


    con,con_count = parseSentence.getValuableWords(cut_words,pos,dep)

    key_ent = parseSentence.getEntity(cut_words)
    print([con,con_count]+key_ent)

    return [con,con_count]+key_ent




def dealBookSBV(words):


    seg, hidden = getSEG(words)
    cut_words = seg[0]
    pos = getPOS(hidden)[0]
    dep = getDEP(hidden)[0]

    _, task_type = parseSentence.getWordsExtractType(cut_words,dep,pos)

    if task_type in ['split','split_end']:
        return None,None,None

    ent, array, extractType = parseSentence.extractBestEnt(cut_words, dep)
    bookent = read_file("../backend/data/历史/bookent.csv")

    if ent in bookent:
        cut_words[cut_words.index(ent)] = "《"+ent+"》"
        entity, ans, task_type = process_nlu.dealNormal("《"+ent+"》", array, cut_words, pos, dep)

        #entity, ans, task_type = process_nlu.dealNormal( ent , array, cut_words, pos, dep)


        return entity, ans, task_type


    return None,None,None


def checkSplitEnt(words):
    sge,hidden = getSEG(words)
    cut_words = seg[0]

    combine_ent = read_file("../backend/data/历史/sep_ent.csv")





