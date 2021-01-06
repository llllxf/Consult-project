# @Language: python3
# @File  : pediaToGeo.py
# @Author: LinXiaofei
# @Date  : 2020-06-04
"""
从百科图谱到k12地理图谱
"""

import sys
import os
project_path = os.path.abspath(os.path.join(os.getcwd(), ".."))
# print(project_path)
sys.path.append(project_path)
from data.data_process import read_file

from nlu.LTPUtil import LTPUtil
from graphSearch.graphSearch import graphSearch
import numpy as np
class pediaToGeo(object):
    def __init__(self):
        """
        图谱工具
        """
        self.search_util = graphSearch()
        """
        转换工具
        """
        """
        河流同一属性：位于（地理位置），流域面积，长度，主要支流，发源地，流经（国家，地区），地位，
        """
        self.rel = {'位于':['位于','地理位置','所属地区','所属国家','所属城市','地点','水区国家','所在地','地址'],
                          '流入':['流入','流入海域','注入','注入海洋','汇入','注入水域'],
                          '首都':['首都'],
                          '主峰':['主峰']}

        self.river_pro = {'流域面积':['流域面积','河流面积','面积','占地面积','地理面积'],'主要支流':['主要支流'],'发源地':['发源地','正源','源头位置','源头'],
                          '流经':['流经国家','流经地区','流经','干流长度'],'长度':['长度','河长','全长','长'],
                          '地位':['地位'],'别名':['别名','别称'],
                          '流向':['流向'],
                          '流量':['流量','平均流量']}

        self.lake_pro = {'海拔':['湖面海拔','海拔','平均海拔'],
                         '面积':['面积','湖泊面积','占地面积','总面积','地理面积'],
                         '蓄水量':['蓄水量','库容量','总蓄水量'],
                         '深度':['深度','平均水深','平均深度','最深处','最大深度','最深深度'],
                         '结冰期':['结冰期'],
                         '盐度':['盐度','含盐量'],
                         '别名':['别名','别称'],
                         '长度':['湖长','长','长度','湖泊长度'],
                         '宽度':['湖泊宽度','宽度','宽']}
        self.mountain_pro = {'经度':['经度'],'纬度':['纬度'],'排名':['世界排名','排名','次序'],
                             '海拔':['海拔','海拔高度','平均海拔','一般海拔','主峰海拔','高度'],
                             '别名':['别名','别称'],
                             '面积':['面积','占地面积','总面积','区域面积','跨地面积','山脉面积'],
                             '宽度':['宽度','宽','南北宽直距约','南北宽'],
                             '长度':['长度','长','东西长直距','东西长'],
                             '走向':['走向','方向']}
        self.hill_pro = {
            '海拔': ['海拔', '海拔高度', '平均海拔', '一般海拔', '主峰海拔', '高度'],
            '长度': ['长度', '长', '全长','东西长直距', '东西长'],
            '宽度': ['宽度', '宽', '南北宽直距约', '南北宽'],
            '别名': ['别名', '别称'],
            '走向': ['走向','方向']
        }

        self.ocean_pro = {'面积':['面积','海域面积','总面积','海洋面积','地理面积'],
                          '深度':['水深','平均水深','平均深度','海水深度','最大水深','最深处','最深点','最深深度'],
                          '盐度':['含盐度','平均含盐度','典型盐度','盐度'],
                          '蓄水量':['蓄水量'],
                          '长度':['全长','长度']}

        self.country_pro = {'面积':['国土面积','面积'],
                            '面积排名':['国土面积排名','面积排名'],
                            '宗教':['宗教','主要宗教'],
                            '人口数量':['人口数量','人口'],
                            '气候类型':['气候类型','气候','气候分布','主要气候','气候条件'],
                            '民族':['民族','主要民族'],
                            '人种':['人种'],
                            '简称':['简称'],
                            '别名':['别名','别称'],
                            '矿产资源':['矿产资源'],
                            '语言':['语言','官方语言']
                            }
        self.city_pro = {'面积':['面积','建城区面积'],
                         '人口数量': ['人口数量', '人口'],
                         '别名': ['别名', '别称'],
                         '气候类型': ['气候类型', '气候', '气候分布', '主要气候', '气候条件'],
                         '地位':['地位']
                         }
        self.province_pro = {
            '面积': ['面积', '建城区面积'],
            '人口数量': ['人口数量', '人口'],
            '别名': ['别名', '别称'],
            '简称': ['简称'],
            '气候类型': ['气候类型', '气候', '气候分布', '主要气候', '气候条件'],
            '地位': ['地位']

        }
        self.country_rel = {'首都':['首都'],
                            '位于':['']}



    def getEntWithoutCerPro(self,type,pro):
        f = open(project_path + "/data2/lake/"+pro+".txt", 'a')

        for t in type:
            ent_list = self.search_util.getEntityByType(t)

            unlake_ent = np.array(self.search_util.getValueByPro(t,pro))[:,0]
            for ent in ent_list:
                if ent not in unlake_ent:
                    f.writelines(ent+"\n")
        f.close()

    def getEntWithoutCerRAT(self,type,rel,limitType):
        f = open(project_path + "/data2/lake/"+rel+".txt", 'a')

        for t in type:
            ent_list = self.search_util.getEntityByType(t)



            for ent in ent_list:
                check_rel = np.array(self.search_util.getObjectBySAPLimitType(ent, rel,limitType))


                if len(check_rel)==0:
                    f.writelines(ent+"\n")
        f.close()

    def getProListByLabel(self,label):
        """
        将固定主语和属性且值有多条的三元组写入删除文件
        :param label:
        :return:
        """

        pro_list = self.search_util.getProByLabel(label)
        if pro_list is None:
            return None
        pro_dict = {}
        for inf in pro_list:
            name = inf[0]
            value = inf[1]
            if name in pro_dict.keys():
                pro_dict[name].append(value)

                pro_dict[name] = sorted(pro_dict[name], key=lambda i: len(i))
            else:
                pro_dict[name] = [value]
        f = open(project_path+"/data/operate/delete.txt",'a')
        for key,value in pro_dict.items():

            if len(value)>1:
                for v in value[1:]:
                    f.writelines(key+","+label+","+v+"\n")
        return pro_dict

    def addTripleToRepertory(self,filename,type):
        """
        添加一条三元组（属性）
        :param subj:
        :param pred:
        :param obje:
        :param type:
        :return:
        """
        log = open(project_path + "/data/log/" + type + ".txt","a")
        tripleList = read_file(project_path + "/data2/inf/"+filename+".csv")
        add_tripleList = []
        sub = []
        pre = []
        obj = []
        for triple in tripleList:


            inf_arr = triple.split(" ")

            pro_list = self.search_util.getProList(inf_arr[0])
            if pro_list is None:

                continue

            if inf_arr[1] in pro_list:

                continue
            sub.append(inf_arr[0])
            pre.append(inf_arr[1])
            obj.append(inf_arr[2])
            subject = self.search_util.getSubject(inf_arr[0])
            predicate = self.search_util.getPredicate(inf_arr[1])
            obje = inf_arr[2]
            print(subject,predicate,obje)
            add_tripleList.append({"subject":subject,"predicate":predicate,"object":obje})

        self.search_util.addTripleToRepertory(add_tripleList)
        for i in range(len(sub)):
            log.writelines("add:  " + sub[i]+ "-" + pre[i] + "-" + obj[i] + "\n")
            log.writelines("=========================================\n")

    def addRelTripleToRepertory(self,filename,type):
        """
        添加一条三元组（属性）
        :param subj:
        :param pred:
        :param obje:
        :param type:
        :return:
        """
        log = open(project_path + "/data/log/" + type + ".txt","a")
        tripleList = read_file(project_path + "/data2/inf/"+filename+".csv")
        add_tripleList = []
        sub = []
        pre = []
        obj = []
        for triple in tripleList:


            inf_arr = triple.split(" ")

            rel_list = self.search_util.getRelList(inf_arr[0])
            if inf_arr[1] in rel_list:
                print(inf_arr[0],inf_arr[1])
                continue

            obje = self.search_util.getSubject(inf_arr[2])
            if obje is None:
                #print(inf_arr[2])
                continue


            sub.append(inf_arr[0])
            pre.append(inf_arr[1])
            obj.append(inf_arr[2])

            subject = self.search_util.getSubject(inf_arr[0])
            predicate = self.search_util.getRelPredicate(inf_arr[1])

            print(subject,predicate,obje)
            add_tripleList.append({"subject":subject,"predicate":predicate,"object":obje})

        self.search_util.addRelTripleToRepertory(add_tripleList)

        for i in range(len(sub)):
            log.writelines("add:  " + sub[i]+ "-" + pre[i] + "-" + obj[i] + "\n")
            log.writelines("=========================================\n")


    def addForgetToRepertory(self,type):
        """
        添加一条三元组（属性）
        :param subj:
        :param pred:
        :param obje:
        :param type:
        :return:
        """
        log = open(project_path + "/data/log/" + type + ".txt","a")
        tripleList = read_file(project_path + "/data2/inf/forget_pro.csv")
        add_tripleList = []
        sub = []
        pre = []
        obj = []
        for triple in tripleList:


            inf_arr = triple.split(" ")

            pro_list = self.search_util.getProList(inf_arr[0])
            if inf_arr[1] in pro_list:
                print(inf_arr[0],inf_arr[1])
                continue
            sub.append(inf_arr[0])
            pre.append(inf_arr[1])
            obj.append(inf_arr[2])
            subject = self.search_util.getSubject(inf_arr[0])
            predicate = self.search_util.getPredicate(inf_arr[1])
            obje = inf_arr[2]
            print(subject,predicate,obje)
            add_tripleList.append({"subject":subject,"predicate":predicate,"object":obje})

        self.search_util.addTripleToRepertory(add_tripleList)

        for i in range(len(sub)):
            log.writelines("add:  " + sub[i]+ "-" + pre[i] + "-" + obj[i] + "\n")
            log.writelines("=========================================\n")

    def getInfForComplete(self, pro_dict,type):
        entity_list = self.search_util.getEntityByType(type)
        #entity_list = read_file(project_path + "/data/hl1.txt")
        f_pro = open(project_path + "/data2/inf/" + type + "_pro.csv", "w")
        f_rel = open(project_path + "/data2/inf/" + type + "_rel.csv", "w")
        count = 0
        for ent in entity_list:
            ent_arr = []
            count = count+1
            inf_dict = self.search_util.completionGraph(ent, type)

            if inf_dict is None:
                continue
            for key, value in inf_dict.items():
                #for r_key,r_value in self.river_pro.items():
                for r_key, r_value in pro_dict.items():
                    if key in r_value:
                        if r_key not in ent_arr:
                            ent_arr.append(r_key)
                            f_pro.writelines(ent + " " + r_key + " " + value + "\n\n")
                for r_key,r_value in self.rel.items():
                    if key in r_value:
                        f_rel.writelines(ent + " " + r_key + " " + value + "\n\n")

    def getInfForForget(self, type):
        entity_list = self.search_util.getEntityByType(type)
        #entity_list = read_file(project_path + "/data/hl1.txt")
        f_pro = open(project_path + "/data2/inf/forget_pro.csv", "w")


        for ent in entity_list:
            ent_arr = []

            inf_dict = self.search_util.completionGraph(ent, type)

            if inf_dict is None:
                continue
            for key, value in inf_dict.items():
                for r_key,r_value in self.foget.items():
                    if key in r_value:
                        if r_key not in ent_arr:
                            ent_arr.append(r_key)
                            f_pro.writelines(ent + " " + r_key + " " + value + "\n\n")


    def searchPedia(self,type):
        entity_list = self.search_util.getEntityByType(type)
        f = open(project_path + "/data2/inf/" + type + ".csv", "w")
        for ent in entity_list:
            inf_dict = self.search_util.completionGraph(ent,type)
            f.writelines(ent + "\n")
            f.writelines("-----------------------------------------\n")
            if inf_dict is None:
                continue
            for key, value in inf_dict.items():
                f.writelines(key + ": " + value + "\n")
            f.writelines("=========================================\n")

