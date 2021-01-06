# @Language: python3
# @File  : generateAns.py
# @Author: LinXiaofei
# @Date  : 2020-05-04
"""
答案生成
"""


from backend.numUtil import getCompareDirNum
from backend.numUtil import getSingelCompareNum
from backend.numUtil import getCompareNum

class generateAns(object):
    def __init__(self):
        pass


    def compareMoreNLG(self,task_type,compare_dict):
        if 'height' in task_type:
            keys = list(compare_dict.keys())
            num_one,num_two = getCompareNum(compare_dict,'海拔')
            if num_one == 'N/A':
                return "很抱歉,没有"+keys[0]+"的数据。\n"
            if num_two == 'N/A':
                return "很抱歉,没有"+keys[1]+"的数据。\n"
            if num_one>num_two:
                return keys[0]+"比"+keys[1]+"高。\n"
            else:
                return keys[1] + "比"+keys[0] + "高。\n"


        elif 'area' in task_type:
            keys = list(compare_dict.keys())
            num_one, num_two = getCompareNum(compare_dict,'面积')
            if num_one == 'N/A':
                return "很抱歉,没有"+keys[0]+"的数据。\n"
            if num_two == 'N/A':
                return "很抱歉,没有"+keys[1]+"的数据。\n"
            if num_one > num_two:
                return keys[0] + "的面积比" + keys[1] + "大。\n"
            else:
                return keys[1] + "的面积比" + keys[0] + "大。\n"

        elif 'volume' in task_type:
            keys = list(compare_dict.keys())
            num_one, num_two = getCompareNum(compare_dict, '蓄水量')
            if num_one == 'N/A':
                return "很抱歉,没有"+keys[0]+"的数据。\n"
            if num_two == 'N/A':
                return "很抱歉,没有"+keys[1]+"的数据。\n"
            if num_one > num_two:
                return keys[0] + "的蓄水量比" + keys[1] + "大。\n"
            else:
                return keys[1] + "的蓄水量比" + keys[0] + "大。\n"


        elif 'long' in task_type:
            keys = list(compare_dict.keys())
            num_one, num_two = getCompareNum(compare_dict, '长度')
            if num_one == 'N/A':
                return "很抱歉,没有"+keys[0]+"的数据。\n"
            if num_two == 'N/A':
                return "很抱歉,没有"+keys[1]+"的数据。\n"
            if num_one > num_two:
                return keys[0] + "比" + keys[1] + "长。\n"
            else:
                return keys[1] + "比" + keys[0] + "长。\n"


        elif 'deep' in task_type:
            keys = list(compare_dict.keys())
            num_one, num_two = getCompareNum(compare_dict, '深度')
            if num_one == 'N/A':
                return "很抱歉,没有"+keys[0]+"的数据。\n"
            if num_two == 'N/A':
                return "很抱歉,没有"+keys[1]+"的数据。\n"
            if num_one > num_two:
                return keys[0] + "比" + keys[1] + "深。\n"
            else:
                return keys[1] + "比" + keys[0] + "深。\n"
        elif 'flow' in task_type:
            keys = list(compare_dict.keys())
            num_one, num_two = getCompareNum(compare_dict, '流量')
            if num_one == 'N/A':
                return "很抱歉,没有"+keys[0]+"的数据。\n"
            if num_two == 'N/A':
                return "很抱歉,没有"+keys[1]+"的数据。\n"
            if num_one > num_two:
                return keys[0] + "比" + keys[1] + "流量大。\n"
            else:
                return keys[1] + "比" + keys[0] + "流量大。\n"
        elif 'south' in task_type:
            keys = list(compare_dict.keys())
            num_one, num_two = getCompareDirNum(task_type,compare_dict, '纬度')
            if num_one == 'N/A':
                return "很抱歉,没有"+keys[0]+"的数据。\n"
            if num_two == 'N/A':
                return "很抱歉,没有"+keys[1]+"的数据。\n"
            if num_one > num_two:
                return keys[0] + "比" + keys[1] + "南。\n"
            else:
                return keys[1] + "比" + keys[0] + "南。\n"
        elif 'north' in task_type:
            keys = list(compare_dict.keys())
            num_one, num_two = getCompareDirNum(task_type, compare_dict, '纬度')
            if num_one == 'N/A':
                return "很抱歉,没有" + keys[0] + "的数据。\n"
            if num_two == 'N/A':
                return "很抱歉,没有" + keys[1] + "的数据。\n"
            if num_one > num_two:
                return keys[0] + "比" + keys[1] + "北。\n"
            else:
                return keys[1] + "比" + keys[0] + "北。\n"
        elif 'east' in task_type:
            keys = list(compare_dict.keys())
            num_one, num_two = getCompareDirNum(task_type, compare_dict, '经度')
            if num_one == 'N/A':
                return "很抱歉,没有" + keys[0] + "的数据。\n"
            if num_two == 'N/A':
                return "很抱歉,没有" + keys[1] + "的数据。\n"
            if num_one > num_two:
                return keys[0] + "比" + keys[1] + "东。\n"
            else:
                return keys[1] + "比" + keys[0] + "东。\n"
        elif 'west' in task_type:
            keys = list(compare_dict.keys())
            num_one, num_two = getCompareDirNum(task_type, compare_dict, '经度')
            if num_one == 'N/A':
                return "很抱歉,没有" + keys[0] + "的数据。\n"
            if num_two == 'N/A':
                return "很抱歉,没有" + keys[1] + "的数据。\n"
            if num_one > num_two:
                return keys[0] + "比" + keys[1] + "西。\n"
            else:
                return keys[1] + "比" + keys[0] + "西。\n"

    def compareLessNLG(self,task_type,compare_dict):
        if 'height' in task_type:
            keys = list(compare_dict.keys())
            num_one,num_two = getCompareNum(compare_dict,'海拔')
            if num_one == 'N/A':
                return "很抱歉,没有"+keys[0]+"的数据。\n"
            if num_two == 'N/A':
                return "很抱歉,没有"+keys[1]+"的数据。\n"
            if num_one<num_two:
                return keys[0]+"比"+keys[1]+"低。\n"
            else:
                return keys[1] + "比"+keys[0] + "低。\n"


        elif 'area' in task_type:
            keys = list(compare_dict.keys())
            num_one, num_two = getCompareNum(compare_dict,'面积')
            if num_one == 'N/A':
                return "很抱歉,没有"+keys[0]+"的数据。\n"
            if num_two == 'N/A':
                return "很抱歉,没有"+keys[1]+"的数据。\n"
            if num_one < num_two:
                return keys[0] + "的面积比" + keys[1] + "小。\n"
            else:
                return keys[1] + "的面积比" + keys[0] + "小。\n"


        elif 'drainage' in task_type:
            keys = list(compare_dict.keys())
            num_one, num_two = getCompareNum(compare_dict, '流域面积')
            if num_one == 'N/A':
                return "很抱歉,没有"+keys[0]+"的数据。\n"
            if num_two == 'N/A':
                return "很抱歉,没有"+keys[1]+"的数据。\n"

            if num_one < num_two:
                return keys[0] + "的流域面积比" + keys[1] + "小。\n"
            else:
                return keys[1] + "的流域面积比" + keys[0] + "小。\n"


        elif 'volume' in task_type:
            keys = list(compare_dict.keys())
            num_one, num_two = getCompareNum(compare_dict, '蓄水量')
            if num_one == 'N/A':
                return "很抱歉,没有"+keys[0]+"的数据。\n"
            if num_two == 'N/A':
                return "很抱歉,没有"+keys[1]+"的数据。\n"
            if num_one < num_two:
                return keys[0] + "的蓄水量比" + keys[1] + "小。\n"
            else:
                return keys[1] + "的蓄水量比" + keys[0] + "小。\n"


        elif 'long' in task_type:
            keys = list(compare_dict.keys())
            num_one, num_two = getCompareNum(compare_dict, '长度')
            if num_one == 'N/A':
                return "很抱歉,没有"+keys[0]+"的数据。\n"
            if num_two == 'N/A':
                return "很抱歉,没有"+keys[1]+"的数据。\n"
            if num_one < num_two:
                return keys[0] + "比" + keys[1] + "短。\n"
            else:
                return keys[1] + "比" + keys[0] + "短。\n"


        elif 'deep' in task_type:
            keys = list(compare_dict.keys())
            num_one, num_two = getCompareNum(compare_dict, '深度')
            if num_one == 'N/A':
                return "很抱歉,没有"+keys[0]+"的数据。\n"
            if num_two == 'N/A':
                return "很抱歉,没有"+keys[1]+"的数据。\n"
            if num_one < num_two:
                return keys[0] + "比" + keys[1] + "浅。\n"
            else:
                return keys[1] + "比" + keys[0] + "浅。\n"
        elif 'flow' in task_type:
            keys = list(compare_dict.keys())
            num_one, num_two = getCompareNum(compare_dict, '流量')
            if num_one == 'N/A':
                return "很抱歉,没有"+keys[0]+"的数据。\n"
            if num_two == 'N/A':
                return "很抱歉,没有"+keys[1]+"的数据。\n"
            if num_one < num_two:
                return keys[0] + "比" + keys[1] + "流量小。\n"
            else:
                return keys[1] + "比" + keys[0] + "流量小。\n"

    def ansMost(self,ans,wether):
        if self.ansWether(wether,ans):
            return self.ansWether(wether,ans)
        else:
            return ans

    def ansWether(self,wether,ans):
        if len(wether) > 0 and wether[0] in ans:
            return "是的\n"
        elif len(wether) > 0 and wether[0] not in ans:
            return "不是\n"
        else:
            return None

    def getAns(self,entity,task_type,ans_array,wether):
        print(entity,task_type,ans_array,wether)

        if ans_array == None:

            if entity == None:
                ans = "对不起，暂时无法回答该方面的问题。\n"
                return ans
            ans = "对不起，暂时无法回答"+entity+"该方面的问题。\n"
            return ans


        if task_type == 'ans_list':

            ans = ",".join(ans_array)
            wether_ans = self.ansWether(wether,ans)
            if wether_ans:
                return wether_ans

            return ans
        if task_type == 'ans_triple':
            ans = ""
            ans = ans + ans_array[0]+"的"+ans_array[1]+": "+ans_array[2]+"\n"
            wether_ans = self.ansWether(wether, ans)
            if wether_ans:
                return wether_ans

            return ans
        if task_type == 'ans_items':
            ans = ""
            for name, value in ans_array.items():
                for pro, provalue in value.items():
                    provalue = sorted(provalue, key=lambda i: len(i), reverse=True)
                    ans = ans+name+"的"+pro+": "+provalue[0]+"\n"
            wether_ans = self.ansWether(wether, ans)
            if wether_ans:
                return wether_ans

            return ans





