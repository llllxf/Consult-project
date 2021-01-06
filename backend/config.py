import configparser

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

with open('pro_config.ini', 'w') as file:
    config.write(file)