if __name__ == '__main__':
    p = pediaToGeo()
    #p.searchPedia('省')
    #p.getInfForComplete(p.country_pro,'省')
    #p.addRelTripleToRepertory('湖泊_rel','湖泊')
    #p.searchPedia('湖泊')
    #p.getInfForComplete('河流')

    #p.addTripleToRepertory('海洋_pro','海洋')

    # p.getInfForForget('河流')
    # p.addForgetToRepertory('河流')

    #p.getProListByLabel('流量')

    """
    p.getEntWithoutCerPro(['河流','山脉'],'长度')
    p.getEntWithoutCerPro(['湖泊','海洋'],'深度')
    p.getEntWithoutCerPro(['山峰', '山脉'], '海拔')

    p.getEntWithoutCerPro(['河流'],'流量')
    p.getEntWithoutCerPro(['河流'], '流域面积')

    p.getEntWithoutCerPro(['湖泊'], '面积')
    p.getEntWithoutCerPro(['湖泊'], '蓄水量')

   

    p.getEntWithoutCerPro(['海洋'], '盐度')

    p.getEntWithoutCerPro(['海洋'], '面积')
    """

    #p.getEntWithoutCerPro(['山峰'], '位于')
    #p.getEntWithoutCerRAT(['河流'], '位于','国家')





