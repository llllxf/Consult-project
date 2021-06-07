from backend.semantic_similarity.hownet.howNet import How_Similarity
from backend.semantic_similarity.cilin.ciLin import CilinSimilarity
import jieba
from backend.nlu.LTPUtil import LTPUtil
import numpy as np

class Similarity():
    ci_lin = CilinSimilarity()
    how_net = How_Similarity()



    @classmethod
    def calSimilarity(cls,phrase,phrase_value,words,stop,phrase_pos,ltp_util):
        print(words)
        print("========================================")
        words_count = 0
        words_list = jieba.cut(words)
        check_list,_ = cls.ci_lin.checkWord(words_list)
        check_phrase,return_index = cls.ci_lin.checkWord(phrase)
        phrase_pos = np.array(phrase_pos)[return_index]
        check_pos = list(ltp_util.get_postag(list(check_list)))
        print("calSimilarity",check_phrase,phrase_pos)
        print("calSimilarity",check_list,check_pos)
        print("calSimilarity",len(phrase_value))

        for p_index in range(len(check_phrase)):
            p_max_count = 0
            f = ""
            best_max = -1
            if check_phrase[p_index] in stop:
                continue

            for w_index in range(len(check_list)):
                print(check_pos[w_index],check_list[w_index],check_phrase[p_index],phrase_pos[p_index])
                w = check_list[w_index]
                if w in stop:
                    continue
                if check_pos[w_index] != phrase_pos[p_index]:
                    continue



                cl_count = cls.ci_lin.sim2018(check_phrase[p_index],w)

                if p_max_count < cl_count:
                    p_max_count = cl_count
                    best_max = p_index
                    f = w

            if p_max_count == 1:
                print(check_phrase[best_max], f, p_max_count)
                words_count += 5
            elif p_max_count >= 0.8:
                print(check_phrase[best_max],f,p_max_count)
                words_count += 4
            elif p_max_count >= 0.7:
                print(check_phrase[best_max], f,p_max_count)
                words_count += 3


        return words_count