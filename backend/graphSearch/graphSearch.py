# @Language: python3
# @File  : graphSearch.py
# @Author: LinXiaofei
# @Date  : 2020-05-01
"""

"""





import requests
import numpy as np
from backend.data.data_process import read_file
import configparser

config = configparser.ConfigParser()
config.read("../backend/config.ini")
subject = config['DEFAULT']['subject']

repertoryName = config['TRANSFORM'][subject]


class graphSearch(object):

    def __init__(self):
        

        self.adapetion_stop = {'湖泊':['出处','图片']}

    def getAll(self):
        uri = "http://localhost:8004/getAll?repertoryName=" + repertoryName
        r = requests.post(uri)
        tri_list = list(r.json())
        return tri_list




    def getRelByType(self,type):
        """
        获得某个类型的实体的所有属性
        :param type:
        :return:
        """
        uri = "http://localhost:8004/getRelByType?repertoryName="+repertoryName+"&type="+type
        r = requests.post(uri)
        rel_list = list(r.json())

        return rel_list

    def getProByType(self,type):
        """
        获得某个类型的实体的所有属性
        :param type:
        :return:
        """
        uri = "http://localhost:8004/getProByType?repertoryName="+repertoryName+"&type="+type
        r = requests.post(uri)
        pro_list = list(r.json())

        return pro_list

    def getPredicate(self,label):
        """
        通过标签得到原始谓词
        :param label:
        :return:
        """

        uri = "http://localhost:8004/getProPredicate?repertoryName="+repertoryName+"&label="+label
        r = requests.post(uri)
        ans = list(r.json())
        if len(ans)>0:
            predicate = list(r.json())[0]
            return predicate
        return None

    def getRelPredicate(self,label):
        """
        通过标签得到原始谓词
        :param label:
        :return:
        """
        uri = "http://localhost:8004/getRelPredicate?repertoryName="+repertoryName+"&label="+label
        r = requests.post(uri)
        predicate = list(r.json())[0]

        return predicate

    def getSubject(self, label):
        """
        通过标签得到原始主语/宾语
        :param label:
        :return:
        """
        uri = "http://localhost:8004/getSubject?repertoryName="+repertoryName+"&label=" + label

        r = requests.post(uri)
        subject = list(r.json())
        if subject is not None and len(subject) > 0:
            return subject[0]
        return None

    def getValueByPro(self,type,property):
        """
        该类型实体的某一属性对应的值
        :param type:
        :param property:
        :return:
        """
        uri = "http://localhost:8004/getValueByPro?repertoryName="+repertoryName+"&entityType=" + type+"&property="+property
        r = requests.post(uri)
        value_list = list(r.json())
        return value_list

    def resetTripleToRepertory(self,data):
        """
        重置属性
        :param data:
        :return:
        """
        uri = "http://localhost:8004/resetTripleToRepertory?"
        ret = requests.post(uri, data=data)
        print(ret)

    def resetRelTripleToRepertory(self,data):
        """
        重置属性到关系
        :param data:
        :return:
        """
        uri = "http://localhost:8004/resetRelTripleToRepertory?"
        ret = requests.post(uri, data=data)
        print(ret)

    def getValueByRel(self,type,property):
        """
        该类型实体的某一关系对应的值
        :param type:
        :param property:
        :return:
        """
        uri = "http://localhost:8004/getValueByRel?repertoryName="+repertoryName+"&entityType=" + type+"&relation="+property
        r = requests.post(uri)
        value_list = list(r.json())
        return value_list

    def addTripleToRepertory(self,tripleList):
        """
        添加属性(现有)
        :param subj:
        :param pred:
        :param obje:
        :return:
        """

        data = {'repertoryName': repertoryName, 'tripleList': str(tripleList)}
        uri = "http://localhost:8004/addTripleToRepertory?"
        ret = requests.post(uri, data=data)
        print(ret)


    def addRelTripleToRepertory(self,tripleList):
        """
        添加属性(现有)
        :param subj:
        :param pred:
        :param obje:
        :return:
        """
        data = {'repertoryName': repertoryName, 'tripleList': str(tripleList)}
        uri = "http://localhost:8004/addRelToRepertory?"
        ret = requests.post(uri, data=data)
        print(ret)

    def deleteTripleToRepertory(self,tripleList):
        """
        添加属性(现有)
        :param subj:
        :param pred:
        :param obje:
        :return:
        """

        data = {'repertoryName': repertoryName, 'tripleList': str(tripleList)}
        uri = "http://localhost:8004/deleteTripleToRepertory?"
        ret = requests.post(uri, data=data)
        print(ret)

    def deleteRelToRepertory(self,tripleList):
        """
        添加属性(现有)
        :param subj:
        :param pred:
        :param obje:
        :return:
        """
        data = {'repertoryName': 'geo4', 'tripleList': str(tripleList)}
        uri = "http://localhost:8004/deleteRelToRepertory?"
        ret = requests.post(uri, data=data)
        print(ret)

    def deleteProperty(self,label):

        propertyUri = self.getPredicate(label)
        print(propertyUri)
        data = {'repertoryName': 'geo4', 'propertyUri': propertyUri}
        uri = "http://localhost:8004/deleteCurProperty?"
        ret = requests.post(uri,data=data)
        print(ret)

    def deleteRelation(self,label):

        propertyUri = self.getRelPredicate(label)
        print(propertyUri)
        data = {'repertoryName': 'geo4', 'propertyUri': propertyUri}
        uri = "http://localhost:8004/deleteCurProperty?"
        ret = requests.post(uri,data=data)
        print(ret)

    def addProperty(self,propertyName,pinyinName):

        data = {'repertoryName': 'geo4', 'propertyName': propertyName, 'pinyinName':pinyinName}
        uri = "http://localhost:8004/addProperty?"
        ret = requests.post(uri, data=data)
        print(ret)

    def addRelation(self, relationName, pinyinName):

        data = {'repertoryName': 'geo4', 'relationName': relationName, 'pinyinName': pinyinName}
        uri = "http://localhost:8004/addRelation?"
        ret = requests.post(uri, data=data)
        print(ret)

    def deleteTripleBySAP(self,subject,predicate):

        data = {'repertoryName': 'geo4', 'subject': subject, 'predicate': predicate}
        uri = "http://localhost:8004/deleteTripleBySAP?"
        ret = requests.post(uri, data=data)
        print(ret)



    #======================================self modify=========================================
    def completionGraph(self, ent, type):

        uri = "https://api.ownthink.com/kg/knowledge?entity=" + ent
        r = requests.post(uri)

        if r.json()['message'] == 'success':
            print(r.json())
            ans_dict = dict(r.json()['data'])
            # print(ans_dict)
            if 'avp' in ans_dict.keys():
                inf_dict = dict(r.json()['data']['avp'])

                return inf_dict
        return None

    # ======================================pedia modify=========================================


    def  getTypeProList(self, type):
        """
        获取某一类型的所有有用属性的属性列表，并生成相关文件
        :param type: 类型
        :return:无
        """

        stop_list =  self.adapetion_stop[type]

        uri = "http://localhost:8004/getTypeProList?repertoryName=geo4&type=" + type
        r = requests.post(uri)
        pro_list = list(r.json())
        w = open("prolist_"+type+".txt","w")
        write_lines = []


        for p in pro_list:
            if p[1] in stop_list:
                continue
            if p[0]+" "+p[1]+" "+p[2]+"\n" not in write_lines:
                 write_lines.append(p[0]+" "+p[1]+" "+p[2]+"\n")
        for line in write_lines:
            w.writelines(line)


    def questionPatternByType(self,type):
        """
        根据类型和模版文件得到该类型所有的问句模版
        :param type: 类型
        :return: 该类型对应的属性的所有问句模版
        """
        file_list = read_file(project_path + "/dealNLU/lake.txt")

        pro_list = self.getProByType(type)

        type_pro_pattern = []
        for p in pro_list:
            if p not in file_list:
                continue


            p_index = file_list.index(p)
            for pattern_index in range(p_index+1,len(file_list)):
                if file_list[pattern_index] == "end":
                    break
                type_pro_pattern.append(file_list[pattern_index])

        return type_pro_pattern

    def GenerationQuestionToFile(self,type):
        """
        根据问句模版生成问句

        :param type: 类型
        :return: 无
        """


        uri = "http://localhost:8004/getEntityByType?repertoryName=geo4&entityName=" + type
        r = requests.post(uri)
        ent_list = list(r.json())
        type_pro_pattern = self.questionPatternByType(type)

        w = open("question_generation_" + type + ".txt", "w")
        write_lines = []

        for ent in ent_list:
            for pa in type_pro_pattern:
                line = pa.replace("ent",ent)
                write_lines.append(line + "\n")
            #write_lines.append("====================================\n")

        for line in write_lines:
            w.writelines(line)


    def getQuestionListToFile(self,type):
        """

        :param type: 类型
        :return:
        """
        pro_name_list = self.getProByType(type)
        stop_list = self.adapetion_stop[type]
        for s in stop_list:
            pro_name_list.remove(s)


    # ======================================question adapetion===================================



    # ===========================================================================================





    def getEntByfuzzySearch(self, description):
        """
        模糊查询属性值得到实体

        :param words:
        :return:
        """

        uri = "http://localhost:8004/fuzzySearch?repertoryName="+repertoryName+"&description=" + description
        r = requests.post(uri)
        ent_list = list(r.json())

        return ent_list[0]

    def getCompareKeyword(self, description,entity):
        """
        模糊查询属性值得到实体

        :param words:
        :return:
        """

        print(description,entity)

        uri = "http://localhost:8004/getCompareKeyword?repertoryName="+repertoryName+"&description=" + description+"&entityname="+entity
        r = requests.post(uri)
        ent_list = list(r.json())

        return ent_list

    def searchEntity(self, entity):
        """
        根据标签分别查找该标签对应的属性和关系信息(同名实体一起)

        :param entity: 实体标签
        :return: 属性列表，关系列表
        """

        """获取属性信息"""
        uri = "http://localhost:8004/getEntityByLabelWithPro?repertoryName="+repertoryName+"&entityName=" + entity
        r = requests.post(uri)
        pro_list = list(r.json())

        """获取关系信息"""
        uri = "http://localhost:8004/getEntityByLabelWithRel?repertoryName="+repertoryName+"&entityName=" + entity
        r = requests.post(uri)
        rel_list = list(r.json())
        return pro_list, rel_list

    def searchEntityProName(self, entity):
        """
        根据标签分别查找该标签对应的属性和关系信息(同名实体一起)

        :param entity: 实体标签
        :return: 属性/关系名称列表
        """

        """获取属性信息"""
        uri = "http://localhost:8004/getEntityByLabelWithProName?repertoryName=geo4&entityName=" + entity
        r = requests.post(uri)
        pro_list = list(r.json())
        return pro_list

    def dealWithEnitity(self, entity):
        """
        根据实体list查找图谱中该标签的实体的信息(同名实体一起)
        :param find_entity: 抽取的实体
        :return: 返回实体具体信息（属性和关系）或 None

        """
        ans = {}
        if len(entity) > 0:
            for e in entity:
                pro_list, rel_list = self.searchEntity(e)
                ans[e] = {'p': pro_list, 'r': rel_list}
                print("查询的实体: ", e,ans[e])
        if ans == {}:
            return None
        else:
            return ans
    """
    def dealWithEnitityPro(self, entity):
        #得到实体的属性列表
        ans = {}
        if len(entity) > 0:
            for e in entity:
                pro_list = self.searchEntityProName(e)
                ans[e] = pro_list
        if ans == {}:
            return None
        else:
            return ans
    """


    def getNums(self,entity, property):
        """
        匹配抽出的属性名称和实体具有的属性名称，与上面的函数不同的是返回形式，上面哪个是多个同名属性放在一个字典里，然后又包在实体属性对字典里

        :param find_pro: 抽取的属性
        :param find_rel: 抽取的关系
        :param entity_deal: 携带信息的实体
        :return: 属性值列表，如果不存在设置为N/A，该函数为比较和计算模块服务
        """
        entity_deal = self.dealWithEnitity(entity)
        ans = []
        for name, content in entity_deal.items():
            flag = False

            pro = np.array(content['p'])

            for p in pro:
                if p[0] in property:
                    flag = True
                    ans.append(p[1])
                    break
            if flag == False:
                ans.append('N/A')

        if len(ans)<1:
            return None
        else:

            return ans


    def getProList(self, entity):
        """
        得到一个实体的属性关系名称
        :param entity: 实体名称
        :return: 实体的属性（限制了类型）
        """

        uri = "http://localhost:8004/getPro?repertoryName="+repertoryName+"&entity=" + entity
        r = requests.post(uri)
        pro_list = list(r.json())

        if pro_list == []:
            return None

        return pro_list
    """
    def getProByLabel(self,label):
        
        uri = "http://localhost:8004/getProByLabel?repertoryName=geo4&label="+label
        r = requests.post(uri)
        pro_list = list(r.json())

        return pro_list
    """

    def getRelList(self, entity):
        """
        得到一个实体的属性关系名称
        :param entity: 实体名称
        :return: 实体的关系名
        """

        uri = "http://localhost:8004/getRel?repertoryName="+repertoryName+"&entity=" + entity
        r = requests.post(uri)
        rel_list = list(r.json())

        if rel_list == []:
            return None

        return rel_list

    def getEntityByType(self, etype):
        """
        得到实体的子类
        :param entity: 实体
        :return: 实体子类
        """


        """获取子类"""
        uri = "http://localhost:8004/getEntityByType?repertoryName="+repertoryName+"&entityName=" + etype
        r = requests.post(uri)
        son_list = list(r.json())

        if son_list == []:
            return None

        return son_list

    def getFather(self, entity):
        """
        得到实体的父类
        :param entity: 实体
        :return: 实体父类
        """

        """获取父类"""
        uri = "http://localhost:8004/getFather?repertoryName="+repertoryName+"&entityName=" + entity

        r = requests.post(uri)
        father_list = list(r.json())

        if father_list == []:
            return None
        return father_list

    def getObjectBySAPLimitType(self,subject,predicate,keytype):
        """
        找到某类实体与特定主语和特定谓语有连线的实例
        :param subject:
        :param predicate:
        :param keytype:
        :return:
        """
        uri = "http://localhost:8004/getObjectBySAPLimitType?repertoryName=geo4&entity=" + subject + "&relation=" + predicate + "&type=" + keytype
        r = requests.post(uri)
        obj_list = list(r.json())
        if obj_list is None:
            return []
        return obj_list


    def getEntityByRelLimitType(self, entity,property,keyword):
        """
        根据关系名和关系值，得到实体，并受限于实体类型
        找到某类实体与特定宾语和谓词有连线的实例
        :param entity: 实体类系
        :param property: 关系名
        :param keyword: 关系值
        :return: 实体列表
        """


        uri = "http://localhost:8004/entitySearchByRelLimitType?repertoryName="+repertoryName+"&entity="+entity+"&relation="+property+"&type="+keyword
        r = requests.post(uri)
        ent_list = list(r.json())

        if ent_list == []:
            return None

        return ent_list

    def getSubByLimit(self, keyword, entity):
        """

        没检测到使用
        得到实体子类中属性值包含keyword的那些子类
        :param keyword:
        :param entity:
        :return:
        """

        sub_entity = []

        son_list = self.getEntityByType(entity[0])
        deal_entity = self.dealWithEnitity(son_list)

        for name, content in deal_entity.items():
            flag = False

            rel = np.array((content['r']))
            for r in rel:
                if keyword[0] in r[1]:
                    sub_entity.append(name)
                    flag = True
                    break

            if flag:
                continue

            pro = np.array(content['p'])
            for p in pro:
                if keyword[0] in p[1]:
                    sub_entity.append(name)
                    break

        if sub_entity != []:

            return sub_entity
        return None













