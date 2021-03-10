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

from backend.dm.GeoDMNormal import GeoDMNormal
from backend.dm.HistoryDM import HistoryDM
from backend.dm.HistoryDMNormal import HistoryDMNormal
from backend.dm.GeoDM import GeoDM
"""
问答引擎
"""

if __name__ == '__main__':

    config = configparser.ConfigParser()
    content = config.read("../backend/config.ini")

    config['DEFAULT']['subject'] = '历史'

    print(config)

    with open('../backend/config.ini', 'w') as file:
        config.write(file)
    file.close()
    """
    rf = open("../backend/data/100.csv", "r")
    wf = open("geo_1.csv", "w")
    rl = rf.readlines()
    """


    h = HistoryDM()
    #g = GeoDM()
    #gn = GeoDMNormal()

    #d = DialogManagement()

    rf = open("h_bad_2.csv","r")
    wf = open("test_a.csv","w")
    rl = rf.readlines()


    count = 0

    for l in rl:
        if len(l)<3:
            continue


        print("=========================")
        #l = l.rstrip()
        print(l)
        print("=========================")
        ans = h.doNLU(l)
        wf.writelines(l+"\n")
        wf.writelines(ans[1]+"\n")
        wf.writelines("=========================\n")
        count = count+1
        print(str(count)+"=========================\n")

    """
    while(1):
        s = input()
        ans = g.doNLU(s)
        print(ans)
    """







