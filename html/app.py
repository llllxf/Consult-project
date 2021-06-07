#!/usr/bin/env Python
# coding=utf-8
from backend.dm.DialogManagement import DialogManagement
from backend.dm.HistoryDM import HistoryDM
from backend.dm.GeoDM import GeoDM
from backend.dm.HistoryDMNormal import HistoryDMNormal
from backend.dm.GeoDMNormal import GeoDMNormal
from flask import Flask, render_template, request, make_response
from flask import jsonify
import json
import time
import threading
from urllib.request import quote, unquote

import configparser

config = configparser.ConfigParser()
content = config.read("../backend/config.ini")

geo = GeoDM()
his = HistoryDM()
geon = GeoDMNormal()
hisn = HistoryDMNormal()

"""
def heartbeat():
    print (time.strftime('%Y-%m-%d %H:%M:%S - heartbeat', time.localtime(time.time())))
    timer = threading.Timer(60, heartbeat)
    timer.start()
timer = threading.Timer(60, heartbeat)
timer.start()

try:  
    import xml.etree.cElementTree as ET  
except ImportError:  
    import xml.etree.ElementTree as ET
"""

#app = Flask(__name__, template_folder=project_path,static_url_path=project_path+"/static/", static_folder=project_path+"/static/")
app = Flask(__name__,static_url_path="/static")

@app.route('/')
def index():
    return render_template("qaindex.html")

@app.route('/goChoose', methods=['POST','GET'])
def goChoose():
    return render_template("chooseSubject.html")

@app.route('/goNormal', methods=['POST','GET'])
def goNormal():

    subject = dict(request.cookies)['subject']

    if subject == '地理':

        response = make_response(render_template("input.html", subject="地理"))
        response.set_cookie("mode", "normal")
    elif subject == '历史':

        response = make_response(render_template("input.html", subject="历史"))
        response.set_cookie("mode", "normal")

    elif subject == '语文':

        response = make_response(render_template("input.html", subject="语文"))
        response.set_cookie("mode", "normal")

    elif subject == '数学':

        response = make_response(render_template("input.html", subject="数学"))
        response.set_cookie("mode", "normal")

    elif subject == '英语':

        response = make_response(render_template("input.html", subject="英语"))
        response.set_cookie("mode", "normal")

    elif subject == '物理':

        response = make_response(render_template("input.html", subject="物理"))
        response.set_cookie("mode", "normal")

    elif subject == '化学':

        response = make_response(render_template("input.html", subject="化学"))
        response.set_cookie("mode", "normal")

    elif subject == '政治':

        response = make_response(render_template("input.html", subject="政治"))
        response.set_cookie("mode", "normal")

    elif subject == '生物':

        response = make_response(render_template("input.html", subject="生物"))
        response.set_cookie("mode", "normal")

    return response


@app.route('/goTest', methods=['POST','GET'])
def goTest():

    subject = dict(request.cookies)['subject']

    if subject == '地理':

        response = make_response(render_template("input.html", subject="地理"))
        response.set_cookie("mode", "test")
    elif subject == '历史':

        response = make_response(render_template("input.html", subject="历史"))
        response.set_cookie("mode", "test")

    elif subject == '语文':

        response = make_response(render_template("input.html", subject="语文"))
        response.set_cookie("mode", "test")

    elif subject == '数学':

        response = make_response(render_template("input.html", subject="数学"))
        response.set_cookie("mode", "test")

    elif subject == '英语':

        response = make_response(render_template("input.html", subject="英语"))
        response.set_cookie("mode", "test")

    elif subject == '物理':

        response = make_response(render_template("input.html", subject="物理"))
        response.set_cookie("mode", "test")

    elif subject == '化学':

        response = make_response(render_template("input.html", subject="化学"))
        response.set_cookie("mode", "test")

    elif subject == '政治':

        response = make_response(render_template("input.html", subject="政治"))
        response.set_cookie("mode", "test")

    elif subject == '生物':

        response = make_response(render_template("input.html", subject="生物"))
        response.set_cookie("mode", "test")

    return response

@app.route('/goView', methods=['POST','GET'])
def goView():
    subject = dict(request.cookies)['subject']

    response = make_response(render_template("tables2.html",subject=subject))

    return response

@app.route('/goEntity', methods=['GET'])
def goEntity():
    subject = dict(request.cookies)['subject']
    entity = request.args['entity']
    return render_template("tables.html",entity=entity,subject=subject)

@app.route('/getType', methods=['POST','GET'])
def getType():
    subject = dict(request.cookies)['subject']
    if subject == '地理':

        type_list = geo.getGeoType()
    elif subject == '历史':
        type_list = his.getHisType()

    return jsonify({'data':type_list})

@app.route('/getEntity', methods=['POST','GET'])
def getEntity():
    subject = dict(request.cookies)['subject']
    entity = request.json.get('entity')
    if subject == '地理':

        ent_list = geo.getEntity(entity)
    elif subject == '历史':
        ent_list = his.getEntity(entity)

    return jsonify({'data':ent_list})

