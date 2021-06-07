# @Language: python3
# @File  : normalBussiness.py
# @Author: LinXiaofei
# @Date  : 2020-06-22
"""

"""


import numpy as np
import configparser

from backend.graphSearch.graphSearch import graphSearch
from backend.semantic_similarity.similarity import Similarity
from backend.nlu.LTPUtil import LTPUtil
import json


class normalBussiness(object):

    def __init__(self):
        config = configparser.ConfigParser()
        config.read("../backend/config.ini")
        self.subject = config['DEFAULT']['subject']



        self.a = float(config[self.subject]['a'])
        self.b = float(config[self.subject]['b'])
        self.cilin = (config[self.subject]['cilin']=='True')
        self.embedding = (config[self.subject]['embedding']=='True')

        self.wether_rel = (config[self.subject]['wether_rel'] == 'True')
        config.read("../backend/data/" + self.subject + "/proconfig.ini")
        if self.wether_rel:
            self.relconfig = config
        self.graph_util = graphSearch()
        self.ltp_util = LTPUtil()


    def seg_sentence(self,words,entity):
        words_list_1 = []
        words_list_2 = []

        if '\n' in words:
            words_list_1 = words.split("\n")
        if '。' in words:
            words_list_2 = words.split("。")

        if len(words_list_2)>len(words_list_1):
            print("words_list_2",words_list_2)


            temp = ""
            for words in words_list_2:
                if entity in words:
                    temp = words

            return temp
        elif len(words_list_1)>0:
            print("words_list_1", words_list_1,entity)
            temp = ""
            for words in words_list_1:
                if entity in words:
                    temp = words
            print("抽取的句子====================")
            print(temp)
            return temp
        else:
            print("抽取的句子====================")
            print(words)
            return words

    def getWordsSimilarCount(self,words,words_count,words_name,question,entity,sum_score):
        pass
        """

        sort_index = np.argsort(words_count)
        words = np.array(words)[sort_index]
        words_count = np.array(words_count)[sort_index]
        question = "".join(question)
        best_count = 0
        best_index = -1

        for i in range(3):

            index = len(words) - i - 1
            if index<0:
                break

            key_words = self.seg_sentence(words[index],entity)
            if len(key_words)<=0:
                continue

            print("question,key_words",question,key_words)

            words_score = synonyms.compare(question,key_words)
            if words_score > best_count:
                best_count = words_score
                best_index = index
        if best_count > 0.4:
            return words_count[best_index]+0.2*sum_score,words[best_index],words_name[best_index]

        else:
            return words_count[len(words)-1],words[len(words)-1],words_name[len(words)-1]
        """

    def judgeCilin(self,count,pvalue,name,words,words_value):
        print("*************************************************")
        print(count)
        print(pvalue)
        print(name)
        print(words)
        print(words_value)
        print("*************************************************")

        sort_index = np.argsort(count)
        count = np.array(count)[sort_index]
        pvalue = np.array(pvalue)[sort_index]
        words = np.array(words)[sort_index]
        words_value = np.array(words_value)[sort_index]
        name = np.array(name)[sort_index]
        n_words = []


        if len(words)>=3:

            row_list = list(set(list(words[-1])+list(words[-2])+list(words[-3])))
            pos = list(self.ltp_util.get_postag(row_list))
            index_count = 0
            for w in row_list:
                if pos[index_count] in ['n','ns'] and (w not in words[len(words)-2] or w not in words[len(words)-3] or w not in words[len(words)-1]):
                    n_words.append(w)
                if pos[index_count] == 'nd':
                    n_words.append(w)
                index_count = index_count+1

        if len(words)==2:

            pos = list(self.ltp_util.get_postag(list(words[len(words)-1])))
            index_count = 0
            for w in words[len(words)-1]:
                if pos[index_count] in ['n', 'ns'] and w not in words[len(words)-2]:
                    n_words.append(w)

        best_index = -1
        best_count = 0

        for i in range(3):

            index = len(count) - i - 1
            if index<0:
                break

            pos = list(self.ltp_util.get_postag(list(words[index])))
            print("judgeCilin",words[index],pos)

            cilin_count = Similarity.calSimilarity(words[index], words_value[index], pvalue[index],n_words,pos,self.ltp_util)
            cilin_add = count[index] + cilin_count
            if cilin_add > best_count:
                best_count = cilin_add
                best_index = index
        if best_index>-1:

            return best_count,pvalue[best_index],name[best_index]
        else:
            return None,None,None

    def searchBinaryRelUseless(self,entity, relation):


        rel_list = self.graph_util.getEntityByLabelWithRel(entity[0])
        print("searchBinaryRel",relation,rel_list)

        ans = []


        for r in rel_list:
            print(r[0],relation)
            if r[0] == relation:

                ans.append(r[1])


        if ans == []:
            print(ans, "ans========================")
            return None
        else:
            print(ans,"ans========================")
            return ans


    def searchBinaryFactoid(self,entity, property):
        """
        匹配抽出的属性名称和实体具有的属性名称

        :param find_pro: 抽取的属性
        :param find_rel: 抽取的关系
        :param entity_deal: 携带信息的实体
        :return:字典，形式入{实体:{属性名:属性值}}
        """

        pro_list, rel_list = self.graph_util.searchEntity(entity[0])
        print("searchBinaryFactoid================")

        print(pro_list)

        print(rel_list)



        #entity_deal = self.graph_util.dealWithEnitity(entity)

        ans = []

        #name, content = list(entity_deal.items())[0]
        #pro = np.array(content['p'])
        for p in pro_list:
            print(p[0])
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

    def searchBinaryFactoidBackup(self,entity, property):
        """
        匹配抽出的属性名称和实体具有的属性名称

        :param find_pro: 抽取的属性
        :param find_rel: 抽取的关系
        :param entity_deal: 携带信息的实体
        :return:字典，形式入{实体:{属性名:属性值}}
        """

        pro = self.graph_util.searchEntityProBackup(entity[0])

        ans = []
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
            ans[p[0]] = p[1]
        return ans


    def getOneEntityRelation(self, entity):
        rel_list = self.graph_util.getEntityByLabelWithRelMore(entity)


        category = ""
        ans = {}
        ans_category = {}

        ans['entity'] = entity

        ans_category['entity'] = entity

        ans_relate = {}
        ans_relate['entity'] = entity

        for p in rel_list:
            if p[0] == '实体限制':
                ans_relate[p[1]] = p[0]
            else:
                ans[p[1]] = p[0]
            if p[0] == '分类' and '地理' not in p[0]:
                category = p[0]

        if len(category)>0:

            son_list = self.graph_util.getEntityByCategory(category)

            print(son_list,"son_list============================")

            for p in son_list[:8]:
                ans_category[p[0]] = "相似实体"

        return ans,ans_category,ans_relate


    def doNormal(self,entity,property):

        print("ans = self.searchBinaryFactoidBackup(entity,property)")

        ans = self.searchBinaryFactoid(entity,property)
        if ans is None:
            ans = self.searchBinaryFactoidBackup(entity,property)
            if ans is None:
                return [entity[0],property,'对不起，没有'+entity[0]+"关于"+property+"的信息"]

        return ans

    def compareContentStrict(self, entity, con_cnt, con_pro):
        con = con_cnt[0]
        word_count = con_cnt[1]


        if len(con) == 2 and sum(word_count)<20:
            return None


        print("compareContentStrict",con,word_count)

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
                        if con[c] == entity[0]:
                            temp_c += word_count[c]
                            continue
                        #print(con[c],p[1])
                        temp_c += word_count[c]

            if (temp_c >= (2*np.sum(word_count))/3 and len(con) > 2) or (temp_c == np.sum(word_count)):
                con_count.append(temp_c)
                con_value.append(p[1])

        #print(con_count)
        #print(con_value)

        if len(con_value) == 0:
            return None
        else:
            max_count = np.max(con_count)

            min_len = 1000
            best_value = ""
            for v_index in range(len(con_value)):
                if con_count[v_index] == max_count:
                    v_len = len(con_value[v_index])
                    if v_len < min_len:
                        best_value = con_value[v_index]

            return best_value


    def compareContent(self, entity, con_cnt, con_pro):
        """
        查询实体一般属性的属性值，匹配属性值于问句，即处理句型为：实体+属性值，实体是主语
        :param entity:实体
        :param con_cnt:匹配数据，共两个，第一个是匹配词汇，第二个是对应的词汇分数
        :param con_pro:每个科目匹配的属性
        :return:最适配属性值
        """
        con = con_cnt[0]
        word_count = con_cnt[1]

        lack_words = []
        lack_words_value = []

        print("compareContent",con,word_count,entity)

        con_count = []
        entity_value = self.graph_util.dealWithEnitity(entity)
        con_value = []
        con_name = []

        bad_value = []
        bad_count = []
        bad_name = []
        delete_sum = 0
        for c in range(len(con)):
            if con[c] == entity[0]:
                delete_sum += word_count[c]


        name, content = list(entity_value.items())[0]
        pro = np.array(content['p'])
        for p in pro:
            temp_c = 0

            temp_lack_words = []
            temp_lack_words_value = []
            if p[0] in con_pro:

                for c in range(len(con)):
                    if con[c] == entity[0]:
                        continue
                    if con[c] in p[1]:
                        temp_c += word_count[c]
                    else:
                        temp_lack_words.append(con[c])
                        temp_lack_words_value.append(word_count[c])

            #print("temp_c",temp_c)

            if (temp_c>=(self.a*(np.sum(word_count)-delete_sum)) and len(con)>2) or (temp_c == (np.sum(word_count)-delete_sum)):
                con_count.append(temp_c)
                con_value.append(p[1])
                con_name.append(name)

            bad_count.append(temp_c)
            bad_value.append(p[1])
            bad_name.append(name)
            lack_words.append(temp_lack_words)
            lack_words_value.append(temp_lack_words_value)


        #print("con_count",con_count)
        #print("delete_sum",delete_sum,np.sum(word_count))

        if len(bad_value) == 0:
            return None

        elif self.cilin:


            if len(con_value) > 0 and np.max(con_count)/(np.sum(word_count)-delete_sum)>=0.6:
                max_count = np.max(con_count)
                min_len = 1000

                for v_index in range(len(con_value)):
                    if con_count[v_index] == max_count:
                        v_len = len(con_value[v_index])
                        if v_len < min_len:
                            min_len = v_len
                            best_value = con_value[v_index]
                            best_name = con_name[v_index]
                return best_name+":"+best_value



            best_count, best_value, best_name = self.judgeCilin(bad_count, bad_value, bad_name, lack_words,
                                                                lack_words_value)
            if best_count and (best_count >= (np.sum(word_count)-delete_sum) * self.b):
                return best_name+":"+best_value
        elif self.embedding and len(con)>2:

            embedding_count,best_value,best_name = self.getWordsSimilarCount(bad_value,bad_count,bad_name,con,entity[0],np.sum(word_count))
            if embedding_count >= self.a * (np.sum(word_count)-delete_sum):
                return best_value

        elif len(con_value) == 0:
            return None

        else:

            max_count = np.max(con_count)
            min_len = 1000
            best_value = ""
            for v_index in range(len(con_value)):
                if con_count[v_index] == max_count:
                    v_len = len(con_value[v_index])
                    if v_len < min_len:
                        min_len = v_len
                        best_value = con_value[v_index]
                        best_name = con_name[v_index]

            return best_name+":"+best_value
        return None

    def compareContentYear(self, entity, con_cnt, con_pro):
        con = con_cnt[0]
        word_count = con_cnt[1]

        print("compareContentYear",con,word_count,entity)

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

            #if (temp_c>=(np.sum(word_count)/3) and len(con)>2) or (temp_c == np.sum(word_count)):
            if '年' in p[1] or '世纪' in p[1] or '公元' in p[1]:
                con_count.append(temp_c)
                con_value.append(p[1])

        print(con_count)
        print(con_value)

        if len(con_value) == 0:
            return None
        else:
            max_count = np.max(con_count)
            min_len = 1000
            best_value = ""
            for v_index in range(len(con_value)):
                if con_count[v_index] == max_count:
                    v_len = len(con_value[v_index])
                    if v_len < min_len:
                        best_value = con_value[v_index]

            return best_value

    def doNormalbyConStrict(self, entity, con, conpro):
        return self.compareContentStrict(entity, con, conpro)

    def doNormalbyCon(self, entity, con, conpro):
        return self.compareContent(entity,con, conpro)

    def doNormalForFalse(self, entity, con_cnt):

        if len(entity)==0:
            return None, None

        con = con_cnt[0]
        word_count = con_cnt[1]
        print(con,word_count)
        con_count = []
        con_value = []
        con_name = []
        lack_words = []
        lack_words_value = []
        bad_count = []
        bad_value = []
        bad_name = []
        delete_sum = 0
        for c in range(len(con)):
            if con[c] == entity:
                print(entity,c,con[c],word_count[c],word_count)
                delete_sum += word_count[c]

        value_list = self.graph_util.fuzzySearchForNormalFalse("?o",entity)
        for v in value_list:

            temp_c = 0

            temp_lack_words_value = []
            temp_lack_words = []
            for c in range(len(con)):
                if con[c] == entity:
                    continue

                if con[c] in v[2]:
                    temp_c += word_count[c]
                else:
                    temp_lack_words.append(con[c])
                    temp_lack_words_value.append(word_count[c])

            if (temp_c >= self.a*(np.sum(word_count)-delete_sum) and len(con) > 2) or (len(con)==2 and temp_c == (np.sum(word_count)-delete_sum)):
                con_count.append(temp_c)
                con_value.append(v[0]+":"+v[2])
                con_name.append(v[0])



            bad_count.append(temp_c)
            bad_value.append(v[2])
            bad_name.append(v[0])
            lack_words.append(temp_lack_words)
            lack_words_value.append(temp_lack_words_value)

        if len(bad_value)==0:
            return None,None

        elif self.cilin:
            best_count, best_value, best_name = self.judgeCilin(bad_count, bad_value, bad_name, lack_words,
                                                                lack_words_value)
            if best_count and (best_count >= (np.sum(word_count) - delete_sum) * self.b):
                return best_name+":"+best_value, best_name
        elif self.embedding:

            embedding_count,best_value,best_name = self.getWordsSimilarCount(bad_value,bad_count,bad_name,con,entity[0],np.sum(word_count))
            if embedding_count >= self.a * (np.sum(word_count)- delete_sum):
                return best_name+":"+best_value,best_name

        elif len(con_value) == 0:
            return None,None
        else:
            cal_value = []
            value_len = []
            cal_name = []
            max_count = np.max(con_count)
            for i in range(len(con_count)):
                if con_count[i] == max_count:
                    cal_value.append(con_value[i])
                    value_len.append(len(con_value[i]))
                    cal_name.append(con_name[i])

            return cal_value[np.argmin(value_len)],cal_name[np.argmin(value_len)]

        return None, None

    def doNormalForFalseYear(self, entity, con_cnt):

        print(entity)
        if len(entity)==0:
            return None, None

        print(con_cnt,entity)

        con = con_cnt[0]
        word_count = con_cnt[1]
        print(con,word_count)
        con_count = []
        con_value = []
        con_name = []
        value_list = self.graph_util.fuzzySearchForNormalFalse("?o",entity)
        for v in value_list:
            temp_c = 0
            for c in range(len(con)):
                if con[c] in v[2]:
                    temp_c += word_count[c]

            if '年' in v[2] or '世纪' in v[2] or '公元' in v[2]:
                con_count.append(temp_c)
                con_value.append(v[0]+":"+v[2])
                con_name.append(v[0])

        if len(con_value) == 0:
            return None,None
        else:
            cal_value = []
            value_len = []
            cal_name = []
            max_count = np.max(con_count)
            for i in range(len(con_count)):
                if con_count[i] == max_count:
                    cal_value.append(con_value[i])
                    value_len.append(len(con_value[i]))
                    cal_name.append(con_name[i])

            return cal_value[np.argmin(value_len)],cal_name[np.argmin(value_len)]


    def doNormalForFalseStrict(self, entity, con_cnt):

        print("doNormalForFalseStrict",entity, con_cnt)



        con = con_cnt[0]
        word_count = con_cnt[1]

        if len(con) == 2:
            return None,None



        con_count = []
        con_value = []
        con_name = []
        value_list = self.graph_util.fuzzySearchForNormalFalse("?o",entity)
        for v in value_list:
            temp_c = 0
            for c in range(len(con)):
                if con[c] == entity:
                    if len(con) == 2:
                        temp_c += word_count[c]
                    continue
                if con[c] in v[2]:
                    #print(v)
                    temp_c += word_count[c]

            if ((temp_c >= (2*np.sum(word_count))/3) and len(con) > 2) or (len(con)==2 and temp_c == np.sum(word_count)):
                con_count.append(temp_c)
                con_value.append(v[0]+":"+v[2])
                con_name.append(v[0])

        if len(con_value) == 0:
            return None,None
        else:
            cal_value = []
            value_len = []
            cal_name = []
            max_count = np.max(con_count)
            for i in range(len(con_count)):
                if con_count[i] == max_count:
                    cal_value.append(con_value[i])
                    value_len.append(len(con_value[i]))
                    cal_name.append(con_name[i])

            return cal_value[np.argmin(value_len)],cal_name[np.argmin(value_len)]

    def doCon(self, entity, con_cnt):
        print("doCon",entity,con_cnt)



        con = con_cnt[0]
        word_count = con_cnt[1]

        sum_count = np.sum(word_count)

        name = []
        content = []
        count = []
        lack_words = []
        lack_words_value = []

        bad_p = []
        bad_count = []
        bad_name = []
        delete_sum = 0
        for c in range(len(con)):
            if con[c] == entity:
                delete_sum += word_count[c]



        pro_list = self.graph_util.getProByType(entity)
        for pro in pro_list:
            if pro in ['图片','出处','分类编号']:
                continue



            value_list = self.graph_util.getValueByPro(entity,pro)

            for value in value_list:
                temp_lack_work = []
                temp_lack_work_value = []
                temp = 0

                for c in range(len(con)):
                    if con[c] == entity:

                        continue

                    if con[c] in value[1]:
                        print(con[c],word_count[c],value[0])
                        temp += word_count[c]
                    else:
                        temp_lack_work.append(con[c])
                        temp_lack_work_value.append(word_count[c])
                if (len(con)>2 and temp >= (np.sum(word_count)-delete_sum)*self.b) or (len(con)<=2  and (temp==np.sum(word_count)+delete_sum or (np.sum(word_count) > 20 and temp >= 20))):
                    name.append(value[0])
                    content.append(value[1])
                    count.append(temp)
                bad_name.append(value[0])
                bad_p.append(value[1])
                bad_count.append(temp)
                lack_words.append(temp_lack_work)
                lack_words_value.append(temp_lack_work_value)

        if len(bad_p)==0:
            return None,None
        elif self.cilin:
            if len(content) > 0 and np.max(count)/(np.sum(word_count)-delete_sum)>0.6:
                max_count = np.max(count)
                print(max_count,np.sum(word_count),delete_sum,max_count/(np.sum(word_count)-delete_sum), "max_count")
                min_len = 1000

                for v_index in range(len(content)):
                    if count[v_index] == max_count:

                        v_len = len(content[v_index])
                        print("content[v_index]", content[v_index],v_len,min_len)
                        if v_len < min_len:
                            min_len = v_len
                            best_value = content[v_index]
                            best_name = name[v_index]
                return best_name+":"+best_value,best_name

            best_count,best_value,best_name = self.judgeCilin(bad_count,bad_p,bad_name,lack_words,lack_words_value)

            if best_count and (best_count >= (np.sum(word_count) - delete_sum) * self.b):
                return best_name+":"+best_value,best_name
        elif self.embedding and len(con)>2:

            embedding_count,best_value,best_name = self.getWordsSimilarCount(bad_p,bad_count,bad_name,con,entity[0],np.sum(word_count))
            if embedding_count >= self.a * (np.sum(word_count)):
                return best_name+":"+best_value,best_name

        elif len(count)>0:
            cal_value = []
            value_len = []
            cal_name = []
            max_count = np.max(count)
            for i in range(len(count)):
                if count[i] == max_count:
                    cal_value.append(content[i])
                    value_len.append(len(content[i]))
                    cal_name.append(name[i])
            return cal_name[np.argmin(value_len)] + ": " + cal_value[np.argmin(value_len)], cal_name[np.argmin(value_len)]


        if len(count)==0:
            return None, None

        return None, None

    def doConStrict(self, entity, con_cnt):
        con = con_cnt[0]

        word_count = con_cnt[1]
        sum_count = np.sum(word_count)

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

                if (temp >= (2*np.sum(word_count))/3 and len(con) > 2) or (temp == np.sum(word_count)):
                    name.append(value[0])
                    content.append(value[1])
                    count.append(temp)
        if len(count)==0:
            return None,None
        cal_value = []
        value_len = []
        cal_name = []
        max_count = np.max(count)
        for i in range(len(count)):
            if count[i] == max_count:
                cal_value.append(content[i])
                value_len.append(len(content[i]))
                cal_name.append(name[i])
        return cal_name[np.argmin(value_len)]+": "+cal_value[np.argmin(value_len)],cal_name[np.argmin(value_len)]


    def searchEnt(self,entity,property):
        pro_list = self.graph_util.getValueByPro(entity,property)
        return pro_list
