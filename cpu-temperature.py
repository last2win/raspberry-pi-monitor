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
    global conn, temperature
    command1 = "insert into temperature \
             (temperature,time) values (?,?,?);"
    try:
        temp = ( temperature, int(round(time.time() * 1000)))
        conn.execute(command1, temp)
#        print("save success!")
    except Exception as e:
        print(e)
        print("insert error!")
        conn.rollback()
    conn.commit()








def main():
    global conn
    conn = None
    create()
    temperature=get_temperature()
    save()
    print("now time is", time.asctime(time.localtime(time.time())),
          "and cpu temperature is", temperature,"℃")


if __name__ == '__main__':
    while 1:
        main()
        time.sleep(60)