# raspberry-pi-monitor
树莓派系统监控--CPU温度监控
## 代码编写
树莓派的CPU温度是存放在一个文件里，使用如下命令查看CPU温度：
```bash
cat /sys/class/thermal/thermal_zone0/temp
```
输出的是五位的整数，除以1000就是CPU的温度了。
python代码如下：
```python
def get_temperature():
    try:
        cpu_temp_file = open("/sys/class/thermal/thermal_zone0/temp")
        cpu_temp = cpu_temp_file.read()
        return cpu_temp
    except Exception as e:
        print(e)
    finally:
        cpu_temp_file.close()
```
然后我使用Python自带的sqlite数据库存储数据：
```python
def create():
    global conn
    conn = sqlite3.connect('data.db')
    conn.execute("""
                create table if not exists temperature(
                id INTEGER PRIMARY KEY ,
                temperature INTEGER DEFAULT NULL,
                time INTEGER DEFAULT NULL)""")
    conn.commit()
def save():
    global conn, temperature, ID
    command1 = "insert into temperature \
             (id,temperature,time) values (?,?,?);"
    try:
        temp = (ID, temperature[-1], int(round(time.time() * 1000)))
        conn.execute(command1, temp)
    except Exception as e:
        print(e)
        print("insert error!")
        conn.rollback()
    conn.commit()
```
最后是画图：
```python
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
    plt.ylim(20 if 20 < min(temperature) else min(temperature),
             100 if 100 > max(temperature) else max(temperature))
    plt.gcf().autofmt_xdate()
    plt.savefig('static/temperature.jpg')
```
## 运行
此项目的GitHub地址：[zhang0peter/raspberry-pi-monitor: 树莓派系统监控--CPU温度监控](https://github.com/zhang0peter/raspberry-pi-monitor)
运行如下命令：
```bash
git clone https://github.com/zhang0peter/raspberry-pi-monitor.git
cd raspberry-pi-monitor/
screen -S raspberry-pi-monitor
bash main.sh
```
然后在浏览器中打开[http://127.0.0.1:4000/cpu](http://127.0.0.1:4000/cpu)即可看到树莓派CPU温度-时间图：
