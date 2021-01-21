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
from backend.nlu.LTPUtil import LTPUtil

"""
问答引擎
"""

if __name__ == '__main__':
    graph = graphSearch()
    pro_list = read_file("../backend/data/地理/cleanpro.csv")
    for p in pro_list:
        config[p] = {
            'type': 'desconpro',
            'alias': p
        }
    with open('proconfig.ini', 'w') as file:
        config.write(file)






