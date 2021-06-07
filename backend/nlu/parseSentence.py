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

        self.valuable_pos = ['a', 'b','m', 'n', 'nd', 'ni', 'nl', 'ns', 'nt', 'nz', 'v', 'j','i','nh']

        instanceArray = list(set(read_file("../backend/data/"+subject+"/entity.csv")))
        self.instanceArray = sorted(instanceArray, key=lambda i: len(i), reverse=True)
        self.sort_instanceArray = sorted(instanceArray, key=lambda i: len(i))
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


    def getSimpleEnt(self,word):

        for ent in self.sort_instanceArray:
            if len(ent) >= len(word):
                return word
            if ent in word:
                return ent


    def getKeyEntity(self,words):

        entity = []
        for word in words:

            if word in self.instanceArray[::-1]:

                entity.append(word)

        return entity

    def getEntity(self,words):

        entity = []
        for word in words:

            if word in self.sort_instanceArray:

                entity.append(word)

        return entity

    def getSimpleEntity(self, words):

        entity = []
        for word in words:
            if word in self.sort_instanceArray:
                simple = self.getSimpleEnt(word)
                entity.append(simple)

        return entity

    def getEntityTwoBack(self,words,reverse_dep):
        keys = reverse_dep.keys()
        for word_index in range(len(words)):

            if words[word_index] in self.sort_instanceArray:
                #print(reverse_dep)
                #print(word_index+1)
                if word_index+1 not in keys:
                    continue
                check_list = reverse_dep[word_index+1]
                for c in check_list:
                    #print(c[1],c[0],words[c[0]-1])
                    if c[1] == 'COO' and words[c[0]-1] in self.sort_instanceArray:
                        return [words[word_index],words[c[0]-1]]
        return None

    def getEntityTwo(self,words):

        ent_list = []

        for word_index in range(len(words)):

            if words[word_index] in self.sort_instanceArray:
                ent_list.append(words[word_index] )

        if len(ent_list) == 2:
            return ent_list

        return None


    def getPositionEntity(self,words,pos,ent):
        entity = []
        for word_index in range(len(words)):
            if words[word_index] == ent:
                continue

            if words[word_index] in self.sort_instanceArray and pos[word_index] == 'ns':
                entity.append(words[word_index])
        return entity

    def getEtype(self,words):
        etype = []

        for word in words:

                if word in self.typeArray:
                    etype.append(word)

        return etype
    def getEtypeForSun(self,words):


        for word in words:
            for etype in self.typeArray[::-1]:
                if word in etype:
                    word_index = words.index(word)
                    return etype,word_index
        return None,None


    def getCount(self,index,dep):

        if dep[index][2] == 'SBV':
            return 5
        elif dep[index][2] == 'ATT':
            while(dep[index][2] == 'ATT'):
                index = dep[index][1]-1
            att_obeject = index

            if dep[att_obeject][2] == 'SBV':
                return 4
            if dep[att_obeject][2] in ['VOB','POB','FOB']:
                return 2
        elif dep[index][2] in ['VOB','POB']:
            return 3
        elif dep[index][2] == 'FOB':
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
                if words[i + 1] in self.typeArray:
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
            """
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

        return None,"normal"

    def checkCombineEnt(self, ent, coo):

        for e in self.instanceArray:
            if ent in e and coo in e and ('和' in e or '与' in e or ent+coo in e) and len(e) <= len(ent)+len(coo)+2:
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

        print(entity)
        print(etype)

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

            c = self.getCount(e_index,dep)
            if e in self.proArray:
                c = c-4
            ent_count.append(c)

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

        if ent_index != -1 and type_index != -1 and ent_c == 2 and type_c==2:
            if words.index(etype[type_index]) > words.index(entity[ent_index]):
                return etype[type_index],[],"etype"
            return entity[ent_index],[],'entity'

        elif ent_index != -1 and ent_c >= type_c:

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

    def getValuableWords(self, words, pos, dep):


        valuable_words = []
        word_count = []

        begin_index = -1
        end_index = -1
        key_word = ""

        if "“" in words and "”" in words:

            begin_index = words.index("“")
            end_index = words.index("”")
            if pos[end_index-1] == 'WP':
                end_index = end_index-1
            key_word = "".join(words[begin_index+1:end_index])

        if "《" in words and "》" in words:
            begin_index = words.index("《")
            end_index = words.index("》")
            if pos[end_index-1] == 'wp':
                end_index = end_index-1
            key_word = "".join(words[begin_index + 1:end_index])

        if "\"" in words:
            begin_index = words.index("\"")
            if "\"" in words[begin_index+1:]:

                end_index = words[begin_index + 1:].index("\"")+begin_index+1
            if pos[end_index-1] == 'WP':
                end_index = end_index-1
            key_word = "".join(words[begin_index + 1:end_index])

        print("getValuableWords", words,begin_index,end_index)

        for i in range(len(words)):
            print(i,"=======================")

            if pos[i] in self.valuable_pos:

                if words[i] in ['是', '有', '在', '于']:
                    continue
                if i > begin_index and i < end_index:

                    if "," in key_word:
                        a = key_word.split(",")
                        for kw in a:
                            if words[i] in kw:
                                valuable_words.append(kw)
                                word_count.append(20)
                                break
                    elif "，" in key_word:
                        a = key_word.split("，")
                        for kw in a:
                            if words[i] in kw:
                                valuable_words.append(kw)
                                word_count.append(20)
                                break
                    else:
                        valuable_words.append(key_word)
                        word_count.append(20)
                    continue

                valuable_words.append(words[i])
                if pos[i] in ["m","nt"]:
                    word_count.append(5)
                elif dep[i][2] == 'HED' and words[i] not in ['是','有','在','于']:
                    word_count.append(4)
                elif dep[i][2] == 'SBV':
                    word_count.append(4)
                elif dep[i][2] in ['VOB','POB','FOB']:
                    word_count.append(3)
                elif dep[i][2] == 'ATT' and dep[i][1] <= len(words) and dep[dep[i][1]-1][2]=='SBV':
                    word_count.append(2)
                elif dep[i][2] == 'ATT' and dep[i][1] <= len(words) and dep[dep[i][1]-1][2]=='VOB':
                    word_count.append(2)
                elif dep[i][2] == 'ADV' and dep[i][1] <= len(words) and dep[dep[i][1]-1][2]=='SBV':
                    word_count.append(2)
                elif dep[i][2] == 'ADV' and dep[i][1] <= len(words) and dep[dep[i][1]-1][2]=='HED':
                    word_count.append(2)
                else:
                    word_count.append(1)

                if '最' in words[i]:
                    word_count[-1] = word_count[-1]+3
                if words[i] in self.instanceArray or words[i] in self.typeArray:
                    word_count[-1] = word_count[-1] + 1

        print("getValuableWords2", valuable_words, word_count)



        return valuable_words,word_count

