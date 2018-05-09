# -*- coding: utf-8 -*-

u'''
******************************************************************************
* 文  件：encoder_demo.py
* 概  述：通过旋转编码器控制LED灯亮度
* 版  本：V0.10
* 作  者：Robin Chen
* 日  期：2018年5月3日
* 历  史： 日期             编辑           版本         记录
          2018年5月3日    Robin Chen    V0.10       创建文件
******************************************************************************'''
from time import sleep_ms
from PYBNano.Encoder import Encoder
from pyb import LED

enc = Encoder(pin_clk='B0', pin_dt='B1', pin_mode=0, clicks=5,
                 min_val=0, max_val=255, accel=1, reverse=False)

u'''
*************************************************************************
* 功   能：读取旋转编码值
* 说   明：获取旋转编码器动作后的编码值
* 输入参数：
          enc: Encoder对象
* 输出参数：None
* 返 回 值：
**************************************************************************'''
def readloop(enc):
    oldval = 0
    while True:
        val = enc.value
        if oldval != val:
            print(val)
            oldval = val
        sleep_ms(50)
        LED(1).intensity(val)
        LED(2).intensity(val)
        LED(3).intensity(val)
        LED(4).intensity(val)

readloop(enc)
enc.close()