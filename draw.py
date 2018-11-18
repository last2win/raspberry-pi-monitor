# -*- coding: utf-8 -*-
import time
import datetime
import sqlite3
conn=None
def connect():
    global conn
    conn = sqlite3.connect('data.db')

def cpu_get():
    global conn
    temperature=[]
    temp = conn.execute(
        "select temperature from temperature  ;").fetchall()
    for i in temp:
        for j in i:
            temperature.append(j/1000)
    return temperature
def cpu():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    global conn
    connect()
    temperature = cpu_get()
    ID = len(temperature)
    past = datetime.datetime.now()-datetime.timedelta(minutes=ID)
    x = [past+datetime.timedelta(minutes=i)
         for i in range(ID)]
    plt.title("time and cpu temperature", fontsize=25)
    plt.xlabel("time", fontsize=15)
    plt.ylabel("cpu temperature", fontsize=15)
    plt.plot(x, temperature)
 #       plt.plot(x[::ID//10], temperature[::ID//10])
    plt.ylim(20 if 20 < min(temperature) else min(temperature),
             100 if 100 > max(temperature) else max(temperature))
    plt.gcf().autofmt_xdate()
    plt.savefig('static/temperature.jpg')

def mem():
    pass

def main():
    print("draw shouldn't be use as main")
    


if __name__ == '__main__':
    main()
