# 树莓派系统监控--CPU温度监控和内存使用情况监控
## 准备
需要安装Python3和Flask：
```bash
apt install python3 python3-pip python3-flask screen
```
## 运行
运行如下命令：
```bash
git clone https://github.com/zhang0peter/raspberry-pi-monitor.git
cd raspberry-pi-monitor/
screen -S raspberry-pi-monitor
bash main.sh
```
然后在浏览器中打开[http://127.0.0.1:4000/](http://127.0.0.1:4000/)即可看到树莓派的监控：





