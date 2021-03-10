# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from ltp import LTP
import configparser
import numpy as np
from backend.data.data_process import read_file



class LTPUtil(object):
    def __init__(self):
        ltp = LTP(path="base")

        config = configparser.ConfigParser()
        config.read("../backend/config.ini")

        subject = config['DEFAULT']['subject']

        instanceArray = list(set(read_file("../backend/data/" + subject + "/entforcut.csv")))
        instanceArray = sorted(instanceArray, key=lambda i: len(i), reverse=True)

        combine = instanceArray

        ltp.add_words(words=combine)

        self.ltp = ltp

    def getSEG(self,words):
        seg, hidden = self.ltp.seg([words])
        return seg, hidden

    def getPOS(self,hidden):
        return self.ltp.pos(hidden)

    def getDEP(self,hidden):
        return self.ltp.dep(hidden)

    def dealLTP(self,hidden):
        pos = self.ltp.pos(hidden)
        dep = self.ltp.dep(hidden)
        dep_array = np.array(dep[0])

        dep_index = dep_array[:, 1]
        dep_role = dep_array[:, 2]

        print(pos)
        print(dep_index)
        print(dep_role)

