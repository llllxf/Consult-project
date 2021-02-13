import configparser
from backend.data.data_process import read_file
config = configparser.ConfigParser()
"""
config["DEFAULT"] = {'Subject': '地理'
                     }

config['TRANSFORM'] = {'地理': 'geo4','历史':'history'}
"""

config["人口数量"] = {
    'type':'numpro',
    'alias':'人口,人口数',
    'noun':'人',
}
pro_arr = read_file("data/历史/pro.csv")
print(pro_arr)
for p in pro_arr:
    config[p] = {
        'type': 'desconpro',
    }
with open('pro_history.ini', 'w') as file:
    config.write(file)