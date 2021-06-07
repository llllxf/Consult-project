# @Language: python3
# @File  : localtionInference.py
# @Author: LinXiaofei
# @Date  : 2020-06-17
"""
位置推理模块
"""

from backend.data.data_process import read_file

from backend.graphSearch.graphSearch import graphSearch

class localtionInfernce(object):
    def __init__(self):
        self.search_util = graphSearch()

    def checkPos(self,entity_list,pos):
        ans_ent = []

        for entity in entity_list:
            rel_list = self.graph_util.getEntityByLabelWithRel(entity)

            check_again = []

            for r in rel_list:
                if r[0] == '位于':
                    if r[1] == pos:
                        ans_ent.append(entity)
                        break
            check_again.append(r[1])

            for ca in check_again:
                rel_list = self.graph_util.getEntityByLabelWithRel(ca)


                for r in rel_list:
                    if r[0] == '位于':
                        if r[1] == pos:
                            ans_ent.append(entity)
                            break
        return ans_ent




    def getLocation(self,entity):
        f = open("lake.txt","a")
        city_list = []
        province_list = []
        country_list = []
        state_list = []
        area_list = []
        city_list += self.search_util.getObjectBySAPLimitType(entity,'位于','城市')
        province_list += self.search_util.getObjectBySAPLimitType(entity,'位于','省')
        country_list += self.search_util.getObjectBySAPLimitType(entity,'位于','国家')
        state_list += self.search_util.getObjectBySAPLimitType(entity,'位于','洲')
        area_list += self.search_util.getObjectBySAPLimitType(entity,'位于','区域')
        if len(city_list)>0:
            for city in city_list:
                province_list += self.search_util.getObjectBySAPLimitType(city, '位于', '省')
                country_list += self.search_util.getObjectBySAPLimitType(city, '位于', '国家')
                state_list += self.search_util.getObjectBySAPLimitType(city, '位于', '洲')
                area_list += self.search_util.getObjectBySAPLimitType(city, '位于', '区域')

        if len(province_list) > 0:
            for province in province_list:
                country_list += self.search_util.getObjectBySAPLimitType(province, '位于', '国家')
                area_list += self.search_util.getObjectBySAPLimitType(province, '位于', '区域')

        if len(country_list)>0:
            for country in country_list:
                state_list += self.search_util.getObjectBySAPLimitType(country, '位于', '洲')
                area_list += self.search_util.getObjectBySAPLimitType(country, '位于', '区域')

        if len(area_list)>0:
            for area in area_list:
                state_list += self.search_util.getObjectBySAPLimitType(area, '位于', '洲')
                country_list += self.search_util.getObjectBySAPLimitType(area, '位于', '国家')

        city_list = list(set(city_list))
        province_list = list(set(province_list))
        country_list = list(set(country_list))
        area_list = list(set(area_list))
        state_list = list(set(state_list))

        location = city_list+province_list+country_list+area_list+state_list


        """
        print("================="+entity+"=================")
        print("所在城市: "+",".join(city_list))
        print("所在省: " + ",".join(province_list))
        print("所在国家: "+",".join(country_list))
        print("所在地区: "+",".join(area_list))
        print("所在洲: "+",".join(state_list))
        """
        """
        if len(country_list)<1 or len(state_list)<1:
            f.writelines(entity+"\n")
            f.writelines("所在城市: "+",".join(city_list))
            f.writelines("\n")
            f.writelines("所在省: " + ",".join(province_list))
            f.writelines("\n")
            f.writelines("所在地区: "+",".join(area_list))
            f.writelines("\n")
            f.writelines("所在洲: "+",".join(state_list))
            f.writelines("\n")
            f.writelines("======================================")
        """
        return location

    def getLocationByLimit(self,entityType,location):
        formed_ent = []


        son_list = self.search_util.getEntityByType(entityType)

        for son in son_list:
            son_location = self.getLocation(son)
            if location in son_location:
                formed_ent.append(son)
        return formed_ent












