# @Language: python3
# @File  : numUtil.py
# @Author: LinXiaofei
# @Date  : 2020-06-20
"""

"""
import jieba
import re
import string


CN_NUM = {
    '〇' : 0, '一' : 1, '二' : 2, '三' : 3, '四' : 4, '五' : 5, '六' : 6, '七' : 7, '八' : 8, '九' : 9, '零' : 0,
    '壹' : 1, '贰' : 2, '叁' : 3, '肆' : 4, '伍' : 5, '陆' : 6, '柒' : 7, '捌' : 8, '玖' : 9, '貮' : 2, '两' : 2,
}

CN_UNIT = {
    '十' : 10,
    '拾' : 10,
    '百' : 100,
    '佰' : 100,
    '千' : 1000,
    '仟' : 1000,
    '万' : 10000,
    '萬' : 10000,
    '亿' : 100000000,
    '億' : 100000000,
    '兆' : 1000000000000,
}

def chinese_to_arabic(cn:str) -> int:
    unit = 0   # current
    ldig = []  # digest
    #reversed_cn = reversed(cn)
    reversed_cn = cn[::-1]


    for cndig_index in range(len(reversed_cn)):
        cndig = reversed_cn[cndig_index]
        print("cndig",cndig)
        if cndig in CN_UNIT:
            unit = CN_UNIT.get(cndig)
            if unit == 10000 or unit == 100000000:
                ldig.append(unit)
                unit = 1
        else:
            if cndig in CN_NUM.keys():
                dig = CN_NUM.get(cndig)
                if unit:
                    dig *= unit
                    unit = 0
                ldig.append(dig)
            """
            if cndig in common_number:

                cn_index = cndig_index
                dig = int(cndig)
                if unit:
                    if dig == 0:
                        dig = 1
                    dig *= unit
                    if cn_index < len(reversed_cn)-1 and reversed_cn[cn_index+1] in common_number:
                        unit = 10
                    else:
                        unit = 0

                ldig.append(dig)
            """



    if unit == 10:
        ldig.append(10)
    print(ldig,"ldig")
    val, tmp = 0, 0
    if len(ldig)==1:
        return ldig[0]

    for x in reversed(ldig):
        if x == 10000 or x == 100000000:
            val += tmp * x
            tmp = 0
        else:
            tmp += x
    val += tmp
    return val

common_used_numerals ={'零':0, '一':1, '二':2, '两':2, '三':3, '四':4, '五':5, '六':6, '七':7, '八':8, '九':9, '十':10, '百':100, '千':1000, '万':10000, '亿':100000000}
common_number = ['0','1','2','3','4','5','6','7','8','9']

#common_used_numerals = {}
#for key in common_used_numerals_tmp:
#    common_used_numerals[key] = common_used_numerals_tmp[key]
def chinese2digits(uchars_chinese):
  total = 0
  r = 1

  for i in range(len(uchars_chinese) - 1, -1, -1):
    print(uchars_chinese[i],total)

    if uchars_chinese[i] in common_used_numerals.keys():
        val = common_used_numerals.get(uchars_chinese[i])

        if val >= 10 and i == 0:
            if val > r:
                r = val
                total = total + val
            else:
                r = r * val
        elif val >= 10:
            if val > r:
                r = val
            else:
                r = r * val
        else:
            total = total + r * val
        print(total, "val,total")
    elif uchars_chinese[i] in common_number:
        total = total + r * int(uchars_chinese[i])
        if i != 0 and uchars_chinese[i-1] in common_number:
            r = r*10

  return total

def getNumFromValue(words):
    return_num = ""
    for w_index in range(len(words)):
        if str.isnumeric(words[w_index]):
            return_num += words[w_index]
        elif words[w_index]== ".":
            return_num += "."
        elif len(return_num)>0:
            return return_num

def getDateNum(value):

    array_num = list(jieba.cut(value))
    print("getDateNum,array_num",array_num)


    year = None
    month = None
    date = None
    if len(array_num) == 1 and str.isnumeric(array_num[0]):
        return int(array_num[0])*10000

    for index in range(len(array_num)):
        sub = array_num[index]

        formed_sub = sub


        if str.isnumeric(formed_sub):

            if index < len(array_num) - 1 and '年' in array_num[index + 1]:
                year = int(formed_sub)
            if index < len(array_num) - 1 and '月' in array_num[index + 1]:
                month = int(formed_sub)
            if index < len(array_num) - 1 and '日' in array_num[index + 1]:
                date = int(formed_sub)
    sum_date = 0
    if year:
        sum_date += year*10000
    if month:
        sum_date += month*100
    if date:
        sum_date += date
    if sum_date > 0:
        print("sum_date",sum_date)
        return sum_date

    return None






