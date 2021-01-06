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
        self.standard_template = []
        self.alias_template = []

    def setEnt(self,ent):
        self.ent = ent

    def setNumPro(self, pro):
        self.numpro = pro

    def setAlias(self,alias):
        alias_array = alias.split(",")
        for a in alias_array:
            self.alias.append(a)

    def setAdj(self,adj):
        adj_array = adj.split(",")
        for a in adj_array:
            self.adj.append(a)

    def setUnit(self,unit):
        unit_array = unit.split(",")
        for u in unit_array:
            self.unit.append(u)

    def setNoun(self,noun):
        noun_array = noun.split(",")
        for n in noun_array:
            self.unit.append(n)

    def getStandard(self):
        self.standard_template.append(self.ent+"的"+self.numpro+"是"+self.r)
        self.standard_template.append(self.ent + "的" + self.numpro + "有" + self.r)

        for u in self.unit:
            self.standard_template.append(self.ent+"的"+self.numpro+"是"+self.r+u)
            self.standard_template.append(self.ent + "的" + self.numpro + "有" + self.r+u)

        for a in self.adj:
            self.standard_template.append(self.ent + "的" + self.numpro + "是" + self.r_adj + a)
            self.standard_template.append(self.ent + "的" + self.numpro + "有" + self.r_adj + a)

        for n in self.noun:
            self.standard_template.append(self.ent+"的"+self.numpro+"是"+self.r+n)
            self.standard_template.append(self.ent + "的" + self.numpro + "有" + self.r+n)



        return self.standard_template

    def getAlias(self):

        for a in self.alias:
            self.alias_template.append(self.ent + "的" + a + "是" + self.r)
            self.alias_template.append(self.ent + "的" + a + "有" + self.r)

            for u in self.unit:
                self.alias_template.append(self.ent + "的" + a + "是" + self.r + u)
                self.alias_template.append(self.ent + "的" + a + "有" + self.r + u)

            for a in self.adj:
                self.alias_template.append(self.ent + "的" + a + "是" + self.r_adj + a)
                self.alias_template.append(self.ent + "的" + a + "有" + self.r_adj + a)

            for n in self.noun:
                self.alias_template.append(self.ent + "的" + a + "是" + self.r + n)
                self.alias_template.append(self.ent + "的" + a + "有" + self.r + n)

        return self.alias_template

    def getTemplate(self):
        template = []
        template += self.getStandard()
        template += self.getAlias()
        return template











