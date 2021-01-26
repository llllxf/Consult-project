# @Language: python3
# @File  : Dmanage.py
# @Author: LinXiaofei
# @Date  : 2020-05-01
"""

"""

from backend.nlu.processNLU import processNLU
from backend.nlg.generateAns import generateAns
from backend.graphSearch.calculateBussiness import calculateBussiness
from backend.graphSearch.compareBussiness import compareBussiness
from backend.graphSearch.normalBussiness import normalBussiness
from backend.graphSearch.graphSearch import graphSearch
import configparser
from backend.dm.DialogManagement import DialogManagement
from backend.sentence_similarity.sentenceSimilarity import SentenceSimilarity
from backend.nlu.parseSentence import ParseSentence
from backend.data.data_process import read_file,read_template
config = configparser.ConfigParser()
#config.read("../backend/config.ini")
from backend.nlu.parseSentence import ParseSentence
from backend.nlu.LTPUtil import *

"""
问答引擎
"""

if __name__ == '__main__':
    d = DialogManagement()

    rf = open("../backend/data/100.csv","r")
    wf = open("ans100.csv","a")
    rl = rf.readlines()
    for l in rl:
        if len(l)<3:
            continue
        ans = d.doNLU(l)
        wf.writelines(l+"\n")
        wf.writelines(ans[1]+"\n")
        wf.writelines("=========================\n")
    """

    while(1):
        s = input()
        ans = d.doNLU(s)
        print(ans)
    """













