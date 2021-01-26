# @Time : 2020/12/27 12:28 PM 
# @Author : LinXiaofei
# @File : ConPro.py
"""
    原因型
    形成 + ent + 的原因是什么
    形成 + ent + 的 + conpro.split("原因")[0]/alias_conpro + "因素是什么"
    造成 + ent + 的 + conpro.split("原因")[0]/alias_conpro + "因素是什么"

    n+n
    名词分离型
    ent + "的" + sepnonepro + "是什么"
    ent + "主要的" + sepnonepro + "是什么"
    ent + "的" + front_pro + "是什么" + end_pro
    ent + "的" + front_pro + "以" + end_pro + "为主"

    v+n
    动词分离型
    ent + "的" + sepverbpro + "是什么"
    ent + front_pro + "的" + end_pro + "是什么"

    描述型
    ent + conpro/alias_conpro + 的概况 + 是什么
    ent + conpro/alias_conpro + 的情况 + 是什么
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

    如何型
    ent + 是怎么 + howpro + 的
    怎么 + howpro + ent

    如何分解型
    ent + 的 + sephowpro + 是什么
    ent + 的 + front_none + 是怎么 + end_verb + 的


"""
class HowPro(object):
    def __init__(self):
        self.ent = ""
        self.howpro = ""
        self.alias = []

    def setEnt(self,ent):
        self.ent = ent

    def setPro(self, pro):
        self.howpro = pro

    def setAlias(self,alias):
        self.alias = []
        alias_array = alias.split(",")
        for a in alias_array:
            self.alias.append(a)

    def getStandard(self):

        standard_template = []
        standard_template.append( self.ent + "是怎么" + self.howpro + "的")
        standard_template.append(self.ent + "是怎么" + self.howpro + "的")
        standard_template.append("怎么" + self.howpro + self.ent)

        return standard_template

    def getAlias(self):
        alias_template = []
        for a in self.alias:
            alias_template.append(self.ent + "是怎么" + a + "的")
            alias_template.append(self.ent + "是怎么" + a + "的")
            alias_template.append("怎么" + a + self.ent)

        return alias_template

    def getTemplate(self):
        template = []
        template += self.getStandard()
        template += self.getAlias()
        return template


class SepHowPro(object):

    def __init__(self):
        self.ent = ""
        self.sephowpro = ""
        self.alias = []

    def setEnt(self,ent):
        self.ent = ent

    def setPro(self, pro):

        self.sephowpro = pro

    def setAlias(self,alias):
        self.alias = []
        alias_array = alias.split(",")
        for a in alias_array:
            self.alias.append(a)

    def getStandard(self):
        front_none = self.sephowpro[:-2]
        end_verb = self.sephowpro[-2:]

        standard_template = []

        standard_template.append(self.ent + "的" + self.sephowpro + "是什么")
        standard_template.append(self.ent + "的" + front_none + "是怎么" + end_verb + "的")
        standard_template.append(self.ent + "的" + front_none + "是怎么" + end_verb + "的")

        return standard_template

    def getAlias(self):
        alias_template = []
        for a in self.alias:
            front_none = a[:-2]
            end_verb = self.sephowpro[-2:]
            alias_template.append(self.ent + "的" + a + "是什么")
            alias_template.append(self.ent + "的" + front_none + "是怎么" + end_verb + "的")
            alias_template.append(self.ent + "的" + front_none + "是怎么" + end_verb + "的")

        return alias_template

    def getTemplate(self):
        template = []
        template += self.getStandard()
        template += self.getAlias()
        return template


class SepNonePro(object):

    def __init__(self):
        self.ent = ""
        self.sepnonepro = ""
        self.alias = []
        self.verb = []

    def setEnt(self,ent):
        self.ent = ent

    def setPro(self, pro):
        if "主要" in pro:
            pro = pro.replace("主要","")
        self.sepnonepro = pro

    def setAlias(self,alias):
        self.alias = []
        alias_array = alias.split(",")
        for a in alias_array:
            self.alias.append(a)

    def setVerb(self,verb):
        self.verb = []
        verb_array = verb.split(",")
        for v in verb_array:
            self.verb.append(v)

    def getStandard(self):
        front_pro = self.sepnonepro[:-2]
        end_pro = self.sepnonepro[-2:]

        standard_template = []
        standard_template.append(self.ent + "的" + self.sepnonepro + "是什么")
        standard_template.append(self.ent + "主要的" + self.sepnonepro + "是什么")
        standard_template.append(self.ent + "的" + front_pro + "以什么" + end_pro + "为主")
        standard_template.append(self.ent + "的" + front_pro + "是什么" + end_pro)

        return standard_template

    def getAlias(self):
        alias_template = []
        for a in self.alias:
            front_pro = a[:-2]
            end_pro = a[-2:]
            alias_template.append(self.ent + "的" + a + "是什么")
            alias_template.append(self.ent + "主要的" + a + "是什么")
            alias_template.append(self.ent + "的" + front_pro + "以什么" + end_pro + "为主")
            alias_template.append(self.ent + "的" + front_pro + "是什么" + end_pro)

        return alias_template

    def getTemplate(self):
        template = []
        template += self.getStandard()
        template += self.getAlias()
        return template

