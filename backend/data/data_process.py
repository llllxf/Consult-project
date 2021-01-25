# @Language: python3
# @File  : dialogManagement.py
# @Author: LinXiaofei
# @Date  : 2020-03-18

import xlrd

def deleteType():
    pro = read_file('地理/cleanpro.csv')
    entity = read_file('地理/allentity.csv')
    clean_entity = []
    for e in entity:
        if e in pro:
            clean_entity.append(e)
    wf = open("proent.csv","w")
    for e in clean_entity:
        wf.writelines(e+"\n")
    wf.close()

def read_file(filename):

    with open(filename,"r") as rf:
        array = []
        lines = rf.readlines()
        for line in lines:
            line = line.strip('\n')
            if line == "":
                continue
            array.append(line)

    rf.close()
    return array


def read_template(filename):

    with open(filename,"r") as rf:
        array = []
        temp = []
        lines = rf.readlines()
        for line in lines:
            line = line.strip('\n')
            if line == "":
                continue
            if line == "==========":
                array += temp[1:]
                temp = []
                continue
            temp.append(line)
    rf.close()
    return array

if __name__ == '__main__':
    book = xlrd.open_workbook('../../100.xlsx')
    print('sheet页名称:', book.sheet_names())
    sheet = book.sheet_by_index(0)
    rows = sheet.nrows
    cols = sheet.ncols
    wf = open("100.csv","w")
    for i in range(sheet.nrows):
        value = sheet.cell(i, 1).value
        clean_value = ""
        if ":" in value:
            clean_value = value.split(":")[0]
        else:
            clean_value = value.split("(")[0]
        c_v = ""
        for c in clean_value:
            if c == " " or c == "\n":
                continue
            c_v += c
        if c_v == "" or c_v == "\n":
            continue
        wf.writelines(c_v+"\n")

