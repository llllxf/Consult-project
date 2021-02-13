# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from ltp import LTP
import configparser
import numpy as np
from backend.data.data_process import read_file
ltp = LTP(path="base")


config = configparser.ConfigParser()
config.read("../backend/config.ini")

subject = config['DEFAULT']['subject']


instanceArray = list(set(read_file("../backend/data/"+subject+"/entforcut.csv")))
instanceArray = sorted(instanceArray, key=lambda i: len(i), reverse=True)

proArray = read_file("../backend/data/"+subject+"/cleanpro.csv")
proArray = sorted(proArray, key=lambda i: len(i), reverse=True)

relArray = read_file("../backend/data/"+subject+"/cleanrel.csv")
relArray = sorted(relArray, key=lambda i: len(i), reverse=True)

combine = instanceArray+proArray+relArray
ltp.add_words(words=combine, max_window=30)

def getSEG(words):

    seg, hidden = ltp.seg([words])
    return seg,hidden


def getPOS(hidden):
    return ltp.pos(hidden)

def getDEP(hidden):
    return ltp.dep(hidden)


def dealLTP(hidden):
    pos = ltp.pos(hidden)
    dep = ltp.dep(hidden)
    dep_array = np.array(dep[0])

    dep_index = dep_array[:,1]
    dep_role = dep_array[:,2]

    print(pos)
    print(dep_index)
    print(dep_role)

if __name__ == '__main__':
    seg, hidden = getSEG("西周的分封制")
    dealLTP(seg, hidden)
