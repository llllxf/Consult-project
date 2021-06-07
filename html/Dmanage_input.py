# @Language: python3
# @File  : Dmanage.py
# @Author: LinXiaofei
# @Date  : 2020-05-01
"""

"""

from backend.nlu.processNLU import processNLU
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

from backend.dm.GeoDMNormal import GeoDMNormal
from backend.dm.HistoryDM import HistoryDM
from backend.dm.HistoryDMNormal import HistoryDMNormal
from backend.dm.GeoDM import GeoDM
"""
问答引擎
"""

if __name__ == '__main__':

    h = HistoryDM()
    #g = GeoDM()
    #gn = GeoDMNormal()
    #d = DialogManagement()

    while(1):
        s = input()
        ans = h.doNLU(s)
        print(ans)
