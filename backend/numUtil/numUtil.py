# @Language: python3
# @File  : numUtil.py
# @Author: LinXiaofei
# @Date  : 2020-06-20
"""

"""
import jieba

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

    index = 0
    for sub in array_num:

        if '.' in sub:
            formed_sub = sub.replace(".", "")

        else:
            formed_sub = sub

        if str.isnumeric(formed_sub):

            num = float(sub)
            if '万亿' in array_num[index + 1]:
                num *= 10000000000000
            elif '亿' in array_num[index + 1]:
                num *= 1000000000
            elif '万' in array_num[index + 1]:
                num *= 10000
            return num
        index = index + 1
    print(array_num,"array")

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




