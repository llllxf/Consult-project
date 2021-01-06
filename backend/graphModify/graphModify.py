# @Language: python3
# @File  : graphModify.py
# @Author: LinXiaofei
# @Date  : 2020-05-19
"""

"""

import sys
import os
project_path = os.path.abspath(os.path.join(os.getcwd(), ".."))
# print(project_path)
sys.path.append(project_path)
from data.data_process import read_file
from nlu.LTPUtil import LTPUtil

from graphSearch.graphSearch import graphSearch

class graphModify(object):
    def __init__(self):
        self.search_util = graphSearch()

    def fileForPro(self,type):
        """
        得到某一类实体基于属性的文档（每个文档针对一个属性）
        :param type:
        :return:
        """

        isExists = os.path.exists(project_path+"/data2/pro/"+type)
        if not isExists:
            os.makedirs(project_path+"/data2/pro/"+type)
        pro = self.search_util.getProByType(type)
        for p in pro:
            f = open(project_path + "/data2/pro/"+type+"/"+p+".txt","w")

            f.writelines(p+"\n")

            value_list = self.search_util.getValueByPro(type,p)
            for value in value_list:
                f.writelines(value[0]+":"+value[1]+"\n")
                f.writelines("\n")
            f.close()

    def filreForRel(self,type):
        """
        得到某一类实体基于关系的文档（每个文档针对一个关系）
        :param type:
        :return:
        """

        isExists = os.path.exists(project_path + "/data/rel/" + type)
        if not isExists:
            os.makedirs(project_path + "/data/rel/" + type)
        if "label" in type:
            return
        rel = self.search_util.getRelByType(type)

        for r in rel:
            f = open(project_path + "/data/rel/" + type + "/" + r + ".txt", "w")

            f.writelines(r + "\n")

            value_list = self.search_util.getValueByRel(type, r)
            for value in value_list:
                f.writelines(value[0] + ":" + value[1] + "\n")
                f.writelines("\n")
            f.close()

    def resetProToRepertory(self,type,old,new):
        """
        读取文件中的三元组，将其中的谓词替换
        :param type:
        :param old:
        :param new:
        :return:
        """

        modify_list = []
        new_list = []
        #old_list = read_file(project_path + "/data/pro/"+type+"/"+old+".txt")
        old_list = read_file(project_path + "/data/operate/add.txt")

        modify_pre = old_list[0]
        predicate = self.search_util.getPredicate(modify_pre)


        new_predicate = self.search_util.getPredicate(new)

        for o in old_list[1:]:
            information = o.split(":")
            sub_label = information[0]
            print("sub_label",sub_label)
            subject = self.search_util.getSubject(sub_label)
            modify_list.append({"subject":subject,"predicate":predicate,"object":information[1]})
            new_list.append({"subject":subject, "predicate":new_predicate, "object":information[1]})
        data = {'repertoryName':'geo4','oldList':str(modify_list),'newList':str(new_list)}
        self.search_util.resetTripleToRepertory(data)
        log = open(project_path + "/data/log/" + type + ".txt", "a")

        log.writelines("reset:  [" + type + "]" + modify_pre + "-->" + new + "\n")
        log.writelines("=========================================\n")

    def resetTripleByDeleteOld(self,filename,type):
        """
        将之前的三元组针对主语和谓词删除（也就是该实体的该属性全部删除），然后添加新的三元组
        :param type:
        :param old:
        :param new:
        :return:
        """

        reset_list = read_file(project_path + "/data/operate/add.txt")

        sub_list = []
        pre_list = []
        obj_list = []
        for r in reset_list:

            triple = r.split(" ")
            sub = triple[0]
            pre = triple[1]
            obj = triple[2]


            self.search_util.deleteTripleBySAP(sub,pre)
            sub_list.append(sub)
            pre_list.append(pre)

            obj_list.append(obj)


        self.addTripleToRepertory(sub_list,pre_list,obj_list,type)

        log = open(project_path + "/data/log/" + type + ".txt", "a")

        log.writelines("add by delete olds: \n")


    def resetNewProToRepertory(self,old, new, new_py,type):
        """
        读取文件中的三元组，将其中的谓词替换为新建谓词
        :param old:
        :param new:
        :param new_py:
        :param type:
        :return:
        """

        modify_list = []
        new_list = []
        old_list = read_file(project_path + "/data/pro/" + type + "/" + old + ".txt")

        modify_pre = old_list[0]
        predicate = self.search_util.getPredicate(modify_pre)

        self.search_util.addProperty(new,new_py)
        new_predicate = self.search_util.getPredicate(new)


        for o in old_list[1:]:
            information = o.split(":")
            sub_label = information[0]
            print("sub_label", sub_label)
            subject = self.search_util.getSubject(sub_label)
            modify_list.append({"subject": subject, "predicate": predicate, "object": information[1]})
            new_list.append({"subject": subject, "predicate": new_predicate, "object": information[1]})
        data = {'repertoryName': 'geo4', 'oldList': str(modify_list), 'newList': str(new_list)}
        self.search_util.resetTripleToRepertory(data)
        operate = open(project_path + "/data/log/operate.txt", "a")
        operate.writelines("add "+new+"\n")
        operate.writelines("=========================================\n")
        log = open(project_path + "/data/log/" + type + ".txt", "a")

        log.writelines("reset:  [" + type + "]" + modify_pre + "-->" + new + "\n")
        log.writelines("=========================================\n")

    def resetProForTriple(self,subj,obje,pred_old,pred_new):
        """
        修改一条三元组的谓词
        :param subj:
        :param obje:
        :param pred_old:
        :param pred_new:
        :return:
        """

        log = open(project_path + "/data/log/"+pred_new+".txt", "a")
        modify_list = []
        new_list = []

        old_predicate = self.search_util.getPredicate(pred_old)
        new_predicate = self.search_util.getPredicate(pred_new)
        subject = self.search_util.getSubject(subj)

        modify_list.append({"subject": subject, "predicate": old_predicate, "object": obje})
        new_list.append({"subject": subject, "predicate": new_predicate, "object": obje})


        data = {'repertoryName': 'geo4', 'oldList': str(modify_list), 'newList': str(new_list)}
        self.search_util.resetTripleToRepertory(data)

        log.writelines("reset: <"+subj+"> " + pred_old + "-->" + pred_new + "\n")
        log.writelines("=========================================\n")

    def resetProToNewOne(self,label,new_label):
        """
        重置已有谓词的标签
        :param label:
        :param new_label:
        :return:
        """

        log = open(project_path + "/data/log/operate.txt", "a")

        modify_list = []
        new_list = []

        predicate = self.search_util.getPredicate(label)
        print(predicate)
        label_uri = "http://www.w3.org/2000/01/rdf-schema#label"

        modify_list.append({"subject": predicate, "predicate": label_uri, "object": label})
        new_list.append({"subject": predicate, "predicate": label_uri, "object": new_label})
        data = {'repertoryName': 'geo4', 'oldList': str(modify_list), 'newList': str(new_list)}
        self.search_util.resetTripleToRepertory(data)

        log.writelines("reset: "+ label + "-->" + new_label + "\n")
        log.writelines("=========================================\n")

    def resetProForPro(self,pro_old):
        """
        读取文件，根据文件中的三元组批量修改（修改三元组中的谓词，与resetProToRepertory不同在于此函数针对属性查询出所有三元组，而后者只差出该属性某一确定类型）
        :param pro_old:
        :return:
        """
        log = open(project_path + "/data/log/"+pro_old+".txt", "a")
        triple_array = read_file(project_path+"/data/prosearch/"+pro_old+".csv")
        for line in triple_array:
            data = line.split(",")
            subj=data[0]
            obje=data[1]
            pro_new = data[2]
            self.resetProForTriple(subj,obje,pro_old,pro_new)

            log.writelines("reset: [" +subj  + ":"+pro_old+"]-->" + pro_new + "\n")
            log.writelines("=========================================\n")

    def resetProForFile(self,fname):
        """
        读取文件，根据文件中的三元组批量修改（修改三元组中的谓词，与resetProToRepertory不同在于此函数针对属性查询出所有三元组，而后者只差出该属性某一确定类型）
        :param pro_old:
        :return:
        """
        log = open(project_path + "/data/log/reset.txt", "a")
        triple_array = read_file(project_path+"/data/prosearch/"+fname+".txt")
        for line in triple_array:
            data = line.split(" ")
            subj=data[0]
            obje=data[1]
            pro_old = data[2]
            pro_new = data[3]
            self.resetProForTriple(subj,obje,pro_old,pro_new)

            log.writelines("reset: [" +subj  + ":"+pro_old+"]-->" + pro_new + "\n")
            log.writelines("=========================================\n")



    def resetRelToRepertory(self,type,old,new):
        """
        读取文件修改三元组中的谓词
        :param type:
        :param old:
        :param new:
        :return:
        """

        modify_list = []
        new_list = []
        old_list = read_file(project_path + "/data/pro/"+type+"/"+old+".txt")

        modify_pre = old_list[0]
        predicate = self.search_util.getPredicate(modify_pre)
        new_predicate = self.search_util.getRelPredicate(new)
        for o in old_list[1:]:
            information = o.split(":")
            sub_label = information[0]
            obj_label = information[1]


            subject = self.search_util.getSubject(sub_label)
            obj = self.search_util.getSubject(obj_label)
            modify_list.append({"subject":subject,"predicate":predicate,"object":obj_label})
            new_list.append({"subject":subject, "predicate":new_predicate, "object":obj})


        data = {'repertoryName':'geo4','oldList':str(modify_list),'newList':str(new_list)}

        self.search_util.resetRelTripleToRepertory(data)
        log = open(project_path + "/data/log/" + type + ".txt", "a")

        log.writelines("reset:  [" + type + "]" + modify_pre + "-->" + new + "\n")
        log.writelines("=========================================\n")

    def addTripleToRepertory(self,subj,pred,obje,type):
        """
        添加一条三元组（属性）
        :param subj:
        :param pred:
        :param obje:
        :param type:
        :return:
        """
        log = open(project_path + "/data/log/" + type + ".txt","a")

        tripleList = []
        for p_index in range(len(pred)):
            predicate = self.search_util.getPredicate(pred[p_index])


            subject = self.search_util.getSubject(subj[p_index])
            tripleList.append({"subject":subject,"predicate":predicate,"object":obje[p_index]})
        self.search_util.addTripleToRepertory(tripleList)
        for i in range(len(subj)):
            log.writelines("add:  " + subj[i] + "-" + pred[i] + "-" + obje[i] + "\n")
            log.writelines("=========================================\n")

    def addRelTripleToRepertory(self,subj,pred,obje,type):
        """
        添加一条三元组（关系）
        :param subj:
        :param pred:
        :param obje:
        :param type:
        :return:
        """
        log = open(project_path + "/data/log/" + type + ".txt","a")
        tripleList = []
        for p_index in range(len(pred)):
            predicate = self.search_util.getRelPredicate(pred[p_index])
            subject = self.search_util.getSubject(subj[p_index])
            obj = self.search_util.getSubject(obje[p_index])
            print(obj,"???",obje[p_index])
            tripleList.append({"subject":subject,"predicate":predicate,"object":obj})
        self.search_util.addRelTripleToRepertory(tripleList)
        for i in range(len(subj)):
            log.writelines("add:  "+subj[i]+"-"+pred[i]+"-"+obje[i]+"\n")
            log.writelines("=========================================\n")

    def deleteTripleToRepertory(self, subj, pred, obje, type):
        """
        删除一条三元组（属性）
        :param subj:
        :param pred:
        :param obje:
        :param type:
        :return:
        """
        print(subj, pred, obje, type)
        log = open(project_path + "/data/log/" + type + ".txt", "a")
        tripleList = []
        for p_index in range(len(pred)):
            predicate = self.search_util.getPredicate(pred[p_index])
            subject = self.search_util.getSubject(subj[p_index])
            tripleList.append({"subject": subject, "predicate": predicate, "object": obje[p_index]})
        self.search_util.deleteTripleToRepertory(tripleList)
        for i in range(len(subj)):
            log.writelines("delete:  " + subj[i] + "-" + pred[i] + "-" + obje[i] + "\n")
            log.writelines("=========================================\n")

    def deleteRelToRepertory(self, subj, pred, obje, type):
        """
        删除一条三元组（关系）
        :param subj:
        :param pred:
        :param obje:
        :param type:
        :return:
        """
        log = open(project_path + "/data/log/" + type + ".txt", "a")
        tripleList = []
        for p_index in range(len(pred)):
            predicate = self.search_util.getRelPredicate(pred[p_index])
            subject = self.search_util.getSubject(subj[p_index])
            object = self.search_util.getSubject(obje[p_index])
            print(object)
            tripleList.append({"subject": subject, "predicate": predicate, "object": "<"+object+">"})
        self.search_util.deleteRelToRepertory(tripleList)
        for i in range(len(subj)):
            log.writelines("delete:  " + subj[i] + "-" + pred[i] + "-" + obje[i] + "\n")
            log.writelines("=========================================\n")


