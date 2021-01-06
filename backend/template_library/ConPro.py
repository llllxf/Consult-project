# @Time : 2020/12/27 12:28 PM 
# @Author : LinXiaofei
# @File : ConPro.py
"""
    描述型
    ent + conpro/alias_conpro + 的概况 + 是什么
    ent + conpro/alias_conpro + 的情况 + 是什么
    ent + conpro/alias_conpro + 的状况 + 是什么
    ent + conpro/alias_conpro + 有 + 什么/哪些 + 特征
    ent + conpro/alias_conpro + 的特征 + 是/有 + 什么/哪些

    范围型
    ent + conpro/alias_conpro + 是/有 + 什么/哪些
    ent + 以 + 什么/哪些 + conpro/alias_conpro 为主
    ent + 有 + 哪些/什么 + conpro/alias_conpro
    ent + 主要的 + conpro/alias_conpro 是/有 + 什么/哪些
    ent + v + 的 + conpro/alias_conpro + 有哪些/有什么

    唯一型
    ent + 的 + conpro/alias_conpro + 是什么
    ent + v + 什么
"""

class DesConPro(object):
    def __init__(self):
        self.ent = ""
        self.conpro = ""
        self.alias = []
        self.standard_template = []
        self.alias_template = []

    def setEnt(self,ent):
        self.ent = ent

    def setConPro(self, pro):
        self.conpro = pro

    def setAlias(self,alias):
        alias_array = alias.split(",")
        for a in alias_array:
            self.alias.append(a)

    def getStandard(self):
        self.standard_template.append(self.ent + self.conpro+"的概况是什么")
        self.standard_template.append(self.ent + "的" +self.conpro + "有什么特征")
        self.standard_template.append(self.ent + "的" + self.conpro + "有哪些特征")
        self.standard_template.append(self.ent  + self.conpro + "的特征有哪些")
        self.standard_template.append(self.ent + self.conpro + "的特征有什么")
        self.standard_template.append(self.ent + self.conpro + "的特征是哪些")
        self.standard_template.append(self.ent + self.conpro + "的特征是什么")

        return self.standard_template

    def getAlias(self):
        for a in self.alias:
            self.alias_template.append(self.ent + a + "的概况是什么")
            self.alias_template.append(self.ent + a + "的情况是什么")
            self.alias_template.append(self.ent + a + "的情况是什么")
            self.alias_template.append(self.ent + "的" + a + "有什么特征")
            self.alias_template.append(self.ent + "的" + a + "有哪些特征")
            self.alias_template.append(self.ent + "的特征" + a + "有哪些")
            self.alias_template.append(self.ent + "的特征" + a + "有什么")
            self.alias_template.append(self.ent + "的特征" + a + "是哪些")
            self.alias_template.append(self.ent + "的特征" + a + "是什么")

        return self.alias_template

    def getTemplate(self):
        template = []
        template += self.getStandard()
        template += self.getAlias()
        return template

class OnlyConPro(object):
    def __init__(self):
        self.ent = ""
        self.conpro = ""
        self.alias = []
        self.verb = []
        self.standard_template = []
        self.alias_template = []

    def setEnt(self,ent):
        self.ent = ent

    def setConPro(self, pro):
        self.conpro = pro

    def setAlias(self,alias):
        alias_array = alias.split(",")
        for a in alias_array:
            self.alias.append(a)

    def setVerb(self,verb):
        verb_array = verb.split(",")
        for v in verb_array:
            self.verb.append(v)

    def getStandard(self):

        self.standard_template.append(self.ent + "的" +self.conpro + "是什么")
        for v in self.verb:
            self.standard_template.append(self.ent + v + "什么")

        return self.standard_template

    def getAlias(self):
        for a in self.alias:
            self.alias_template.append(self.ent + "的" + a + "是什么")
        return self.alias_template

    def getTemplate(self):
        template = []
        template += self.getStandard()
        template += self.getAlias()
        return template


class RangeConPro(object):
    def __init__(self):
        self.ent = ""
        self.conpro = ""
        self.alias = []
        self.verb = []
        self.standard_template = []
        self.alias_template = []

    def setEnt(self,ent):
        self.ent = ent

    def setConPro(self, pro):
        self.conpro = pro

    def setAlias(self,alias):
        alias_array = alias.split(",")
        #print(alias_array)
        for a in alias_array:
            self.alias.append(a)

    def setVerb(self,verb):
        verb_array = verb.split(",")
        for v in verb_array:
            self.verb.append(v)

    def getStandard(self):
        self.standard_template.append(self.ent + "主要的" + self.conpro + "是什么")
        self.standard_template.append(self.ent + "的" +self.conpro + "有什么")
        self.standard_template.append(self.ent + "的" +self.conpro + "是哪些")
        self.standard_template.append(self.ent + "的" +self.conpro + "有哪些")
        self.standard_template.append(self.ent + "主要的" +self.conpro + "有什么")
        self.standard_template.append(self.ent + "主要的" + self.conpro + "有哪些")
        self.standard_template.append(self.ent + "主要的" + self.conpro + "是哪些")
        self.standard_template.append(self.ent + "以哪些" + self.conpro + "为主")
        self.standard_template.append(self.ent + "以什么" + self.conpro + "为主")
        self.standard_template.append(self.ent + "有哪些" + self.conpro)
        self.standard_template.append(self.ent + "有什么" + self.conpro)

        for v in self.verb:
            self.standard_template.append(self.ent + v + "的"+ self.conpro + "有什么")
            self.standard_template.append(self.ent + v + "的"+ self.conpro + "是哪些")
            self.standard_template.append(self.ent + v + "的"+ self.conpro + "是什么")
            self.standard_template.append(self.ent + v + "的" + self.conpro + "是哪些")




        return self.standard_template

    def getAlias(self):
        #print(self.alias, "====================",1)
        for a in self.alias:
            #self.standard_template.append(self.ent + a + "是什么")
            #self.standard_template.append(self.ent + a + "有什么")
            #self.standard_template.append(self.ent + a + "是哪些")
            #self.standard_template.append(self.ent + a + "有哪些")
            self.alias_template.append(self.ent + "主要的" + a + "有什么")
            self.alias_template.append(self.ent + "主要的" + a + "有哪些")
            self.alias_template.append(self.ent + "主要的" + a + "是什么")
            self.alias_template.append(self.ent + "主要的" + a + "是哪些")

            self.alias_template.append(self.ent + "以哪些" + a + "为主")
            self.alias_template.append(self.ent + "以什么" + a + "为主")
            self.alias_template.append(self.ent + "有哪些" + a)
            self.alias_template.append(self.ent + "有什么" + a)

            for v in self.verb:
                self.alias_template.append(self.ent + v + "的" + a + "有什么")
                self.alias_template.append(self.ent + v + "的" + a + "是哪些")
                self.alias_template.append(self.ent + v + "的" + a + "是什么")
                self.alias_template.append(self.ent + v + "的" + a + "是哪些")

        return self.alias_template

    def getTemplate(self):
        template = []
        template += self.getStandard()
        template += self.getAlias()
        return template






