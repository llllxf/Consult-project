# @Time : 2020/12/27 12:27 PM 
# @Author : LinXiaofei
# @File : NumPro.py


class NumPro(object):
    """

    ent + numpro/numpro_alias + v + r
    ent + numpro/numpro_alias + v + r + unit/noun
    ent + numpro/numpro_alias + v + r + adj


    """

    def __init__(self):
        self.ent = ""
        self.numpro = ""
        self.alias = []
        self.adj = []
        self.unit = []
        self.noun = []
        self.r = '多少'
        self.r_adj = '多'


    def setEnt(self,ent):
        self.ent = ent

    def setPro(self, pro):
        self.numpro = pro

    def setAlias(self,alias):
        self.alias = []
        alias_array = alias.split(",")
        for a in alias_array:
            self.alias.append(a)

    def setAdj(self,adj):
        self.adj = []
        adj_array = adj.split(",")
        for a in adj_array:
            self.adj.append(a)

    def setUnit(self,unit):
        self.unit = []
        unit_array = unit.split(",")
        for u in unit_array:
            self.unit.append(u)

    def setNoun(self,noun):
        self.noun = []
        noun_array = noun.split(",")
        for n in noun_array:
            self.noun.append(n)

    def getStandard(self):
        standard_template = []
        standard_template.append(self.ent+"的"+self.numpro+"是"+self.r)
        #standard_template.append(self.ent + "的" + self.numpro + "有" + self.r)

        for u in self.unit:
            standard_template.append(self.ent+"的"+self.numpro+"是"+self.r+u)
            #standard_template.append(self.ent + "的" + self.numpro + "有" + self.r+u)

        for a in self.adj:
            standard_template.append(self.ent + "的" + self.numpro + "是" + self.r_adj + a)
            #standard_template.append(self.ent + "的" + self.numpro + "有" + self.r_adj + a)

        for n in self.noun:
            standard_template.append(self.ent+"的"+self.numpro+"是"+self.r+n)
            standard_template.append(self.ent + "是" + self.r+n)

        return standard_template

    def getAlias(self):

        alias_template = []

        for a in self.alias:
            alias_template.append(self.ent + "的" + a + "是" + self.r)
            alias_template.append(self.ent + "的" + a + "有" + self.r)

            for u in self.unit:
                alias_template.append(self.ent + "的" + a + "是" + self.r + u)
                alias_template.append(self.ent + "的" + a + "有" + self.r + u)

            for a in self.adj:
                alias_template.append(self.ent + "的" + a + "是" + self.r_adj + a)
                alias_template.append(self.ent + "的" + a + "有" + self.r_adj + a)

            for n in self.noun:
                alias_template.append(self.ent + "的" + a + "是" + self.r + n)
                alias_template.append(self.ent + "的" + a + "有" + self.r + n)

        return alias_template

    def getTemplate(self):
        template = []
        template += self.getStandard()
        template += self.getAlias()
        return template