class SepVerbPro(object):

    def __init__(self):
        self.ent = ""
        self.sepverbpro = ""
        self.alias = []
        self.verb = []

    def setEnt(self,ent):
        self.ent = ent

    def setPro(self, pro):
        self.sepverbpro = pro

    def setAlias(self,alias):
        self.alias = []
        alias_array = alias.split(",")
        for a in alias_array:
            self.alias.append(a)

    def setVerb(self,verb):
        self.verb = []
        verb_array = verb.split(",")
        for v in verb_array:
            self.verb.append(v)

    def getStandard(self):
        front_pro = self.sepverbpro[:-2]
        end_pro = self.sepverbpro[-2:]

        standard_template = []
        standard_template.append(self.ent + "的" + self.sepverbpro + "是什么")
        standard_template.append(self.ent + front_pro + "的" + end_pro + "是什么")
        standard_template.append(self.ent + front_pro + "什么" + end_pro)

        for v in self.verb:
            standard_template.append(self.ent + v + "什么")
            standard_template.append(self.ent + v + "什么")


        return standard_template

    def getAlias(self):
        alias_template = []
        for a in self.alias:
            front_pro = a[:-2]
            end_pro = a[-2:]
            alias_template.append(self.ent + "的" + a + "是什么")
            alias_template.append(self.ent + front_pro + "的" + end_pro + "是什么")
            alias_template.append(self.ent + front_pro + "什么" + end_pro)

        return alias_template

    def getTemplate(self):
        template = []
        template += self.getStandard()
        template += self.getAlias()
        return template

class ReasonPro(object):

    def __init__(self):
        self.ent = ""
        self.reasonpro = ""
        self.alias = []

    def setEnt(self,ent):
        self.ent = ent

    def setPro(self, pro):
        self.reasonpro = pro

    def setAlias(self,alias):
        self.alias = []
        alias_array = alias.split(",")
        for a in alias_array:
            self.alias.append(a)

    def getStandard(self):
        if '原因' in self.reasonpro:

            pro = self.reasonpro.replace("原因","")
        if '因素' in self.reasonpro:
            pro = self.reasonpro.replace("因素", "")
        standard_template = []
        standard_template.append("形成" + self.ent + "的" + self.reasonpro + "是什么")
        standard_template.append("形成" + self.ent + "的" + pro + "因素是什么")
        standard_template.append("造成" + self.ent + "的" + pro + "因素是什么")

        return standard_template

    def getAlias(self):
        alias_template = []
        for a in self.alias:
            alias_template.append("形成" + self.ent + "的"+ a +"是什么")
            alias_template.append("造成" + self.ent + "的" + a + "因素是什么")
            alias_template.append("造成" + self.ent + "的" + a + "因素是什么")

        return alias_template

    def getTemplate(self):
        template = []
        template += self.getStandard()
        template += self.getAlias()
        return template

class DesConPro(object):
    def __init__(self):
        self.ent = ""
        self.conpro = ""
        self.alias = []


    def setEnt(self,ent):
        self.ent = ent

    def setPro(self, pro):
        self.conpro = pro

    def setAlias(self,alias):
        self.alias = []
        alias_array = alias.split(",")
        for a in alias_array:
            self.alias.append(a)

    def getStandard(self):
        standard_template = []
        standard_template.append(self.ent + self.conpro + "的特征是什么")
        standard_template.append(self.ent + self.conpro+"的概况是什么")
        standard_template.append(self.ent + "的" +self.conpro + "是什么特征")


        return standard_template

    def getAlias(self):
        alias_template = []
        for a in self.alias:
            alias_template.append(self.ent + a + "的特征是什么")
            alias_template.append(self.ent + a + "的概况是什么")
            alias_template.append(self.ent + "的" + a + "是什么特征")

        return alias_template

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

    def setEnt(self,ent):
        self.ent = ent

    def setPro(self, pro):
        self.conpro = pro

    def setAlias(self,alias):
        self.alias = []
        alias_array = alias.split(",")
        for a in alias_array:
            self.alias.append(a)

    def setVerb(self,verb):
        self.verb = []
        verb_array = verb.split(",")
        for v in verb_array:
            self.verb.append(v)

    def getStandard(self):
        standard_template = []
        standard_template.append(self.ent + "的" +self.conpro + "是什么")
        standard_template.append(self.ent + "有什么" + self.conpro)
        standard_template.append(self.ent + "的" + self.conpro + "有什么")

        for v in self.verb:
            standard_template.append(self.ent + v + "什么")
        return standard_template

    def getAlias(self):
        alias_template = []
        for a in self.alias:
            alias_template.append(self.ent + "的" + a + "是什么")
            alias_template.append(self.ent + "有什么" + a)
            alias_template.append(self.ent + "的" + a + "有什么")


        return alias_template

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


    def setEnt(self,ent):
        self.ent = ent

    def setPro(self, pro):
        if "主要" in pro:
            pro = pro.replace("主要","")

        self.conpro = pro

    def setAlias(self,alias):
        self.alias = []
        alias_array = alias.split(",")
        for a in alias_array:
            self.alias.append(a)

    def setVerb(self,verb):
        self.verb = []
        verb_array = verb.split(",")
        for v in verb_array:
            self.verb.append(v)

    def getStandard(self):
        standard_template = []
        standard_template.append(self.ent + "的" + self.conpro + "以什么为主")
        standard_template.append(self.ent + "主要的" + self.conpro + "是什么")
        standard_template.append(self.ent + "的" +self.conpro + "是什么")
        standard_template.append(self.ent + "以什么" + self.conpro + "为主")


        for v in self.verb:
            standard_template.append(self.ent + v + "的"+ self.conpro + "是什么")
            standard_template.append(self.ent + v + "的" + self.conpro + "是什么")

        return standard_template

    def getAlias(self):
        alias_template = []

        for a in self.alias:
            alias_template.append(self.ent + "的" + a + "以什么为主")
            alias_template.append(self.ent + "主要的" + a + "是什么")
            alias_template.append(self.ent + "的" + a + "是什么")
            alias_template.append(self.ent + "以什么" + a + "为主")


            for v in self.verb:
                alias_template.append(self.ent + v + "的" + a + "是什么")

        return alias_template

    def getTemplate(self):
        template = []
        template += self.getStandard()
        template += self.getAlias()
        return template