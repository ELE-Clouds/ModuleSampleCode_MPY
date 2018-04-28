# -*- coding: UTF-8 -*-

u'''
******************************************************************************
* 文  件：HCSR04.py
* 概  述：HCSR04超声波传感器模块功能模块
* 版  本：V0.10
* 作  者：Robin Chen
* 日  期：2018年4月27日
* 历  史：  日期              编辑          版本      记录
           2018年4月27日     Robin Chen   V0.10    创建文件
******************************************************************************'''

from pyb import Pin
from time import sleep_us,ticks_us,sleep

trig = Pin('A0',Pin.OUT_PP)
echo = Pin('A1',Pin.IN)

u'''
*************************************************************************
* 功   能：获取距离值
* 说   明：获取并返回超声波传感器所测值（单位：米）
* 输入参数：None
* 输出参数：None
* 返 回 值：
          distance：距离（单位：米）

**************************************************************************'''
def getlang():
    distance=0
    trig.value(1)
    sleep_us(20)
    trig.value(0)
    while echo.value() == 0:
        pass
    if echo.value() == 1:
        ts=ticks_us()                   #开始时间
        while echo.value() == 1:        #等待脉冲高电平结束
            pass
        te=ticks_us()                   #结束时间
        tc=te-ts                        #回响时间（单位us）
        distance=(tc*170)/1000000       #距离计算（单位为:m）
    return distance
