# -*- coding: UTF-8 -*-

u'''
******************************************************************************
* 文  件：netConnect.py
* 概  述：网络连接函数
* 版  本：V0.10
* 作  者：Robin Chen
* 日  期：2018年5月8日
* 历  史： 日期             编辑           版本         记录
          2018年5月8日    Robin Chen    V0.10       创建文件
******************************************************************************'''

import network
import time

# 设当前设备为“客户端”模式，并连接WIFI
def connectWifi(_ssid, _passwd):
    global wlan
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.disconnect()
    wlan.connect(_ssid, _passwd)
    while (wlan.ifconfig()[0] == '0.0.0.0'):
        time.sleep(3)   # 3秒后重新连接
    return wlan.ifconfig()[0]

# 设当前设备为AP模式