@app.route('/goChineseMode', methods=['POST','GET'])
def goChineseMode():

    response = make_response(render_template("chooseM.html",subject="语文"))
    response.set_cookie("subject","语文")
    return response

@app.route('/goMathMode', methods=['POST','GET'])
def goMathMode():

    response = make_response(render_template("chooseM.html", subject="数学"))
    response.set_cookie("subject", "数学")
    return response


@app.route('/goEnglishMode', methods=['POST','GET'])
def goEnglishMode():

    response = make_response(render_template("chooseM.html", subject="英语"))
    response.set_cookie("subject", "英语")
    return response


@app.route('/goPhysicsMode', methods=['POST','GET'])
def goPhysicsMode():

    response = make_response(render_template("chooseM.html", subject="物理"))
    response.set_cookie("subject", "物理")
    return response

@app.route('/goChemistryMode', methods=['POST','GET'])
def goChemistryMode():

    response = make_response(render_template("chooseM.html", subject="化学"))
    response.set_cookie("subject", "化学")
    return response


@app.route('/goBiologyMode', methods=['POST','GET'])
def goBiologyMode():

    response = make_response(render_template("chooseM.html", subject="生物"))
    response.set_cookie("subject", "生物")
    return response


@app.route('/goHistoryMode', methods=['POST','GET'])
def goHistoryMode():

    response = make_response(render_template("chooseM.html", subject="历史"))
    response.set_cookie("subject", "历史")
    config['DEFAULT']['subject'] = '历史'

    with open('../backend/config.ini', 'w') as file:
        config.write(file)
    file.close()

    return response


@app.route('/goPoliticsMode', methods=['POST','GET'])
def goPoliticsMode():

    response = make_response(render_template("chooseM.html", subject="政治"))
    response.set_cookie("subject", "政治")
    return response


@app.route('/goGeographyMode', methods=['POST','GET'])
def goGeographyMode():

    config['DEFAULT']['subject'] = '地理'

    with open('../backend/config.ini', 'w') as file:
        config.write(file)
    file.close()
    response = make_response(render_template("chooseM.html", subject="地理"))
    response.set_cookie("subject", "地理")

    return response



@app.route('/goChinese', methods=['POST','GET'])
def goChinese():

    response = make_response(render_template("input.html",subject="语文"))
    response.set_cookie("subject","语文")
    return response

@app.route('/goMath', methods=['POST','GET'])
def goMath():

    response = make_response(render_template("input.html", subject="数学"))
    response.set_cookie("subject", "数学")
    return response


@app.route('/goEnglish', methods=['POST','GET'])
def goEnglish():
    response = make_response(render_template("input.html", subject="英语"))
    response.set_cookie("subject", "英语")
    return response


@app.route('/goPhysics', methods=['POST','GET'])
def goPhysics():
    response = make_response(render_template("input.html", subject="物理"))
    response.set_cookie("subject", "物理")
    return response

@app.route('/goChemistry', methods=['POST','GET'])
def goChemistry():
    response = make_response(render_template("input.html", subject="化学"))
    response.set_cookie("subject", "化学")
    return response


@app.route('/goBiology', methods=['POST','GET'])
def goBiology():
    response = make_response(render_template("input.html", subject="生物"))
    response.set_cookie("subject", "生物")
    return response


@app.route('/goHistory', methods=['POST','GET'])
def goHistory():
    response = make_response(render_template("input.html", subject="历史"))
    response.set_cookie("subject", "历史")
    config['DEFAULT']['subject'] = '历史'

    with open('../backend/config.ini', 'w') as file:
        config.write(file)
    file.close()

    return response


@app.route('/goPolitics', methods=['POST','GET'])
def goPolitics():
    response = make_response(render_template("input.html", subject="政治"))
    response.set_cookie("subject", "政治")
    return response


@app.route('/goGeography', methods=['POST','GET'])
def goGeography():
    config['DEFAULT']['subject'] = '地理'

    with open('../backend/config.ini', 'w') as file:
        config.write(file)
    file.close()
    response = make_response(render_template("input.html", subject="地理"))
    response.set_cookie("subject", "地理")

    return response


