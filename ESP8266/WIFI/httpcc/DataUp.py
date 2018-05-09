import socket 
from machine import Pin
from dht import DHT11
from time import * 
import network
 

SSID="NTS"
PASSWORD="nanjingtiansu"
port=80
wlan=None
listenSocket=None

def connectWifi(ssid,passwd): #建立wifi连接
  global wlan
  wlan=network.WLAN(network.STA_IF)
  wlan.active(True)
  wlan.disconnect()
  wlan.connect(ssid,passwd)
  while(wlan.ifconfig()[0]=='0.0.0.0'):
    sleep(1)
  return True


#HTML to send to browsers

hts =  """<!DOCTYPE html>
<html>
<head>
<title>ESP8266 数据上传演示</title>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<meta http-equiv="refresh" content="1">
<style>
body {background-color: white}
h1 {color:red}
</style>
</head>
<body>
<center><h1>ESP8266 DHT11 温、湿度数据上送</h1>
<form>
<div>
<table>
<tr>
<td>温度：</td><td>%2.2d</td>
</tr>
<tr>
<td>湿度：</td><td>%2.2d</td>
</tr>
</table>
</div>
</form>
</center>
</body>
</html>
"""
#hts = "Start:{0:2.2f} and End:{1:0.3f}"
#Wemos Dpin to GPIO
#D1->GPIO5  ----  红色 
#D2->GPIO4  ----  绿色
#D5->GPIO14  ----  蓝色



ledBlue = Pin(14, Pin.OUT)  # 蓝色
ledGrean = Pin(4, Pin.OUT)  # 绿色
ledRed = Pin(5, Pin.OUT)  # 红色

dHt = DHT11(Pin(12))


# 只亮绿色
def greanOnly():
  #ledBlue.off()
  ledGrean.on()
  ledRed.off()


# 只亮红色
def redOnly():
  #ledBlue.off()
  ledGrean.off()
  ledRed.on()


connectWifi(SSID,PASSWORD)
ip=wlan.ifconfig()[0]

listenSocket = socket.socket() #建立一个实例
listenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listenSocket.bind((ip,port))  #绑定建立网路连接的ip地址和端口
listenSocket.listen(5) #开始侦听

print ('tcp waiting...')

while True:
  print("accepting.....")
  conn, addr = listenSocket.accept()
  print("Got a connection from %s" % str(addr))
  request = conn.recv(1024)
  print("Content = %s" % str(request))
  request = str(request)
 
  dHt.measure()
  t = dHt.temperature()
  h = dHt.humidity()
  if t > 25:
    redOnly()
  else:
    greanOnly()
  response = hts%(t,h) #html #将html的网页定义装载在回应字段
  conn.send(response) #send到浏览器上，就形成了控制界面
  conn.close()
  if ledBlue.value():
    ledBlue.off()
  else:
    ledBlue.on()