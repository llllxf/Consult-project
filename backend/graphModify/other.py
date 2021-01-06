# @Language: python3
# @File  : other.py.py
# @Author: LinXiaofei
# @Date  : 2020-05-27
"""

"""
import sys
import os
import numpy as np
project_path = os.path.abspath(os.path.join(os.getcwd(), ".."))
# print(project_path)
sys.path.append(project_path)

from data.data_process import read_file

def getProEnt():
    entpro = read_file(project_path+"/entpro.txt")
    enttype = read_file(project_path + "/data/etype.csv")

    inf = open("in.txt","w")
    outf = open("out.txt","w")
    for sub in enttype:
        if sub in entpro:
            inf.writelines(sub+"\n")
        else:
            outf.writelines(sub+"\n")


if __name__ == '__main__':
    getProEnt()
