# @Language: python3
# @File  : normalBussiness.py
# @Author: LinXiaofei
# @Date  : 2020-06-22
"""

"""


import numpy as np



from backend.graphSearch.graphSearch import graphSearch

import json


class normalBussiness(object):

    def __init__(self):
        self.graph_util = graphSearch()
        #self.form_util = formWords()





    def seacrchAll(self,longWords,shortWords):
        """

        :param longWords: 问句和属性值中较长的一方
        :param shortWords: 较短的一方
        :return: 较短的那方匹配情况
        """
        count = 0.
        for sw in shortWords:
            if sw in longWords:
                count = count+1
        return count

    def matchFuzzySearch(self, words, triple):
        """
        匹配三元组的o和句子
        """



        ans_con = []
        count_rate = []

        for name,key,value in triple:

            value = self.form_util.preProcessWords(value)
            while (name in words):
                words = words.replace(name, '')
            while (name in value):
                value = value.replace(name, '')
            count = self.seacrchAll(value, words)
            c_len = len(words)
            if float(count) / float(c_len) >= 0.65:
                ans_con.append([name,key,value])
                count_rate.append(count / c_len)

        if ans_con != []:

            max_index = np.argmax(np.array(count_rate))
            return ans_con[max_index]
        return None


    def matchProConWithPro(self, words, deal_entity,property):
        """
        根据实体携带的属性信息和问句原文匹配得到与答案相符的属性信息
        该函数制定了属性名字
        1. 遍历实体所有的属性信息
        2. 按字符匹配问句和属性信息
        3. 2得到空则按向量相似度得到匹配信息
        4. 2,3均空则返回空

        这个没有答案二次reverse匹配
        :param words: 问句
        :param deal_entity: 实体及其信息
        :return: 答案或空
        """


        ans_con = []
        count_rate = []


        for name, content in deal_entity.items():
            """
            抽取出的实体的属性
            """
            pro = np.array(content['p'])

            """
            去掉问题中的实体方便匹配
            """
            while (name in words):
                words = words.replace(name, '')

            for p in pro:
                if p[0] != property[0]:
                    continue
                con = self.form_util.preProcessWords(p[1])

                while (name in con):
                    con = con.replace(name, '')

                if len(con) > len(words):
                    c_len = len(words)
                    count = self.seacrchAll(con, words)

                else:

                    c_len = len(con)
                    count = self.seacrchAll(words, con)
                if float(count) / float(c_len) >= 0.65:
                    ans_con.append([name, p[0], p[1]])
                    count_rate.append(count / c_len)
        if ans_con != []:

            max_index = np.argmax(np.array(count_rate))
            return ans_con[max_index]
        return None


    def matchByProACon(self, words, deal_entity):
        """
        根据实体携带的属性信息和问句原文匹配得到与答案相符的属性信息
        1. 遍历实体所有的属性信息
        2. 按字符匹配问句和属性信息
        3. 2得到空则按向量相似度得到匹配信息
        4. 2,3均空则返

        有答案二次reverse匹配
        :param words: 问句
        :param deal_entity: 实体及其信息
        :return: 答案或空
        """

        ans_con = []
        count_rate = []

        for name, content in deal_entity.items():

            """
            抽取出的实体的属性
            """
            pro = np.array(content['p'])

            """
            去掉问题中的实体方便匹配
            """
            while (name in words):
                words = words.replace(name, '')

            for p in pro:

                con = self.form_util.preProcessWords(p[1])

                while (name in con):
                    con = con.replace(name, '')

                if len(con) > len(words):
                    c_len = len(words)
                    count = self.seacrchAll(con, words)
                else:
                    c_len = len(con)
                    count = self.seacrchAll(words, con)
                if c_len == 0:
                    continue
                if float(count) / float(c_len) >= 0.65:
                    ans_con.append([name, p[0], p[1]])
                    count_rate.append(count / c_len)
        if ans_con != []:
            revers_count = []

            for ans in ans_con:
                if len(words) >= len(ans[2]):
                    revers_count.append(self.seacrchAll(words, ans[2]) / len(words))
                else:
                    revers_count.append(self.seacrchAll(ans[2], words) / len(ans[2]))
            max_index = np.argmax(np.array(revers_count))
            return ans_con[max_index]
        return None


    #======================================================================


    def searchBinaryFactoidAll(self,entity, property):
        """
        匹配抽出的属性名称和实体具有的属性名称

        :param find_pro: 抽取的属性
        :param find_rel: 抽取的关系
        :param entity_deal: 携带信息的实体
        :return:字典，形式入{实体:{属性名:属性值}}
        """

        entity_deal = self.graph_util.dealWithEnitity(entity)

        ans = []

        for name, content in entity_deal.items():

            pro = np.array(content['p'])


            for p in pro:
                if p[0] == property:

                    ans.append(name,p[1])

        if ans == []:
            return None
        else:
            return ans



    def searchBinaryFactoid(self,entity, property):
        """
        匹配抽出的属性名称和实体具有的属性名称

        :param find_pro: 抽取的属性
        :param find_rel: 抽取的关系
        :param entity_deal: 携带信息的实体
        :return:字典，形式入{实体:{属性名:属性值}}
        """

        entity_deal = self.graph_util.dealWithEnitity(entity)

        ans = []

        name, content = list(entity_deal.items())[0]
        pro = np.array(content['p'])
        for p in pro:
            if p[0] == property:
                ans.append(entity[0])
                ans.append(p[0])
                ans.append(p[1])
                return ans
        if ans == []:
            return None
        else:
            print(ans)
            return ans

    def getOneEntity(self,entity):
        entity_deal = self.graph_util.dealWithEnitity([entity])
        ans = {}
        ans['entity']=entity
        name, content = list(entity_deal.items())[0]
        pro = np.array(content['p'])
        for p in pro:
            if p[0] in ans.keys():
                continue
            else:
                ans[p[0]] = p[1]
        return ans


    def matchByProName(self,entity, property):
        """
        匹配抽出的属性名称和实体具有的属性名称

        :param find_pro: 抽取的属性
        :param find_rel: 抽取的关系
        :param entity_deal: 携带信息的实体
        :return:字典，形式入{实体:{属性名:属性值}}
        """
        #print(entity,property,"???")
        entity_deal = self.graph_util.dealWithEnitity(entity)

        ans = {}

        for name, content in entity_deal.items():
            name_dict = {}
            pro = np.array(content['p'])
            for p in pro:
                if p[0] in property:

                    if p[0] in name_dict.keys():
                        name_dict[p[0]].append(p[1])
                    else:
                        name_dict[p[0]] = [p[1]]

            if name_dict != {}:
                ans[name]=name_dict

        if ans == {}:
            return None
        else:
            print(ans)
            return ans
    def matchByRelName(self,entity, property):
        """
        匹配抽出的关系名称和实体具有的关系名称，返回形式如matchByProName

        :param find_pro: 抽取的属性
        :param find_rel: 抽取的关系
        :param entity_deal: 携带信息的实体
        :return:
        """
        entity_deal = self.graph_util.dealWithEnitity(entity)


        ans = {}

        for name, content in entity_deal.items():

            name_dict = {}

            rel = np.array(content['r'])
            for r in rel:
                if r[0] in property:
                    if r[0] in name_dict.keys():
                        name_dict[r[0]].append(r[1])
                    else:
                        name_dict[r[0]] = [r[1]]
            if name_dict != {}:
                ans[name]=name_dict

        if ans == {}:
            return None
        else:
            return ans

    def taskNormalPro(self, entity, property):
        ans = self.matchByProName(entity, property)
        return ans



    def taskNormalRel(self, entity, property):
        """
        根据实体和关系名称得到三元组
        :param entity:
        :param property:
        :return:
        """
        ans = self.matchByRelName(entity, property)

        return ans

    def taskTAPAO(self, words, entity, property):
        """
        给出属性和实体类型以及问句，匹配得到精度最高的实体（闽是哪个省的简称）

        :param words:
        :param entity:
        :param property:
        :return:
        """

        son_list = self.graph_util.getEntityByType(entity[0])
        if son_list == None:
            return None
        deal_entity = self.graph_util.dealWithEnitity(son_list)
        ans = self.matchProConWithPro(words, deal_entity, property)
        return ans


    def taskTARAO(self, entity, property, keyword):
        """
        给出关系和宾语，得到主语，并限制主语的类型
        :param entity: 实体类型
        :param property: 关系
        :param keyword: 宾语
        :return:
        """

        ans = self.graph_util.getEntityByRelLimitType(keyword[0], property[0], entity[0])
        if ans != None:
            return ans
        return None

        return ans

    def taskSTAO(self, words, entity):
        """
        给出主语和宾语，得出谓词
        给出主语类型和宾语，确定主语和谓词


        :param words: 问句（代表宾语）
        :param entity: 实体或实体类型（主语）
        :return: 三元组
        """

        deal_entity = self.graph_util.dealWithEnitity(entity)
        ans = self.matchByProACon(words, deal_entity)

        if ans != None:
            return ans
        son_list = self.graph_util.getEntityByType(entity[0])
        if son_list == None:
            return None
        deal_entity = self.graph_util.dealWithEnitity(son_list)
        ans = self.matchByProACon(words, deal_entity)
        return ans


    def taskReverse(self, words, key_words):
        """
        从属性关键词找到对应实体及三元组，然后得到与句子最匹配的三元组
        :param words:
        :param key_words:
        :return:
        """
        triple = self.graph_util.getEntByfuzzySearch(key_words[0])
        ans = self.matchFuzzySearch(words, triple)
        return ans


    #==================================================================


    def doNormal(self,entity,property):

        ans = self.searchBinaryFactoid(entity,property)
        if ans is None:
            return [entity[0],property,'对不起，没有'+entity[0]+"关于"+property+"的信息"]

        return ans

    def compareContent(self, entity, con_cnt, con_pro):
        con = con_cnt[0]
        word_count = con_cnt[1]

        print("compareContent",con,word_count)

        con_count = []


        entity_value = self.graph_util.dealWithEnitity(entity)


        con_value = []

        name, content = list(entity_value.items())[0]
        pro = np.array(content['p'])
        for p in pro:
            temp_c = 0
            if p[0] in con_pro:
                for c in range(len(con)):
                    if con[c] in p[1]:
                        print(con[c],p[1])
                        temp_c += word_count[c]

            print(temp_c,temp_c/len(con))

            if temp_c>=len(con):
                con_count.append(temp_c)
                con_value.append(p[1])

        print(con_count)
        print(con_value)

        if len(con_value) == 0:
            return None
        else:
            return con_value[np.argmax(con_count)]

    def doNormalbyCon(self, entity, con, conpro):
        return self.compareContent(entity,con, conpro)

    def doNormalForFalse(self, entity, con_cnt):

        print(entity)

        print("asdhgalshjdgsajkdashd")
        print(con_cnt)

        con = con_cnt[0]
        word_count = con_cnt[1]
        print(con,word_count)
        con_count = []
        con_value = []
        value_list = self.graph_util.fuzzySearchForNormalFalse("?o",entity)
        for v in value_list:
            temp_c = 0
            for c in range(len(con)):
                if con[c] in v[2]:
                    print(v)
                    temp_c += word_count[c]

            if temp_c>=len(con):
                con_count.append(temp_c)
                con_value.append(v[0]+":"+v[2])

        print(con_count,con_value,"asdaskdjgasdjlagsdh")

        if len(con_value) == 0:
            return None
        else:
            return con_value[np.argmax(con_count)]

    def doCon(self, entity, con_cnt):
        con = con_cnt[0]
        word_count = con_cnt[1]

        name = []
        content = []
        count = []
        pro_list = self.graph_util.getProByType(entity)
        for pro in pro_list:

            value_list = self.graph_util.getValueByPro(entity,pro)
            print(value_list)
            for value in value_list:
                temp = 0
                for c in range(len(con)):
                    if con[c] in value[1]:
                        print(con[c],word_count[c],value[0])
                        temp += word_count[c]
                if temp>=len(con):
                    name.append(value[0])
                    content.append(value[1])
                    count.append(temp)
        if len(count)==0:
            return None
        max_count_index = np.argmax(count)

        print(name)
        print(count)
        print(len(content),count[max_count_index],count[max_count_index]/len(content))
        if count[max_count_index]>=len(con):

            return name[max_count_index]+": "+content[max_count_index]
        else:
            return None

    def doMost(self,etype,match):
        print("doMost",etype,match)


        tri_list = self.graph_util.fuzzySearchOne("?plabel","特征",etype)
        for i in range(len(tri_list)):
            flag = True
            for m in match:
                if m not in tri_list[i][2]:
                    flag = False
                    break
            if flag:
                return tri_list[i][0]


        most_pro = ['地位','作用','定义','内容']
        for p in most_pro:
            result = self.graph_util.getValueByPro(etype,p)
            for i in range(len(result)):
                flag = True
                for m in match:
                    if m not in result[i][1]:
                        flag = False
                        break
                if flag:
                    return result[i][0]

        if '世界' in match or '地球' in match:
            for i in range(len(tri_list)):
                flag = True
                for m in match:
                    if m == '世界' or m == '地球':
                        continue
                    if m not in tri_list[i][2]:
                        flag = False
                        break
                if flag:
                    return tri_list[i][0]
            for i in range(len(result)):
                flag = True
                for m in match:
                    if m == '世界' or m == '地球':
                        continue
                    if m not in result[i][1]:
                        flag = False
                        break
                if flag:
                    return result[i][0]

        return None



    def searchEnt(self,entity,property):
        pro_list = self.graph_util.getValueByPro(entity,property)
        return pro_list


    def doNormal2(self,words,task_type,entity,property,keywords):


        if task_type == 'task_normal_pro':

            ans = self.taskNormalPro(entity,property)

            if ans != None:
                return entity[0], "ans_items", ans

        if task_type == 'task_normal_rel':
            ans = self.taskNormalRel(entity,property)
            if ans != None:
                return entity[0], "ans_items", ans

        if task_type == 'task_son_kw_match':
            ans = self.taskTARAO(entity, property,keywords)
            if ans != None:
                return keywords[0], "ans_list", ans
            else:
                return keywords[0],None,None

        if task_type == 'task_son_match':
            ans = self.taskTAPAO(keywords,entity,property)
            if ans != None:
                return entity[0], "ans_triple", ans

        if task_type == 'task_singal_entity':
            ans = self.taskSTAO(words,entity)
            if ans != None:
                return entity[0], "ans_triple", ans

        if task_type == 'task_reverse' and len(entity)>0:
            ans = self.taskReverse(words,entity)
            if ans != None:
                return entity[0], "ans_triple", ans


        if len(entity)==0 or entity == None:

            return None,None,None

        return entity[0], None, None