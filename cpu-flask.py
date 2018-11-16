# -*- coding: utf-8 -*-
import time
import datetime
import sqlite3
from flask import Flask, render_template, url_for
from datetime import timedelta
conn = None
temperature = []
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(
    seconds=60)  # 设置图片的缓存时间为1分钟


def get():
    global temperature
    conn = sqlite3.connect('data.db')
    temperature = conn.execute(
        "select temperature,time from temperature  ;").fetchall()


@app.route('/', methods=['GET'])
def hello_world():
    get()
    return render_template('index.html', data=temperature)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)
