# -*- coding: UTF-8 -*-

u'''
******************************************************************************
* 文  件：__init__.py
* 概  述：模块初始化
* 版  本：V0.10
* 作  者：Robin Chen
* 日  期：2018年5月8日
* 历  史： 日期             编辑           版本         记录
          2018年5月8日    Robin Chen    V0.10       创建文件
******************************************************************************'''

from ESP8266.WIFI.httpcc import netConnect

SSID="WIFI名称"
PASSWORD="WIFI连接密码"

ip = netConnect.connectWifi(SSID,PASSWORD)   #连接网络

if ip != "0,0,0,0":
    print("连接成功，当前IP为：",ip)
else:
    print("连接失败，3秒后重新连接！")

l = ("Web控制功能演示","WEB数据传输功能演示")


while True:
    print("\n\n\n  操作选择  \n  -------")
    for i in range(len(l)):
        print(i, ":", l[i])
    print("====================")
    n = input("请输入序号进行选择，输入'Q'或'q'回车后退出：")

    if n == "0":
        from ESP8266.WIFI.httpcc import WebControl
        break
    elif n == "1":
        from ESP8266.WIFI.httpcc import DataUp
        break
    elif n == "Q" or n == "q":
        break
    else:
        continue