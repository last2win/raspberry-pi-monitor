# -*- coding: utf-8 -*-
import time
import datetime
import sqlite3
import os


def create():
    # 创建数据库
    global conn
    conn = sqlite3.connect('data.db')
    conn.execute("""
                create table if not exists mem(
                id INTEGER PRIMARY KEY ,
                mem DOUBLE DEFAULT NULL,
                time INTEGER DEFAULT NULL)""")
    conn.commit()


def get_mem():
    global MemTotal
    try:
        MemTotal = os.popen(
            "cat /proc/meminfo | grep MemTotal |awk  '{print $2 / 1024}'").readline()
        MemTotal=float(MemTotal)
        MemAvailable=os.popen(
        "cat /proc/meminfo | grep MemAvailable |awk  '{print $2 / 1024}'").readline()
        MemAvailable=float(MemAvailable)
        return MemAvailable
    except Exception as e:
        print(e)


def save():
    # 将数据保存至本地
    global conn, temperature, ID
    command1 = "insert into temperature \
             (id,mem,time) values (?,?,?);"
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
          "and free memory is", temperature[-1], "M")


if __name__ == '__main__':
    while 1:
        main()
        time.sleep(60)