if __name__ == '__main__':
    g = graphModify()
    #rel_add = read_file(project_path + "/data/operate/add.txt")
    rel_add = read_file(project_path + "/data3/complete/海洋_rel.csv")
    #pro_add = read_file(project_path + "/data3/complete/城市_pro.csv")
    rel_delete = read_file(project_path + "/data/operate/deleterel.txt")
    pro_delete = read_file(project_path + "/data/operate/delete.txt")


    #g.getInfForComplete('河流')

    #g.resetProForFile('河流pro')
    #g.search_util.addProperty("气候特征",'qihoutezheng')

    #g.resetProToNewOne('养殖对象','养殖物种')

    #rel_reset = read_file(project_path + "data/operate/relreset.txt")
    #pro_reset = read_file(project_path + "data/operate/reset.txt")

    """
    for r in rel_add:
        triples = r.split(" ")
        print(triples)
        g.addRelTripleToRepertory([triples[0]],[triples[1]],[triples[2]],"海洋")
    """




    g.resetTripleByDeleteOld('add', '河流')

    """
    for p in pro_add:
        triples = p.split(" ")
        print(triples)
        g.addTripleToRepertory([triples[0]], [triples[1]], [triples[2]], "城市")
    """




    """
    for p in pro_delete:
        triples = p.split(" ")
        print(triples)
        g.deleteTripleToRepertory([triples[0]],[triples[1]],[triples[2]],"海洋")
    """





    #g.resetTripleByDeleteOld('2','地位')





    """
    for r in rel_delete:
        triples = r.split(" ")
        print(triples)
        g.deleteRelToRepertory([triples[0]], [triples[1]], [triples[2]], "区域")
    """

    """
    type_list = read_file(project_path + "/data/类型.csv")
    count = 0
    
    for t in type_list:
        print(t)
        count = count+1
        g.filreForRel(t)
        g.fileForPro(t)
    """

    #g.resetRelToRepertory('平原','国家','位于')
    #g.resetProToRepertory('洋流','流向','流向')
    #g.resetNewProToRepertory('流向','方位流向','fangweiliuxiang','洋流')
    #g.resetPro('三江源地区','湖泊','特征',"湖泊和沼泽是三江源地区重要的调蓄器。它们和雪山、冰川一起，使长江、黄河、澜沧江的水源源不断，流向大海。三江源地区的湖泊、沼泽对河流流量起着天然的调蓄作用。","区域")



