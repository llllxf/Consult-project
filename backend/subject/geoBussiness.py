# @Time : 2021/2/8 7:21 PM
# @Author : LinXiaofei
# @File : geoBussiness.py

from backend.nlu.LTPUtil import *
from backend.nlu.parseSentence import *
from backend.graphSearch.graphSearch import graphSearch
from backend.template_library.ConProStrict import ConProStrict
import numpy as np
from backend.numUtil.numUtil import getSingelCompareNum,chinese_to_arabic


class GeoBussiness(object):
    def __init__(self):
        self.ltp_util = LTPUtil()
        self.graph_util = graphSearch()
        self.parseSen = ParseSentence()
        self.pro_strict_util = ConProStrict()
        #self.num_pro = ['人口数量', '蓄水量', '海拔', '流域面积', '面积', '深度', '陆地面积', '长度']
        #self.num_type = ['湖泊','河流']

        self.sum_arg = {'人口数量':['国家'],'面积':['湖泊'],'海拔':['山峰','山脉'],'长度':['河流'],'深度':['湖泊']}

        self.below = ['少于','低于','小于','不足']
        self.over = ['超过','高于','大于','超','过','达到','多于']

        #self.combine = {'长于':['长度','大于'],'短于':['长度','短于'],'高于':['海拔','大于'],'低于':['海拔','小于'],''}

        #self.num_util = numUtil()
        """
        self.dm = DialogManagement()
        year_pro = read_file("../backend/data/历史/year_pro.csv")
        self.dm.setConpro(year_pro)
        self.history_business = HistoryBussiness()
        print("HistoryDM????????????????????????????")
        """

    def checkType(self, entity_list, etype):
        ans_ent = []
        for entity in entity_list:
            rel_list = self.graph_util.getEntityByLabelWithRel(entity)
            if rel_list is None or len(rel_list)==0:
                return [],[]

            for r in rel_list:
                if r[0] == '类型':
                    if r[1] == etype:
                        ans_ent.append(entity)
                        break
                if entity in ans_ent:
                    break
        print(ans_ent)
        return ans_ent



    def checkPos(self,entity_list,pos):
        ans_ent = []
        ans_index = []

        for entity in entity_list:
            rel_list = self.graph_util.getEntityByLabelWithRel(entity)
            if rel_list is None or len(rel_list)==0:
                return [],[]

            check_again = []

            for r in rel_list:
                if r[0] == '位于':
                    if r[1] == pos:
                        ans_ent.append(entity)
                        ans_index.append(entity_list.index(entity))
                        break
            check_again.append(r[1])

            for ca in check_again:
                rel_list = self.graph_util.getEntityByLabelWithRel(ca)


                for r in rel_list:
                    if r[0] == '位于':
                        if r[1] == pos:
                            ans_ent.append(entity)
                            ans_index.append(entity_list.index(entity))
                            break
        return ans_ent,ans_index

    def getEntity(self,etype):
        ent_list = self.graph_util.getEntityByTypeAddType(etype)

        return ent_list

    def searchBinaryPRel(self,arg):
        entity = arg[1]
        relation = arg[0][0]
        etype = arg[0][1]
        ans = self.graph_util.getValueByRelAndObj(etype,relation,entity)
        print(ans)
        if len(ans)>0:
            if len(ans) >= 10:
                ans = ans[:10]
            if '我国' in ans:
                ans.remove('我国')
            ans = list(set(ans))
            return [1,",".join(ans),entity]
        return [0,'无法回答',entity]

    def searchBinaryRel(self,words,arg):

        print("arg",arg)

        entity = arg[1]
        relation  = arg[0][0]
        etype = arg[0][1]

        print(entity)
        print(relation)
        print(etype)

        cut_words = self.ltp_util.get_seg(words)
        pos = list(self.ltp_util.get_postag(cut_words))
        print(cut_words)
        print(pos)
        pos_ent = self.parseSen.getPositionEntity(cut_words,pos,entity)


        print("pos_ent",pos_ent)

        rel_list = self.graph_util.getEntityByLabelWithRel(entity)
        print("searchBinaryRel",relation,rel_list)

        ans = []

        for r in rel_list:
            print(r[0],relation)
            if r[0] == relation:
                if r[1] in ans or r[1]=='我国':
                    continue

                ans.append(r[1])

        print("ans==========final",ans)

        if ans == []:

            return [0,'无法回答']
        else:
            if len(pos_ent)>0:
                pent = pos_ent[-1]
                pos_ans,_ = self.checkPos(ans,pent)
                ans = pos_ans
                #return [1, ",".join(pos_ans),entity]
            if etype:
                type_ans = self.checkType(ans,etype)
                ans = type_ans

            if len(ans)>0:
                return [1, ",".join(ans), entity]

            print(ans,"ans========================")
            return [0,'无法回答',entity]




    def dealMostType(self,etype,con,word_count,key_word):

        name = []
        content = []
        count = []

        pos = self.ltp_util.get_postag(con)

        pos_ent = self.parseSen.getPositionEntity(con, pos, etype)
        print("pos_ent",pos_ent)


        tri_list = self.graph_util.fuzzySearchOne("?plabel", "特征", etype)
        for value in tri_list:
            #print(value)
            temp = 0
            for c in range(len(con)):
                if con[c] in value[2]:
                    #print(con[c], word_count[c], value[0])
                    temp += word_count[c]

            if (temp >= np.sum(word_count) / 2):
                flag = True
                for kw in key_word:
                    if kw not in value[2]:
                        flag = False
                if flag:
                    name.append(value[0])
                    content.append(value[2])
                    count.append(temp)

        most_pro = ['地位', '作用', '定义', '优点', '意义', '示例', '内容']
        for p in most_pro:
            result = self.graph_util.getValueByPro(etype, p)
            for value in result:
                #print(value)
                temp = 0
                for c in range(len(con)):
                    if con[c] in value[1]:
                        #print(con[c], word_count[c], value[0])
                        temp += word_count[c]

                if (temp >= np.sum(word_count) / 2):
                    flag = True
                    for kw in key_word:
                        if kw not in value[1]:
                            flag = False
                    if flag:
                        name.append(value[0])
                        content.append(value[1])
                        count.append(temp)

        if len(count) == 0:
            return [0]
        cal_value = []
        value_len = []
        cal_name = []

        check_name = []
        check_content = []
        check_count = []


        if len(pos_ent) > 0:

            ans,ans_index = self.checkPos(name,pos_ent[-1])
            check_name = ans
            check_content = np.array(content)[ans_index]
            check_count = np.array(count)[ans_index]
        else:
            check_name = name
            check_content = content
            check_count = count

        print(check_name)
        print(check_content)
        print(check_count)

        if len(check_content) == 0:
            return [0]
        max_count = np.max(list(check_count))
        for i in range(len(check_count)):
            if check_count[i] == max_count:
                cal_value.append(check_content[i])
                value_len.append(len(check_content[i]))
                cal_name.append(check_name[i])
        return [1, cal_name[np.argmin(value_len)] + ": " + cal_value[np.argmin(value_len)],
                cal_name[np.argmin(value_len)]]

    def dealMostEnt(self,entity,con,word_count,key_word):
        print("dealMostEnt",entity,key_word)

        name = []
        content = []
        count = []

        pro_list, rel_list = self.graph_util.searchEntity(entity)

        for p in pro_list:
            temp = 0
            for c in range(len(con)):
                if con[c] in p[1]:
                    print(con[c], word_count[c], p[1])
                    temp += word_count[c]
            if (temp >= np.sum(word_count) / 2):
                flag = True
                for kw in key_word:
                    if kw not in p[1]:
                        flag = False
                if flag:

                    content.append(p[1])
                    count.append(temp)
        if len(count) == 0:
            return [0]
        cal_value = []
        value_len = []
        print(content)
        print(count)

        max_count = np.max(count)
        for i in range(len(count)):
            if count[i] == max_count:
                cal_value.append(content[i])
                value_len.append(len(content[i]))

        return [1, cal_value[np.argmin(value_len)],
                entity]
    """
    def checkCompare(self,words):
        cut_word, pos, dep, reverse_dep = self.ltp_util.get_sentence_data(words)
        if '比' in words or '更' in words:
            ent_list = self.parseSen.getEntityTwo(cut_word)
            if ent_list:
                pro_list = self.graph_util.getProList(ent_list[0])
                num_list = self.pro_strict_util.getNumPro(pro_list)
                pro = self.pro_strict_util.checkNumberPro(pro_list,cut_word,pos)
                if pro:
                    self.num_util.getSingelCompareNum()
    """


    def checkNumPro(self,words):

        cut_word, pos, dep,reverse_dep = self.ltp_util.get_sentence_data(words)
        if '共' in words and ('多少' in words or '几' in words):
            entity,ent_index = self.ParseSentence.getEntityTwo(cut_word)
            etype,ent_index = self.ParseSentence.getEtype(cut_word)
            if entity is None or etype is None:
                return False,None,None,None

        return False,None,None,None

    def getSum(self,words):
        #if '几' not in words and '多少' not in words:
        #    return False

        cut_word, pos, dep, reverse_dep = self.ltp_util.get_sentence_data(words)
        ask_pro = None
        ask_index = -1

        numpro = list(self.sum_arg.keys())
        print("numpro",numpro)


        ask_type = None
        des = None
        num_limit = ""

        ask_pro, ask_index = self.pro_strict_util.checkSPNumPro(words, numpro)
        print("ask_pro, ask_index",ask_pro, ask_index)


        if ask_pro is None:
            return False

        for v in self.sum_arg[ask_pro]:
            if v in cut_word:
                ask_type = v

        if ask_type is None:
            return False



        print("ask_type,ask_pro,des",ask_type,ask_pro,des)
        sum_flag = None


        for o in self.over:
            if o in cut_word:
                if '没' in words or '不' in words:
                    be_index = cut_word.index(o)

                    sum_flag = "below"
                else:
                    be_index = cut_word.index(o)

                    sum_flag = "over"



        for b in self.below:
            if b in cut_word:
                if '没' in words or '不' in words:
                    be_index = cut_word.index(b)

                    sum_flag = "over"

                else:
                    be_index = cut_word.index(b)

                    sum_flag = "below"



        if sum_flag is None:
            return False
        for i in range(be_index+1,len(cut_word)):
            print("cut_word",cut_word[i])
            if  pos[i] == 'm':
                num_limit += cut_word[i]
            else:
                break
        if  len(num_limit)<=0:
            return False

        n = chinese_to_arabic(num_limit)
        print("chinese_to_arabic",n,sum_flag)
        ans_ent = []

        result = self.graph_util.getValueByPro(ask_type, ask_pro)
        for i in range(len(result)):
            check_num = getSingelCompareNum(result[i][1])
            print("check_num",check_num)

            if check_num is None:
                continue

            if sum_flag == 'over':

                if check_num >= n:
                    if result[i][0] in ans_ent:
                        continue
                    ans_ent.append(result[i][0])

            elif sum_flag == 'below':
                if check_num < n:
                    print(result[i][0],result[i][1])
                    if result[i][0] in ans_ent:
                        continue
                    ans_ent.append(result[i][0])

        pos_ent = self.parseSen.getPositionEntity(cut_word, pos, None)
        print("pos_ent",pos_ent)

        if len(pos_ent)>0:
            ans_ent, _ = self.checkPos(ans_ent, pos_ent[-1])

        if len(ans_ent) > 0:

            if '我国' in ans_ent and '中国' in ans_ent:
                ans_ent.remove('我国')

            if '中国' in ans_ent and '中华人民共和国' in ans_ent:
                ans_ent.remove('中国')



            print("共查到" + str(len(ans_ent)) + "个,包括" + ",".join(ans_ent))


            return [1, "共查到" + str(len(ans_ent)) + "个,包括" + ",".join(ans_ent),ans_ent[0]]

        else:
            return [0,'未查到相关数据',None]

    def getCompare(self,words):

        cut_word, pos, dep,reverse_dep = self.ltp_util.get_sentence_data(words)
        print("getCompar===================")
        print(cut_word)
        print(pos)
        print(dep)
        ent_list = self.parseSen.getEntityTwo(cut_word)
        print("ent_list",ent_list)
        if ent_list is None:
            return False,None
        if len(ent_list) != 2:
            return False, None

        print(ent_list)
        pro_list = self.graph_util.getProList(ent_list[0])
        print("pro_list,",pro_list)
        num_pro_temp = self.pro_strict_util.getNumPro(pro_list)
        print("num_pro_temp",num_pro_temp)
        pro_list2 = self.graph_util.getProList(ent_list[1])
        print("pro_list2,", pro_list2)

        num_pro = []
        for pro in num_pro_temp:
            if pro in pro_list2:
                num_pro.append(pro)
        if len(num_pro)<1:
            return False, None
        print(num_pro)

        pro_cal,adj,compare_type = self.pro_strict_util.checkNumberProForCompare(num_pro,cut_word,pos)
        print("pro_cal,",pro_cal,adj,compare_type)

        if pro_cal:

            value_list1,_ = self.graph_util.searchEntity(ent_list[0])
            value_list2,_ = self.graph_util.searchEntity(ent_list[1])
            temp = []
            temp_len = []
            for v in value_list1:

                if v[0] == pro_cal:
                    temp.append(v[1])
                    temp_len.append(len(v[1]))

            value_1 = temp[np.argmin(temp_len)]
            temp = []
            temp_len = []
            for v in value_list2:

                if v[0] == pro_cal:
                    temp.append(v[1])
                    temp_len.append(len(v[1]))
            value_2 = temp[np.argmin(temp_len)]
            num1 = getSingelCompareNum(value_1)
            num2 = getSingelCompareNum(value_2)
            print("===================================")
            print(value_1)
            print(value_2)
            print("num1,num2",num1,num2)
            ans = ""
            if num1-num2>0:
                if compare_type == 'positive':
                    ans += ent_list[0] + adj
                    ans += "\n" + ent_list[0] + ":" + value_1 + "\n" + ent_list[1] + ":" + value_2
                    return True, [1, ans, ent_list[0]]
                if compare_type == 'negative':
                    ans += ent_list[1] + adj
                    ans += "\n" + ent_list[0] + ":" + value_1 + "\n" + ent_list[1] + ":" + value_2
                    return True, [1, ans, ent_list[1]]
            else:
                if compare_type == 'positive':
                    ans+=ent_list[1]+adj
                    ans += "\n" + ent_list[0] + ":" + value_1 + "\n" + ent_list[1] + ":" + value_2
                    return True, [1, ans, ent_list[1]]
                if compare_type == 'negative':
                    ans += ent_list[0] + adj
                    ans += "\n" + ent_list[0] + ":" + value_1 + "\n" + ent_list[1] + ":" + value_2
                    return True, [1, ans, ent_list[0]]
        return False,None

    def getOneEntityRelation(self, entity):
        rel_list = self.graph_util.getEntityByLabelWithRelMore(entity)
        print("rel_list",rel_list)
        ans = {}
        ans['entity'] = entity
        ans_category = {}
        ans_category['entity'] = entity
        ans_relate = {}
        ans_relate['entity'] = entity

        category = ""

        for p in rel_list:
            if p[0] in ['类型', '相关于','强相关于','部分于']:
                continue
            else:
                if p[0] == '实体限制':
                    ans_relate[p[1]] = '相关考点'
                else:
                    ans[p[1]]=p[0]
                if p[0] == '分类' and '地理' not in p[0]:
                    category = p[0]

        if len(category)>0:

            son_list = self.graph_util.getEntityByCategory(category)

            print(son_list,"son_list============================")

            for p in son_list[:8]:
                ans_category[p[0]] = "相似实体"


        return ans, ans_category,ans_relate

    def doMost(self,words):

        """
        我国最高气温在哪一个盆地中

        :param words:
        :return:
        """
        cut_word, pos, dep, reverse_dep = self.ltp_util.get_sentence_data(words)
        key_word = []

        for w_index in range(len(cut_word)):
            if '最' == cut_word[w_index]:
                key_word.append(cut_word[w_index])
                key_word.append(cut_word[w_index+1])
            elif '最' in cut_word[w_index]:
                key_word.append(cut_word[w_index])

        print("key_word",key_word)

        con, word_count = self.parseSen.getValuableWords(cut_word, pos, dep)
        ent, parseType = self.parseSen.extractType(cut_word)
        if parseType in ['split', 'split_end']:
            return self.dealMostType(ent,con,word_count,key_word)
        elif parseType== 'normal':
            ent,_,ent_type = self.parseSen.extractBestEnt(cut_word,dep)
            if ent_type=='entity' and ent:
                return self.dealMostEnt(ent,con,word_count,key_word)
        return [0]




    def doMost2(self,words):
        cut_word, pos, dep = self.ltp_util.get_sentence_data(words)


        #cut_word, hidden = self.ltp_util.getSEG(words)
        #dep = self.ltp_util.getDEP(hidden)[0]
        #pos = self.ltp_util.getPOS(hidden)[0]
        #print(pos)
        #cut_word = cut_word[0]

        ent, parseType = parseSen.extractType(cut_word)
        print(parseType, "parseType")
        if parseType in ['split', 'split_end']:
            etype = ent
        else:
            return [0]

        pos_entity = parseSen.getEntity(cut_word)
        print("===========================================")

        for w_idnex in range(len(cut_word)):

            print(cut_word[w_idnex])

            if '最' in cut_word[w_idnex]:

                if cut_word[w_idnex] == '最':
                    key_adj = "最" + cut_word[w_idnex + 1]
                else:
                    key_adj = cut_word[w_idnex]

                begin = w_idnex
                left = 1
                none_array = []
                while (begin >= left):

                    if '最' in cut_word[begin - left]:

                        none_array += pos_entity
                        none_array = list(set(none_array))
                        break

                    if pos[begin - left] in ['n', 'nl', 'ni', 'ns', 'nz'] and cut_word[begin - left] not in none_array:
                        none_array.append(cut_word[begin - left])
                    left = left + 1
                #key_adj = "最" + cut_word[w_idnex + 1]
                none_array.append(key_adj)
                print(none_array)

                ans,ent = self.dealMost(etype, none_array)

                if ans:
                    print("ajshdkajshdoaiuehdlud==============",ans)
                    return [1, ans, ent]

        return [0]

    def dealMost(self,etype, match):

        tri_list = self.graph_util.fuzzySearchOne("?plabel", "特征", etype)

        for i in range(len(tri_list)):
            flag = True
            for m in match:
                if m not in tri_list[i][2]:
                    flag = False
                    break
            if flag:
                print(tri_list[i][0],"dealMost")
                return tri_list[i][0]+":"+tri_list[i][2],tri_list[i][0]

        most_pro = ['地位', '作用', '定义', '优点', '意义', '示例', '内容']
        for p in most_pro:
            result = self.graph_util.getValueByPro(etype, p)
            for i in range(len(result)):
                flag = True
                for m in match:
                    if m not in result[i][1]:
                        flag = False
                        break
                if flag:
                    print(result[i][0], "dealMost")
                    return result[i][0]+":"+result[i][1],result[i][0]

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
                    print(tri_list[i][0], "dealMost")
                    return tri_list[i][0]+":"+tri_list[i][2],tri_list[i][0]
            for i in range(len(result)):
                flag = True
                for m in match:
                    if m == '世界' or m == '地球':
                        continue
                    if m not in result[i][1]:
                        flag = False
                        break
                if flag:
                    print(result[i][0], "dealMost")
                    return result[i][0]+":"+result[i][1],result[i][0]

        return None

