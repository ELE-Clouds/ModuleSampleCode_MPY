# -*- coding: UTF-8 -*-

u'''
******************************************************************************
* 文  件：WebControl.py
* 概  述：Web页面控制设备
* 版  本：V0.10
* 作  者：Robin Chen
* 日  期：2018年5月8日
* 历  史： 日期             编辑           版本         记录
          2018年5月8日    Robin Chen    V0.10       创建文件
******************************************************************************'''
from ESP8266.WIFI.httpcc import netConnect  # 此处引用为获取netConnect文件中的全局变量“wlan”。
import socket
from machine import Pin

# 读取WEB页面代码文件
htmls = open("ESP8266/WIFI/httpcc/WebKZ.html")
html= htmls.read()      #此处直接由文件读取，如果直接在此处写入页面代码，须使用 '''  ''' 将代码包含，否则无法显示
htmls.close()


#Wemos Dpin to GPIO
#D1->GPIO5	----	红色 
#D2->GPIO4	----	绿色
#D5->GPIO14	----	蓝色


ledBlue = Pin(14, Pin.OUT)	# 蓝色
ledGrean = Pin(4, Pin.OUT)	# 绿色
ledRed = Pin(5, Pin.OUT)	# 红色

 
# 只亮绿色
def greanOnly():
  ledBlue.off()
  ledGrean.on()
  ledRed.off()

# 全开
def allOn():
  ledBlue.on()
  ledGrean.on()
  ledRed.on()

# 只亮红色
def redOnly():
  ledBlue.off()
  ledGrean.off()
  ledRed.on()

# 只亮蓝色
def blueOnly():
  ledBlue.on()
  ledGrean.off()
  ledRed.off()

# 全关
def allOff():
  ledBlue.off()
  ledGrean.off()
  ledRed.off()


port=80
listenSocket=None
ip=netConnect.wlan.ifconfig()[0]

listenSocket = socket.socket() #建立一个实例
listenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listenSocket.bind((ip,port))   #绑定建立网路连接的ip地址和端口
listenSocket.listen(5)         #开始侦听

print ('等待TCP连接...')

while True:
    print("连接中.....")
    conn, addr = listenSocket.accept()
    print("已连接 %s" % str(addr))
    request = conn.recv(1024)
    print("内容： %s" % str(request))
    request = str(request)


    CMD_grean = request.find('/?CMD=greenlight') #如果在请求的包中，发现有?CMD=greenlight，下同
    CMD_allon = request.find('/?CMD=allon')
    CMD_red = request.find('/?CMD=redlight')
    CMD_blue = request.find('/?CMD=bluelight')
    CMD_alloff = request.find('/?CMD=alloff')
 

    print("Data: " + str(CMD_grean))
    print("Data: " + str(CMD_allon))
    print("Data: " + str(CMD_red))
    print("Data: " + str(CMD_blue))
    print("Data: " + str(CMD_alloff))

 
    if CMD_grean == 6:  #如果此命令有效，下同
        print('+grean')
        greanOnly()     #调用仅点亮绿灯函数，下同
 
    if CMD_allon == 6:
        print('+allon')
        allOn()

    if CMD_red == 6:
        print('+red')
        redOnly()

    if CMD_blue == 6:
        print('+blue')
        blueOnly()

    if CMD_alloff == 6:
        print('+alloff')
        allOff()

    response = html       #将html的网页定义装载在回应字段
    conn.send(response)   #send到浏览器上，就形成了控制界面
    conn.close()