def getSingelCompareNum(value):
    """
    得到单个数据，用于计算模块
    :param value:
    :return:
    """
    while(' ' in value):
        value = value.replace(' ','')
    while(',' in value):
        value = value.replace(',','')
    array_num = list(jieba.cut(value))

    if array_num == ['N', '/', 'A']:
        return 0

    num = None
    for index in range(len(array_num)):
        sub = array_num[index]


        formed_sub = sub

        if str.isnumeric(formed_sub) or "." in formed_sub:

            if index < len(array_num)-1 and '年' in array_num[index + 1]:
                continue
            if index < len(array_num)-1 and '月' in array_num[index + 1]:
                continue
            if index < len(array_num)-1 and '日' in array_num[index + 1]:
                continue

            num = float(formed_sub)
            #print(array_num[index + 1],array_num,"array_num[index + 1]")
            if index+1>=len(array_num):
                return num
            if index < len(array_num)-1 and '万亿' in array_num[index + 1]:

                num *= 10000000000000
                return num
            elif index < len(array_num)-1 and '亿' in array_num[index + 1]:
                num *= 1000000000
                return num

            elif index < len(array_num)-1 and '万' in array_num[index + 1]:
                num *= 10000
                return num
        elif num:
            return num

    return num

def getCompareDirNum(task_type, compare_dict, property):
    """
    得到纬度的数据,用于比较模块,返回比较的两个值
    :param task_type:
    :param compare_dict:
    :param property:
    :return:
    """
    keys = list(compare_dict.keys())
    array_one = list(jieba.cut(compare_dict[keys[0]][property][0]))
    array_two = list(jieba.cut(compare_dict[keys[1]][property][0]))

    if array_one == ['N', '/', 'A']:
        return 'N/A', None
    if array_two == ['N', '/', 'A']:
        return None, 'N/A'
    index = 0
    for sub in array_one:

        if '.' in sub:
            formed_sub = sub.replace(".", "")
        else:
            formed_sub = sub

        if str.isnumeric(formed_sub):

            num_one = float(sub)
            # print(array_one[index-1])
            if ('south' in task_type and '北' in array_one[index - 1]) or (
                    'north' in task_type and '南' in array_one[index - 1]) \
                    or ('east' in task_type and '西' in array_one[index - 1]) or (
                    'west' in task_type and '东' in array_one[index - 1]):
                num_one = -num_one
                # print(num_one)

            break
        index = index + 1

    index = 0
    for sub in array_two:
        if '.' in sub:
            formed_sub = sub.replace(".", "")
        else:
            formed_sub = sub
        if str.isnumeric(formed_sub):
            num_two = float(sub)
            # print(array_two[index-1])
            if ('south' in task_type and '北' in array_two[index - 1]) or (
                    'north' in task_type and '南' in array_two[index - 1]) \
                    or ('east' in task_type and '西' in array_two[index - 1]) or (
                    'west' in task_type and '东' in array_two[index - 1]):
                num_two = -num_two
                # print(num_two)
            break
        index = index + 1
    return num_one, num_two


def getCompareNum(compare_dict,property):
    """
    得到数据, 用于比较模块, 返回比较的两个值
    :param compare_dict:
    :param property:
    :return:
    """
    #print(compare_dict,property)

    keys = list(compare_dict.keys())
    array_one = list(jieba.cut(compare_dict[keys[0]][property][0]))
    array_two = list(jieba.cut(compare_dict[keys[1]][property][0]))

    if array_one == ['N', '/', 'A']:
        return 'N/A', None
    if array_two == ['N', '/', 'A']:
        return None, 'N/A'
    index = 0
    num_one = 'N/A'
    num_two = 'N/A'
    for sub in array_one:

        if '.' in sub:
            formed_sub = sub.replace(".", "")
        else:
            formed_sub = sub

        if str.isnumeric(formed_sub):

            num_one = float(sub)
            if index == len(array_one)-1:
                break
            if '万亿' in array_one[index + 1]:
                num_one *= 10000000000000
            elif '亿' in array_one[index + 1]:
                num_one *= 1000000000
            elif '万' in array_one[index + 1]:
                num_one *= 10000
            break
        index = index + 1
    index = 0
    for sub in array_two:
        if '.' in sub:
            formed_sub = sub.replace(".", "")
        else:
            formed_sub = sub
        if str.isnumeric(formed_sub):
            num_two = float(sub)
            if index == len(array_two)-1:
                break

            if '万亿' in array_two[index + 1]:
                num_two *= 10000000000000
            elif '亿' in array_two[index + 1]:
                num_two *= 1000000000
            elif '万' in array_two[index + 1]:
                num_two *= 10000
            break
        index = index + 1
    return num_one, num_two



def getSingelDirNum(value,task_type):
    """
    得到纬度的数据,用于比较模块,返回比较的两个值
    :param task_type:
    :param compare_dict:
    :param property:
    :return:
    """
    while (' ' in value):
        value = value.replace(' ', '')
    while (',' in value):
        value = value.replace(',', '')
    array_num = list(jieba.cut(value))

    if array_num == ['N', '/', 'A']:
        return 0

    index = 0
    for sub in array_num:

        if '.' in sub:
            formed_sub = sub.replace(".", "")
        else:
            formed_sub = sub

        if str.isnumeric(formed_sub):

            num = float(sub)
            # print(array_one[index-1])
            if ('south' in task_type and '北' in array_num[index - 1]) or (
                    'north' in task_type and '南' in array_num[index - 1]) \
                    or ('east' in task_type and '西' in array_num[index - 1]) or (
                    'west' in task_type and '东' in array_num[index - 1]):
                num = -num
            return num
        index = index + 1




