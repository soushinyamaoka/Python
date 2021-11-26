#import pandas as pd
#import numpy as np
#from scipy.stats import chi2_contingency
from flask import Flask, redirect ,request,render_template,jsonify
#from flask_bootstrap import Bootstrap
#import json
#import requests
import os
import base64
import tfLiteModel as learn
import model as model
from PIL import Image
import io
import setting
from datetime import datetime

#app = Flask(__name__)
app = Flask(__name__, static_url_path=setting.STATIC_PATH)

def init(environ, start_response):
    return render_template('form.html', modelList=[])

@app.route("/")
def check():
    return render_template('form.html')

@app.route('/output', methods=['POST'])
def output():
    base64Url = request.form['upImage']
    if not base64Url:
        return render_template('form.html', modelList=[])
    # アップロードされた画像をデコード
    #base64Url = request.json['base64Url']
    image = base64.b64decode(base64Url.split(',')[1])
    # 画像データから Image オブジェクトを生成
    inst = io.BytesIO(image)
    img = Image.open(inst)
    date_s = (datetime.now().strftime('%Y%m%d%H%M%S%f'))
    fileName = date_s + ".png"
    if setting.LOCAL＿MODE:
        fileDir = setting.LOCAL_IMAGE_FILE_PATH
    else:
        fileDir = setting.IMAGE_FILE_PATH
    img.save(os.path.join(fileDir, fileName))

    degree = 0.5
    if setting.LOCAL＿MODE:
        #resultList = setting.NAME_LIST
        resultList = learn.learning(fileName, degree)
    else:
        resultList = learn.learning(fileName, degree)
    modelList = model.getModel(resultList)
    os.remove(os.path.join(fileDir, fileName))
    return render_template("form.html", modelList=modelList)
    #return jsonify(ResultSet=json.dumps(modelList))

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)