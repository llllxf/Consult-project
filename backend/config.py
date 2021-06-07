import configparser
from backend.data.data_process import read_file
config = configparser.ConfigParser()
rel_arr = read_file("data/地理/cleanrel.csv")

for r in rel_arr:
    config[r] = {
        'type': 'normal',
        'alias': ''
    }




with open('data/地理/relconfig.ini', 'w') as file:
    config.write(file)

"""
config["DEFAULT"] = {'Subject': '地理'
                     }

config['TRANSFORM'] = {'地理': 'geo4','历史':'history'}



pro_arr = read_file("data/历史/sep_ent_clean2.csv")


for p in pro_arr:



    seg,hidden = myltp.seg([p])
    #print(seg,hidden)
    p_cut = seg[0]
    p_pos = myltp.pos(hidden)[0]
    de_index = p_cut.index('的')
    #print(p_cut,p_pos)
    match_words = []
    for sub_index in range(0,de_index):
        print(len(p_pos),sub_index)
        if p_pos[sub_index] in ['n', 'v', 'ni', 'nl', 'ns', 'nt', 'nz']:
            match_words.append(p_cut[sub_index])

    print(",".join(match_words))
    print(p_cut[-1])

    if '不同' in p_cut:

        config[p] = {
            'type': 'compare',
            'keyword': '不同点,比较,不同',
            'matchword': ",".join(match_words)
        }
    elif '相同' in p_cut:

        config[p] = {
            'type': 'compare',
            'keyword': '相同点,比较,相同',
            'matchword': ",".join(match_words)
        }
    elif '关系' in p_cut:

        config[p] = {
            'type': 'compare',
            'keyword': '关系,比较',
            'matchword': ",".join(match_words)
        }
    elif '比较' in p_cut:

        config[p] = {
            'type': 'compare',
            'keyword': '不同点,比较,不同,异同,相同,相同点',
            'matchword': ",".join(match_words)
        }

    elif '特点' in p_cut:
        config[p] = {
            'type': 'feature',
            'keyword': '特点',
            'matchword': ",".join(match_words)
        }

    elif  '影响' in p_cut:
        config[p] = {
            'type': 'influence',
            'keyword': '影响',
            'matchword': ",".join(match_words)
        }

    elif  '性' in p_cut[-1]:
        config[p] = {
            'type': 'nature',
            'keyword': p_cut[-1],
            'matchword': ",".join(match_words)
        }

    elif  '条件' in p_cut[-1]:
        config[p] = {
            'type': 'reason',
            'keyword': '条件',
            'matchword': ",".join(match_words)
        }
    elif '时间' in p_cut[-1]:
        config[p] = {
            'type': 'time',
            'keyword': '时间',
            'matchword': ",".join(match_words)
        }
    elif '意义' in p_cut:
        config[p] = {
            'type': 'meaning',
            'keyword': '意义',
            'matchword': ",".join(match_words)
        }
    elif '因' in p_cut:
        config[p] = {
            'type': 'reason',
            'keyword': '原因,缘由,理由',
            'matchword': ",".join(match_words)
        }
    elif '方针' in p_cut or '政策' in p_cut:
        config[p] = {
            'type': 'plan',
            'keyword': '方针,政策',
            'matchword': ",".join(match_words)
        }
    elif '评价' in p_cut or '认识' in p_cut:
        config[p] = {
            'type': 'evaluate',
            'keyword': '认识,评价',
            'matchword': ",".join(match_words)
        }

"""


