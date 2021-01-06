# @Language: python3
# @File  : numUtil.py
# @Author: LinXiaofei
# @Date  : 2020-06-18
"""
计算模块的前期处理
"""



from backend.aiml_cn import Kernel
from backend.data.data_process import read_file


class calculateNLU(object):
    def __init__(self):
        """
        计算aiml
        """

        self.calculate_most_aiml = Kernel()
        self.calculate_most_aiml.learn(project_path + '/resource/pattern_for_most.aiml')
        self.calculate_dist_aiml = Kernel()
        self.calculate_dist_aiml.learn(project_path + '/resource/pattern_for_distance.aiml')

    def is_Chinese(self,word):
        for ch in word:
            if '\u4e00' <= ch <= '\u9fff':
                return True
        return False

    def checkCalculateDist(self,question):
        """
        计算山之间的距离模块
        :param question:
        :return:
        """
        print(question)
        mountain_list = read_file(project_path + "/data/compare/mountain.csv")
        hill_list = read_file(project_path + "/data/compare/hill.csv")
        mountain_list = sorted(mountain_list, key=lambda i: len(i), reverse=True)
        hill_list = sorted(hill_list, key=lambda i: len(i), reverse=True)

        ask_hill = []
        ask_mountain = []

        for mountain in mountain_list:
            if mountain in question:

                question = question.replace(mountain,"MOUNTAIN")
                ask_mountain.append(mountain)

        for hill in hill_list:
            if hill in question:

                question = question.replace(hill,"HILL")
                ask_hill.append(hill)

        ans = self.calculate_dist_aiml.respond(question)
        if ans == "" or ans is None:
            return None, None, None
        else:
            entity = ask_hill+ask_mountain

            return "task_calculate_dist",{'entity':entity},ans

    def checkCalculateMost(self,question):
        """
        计算最值模块
        :param question:
        :return:
        """
        country_list = read_file(project_path+"/backend/data/calculate/country.csv")
        city_list = read_file(project_path+"/backend/data/calculate/city.csv")
        province_list = read_file(project_path+"/backend/data/calculate/province.csv")
        state_list = read_file(project_path+"/backend/data/calculate/state.csv")


        country_list = sorted(country_list, key=lambda i: len(i), reverse=True)
        city_list = sorted(city_list, key=lambda i: len(i), reverse=True)
        province_list = sorted(province_list,key=lambda i: len(i), reverse=True)
        state_list = sorted(state_list,key=lambda i: len(i), reverse=True)



        limit_location= []
        ask_type = []
        ask_predicate = []
        predicate_adj = []


        for country in country_list:
            if country in question:
                limit_location.append(country)
                break

        for city in city_list:
            if city in question:
                limit_location.append(city)

        for province in province_list:
            if province in question:
                limit_location.append(province)

        for state in state_list:
            if state in question:
                limit_location.append(state)

        if len(limit_location)<1:
            limit_location.append("世界")

        #limit_location = ['世界']


        ans = self.calculate_most_aiml.respond(question)

        if ans == "":
            return None,None,None
        if self.is_Chinese(ans):
            return 'task_calculate','task_calculate_ask',ans

        if 'lake' in ans:

            if '淡水湖' in question:
                ask_type.append('淡水湖')
            elif '咸水湖' in question:
                ask_type.append('咸水湖')
            else:
                ask_type.append('湖泊')

            if 'area' in ans:
                ask_predicate.append('面积')
                if 'most' in ans:

                    predicate_adj.append('最大')
                elif 'least' in ans:
                    predicate_adj.append('最小')
            elif 'vol' in ans:
                ask_predicate.append('蓄水量')
                if 'most' in ans:

                    predicate_adj.append('最大')
                elif 'least' in ans:
                    predicate_adj.append('最小')
            elif 'deep' in ans:
                ask_predicate.append('深度')
                if 'most' in ans:
                    predicate_adj.append('最深')
                elif 'least' in ans:
                    predicate_adj.append('最浅')


        elif 'river' in ans:

            ask_type.append('河流')

            if 'area' in ans:
                ask_predicate.append('面积')
                if 'most' in ans:
                    predicate_adj.append('最大')
                elif 'least' in ans:
                    predicate_adj.append('最小')
            elif 'flow' in ans:
                ask_predicate.append('流量')
                if 'most' in ans:
                    predicate_adj.append('最大')
                elif 'least' in ans:
                    predicate_adj.append('最小')
            elif 'long' in ans:
                ask_predicate.append('长度')
                if 'most' in ans:
                    predicate_adj.append('最长')
                elif 'least' in ans:
                    predicate_adj.append('最短')

        elif 'mountain' in ans:
            ask_type.append('山峰')
            ask_type.append('山脉')
            if 'high' in ans:
                ask_predicate.append('海拔')
                if 'most' in ans:

                    predicate_adj.append('最高')
                elif 'least' in ans:
                    predicate_adj.append('最低')
            if 'south' in ans:
                ask_predicate.append('纬度')
                predicate_adj.append('最南')
            if 'north' in ans:
                ask_predicate.append('纬度')
                predicate_adj.append('最北')
            if 'east' in ans:
                ask_predicate.append('经度')
                predicate_adj.append("最东")
            if 'west' in ans:
                ask_predicate.append('经度')
                predicate_adj.append('最西')
            if 'long' in ans:
                ask_predicate.append('长度')
                ask_predicate.append('')
                predicate_adj.append('最长')
        elif 'sea' in ans:
            ask_type.append('海洋')
            if 'area' in ans:
                ask_predicate.append('面积')
                if 'most' in ans:
                    predicate_adj.append('最大')
                elif 'least' in ans:
                    predicate_adj.append('最小')
            if 'deep' in ans:
                ask_predicate.append('深度')
                ask_predicate.append('')
                if 'most' in ans:
                    predicate_adj.append('最深')
                elif 'least' in ans:
                    predicate_adj.append('最浅')


        ent_dict = {'limit': limit_location, 'ask': ask_type, 'predicate': ask_predicate, 'predicate_adj':predicate_adj}

        return "task_calculate_most", ent_dict, ans



if __name__ == '__main__':
    a = calculateUtil()
    a.checkCalculate("美国面积最大的淡水湖")

