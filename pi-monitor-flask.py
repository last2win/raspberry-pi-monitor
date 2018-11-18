# -*- coding: utf-8 -*-
import draw
import sqlite3
from flask import Flask, render_template, url_for
from datetime import timedelta
import os

conn = None
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(
    seconds=60)  # 设置图片的缓存时间为1分钟


def get_temperature():
    temperature = conn.execute(
        "select temperature,time from temperature  ;").fetchall()
    return temperature


def get_mem():
    MemTotal = os.popen(
            "cat /proc/meminfo | grep MemTotal |awk  '{print $2 / 1024}'").readline()
    MemTotal = float(MemTotal)
    mem = conn.execute(
        "select mem,time from mem  ;").fetchall()
    return mem,MemTotal


@app.route('/', methods=['GET'])
def main():
    temperature = get_temperature()
    mem,MemTotal = get_mem()
    return render_template('index.html', temperature=temperature, mem=mem,MemTotal=MemTotal)


@app.route('/mem', methods=['GET'])
def memory():
    draw.mem()
    return render_template('mem.html')


@app.route('/cpu', methods=['GET'])
def cpu():
    draw.cpu()
    return render_template('cpu.html')


if __name__ == '__main__':
    global conn
    conn = sqlite3.connect('data.db')
    app.run(host='0.0.0.0', port=4000, debug=True)
