# @Time : 2021/1/14 6:21 PM 
# @Author : LinXiaofei
# @File : analysisWords.py
import numpy as np

class analysisWords(object):
    def __init__(self):
        self.none_req = ['哪','哪里','何','哪些','什么','哪些','哪个']
        self.v_req = ['如何','怎么']
        self.num_req = ['多少','多']
        self.valuable_pos = ['a','b','m','n','nd','ni','nl','ns','nt','nz','v','j']


    def getTemplateMode(self,words):
        template_mode = list(np.copy(words))

        index = 0
        flag = ""
        for word in template_mode:

            if word == '有':
                template_mode[index] = '是'
            if word in self.none_req[:-1]:
                template_mode[index] = self.none_req[-1]
                flag = "none"
            if word in self.v_req[:-1]:
                template_mode[index] = self.v_req[-1]
                flag = "v"
            if word in self.num_req[:-1]:
                template_mode[index] = self.num_req[-1]
                flag = "num"
            index = index+1
        return flag,"".join(template_mode)


    def getRIndex(self,words):

        r_array = self.none_req+self.v_req+self.num_req

        for r in r_array:
            if r in words:
                return words.index(r)


    def analysisPro(self,words,pro_list,key_list):


        best_pro = pro_list[0]
        r_index = self.getRIndex(words)

        dis = 1000000
        index = 0
        for k in key_list:
            p = pro_list[index]
            k_index = words.index(k)
            tem_dis = np.abs(k_index-r_index)
            if tem_dis < dis:
                dis = tem_dis
                best_pro = p
            index = index+1


        return best_pro