@app.route('/qa', methods=['POST','GET'])
def message():
    question = request.json.get('question')

    subject = dict(request.cookies)['subject']

    if 'mode' in dict(request.cookies).keys():
        mode = dict(request.cookies)['mode']
    else:
        mode = 'normal'
    print("==============================",subject,mode)

    if subject == '地理':

        if mode == 'normal':
            ans = geon.doNLU(question)
        else:

            ans = geo.doNLU(question)

        if ans[0] == 2:
            return jsonify({'ans': ans[1], 'flag': ans[0], 'ask_back': ans[2], 'entity': ans[3]})
        elif ans[0] == 1:
            return jsonify({'ans': ans[1], 'flag': ans[0], 'entity': ans[2]})
        else:
            return jsonify({'ans': ans[1], 'flag': ans[0]})

    elif subject == '历史':

        if mode == 'normal':
            ans = hisn.doNLU(question)
        else:

            ans = his.doNLU(question)

        if ans[0] == 2:
            return jsonify({'ans': ans[1], 'flag': ans[0], 'ask_back': ans[2], 'entity': ans[3]})
        elif ans[0] == 1:
            return jsonify({'ans': ans[1], 'flag': ans[0], 'entity': ans[2]})
        else:
            return jsonify({'ans': ans[1], 'flag': ans[0]})

    else:
        return jsonify({'ans': '无法回答'+subject+"的问题",'flag':0})


@app.route('/goKnowledgePoint', methods=['GET'])
def goKnowledgePoint():
    entity = request.args['entity']
    subject = dict(request.cookies)['subject']

    if subject == '地理':
        return render_template("graph.html")

    elif subject == '历史':
        return render_template("graph.html")


@app.route('/goGraph', methods=['GET'])
def goGraph():
    entity = request.args['entity']
    subject = dict(request.cookies)['subject']

    if 'show_mode' in dict(request.cookies).keys():
        show_mode = dict(request.cookies)['show_mode']
        if show_mode == 'rel':
            return render_template("graph2.html")
        else:
            return render_template("graph.html")
    else:
        response = make_response(render_template("graph2.html"))
        response.set_cookie("show_mode", "rel")
        return response


@app.route('/setSubject', methods=['GET'])
def setSubject():
    subject = request.args['subject']
    if subject == 'Chinese':
        response = make_response(render_template("tables2.html",subject="语文"))
        response.set_cookie("subject", "语文")
        return response
    elif subject == 'Math':
        response = make_response(render_template("tables2.html",subject="数学"))
        response.set_cookie("subject", "数学")
        return response
    elif subject == 'English':
        response = make_response(render_template("tables2.html",subject="英语"))
        response.set_cookie("subject", "英语")
        return response
    elif subject == 'Physics':
        response = make_response(render_template("tables2.html",subject="物理"))
        response.set_cookie("subject", "物理")
        return response
    elif subject == 'Chemistry':
        response = make_response(render_template("tables2.html",subject="化学"))
        response.set_cookie("subject", "化学")
        return response
    elif subject == 'Biology':
        response = make_response(render_template("tables2.html",subject="生物"))
        response.set_cookie("subject", "生物")
        return response
    elif subject == 'Politics':
        response = make_response(render_template("tables2.html",subject="政治"))
        response.set_cookie("subject", "政治")
        return response
    elif subject == 'History':
        response = make_response(render_template("tables2.html",subject="历史"))
        response.set_cookie("subject", "历史")
        return response
    elif subject == 'Geography':
        response = make_response(render_template("tables2.html",subject="地理"))
        response.set_cookie("subject", "地理")
        return response

@app.route('/setMode', methods=['GET'])
def setMode():
    mode = request.args['mode']
    subject = dict(request.cookies)['subject']


    if mode == 'relation':
        response = make_response(render_template("tables2.html",subject=subject))
        response.set_cookie("show_mode", "rel")
        return response
    else:
        response = make_response(render_template("tables2.html",subject=subject))
        response.set_cookie("show_mode", "att")
        return response


@app.route('/showGraphAtt', methods=['POST','GET'])
def showGraphAtt():

    entity = request.json.get('entity')
    entity = unquote(entity)


    print("================================================",entity)
    subject = dict(request.cookies)['subject']
    if subject == '地理':

        ans = geo.AEntityInformation(entity)
        return jsonify(dict(ans))


    elif subject == '历史':
        ans = his.AEntityInformation(entity)

        return jsonify(dict(ans))


@app.route('/showGraph', methods=['POST','GET'])
def showGraph():

    entity = request.json.get('entity')
    entity = unquote(entity)

    if 'show_mode' in dict(request.cookies).keys():
        show_mode = dict(request.cookies)['show_mode']
    else:
        show_mode = 'rel'

    print("================================================",entity)
    subject = dict(request.cookies)['subject']
    if subject == '地理':
        if show_mode == 'rel':
            ans, ans_category,ans_relate = geo.AEntityRelation(entity)

            return jsonify(dict({'ans': ans, 'ans_category': ans_category,'ans_relate':ans_relate}))
        else:
           ans = geo.AEntityInformation(entity)
        return jsonify(dict(ans))


    elif subject == '历史':
        if show_mode == 'rel':
            ans,ans_category,ans_relate = his.AEntityRelation(entity)
            return jsonify(dict({'ans':ans,'ans_category':ans_category,'ans_relate':ans_relate}))
        else:
            ans = his.AEntityInformation(entity)

        return jsonify(dict(ans))


# 启动APP
if (__name__ == "__main__"):

    app.run(host = '127.0.0.1', port = 8809)


