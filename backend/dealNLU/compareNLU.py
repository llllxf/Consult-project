# !/usr/bin/env python3
# -*- coding: utf-8 -*-


from backend.aiml_cn import Kernel
from backend.data.data_process import read_file
from backend.graphSearch.graphSearch import graphSearch
"""
比较模块的前期处理

"""


class compareNLU(object):
    def __init__(self):

        """
        比较aiml
        """

        self.compare_aiml = Kernel()
        self.compare_aiml.learn(project_path+'/resource/pattern_for_compare.aiml')
        self.graphsearch = graphSearch()

    def is_Chinese(self,word):
        for ch in word:
            if '\u4e00' <= ch <= '\u9fff':
                return True
        return False

    def checkCompareBySchema(self,question):
        """
        匹配比较模版，得到匹配结果
        :param question: 问句
        :return:
        1.比较信号
        2.抽取的信息
        3.匹配到的句子形式（其实就是更具体的任务类型）


        如果可以匹配上比较模版，那么第一个返回参数就是task_compare
        抽取的信息就是实体
        模版得到的返回结果不仅可以知道任务类型，实际上也携带了属性信息

        加入实行反问，那么抽取的实体将替换为反问表示，第一个返回数据仍然是比较标识，最后一个仍然是模版匹配结果
        """

        compare_words_more = ['大','深','高','东','南','西','北','长']
        compare_words_less = ['小','浅','低','短']

        mountain_list = read_file(project_path+"/data/compare/mountain.csv")
        lake_list = read_file(project_path+"/data/compare/lake.csv")
        hill_list = read_file(project_path+"/data/compare/hill.csv")
        river_list = read_file(project_path+"/data/compare/river.csv")
        sea_list = read_file(project_path+"/data/compare/sea.csv")

        mountain_list = sorted(mountain_list, key=lambda i: len(i), reverse=True)
        lake_list = sorted(lake_list, key=lambda i: len(i), reverse=True)
        hill_list = sorted(hill_list, key=lambda i: len(i), reverse=True)
        river_list = sorted(river_list, key=lambda i: len(i), reverse=True)
        sea_list = sorted(sea_list, key=lambda i: len(i), reverse=True)


        ask_hill= []
        ask_mountain = []
        ask_lake = []
        ask_river = []
        ask_sea = []
        ask_entity = []

        keyword = ""
        flag = ""

        ask_attr = ""

        for q in question[::-1]:
            if q in compare_words_more:
                keyword = q
                flag = "more"
                break
            if q in compare_words_less:
                keyword = q
                flag = "less"
                break

        for mountain in mountain_list:
            if mountain in question:
                question = question.replace(mountain,"MOUNTAIN")
                ask_mountain.append(mountain)
        if len(ask_mountain)>=2:
            ask_attr = self.graphsearch.getCompareKeyword(keyword,ask_mountain[0])
            ask_entity = ask_mountain
            ans_dict = {'entity': ask_entity, 'property': ask_attr, "flag":flag}
            return "task_compare",ans_dict
            #print(ask_attr)

        for hill in hill_list:
            if hill in question:
                question = question.replace(hill,"HILL")
                ask_hill.append(hill)
        if len(ask_hill)>=2 or len(ask_mountain+ask_hill)>=2:
            ask_attr = self.graphsearch.getCompareKeyword(keyword, ask_hill[0])
            ask_entity = ask_hill+ask_mountain
            ans_dict = {'entity': ask_entity, 'property': ask_attr, "flag": flag}
            return "task_compare",ans_dict
            #print(ask_attr)

        for lake in lake_list:
            if lake in question:
                question = question.replace(lake,"LAKE")
                ask_lake.append(lake)
        if len(ask_lake)>=2:
            ask_attr = self.graphsearch.getCompareKeyword(keyword, ask_lake[0])
            ask_entity = ask_lake
            ans_dict = {'entity': ask_entity, 'property': ask_attr, "flag": flag}
            return "task_compare",ans_dict
            #print(ask_attr)


        for river in river_list:
            if river in question:
                question = question.replace(river,"RIVER")
                ask_river.append(river)
        if len(ask_river) >= 2:
            ask_attr = self.graphsearch.getCompareKeyword(keyword, ask_river[0])
            ask_entity = ask_river
            ans_dict = {'entity': ask_entity, 'property': ask_attr, "flag": flag}
            return "task_compare",ans_dict
            #print(ask_attr)

        for sea in sea_list:
            if sea in question:
                question = question.replace(sea,"SEA")
                ask_sea.append(sea)
        if len(ask_sea) >= 2:
            ask_attr = self.graphsearch.getCompareKeyword(keyword, ask_sea[0])
            ask_entity = ask_sea
            ans_dict = {'entity': ask_entity, 'property': ask_attr, "flag": flag}
            return "task_compare",ans_dict
            #print(ask_attr)






        return "task_normal"


    def checkCompare(self,question):
        """
        匹配比较模版，得到匹配结果
        :param question: 问句
        :return:
        1.比较信号
        2.抽取的信息
        3.匹配到的句子形式（其实就是更具体的任务类型）


        如果可以匹配上比较模版，那么第一个返回参数就是task_compare
        抽取的信息就是实体
        模版得到的返回结果不仅可以知道任务类型，实际上也携带了属性信息

        加入实行反问，那么抽取的实体将替换为反问表示，第一个返回数据仍然是比较标识，最后一个仍然是模版匹配结果
        """
        mountain_list = read_file(project_path+"/backend/data/compare/mountain.csv")
        lake_list = read_file(project_path+"/backend/data/compare/lake.csv")
        hill_list = read_file(project_path+"/backend/data/compare/hill.csv")
        river_list = read_file(project_path+"/backend/data/compare/river.csv")
        sea_list = read_file(project_path+"/backend/data/compare/sea.csv")

        mountain_list = sorted(mountain_list, key=lambda i: len(i), reverse=True)
        lake_list = sorted(lake_list, key=lambda i: len(i), reverse=True)
        hill_list = sorted(hill_list, key=lambda i: len(i), reverse=True)
        river_list = sorted(river_list, key=lambda i: len(i), reverse=True)
        sea_list = sorted(sea_list, key=lambda i: len(i), reverse=True)

        ask_hill= []
        ask_mountain = []
        ask_lake = []
        ask_river = []
        ask_sea = []

        for mountain in mountain_list:
            if mountain in question:
                question = question.replace(mountain,"MOUNTAIN")
                ask_mountain.append(mountain)

        for lake in lake_list:
            if lake in question:
                question = question.replace(lake,"LAKE")
                ask_lake.append(lake)

        for hill in hill_list:
            if hill in question:
                question = question.replace(hill,"HILL")
                ask_hill.append(hill)

        for river in river_list:
            if river in question:
                question = question.replace(river,"RIVER")
                ask_river.append(river)

        for sea in sea_list:
            if sea in question:
                question = question.replace(sea,"SEA")
                ask_sea.append(sea)

        ent_dict = {'mountain':ask_mountain,'hill':ask_hill,'river':ask_river
                    ,'lake':ask_lake,'sea':ask_sea}

        ans = self.compare_aiml.respond(question)
        if ans == "":
            return None,None,None
        elif self.is_Chinese(ans):
            return 'task_compare','task_compare_ask',ans
        else:
            entity,property=self.getCompareInfo(ans,ent_dict)
            ans_dict = {'entity':entity,'property':property}
            return "task_compare",ans_dict,ans

    def getCompareInfo(self,task_type,ask_ent):
        """
        处理比较类型的问题，抽取需要的实体和属性，通过前期抽取的实体和问题匹配后得到的模版结合处理得到最终需要抽取的实体和属性
        :param task_type: 任务类型（携带了属性和实体信息）
        :param ask_ent: 抽取到的实体信息
        :return:
        """

        if 'task_mountain_height' in task_type:
            entity = [ask_ent['mountain'][0],ask_ent['mountain'][1]]
            property = '海拔'
            return entity,property

        if 'task_mountain_long' in task_type:
            entity = [ask_ent['mountain'][0], ask_ent['mountain'][1]]
            property = '长度'
            return entity, property

        if 'task_hill_height' in task_type:
            entity = [ask_ent['hill'][0], ask_ent['hill'][1]]
            property = '海拔'
            return entity, property

        if 'task_mountain_hill_height' in task_type:
            entity = [ask_ent['mountain'][0], ask_ent['hill'][0]]
            property = '海拔'
            return entity, property

        if 'task_lake_area' in task_type:
            entity = [ask_ent['lake'][0], ask_ent['lake'][1]]
            property = '面积'
            return entity, property

        if 'task_lake_deep' in task_type:
            entity = [ask_ent['lake'][0], ask_ent['lake'][1]]
            property = '深度'
            return entity, property

        if 'task_lake_volume' in task_type:
            entity = [ask_ent['lake'][0], ask_ent['lake'][1]]
            property = '蓄水量'
            return entity, property

        if 'task_sea_area' in task_type:
            entity = [ask_ent['sea'][0], ask_ent['sea'][1]]
            property = '面积'
            return entity, property
        if 'task_sea_deep' in task_type:
            entity = [ask_ent['sea'][0], ask_ent['sea'][1]]
            property = '深度'
            return entity, property

        if 'task_river_flow' in task_type:
            entity = [ask_ent['river'][0], ask_ent['river'][1]]
            property = '流量'
            return entity, property

        if 'task_river_area' in task_type:
            entity = [ask_ent['river'][0], ask_ent['river'][1]]
            property = '面积'
            return entity, property

        if 'task_river_long' in task_type:
            entity = [ask_ent['river'][0], ask_ent['river'][1]]
            property = '长度'
            return entity, property
        if task_type == 'task_mountain_south' or task_type == 'task_mountain_north':
            entity = [ask_ent['mountain'][0],ask_ent['mountain'][1]]
            property = '纬度'
            return entity,property
        if task_type == 'task_mountain_east' or task_type == 'task_mountain_west':
            entity = [ask_ent['mountain'][0], ask_ent['mountain'][1]]
            property = '经度'
            return entity,property

        if task_type == 'task_mountain_hill_south' or task_type == 'task_mountain_hill_north':
            entity = [ask_ent['mountain'][0],ask_ent['hill'][0]]
            property = '纬度'
            return entity,property
        if task_type == 'task_mountain_hill_east' or task_type == 'task_mountain_hill_west':
            entity = [ask_ent['mountain'][0], ask_ent['hill'][0]]
            property = '经度'
            return entity,property

        if task_type == 'task_hill_south' or task_type == 'task_hill_north':
            entity = [ask_ent['hill'][0],ask_ent['hill'][1]]
            property = '纬度'
            return entity,property
        if task_type == 'task_hill_east' or task_type == 'task_hill_west':
            entity = [ask_ent['hill'][0], ask_ent['hill'][1]]
            property = '经度'
            return entity,property





if __name__ == '__main__':

    cnlu = compareNLU()
    cnlu.checkCompareBySchema("长江和黄河哪个长")



