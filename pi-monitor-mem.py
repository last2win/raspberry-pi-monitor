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
    global conn, mem, ID
    command1 = "insert into mem \
             (id,mem,time) values (?,?,?);"
    try:
        temp = (ID, mem[-1], int(round(time.time() * 1000)))
        conn.execute(command1, temp)
#        print("save success!")
    except Exception as e:
        print(e)
        print("insert error!")
        conn.rollback()
    conn.commit()


def get():
    global conn, mem, ID
    temp = conn.execute(
        "select mem from mem  ;").fetchall()
    for i in temp:
        for j in i:
            mem.append(j)



def main():
    global conn, mem, ID
    mem = []
    conn = None
    ID = 0
    create()
    get()
    mem.append(get_mem())
    ID = len(mem)
    save()
    print("now time is", time.asctime(time.localtime(time.time())),
          "and free memory is", mem[-1], "M")


if __name__ == '__main__':
    while 1:
        main()
        time.sleep(60)
