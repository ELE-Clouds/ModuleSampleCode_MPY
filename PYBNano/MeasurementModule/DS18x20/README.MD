MicroPython 驱动 DS18B20
====

![][2]

主题：
----
单总线温度传感器模块 DS18B20 在 MicroPython 下的应用


演示环境：
----


演示说明：
----
本次主要演示多个单总线设备如何进行正常工作。


演示代码：
----
由于当前开发板的当前版本固件自带 onewire.py ，因而，此处仅需要加入ds18x20.py文件即可，请在官方github下载 [ds18x20.py][1] 文件到当前文件夹。

<pre><code>
# -*- coding: UTF-8 -*-

u'''
******************************************************************************
* 文  件：DS18B20_Demo.py
* 概  述：温度传感器
* 版  本：V0.10
* 作  者：Robin Chen
* 日  期：2018年5月2日
* 历  史： 日期             编辑           版本         记录
          2018年5月2日    Robin Chen    V0.10       创建文件
          2018年5月7日    Robin Chen    V0.11       修改了打印内容，并整理到分类文件夹
******************************************************************************'''
from machine import Pin
import onewire
from MeasurementModule.DS18x20.ds18x20 import DS18X20
from time import sleep

ow=onewire.OneWire(Pin('A0'))
ds = DS18X20(ow)
rom = ds.scan()
while True:
    ds.convert_temp()
    print('--------------')
    for i in range(len(rom)):
        dt=ds.read_temp(rom[i])
        print('DS-',i,':',dt,'℃')
    print('--------------')
    sleep(3)
</code></pre>

参数说明：
----
![][4]

效果图：
----
![][3]

总结
----


[1]: https://github.com/micropython/micropython/tree/master/drivers/onewire "单总线设备驱动"
[2]: ./img/DS18b20.jpg "主题图片"
[3]: ./img/DS18B20.png "效果图"
[4]: ./img/canshu.png "参数说明"
[5]: http://www.elecfans.com/yuanqijian/sensor/20160512418254_a.html '参考资料'