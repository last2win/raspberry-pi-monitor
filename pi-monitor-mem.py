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
    try:
        MemAvailable = os.popen(
            "cat /proc/meminfo | grep MemAvailable |awk  '{print $2 / 1024}'").readline()
        MemAvailable = float(MemAvailable)
        return MemAvailable
    except Exception as e:
        print(e)


def save(mem):
    # 将数据保存至本地
    global conn
    command1 = "insert into mem \
             (mem,time) values (?,?);"
    try:
        temp = (mem, int(round(time.time() * 1000)))
        conn.execute(command1, temp)
    except Exception as e:
        print(e)
        print("insert error!")
        conn.rollback()
    conn.commit()



def main():
    global conn
    conn = None
    create()
    mem = get_mem()
    save(mem)
    print("now time is", time.asctime(time.localtime(time.time())),
          "and free memory is", mem, "M")


if __name__ == '__main__':
    while 1:
        main()
        time.sleep(60)
