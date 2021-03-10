# @Language: python3
# @File  : dialogManagement.py
# @Author: LinXiaofei
# @Date  : 2020-03-18


import csv
#from ltp import LTP
import jieba
#myltp = LTP(path="base")




def dealEntity():
    wf = open("历史/bookent_clean.csv", "w")
    entity = read_file('历史/bookent.csv')
    for e in entity:
        if e[0] == "《":
            e = e[1:]
        if e[-1] == "》":
            e = e[:-1]
        if e[0] == "\"":
            e = e[1:]
        if e[-1] == "\"":
            e = e[:-1]
        wf.writelines(e+"\n")
    wf.close()



def deleteType():
    pro = read_file('地理/etype.csv')
    entity = read_file('地理/entity.csv')
    print(len(entity),len(pro))
    clean_entity = []
    for e in entity:
        if e not in pro:
            clean_entity.append(e)
    print(len(clean_entity))
    wf = open("地理/entity.csv","w")
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
def deal100ans():
    book = xlrd.open_workbook('history_100.xlsx')
    print('sheet页名称:', book.sheet_names())
    sheet = book.sheet_by_index(0)
    rows = sheet.nrows
    cols = sheet.ncols
    wf = open("history_100_ans.csv", "w")
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
        wf.writelines(c_v + "\n")


        value = sheet.cell(i, 2).value
        clean_value = ""


        if ":" in str(value):
            clean_value = value.split(":")[0]
        elif "(" in str(value):
            clean_value = value.split("(")[0]
        else:
            clean_value = str(value)
        c_v = ""
        for c in clean_value:
            if c == " " or c == "\n":
                continue
            c_v += c
        if c_v == "" or c_v == "\n":
            continue
        wf.writelines(c_v + "\n")



        wf.writelines("=============================================\n")
def deal100():
    book = xlrd.open_workbook('history_100.xlsx')
    print('sheet页名称:', book.sheet_names())
    sheet = book.sheet_by_index(0)
    rows = sheet.nrows
    cols = sheet.ncols
    wf = open("history_100.csv", "w")
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
        wf.writelines(c_v + "\n")
"""
def generateQuestion():
    ent = read_file('地理/type.csv')

    wf = open("typequestion.csv","a")
    for e in ent:
        que = e+"的别名是什么"
        print(que)
        a,b = myltp.seg([que])
        print(a[0])

        cut_words = a[0]

        if e not in cut_words:
            wf.writelines(e+"\n")
"""
def recordnormalent():
    ent = read_file('地理/check.csv')
    unnormal = read_file('generatequestion.csv')

    wf = open("normal.csv", "w")

    for e in ent:
        if e not in unnormal:
            wf.writelines(e+"\n")
"""
def checkEnt():
    checkent = read_file('地理/checkent.csv')
    ent = read_file('typequestion.csv')
    wf = open("notin.csv", "w")
    for e in checkent:
        if e not in ent:
            wf.writelines(e+"\n"）
"""

def checkEnt():
    ques = read_file('100.csv')
    copyques = read_file('copy100.csv')
    wf = open("bad100.csv", "a")
    bad = read_file('bad100.csv')

    for e in copyques:
        if e not in ques and e not in bad:
            wf.writelines(e+"\n")

def dealgraphdata():

    wf = open('graphdata_deal.csv',"w")
    wf2 = open('graphdata_content.csv', "w")
    with open('graphdata.csv')as f:
        f_csv = csv.reader(f)

        rows = [row for row in f_csv]

        for r in rows:
            r = list(r)
            if len(r)<3:
                print(r)
                continue

            if r[1] in ['示例'] and len(r[1])>=10:
                wf.writelines(r[2]+"\n")
            elif r[1] == '内容':
                wf2.writelines(r[2]+"\n")
            elif r[1] in ['降水位置图','出处','符号图','分类编号','天气图','图片']:
                continue
            else:
                wf.writelines(r[0]+"的"+r[1]+"是"+r[2]+"\n")

def dealgraphdata2():
    data = read_file('graphdata_deal.csv')

    wf = open('graphdata_deal2.csv', "w")

    for a in data:
        deal_a = ""
        for i in a:
            if i in [" ","\\n","\\t"]:
                continue
            deal_a += i
        if len(deal_a)<7:
            continue
        wf.writelines(a+"\n")

def readgraph():
    wf = open("graphdata_cut.txt", "w")
    rf = open("graphdata_deal2.csv", "r")
    lines = list(rf.readlines())
    for line in lines:
        cut_line = jieba.cut(line)
        cut_words = " ".join(cut_line)
        wf.writelines(cut_words)
    wf.close()


def getbad():
    rf1 = open("../../html/history_good.csv", "r")
    rf2 = open("history_100.csv", "r")
    wf = open("historybad.csv", "w")
    r1 = list(rf1.readlines())
    r2 = list(rf2.readlines())[:100]

    for q in r2:
        if q not in r1:
            wf.writelines(q+"\n")
    wf.close()


def getTypeQues():
    rf1 = open("历史/etype.csv", "r")
    rf2 = open("history_100.csv", "r")
    wf = open("history_etype_question.csv", "w")
    r1 = list(rf1.readlines())
    r2 = list(rf2.readlines())

    for q in r2:
        for etype in r1:
            if etype in q:
                wf.writelines(etype + "\n")
                wf.writelines(q+"\n")

                wf.writelines("=========================\n")
    wf.close()
"""
def dealsplitent():
    sep_ent = read_file("历史/sep_ent.csv")

    combine_ent = open("历史/combine_de_ent.csv","w")

    s,hidden = myltp.seg(sep_ent)
    for sub in s:
        de_index = sub.index("的")
        print(sub[de_index+1:])
        if len(sub) > de_index+2:
            combine_ent.writelines("".join(sub[de_index+1:])+"\n")

    combine_ent.close()
"""

def deleteOneVale(graph):
    ent = read_file("../backend/data/地理/entity.csv")
    wf = open("../backend/data/地理/entity.csv","w")
    flag = False
    for e in ent:
        flag = False
        pro_list, rel_list = graph.searchEntity(e)
        for pro in pro_list:
            if pro[0] not in ['出处','分类编号']:
                flag = True
                break
        if flag:

            wf.writelines(e+"\n")
    wf.close()

if __name__ == '__main__':
    deleteType()



