# @Time : 2021/1/14 6:21 PM 
# @Author : LinXiaofei
# @File : analysisWords.py
import numpy as np

class analysisWords(object):
    def __init__(self):
        self.none_req = ['哪','哪里','何','哪些','什么']
        self.v_req = ['如何','怎么']
        self.num_req = ['多','多少']


    def getTemplateMode(self,words):
        template_mode = list(np.copy(words))
        #print(template_mode)
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






