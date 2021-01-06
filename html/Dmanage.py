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
config.read("../backend/config.ini")
from backend.nlu.parseSentence import ParseSentence
from backend.nlu.LTPUtil import LTPUtil

"""
问答引擎
"""


if __name__ == '__main__':
    #c = ParseSentence()
    #words = c.getCutWords("信奉佛教的是哪一个国家")
    #b = LTPUtil()
    #b.get_sentence_pattern(words)
    #b.get_postag(words)
    #sen = read_template("../backend/template_library/地理/国家.csv")
    #print(sen)
    #a = SentenceSimilarity()

    dm = DialogManagement()
    ans = dm.doNLU("日本的人口数量是多少")


    print(ans)
    #a.set_sentences(sen)
    #a.LsiModel()
    #a.TfidfModel()
    #a.LdaModel()
    #ans = a.similarity_top_k("被称为欧洲小虎的是哪一个国家", 10)
    #print(ans)
    """
    questions = read_file("../backend/data/allentity.csv")
    wf = open("../backend/data/match.csv","a")
    for q in questions:
        ans = a.similarity_top_k(q, 10)
        print(ans[0])
        wf.writelines(q+"\t"+ans[0][0]+"\n")
    """


    #a.simple_model()
    """
    print("=================LdaModel===============")
    arr = ["日本的人口特征","日本人口","日本人口数","日本多少人"]

    for s in arr:
        print(s)
        print(a.similarity_top_k(s,2))
        print("========================================")
    """
    """
    a = DialogManagement()
    config.set('DEFAULT','subject','地理')
    while(1):
        s = input("user: ")
        if s == "":
            continue
        ans = a.doNLU(s)
        print(ans)
    """