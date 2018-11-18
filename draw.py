# -*- coding: utf-8 -*-
import time
import datetime
import sqlite3
import os

conn=None

def connect():
    global conn
    conn = sqlite3.connect('data.db')

def cpu_get():
    global conn
    connect()
    temperature=[]
    temp = conn.execute(
        "select temperature from temperature  ;").fetchall()
    for i in temp:
        for j in i:
            temperature.append(j/1000)
    return temperature

def mem_get():
    global conn
    connect()
    mem=[]
    MemTotal = os.popen(
            "cat /proc/meminfo | grep MemTotal |awk  '{print $2 / 1024}'").readline()
    MemTotal = float(MemTotal)
    temp = conn.execute(
        "select mem from mem  ;").fetchall()
    for i in temp:
        for j in i:
            mem.append(j)
    return mem,MemTotal

def cpu():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    global conn
    temperature = cpu_get()
    ID = len(temperature)
    past = datetime.datetime.now()-datetime.timedelta(minutes=ID)
    x = [past+datetime.timedelta(minutes=i)
         for i in range(ID)]
    plt.title("time and cpu temperature", fontsize=25)
    plt.xlabel("time", fontsize=15)
    plt.ylabel("cpu temperature", fontsize=15)
    plt.plot(x, temperature)
    plt.ylim(20 if 20 < min(temperature) else min(temperature),
             100 if 100 > max(temperature) else max(temperature))
    plt.gcf().autofmt_xdate()
    plt.savefig('static/temperature.jpg')

def mem():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    global conn
    connect()
    mem,MemTotal = mem_get()
    ID = len(mem)
    past = datetime.datetime.now()-datetime.timedelta(minutes=ID)
    x = [past+datetime.timedelta(minutes=i)
         for i in range(ID)]
    plt.title("time and memory usage", fontsize=25)
    plt.xlabel("time", fontsize=15)
    plt.ylabel("memory usage", fontsize=15)
    plt.plot(x, mem)
    plt.ylim(0,MemTotal)
    plt.gcf().autofmt_xdate()
    plt.savefig('static/mem.jpg')

def main():
    print("draw shouldn't be use as main")
    


if __name__ == '__main__':
    main()
