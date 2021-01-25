# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from ltp import LTP
import configparser
import numpy as np
ltp = LTP(path="base")


"""
config = configparser.ConfigParser()
config.read("../backend/config.ini")

subject = config['DEFAULT']['subject']

ltp.init_dict(path="../backend/data/"+subject+"/allentity.csv", max_window=10)
ltp.init_dict(path="../backend/data/"+subject+"/cleanpro.csv", max_window=10)
ltp.init_dict(path="../backend/data/"+subject+"/cleanrel.csv", max_window=10)
"""


def getSEG(words):
    seg, hidden = ltp.seg([words])
    return seg,hidden


def getPOS(hidden):
    return ltp.pos(hidden)

def getDEP(hidden):
    return ltp.dep(hidden)



def dealLTP(seg,hidden):
    pos = ltp.pos(hidden)
    dep = ltp.dep(hidden)
    dep_array = np.array(dep[0])

    dep_index = dep_array[:,1]
    dep_role = dep_array[:,2]

    print(pos)
    print(dep_index)
    print(dep_role)

if __name__ == '__main__':
    seg, hidden = getSEG("世界上最大的湖泊是什么")
    print(seg)
    dealLTP(seg, hidden)
