#!/usr/bin/env Python
# coding=utf-8

from flask import Flask, render_template, request, make_response


#app = Flask(__name__, template_folder=project_path,static_url_path=project_path+"/static/", static_folder=project_path+"/static/")
app = Flask(__name__,static_url_path="/static")

@app.route('/')
def index():
    return render_template("input.html")

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


@app.route('/goEnglisgMode', methods=['POST','GET'])
def goEnglisgMode():

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


@app.route('/goPoliticsMode', methods=['POST','GET'])
def goPoliticsMode():

    response = make_response(render_template("chooseM.html", subject="政治"))
    response.set_cookie("subject", "政治")
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


@app.route('/goEnglisg', methods=['POST','GET'])
def goEnglisg():
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

@app.route('/goPolitics', methods=['POST','GET'])
def goPolitics():
    response = make_response(render_template("input.html", subject="政治"))
    response.set_cookie("subject", "政治")
    return response


@app.route('/goGraph', methods=['GET'])
def goGraph():
    entity = request.args['entity']
    subject = dict(request.cookies)['subject']
    if subject == '地理':
        print("...")
        return render_template("graph.html")
    else:
        render_template("graph.html", entity=entity)

# 启动APP
if (__name__ == "__main__"):

    app.run(host = '127.0.0.1', port = 8809)


