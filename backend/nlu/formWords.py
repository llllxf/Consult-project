# @Language: python3
# @File  : formWords.py
# @Author: LinXiaofei
# @Date  : 2020-04-24
"""

"""



class formWords(object):
    """
    调整句子

    """

    def __init__(self):
        pass



















    def preProcessWords(self, words):
        """
        句子预处理
        1.去掉符号和停用词
        2.去掉"的"，如果有目的，则复原
        :param words: 句子
        :return: 处理后的句子
        """
        """
        for stop in self.stopword:
            while(stop in words):
                words = words.replace(stop,'')
        for sym in self.symbol:
            while(sym in words):
                words = words.replace(sym,'')

        flag = False
        if "目的" in words:
            flag = True
        words = self.deletDE(words)

        if flag:
            words = words.replace("目","目的")

        return words
        """
        pass





if __name__ == '__main__':
    pass

