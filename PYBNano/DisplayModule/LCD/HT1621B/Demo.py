# -*- coding:UTF-8 -*-

u'''
******************************************************************************
* 文  件：Demo.py
* 概  述：用于演示ht1621x芯片驱动GDC03849段式液晶显示DHT11采集的温湿度值
* 版  本：V0.10
* 作  者：Robin Chen
* 日  期：2018年5月14日
* 历  史： 日期             编辑           版本         记录
          2018年5月14日    Robin Chen    V0.10       创建文件
******************************************************************************'''
from PYBNano.DisplayModule.LCD.HT1621B.GDC03849 import viewTemp,viewRH
from machine import Pin
from dht import DHT11
from time import sleep
from pyb import LED

# DHT11引脚设置
dhtgnd = Pin('Y10',Pin.OUT,Pin.PULL_DOWN)
dhtvcc = Pin('Y9',Pin.OUT,Pin.PULL_UP)
dhts   = Pin('Y8')
dhtgnd.off()
dhtvcc.on()
sleep(2)
dt = DHT11(dhts)

while True:
    LED(4).on()
    dt.measure()
    LED(4).off()
    LED(3).on()
    te = dt.temperature()   # 温度
    dh = dt.humidity()      # 湿度
    viewTemp(te)
    viewRH(dh)
    LED(3).off()
    print('当前温度：',te,' | 当前湿度：',dh)
    sleep(2)
