# @Time : 2020/12/13 1:55 PM 
# @Author : LinXiaofei
# @File : parseSentence.py



import configparser
from backend.data.data_process import read_file



class ParseSentence(object):
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("../backend/config.ini")
        subject = config['DEFAULT']['subject']
        #self.graph_util = graphSearch()
        #self.nlu_util = SentenceSimilarity()
        self.valuable_pos = ['a', 'b', 'm', 'n', 'nd', 'ni', 'nl', 'ns', 'nt', 'nz', 'v', 'j','i','nh']

        instanceArray = list(set(read_file("../backend/data/"+subject+"/entity.csv")))
        self.instanceArray = sorted(instanceArray, key=lambda i: len(i), reverse=True)
        print("=====================================================================")
        print(self.instanceArray)
        print("=====================================================================")


        proArray = read_file("../backend/data/"+subject+"/cleanpro.csv")
        self.proArray = sorted(proArray, key=lambda i: len(i), reverse=True)

        relArray = read_file("../backend/data/"+subject+"/cleanrel.csv")
        self.relArray = sorted(relArray, key=lambda i: len(i), reverse=True)

        etype = list(set(read_file("../backend/data/" + subject + "/etype.csv")))
        self.typeArray = sorted(etype, key=lambda i: len(i), reverse=True)

        self.r = ['什么','何','怎么','哪里','哪','哪些','哪个','如何','多少','多']

    def getEntity(self,words):
        entity = []
        for word in words:

            if word in self.instanceArray:
                entity.append(word)

        return entity

    def getPositionEntity(self,words,pos):
        entity = []
        for word_index in range(len(words)):

            if words[word_index] in self.instanceArray and pos[word_index] == 'ns':
                entity.append(words[word_index])

        return entity


    def getEtype(self,words):
        etype = []

        for word in words:
            if word in self.typeArray:
                etype.append(word)

        return etype

    def getCount(self,index,dep):

        if dep[index][2] == 'SBV':
            return 5
        if dep[index][2] == 'ATT':
            att_obeject = dep[index][1]-1

            if dep[att_obeject][2] == 'SBV':
                return 4
            if dep[att_obeject][2] == 'VOB':
                return 2
        if dep[index][2] == 'VOB':
            return 3
        if dep[index][2] == 'FOB':
            return 3

        return 0

    def extractType(self, words):

        de_index = -1
        r_index = -1
        for i in range(len(words)):
            print(words[i])

            if words[i] in self.r:
                r_index = i

            if i == 0 and words[i + 1] in self.typeArray and words[i] in self.r:
                split_index = i + 1
                end_words = words[split_index + 1:]
                ent = words[split_index]
                return ent, "split_end"

            if len(words) > i + 3 and words[i + 1] in ['是', '有', '在']:
                if words[i + 2] in self.r and words[i + 3] in self.typeArray:
                    split_index = i
                    front_words = words[:split_index]
                    end_words = words[split_index + 1:]
                    ent = words[split_index + 3]
                    return ent, "split"

            if words[i] == '的':


                de_index = i
                if words[i + 1] in self.typeArray and words[i + 1] not in self.proArray:
                    split_index = i
                    front_words = words[:split_index]
                    end_words = words[split_index + 1:]
                    ent = words[split_index + 1]

                    return ent, "split"

        return None, "normal"

    def getWordsExtractType(self, words, dep, pos):

        SBV = 0
        VOB = 0
        for i in range(len(words)):

            if dep[i][2] == 'SBV':
                SBV = SBV+1
            if dep[i][2] == 'VOB':
                VOB = VOB+1
        if VOB >=2 or SBV >=2:
            """
            if ',' in words:
                split_index = words.index(",")
                front_words = words[:split_index]
                end_words = words[split_index+1:]
                for r in self.r:
                    if r in end_words:
                        return [front_words,end_words,split_index,"end"],"WPwords"
                return [front_words,end_words,split_index,"front"],"WPwords"

            if '，' in words:
                split_index = words.index("，")

                front_words = words[:split_index]
                end_words = words[split_index+1:]
                for r in self.r:
                    if r in end_words:
                        return [front_words,end_words,split_index,"end"],"WPwords"
                return [front_words, end_words, split_index,"front"], "WPwords"
            """
            de_index = -1
            r_index = -1
            for i in range(len(words)):

                if words[i] in self.r:
                    r_index = i

                if i == 0 and words[i + 1] in self.typeArray and words[i] in self.r:
                    split_index = i + 1
                    end_words = words[split_index + 1:]
                    ent = words[split_index]
                    return [end_words, split_index, ent], "split_end"

                if len(words) > i + 3 and words[i + 1] in ['是','有','在']:
                    if words[i + 2] in self.r and words[i + 3] in self.typeArray:
                        split_index = i
                        front_words = words[:split_index]
                        end_words = words[split_index + 1:]
                        ent = words[split_index + 3]
                        return [front_words, split_index, ent], "split"

                if words[i] == '的' and len(words)>i+1:
                    print(words,len(words))
                    print(words[i+1],"asdasdasdasdsadasd")


                    de_index = i
                    if words[i+1] in self.typeArray and words[i+1] not in self.proArray:
                        split_index = i
                        front_words = words[:split_index]
                        end_words = words[split_index + 1:]
                        ent = words[split_index+1]
                        print([front_words, split_index, ent],"split")
                        return  [front_words, split_index, ent],"split"

            print(r_index,de_index,pos[de_index + 1],words[de_index + 1])
            if r_index > de_index and (pos[de_index + 1] in ['n', 'nd', 'ni', 'nl', 'ns', 'nt', 'nz']
            or words[de_index + 1] in ['是','有','在']):
                split_index = de_index
                front_words = words[:split_index]
                end_words = words[split_index + 1:]
                ent = ""

                for w in front_words:
                    if w in self.instanceArray or w in self.typeArray:
                        ent = w

                if len(ent)>0:

                    return [front_words, split_index, ent], "split_false"

            """
            if '的' in words:

                split_index = words.index("的")

                front_words = words[:split_index]
                end_words = words[split_index+1:]
                for r in self.r:
                    if r in end_words:
                        return [front_words,end_words,split_index,"end"],"RADwords"
                return [front_words, end_words,split_index,"front"], "RADwords"
            """

        return None,"normal"

    def checkCombineEnt(self, ent, coo):

        for e in self.instanceArray:
            if ent in e and coo in e:
                return e

    def getExpandEnt(self, ent):
        print(ent)
        array = []

        for e in self.instanceArray:
            if ent in e:
                array.append(e)

        array = sorted(array, key=lambda i: len(i))
        print(array,"array==============")
        return array

    def extractBestEnt(self,words,dep):

        entity = self.getEntity(words)
        etype = self.getEtype(words)

        if len(entity) == 0 and len(etype)==0:

            return None,[],"false"
        if len(entity)==1 and len(etype)==0:
            array = self.getExpandEnt(entity[0])
            return entity[0],array,"entity"
        if len(entity)==0 and len(etype)==1:
            return etype[0],[],"etype"

        ent_count = []
        type_count = []
        for e in entity:

            e_index = words.index(e)
            print("====================e",e, words,e_index)
            ent_count.append(self.getCount(e_index,dep))

        for t in etype:
            t_index = words.index(t)
            print("====================t", t, words, t_index)
            c = self.getCount(t_index,dep)
            if t in self.proArray:
                c = c-4

            type_count.append(c)

        ent_index = -1
        ent_c = 0

        type_c = 0
        type_index = -1


        for c_i in range(len(ent_count)):


            if ent_count[c_i] >= ent_c:
                ent_c = ent_count[c_i]
                ent_index = c_i

        for c_i in range(len(type_count)):


            if type_count[c_i] > type_c:
                type_c = type_count[c_i]
                type_index = c_i
        print(entity,ent_count)
        print(etype, type_count)

        if ent_index == -1 and type_index == -1:
            return None, [], "false"
        print(ent_c,type_c)



        if ent_index != -1 and ent_c >= type_c:

            for i in range(len(words)):

                if ent_index > -1 and dep[i][2] == 'COO' and words[dep[i][1]-1] == entity[ent_index]:
                    coo_entity = self.checkCombineEnt(entity[ent_index],words[i])
                    if coo_entity:
                        array = self.getExpandEnt(coo_entity)
                        print("============================1")
                        return [coo_entity,dep[i][1]-1],array,"coo_entity"
            print("============================2")
            array = self.getExpandEnt(entity[ent_index])
            return entity[ent_index],array,"entity"

        else:
            print(words)
            for i in range(len(words)):
                print(type_index,dep[i][1],dep[i][2])
                if type_index > -1 and dep[i][2] == 'COO' and words[dep[i][1]-1] == etype[type_index]:
                    coo_entity = self.checkCombineEnt(etype[type_index],words[i])
                    if coo_entity:
                        array = self.getExpandEnt(coo_entity)
                        print("============================5")
                        return [coo_entity,dep[i][1]-1],array,"coo_entity"
            print("============================3")
            return etype[type_index],[],"etype"
        print("============================4")


    def getConcept(self, entity):
        pass
        """
        type_list = self.graph_util.getFather(entity)

        best_father = ""
        max_count = 0

        for father in type_list:
            son_count = len(self.graph_util.getEntityByType(father))
            if son_count > max_count:
                max_count = son_count
                best_father = father

        return best_father
        """

    def getStandard(self,entity,best_father,words):
        return words.replace(entity, best_father)

    """
    def getSimilar(self, words, templates):
        print(templates)
        self.nlu_util.set_sentences(templates)
        self.nlu_util.TfidfModel()
        return self.nlu_util.similarity_top_k(words,3)

    def getSimilarByLsi(self, words, templates):
        self.nlu_util.set_sentences(templates)
        self.nlu_util.LsiModel()
        return self.nlu_util.similarity_top_k(words,5)[0]


    def getSimilarPro(self, words, pros):


        self.nlu_util.set_sentences(list(pros))
        self.nlu_util.LsiModel()

        return self.nlu_util.similarity_top_k(words,1)[0]



    def matchTemplate(self, father, words):
        raw_template = list(read_file("../backend/template_library/"+subject+"/"+father+".csv"))
        template_arr = []
        for template in raw_template:

            if template != "==========":
                template_arr.append(template)
            else:
                if words in template_arr:
                    #print(template_arr)
                    return [template_arr[0],template_arr[1]]
                else:
                    template_arr = []
        return None


    def getMatchResult(self, templates, words):

        if words in templates:
            return [1,templates.index(words)]
        else:
            similar_tempalte = self.getSimilar(words, templates)
            print(similar_tempalte,"===============")
            similar_tempalte_index = []
            for tem in similar_tempalte:
                similar_tempalte_index.append(templates.index(tem[0]))
            if similar_tempalte[0][1] >= 0.6:
                return [2,similar_tempalte_index]
        return [0,"无法回答"]
    """

    def getValuableWords(self, words, pos, dep):

        valuable_words = []
        word_count = []

        begin_index = -1
        end_index = -1

        if "“" in words and "”" in words:
            begin_index = words.index("“")
            end_index = words.index("”")
        if "《" in words and "》" in words:
            begin_index = words.index("《")
            end_index = words.index("》")

        for i in range(len(words)):
            print(i,"=======================")
            if begin_index == "-1":
                if i == "\"" and "\"" in words[i:]:
                    begin_index = i
                    end_index = words[i+1:].index("\"")

            print(i,dep[i][1],"asdgalsjdhaskldjhasldjhasljdhaskldjashd")
            #print(dep[dep[i][1]-1],words[i],len(dep),len(words),"=======================")
            if pos[i] in self.valuable_pos:
                if words[i] in ['是', '有', '在', '于']:
                    continue
                valuable_words.append(words[i])
                if i>begin_index and i < end_index:
                    word_count.append(10)
                elif pos[i] in ["m","nt"]:
                    word_count.append(5)
                elif words[i] in self.instanceArray or words[i] in self.typeArray:
                    word_count.append(4)
                elif dep[i][2] == 'HED' and words[i] not in ['是','有','在','于']:
                    word_count.append(4)
                elif dep[i][2] == 'SBV':
                    word_count.append(4)
                elif dep[i][2] == 'VOB':
                    word_count.append(3)
                elif dep[i][2] == 'ATT' and dep[i][1] <= len(words) and dep[dep[i][1]-1][2]=='SBV':
                    word_count.append(2)
                elif dep[i][2] == 'ATT' and dep[i][1] <= len(words) and dep[dep[i][1]-1][2]=='VOB':
                    word_count.append(2)
                else:
                    word_count.append(1)


        return valuable_words,word_count

