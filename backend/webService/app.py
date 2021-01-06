
#!/usr/bin/env Python
# coding=utf-8
import sys
import os


from flask import Flask, render_template, request, make_response
from flask import jsonify

import time
import threading


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


import re
zhPattern = re.compile(u'[\u4e00-\u9fa5]+')


app = Flask(__name__,static_url_path="/static") 

@app.route('/message', methods=['POST'])
def why():
    return jsonify({'text': "test"})

@app.route("/")
def index():
    return render_template("main.html")

# 启动APP
if (__name__ == "__main__"): 
    app.run(host = '0.0.0.0', port = 8899)


