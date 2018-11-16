# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 09:12:16 2018

@author: peter
"""
import time
import datetime
import sqlite3




def create():
    # 创建数据库
    global conn
    conn = sqlite3.connect('data.db')
    conn.execute("""
                create table if not exists temperature(
                id INTEGER PRIMARY KEY ,
                temperature INTEGER DEFAULT NULL,
                time INTEGER DEFAULT NULL)""")
    conn.commit()


def get_temperature():
    try:
        cpu_temp_file = open("/sys/class/thermal/thermal_zone0/temp")
        cpu_temp = cpu_temp_file.read()
        return cpu_temp
    except Exception as e:
        print(e)
    finally:
        cpu_temp_file.close()


def save():
    # 将数据保存至本地
    global conn, temperature, ID
    command1 = "insert into temperature \
             (id,temperature,time) values (?,?,?);"
    try:
        temp = (ID, temperature[-1], int(round(time.time() * 1000)))
        conn.execute(command1, temp)
#        print("save success!")
    except Exception as e:
        print(e)
        print("insert error!")
        conn.rollback()
    conn.commit()


def get():
    global conn, temperature, ID
    temp = conn.execute(
        "select temperature from temperature  ;").fetchall()
    for i in temp:
        for j in i:
            temperature.append(j/1000)


def draw():
    global ID, temperature
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
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


def main():
    global conn, temperature, ID
    temperature = []
    conn = None
    ID = 0
    create()
    get()
    temperature.append(get_temperature())
    ID = len(temperature)
    save()
    temperature[-1] = int(temperature[-1])/1000
    print("now time is", time.asctime(time.localtime(time.time())),
          "and cpu temperature is", temperature[-1],"℃")
    draw()
#    print(x[-1])


if __name__ == '__main__':
    while 1:
        main()
        time.sleep(60)