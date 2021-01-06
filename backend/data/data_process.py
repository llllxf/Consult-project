# @Language: python3
# @File  : dialogManagement.py
# @Author: LinXiaofei
# @Date  : 2020-03-18

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
    deleteType()

