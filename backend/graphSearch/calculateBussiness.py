# @Language: python3
# @File  : calculateBussiness.py
# @Author: LinXiaofei
# @Date  : 2020-06-22
"""

"""

from backend.numUtil import getSingelCompareNum,getSingelDirNum
import numpy as np

from backend.graphSearch.graphSearch import graphSearch
from backend.inference import localtionInfernce
class calculateBussiness(object):

    def __init__(self):
        self.graph_util = graphSearch()
        self.localtion_util = localtionInfernce()


    def matchSpecify(self,son_list,keywords):
        """
        匹配实例集的特征属性，匹配标准是words精确匹配
        :param son_list:
        :param words:
        :return:
        """


        deal_entity = self.graph_util.dealWithEnitity(son_list)

        for name, content in deal_entity.items():
            """
            抽取出的实体的属性
            """
            pro = np.array(content['p'])

            """
            去掉问题中的实体方便匹配
            """

            for p in pro:
                if p[0] != '特征' and p[0] != '地位' and p[0] != '内容':
                    continue
                flag = True
                for keyword in keywords:
                    if keyword not in p[1]:
                        flag = False
                        break
                if flag:
                    return name

        return None

    def getNumCollect(self, son_list, property):
        """
        根据属性名称得到实体集该属性值集合
        :param son_list:
        :param property:
        :return:
        """

        ans = self.graph_util.getNums(son_list, property)

        return son_list, ans

    #==================================================================

    def doMostCalculate(self,ans_dict):
        spefify = ans_dict['predicate'] + ans_dict['predicate_adj']
        if ans_dict['limit'][0] != '世界':
            son_list = self.localtion_util.getLocationByLimit(ans_dict['ask'][0], ans_dict['limit'][0])
        else:

            son_list = []
            for ask in ans_dict['ask']:

                son_list = son_list + self.graph_util.getEntityByType(ask)

            son_list = list(set(son_list))
        if len(son_list) < 1:
            return "对不起，暂时无法回答。\n", ans_dict['task_type']

        print("查找子类： ", son_list)

        ans = self.matchSpecify(son_list, spefify)

        if ans != None and len(ans) > 0:
            print("通过匹配实体的特征值得到最值信息")
            print("===========================================")
            return ans, ans_dict['task_type']
        else:

            ent_list, num_list = self.getNumCollect(son_list, ans_dict['predicate'])

            if 'dir' in ans_dict['task_type']:
                form_num_list = [getSingelDirNum(num, ans_dict['task_type']) for num in num_list]
            else:
                form_num_list = [getSingelCompareNum(num) for num in num_list]

            max_index = np.argmax(np.array(form_num_list))

            print("通过比较实体的" + ans_dict['predicate'][0] + "得到最值信息")
            print("===========================================")

            return ent_list[max_index], ans_dict['task_type']

    def doLeastCalculate(self,ans_dict):
        spefify = ans_dict['predicate'] + ans_dict['predicate_adj']
        if ans_dict['limit'][0] != '世界':
            son_list = self.localtion_util.getLocationByLimit(ans_dict['ask'][0], ans_dict['limit'][0])
        else:

            son_list = []
            for ask in ans_dict['ask']:

                son_list = son_list + self.graph_util.getEntityByType(ask)
                print("???",son_list)
            son_list = list(set(son_list))
        if len(son_list) < 1:
            return "对不起，暂时无法回答。\n", ans_dict['task_type']

        print("查找子类： ", son_list)

        ans = self.matchSpecify(son_list, spefify)

        if ans != None and len(ans) > 0:
            print("通过匹配实体的特征值得到最值信息")
            print("===========================================")
            return ans, ans_dict['task_type']
        else:

            ent_list, num_list = self.getNumCollect(son_list, ans_dict['predicate'])

            if 'dir' in ans_dict['task_type']:
                form_num_list = [getSingelDirNum(num, ans_dict['task_type']) for num in num_list]
            else:
                form_num_list = [getSingelCompareNum(num) for num in num_list]

            min_index = np.argmin(np.array(form_num_list))

            print("通过比较实体的" + ans_dict['predicate'][0] + "得到最值信息")
            print("===========================================")

            return ent_list[min_index], ans_dict['task_type']

    def doDistCalculate(self, ans_dict):
        entity_list = ans_dict['entity']
        latitude = self.graph_util.getNums(entity_list,"纬度")
        longitude = self.graph_util.getNums(entity_list,"经度")
        #print(latitude)
        #print(longitude)
        formed_latitude = []
        formed_longitude = []
        for l in latitude:
            formed_latitude.append(getSingelDirNum(l,"north"))
        for l in longitude:
            formed_longitude.append(getSingelDirNum(l,"east"))
        #print(formed_latitude)
        #print(formed_longitude)
        a = np.abs(formed_latitude[0]-formed_latitude[1])*111
        b = np.abs(formed_longitude[0]-formed_longitude[1])*111
        c = "直线距离约为"+str(np.sqrt(a*a+b*b)).split('.')[0]+"千米"
        return c,ans_dict['task_type']