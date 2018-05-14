# -*- coding:UTF-8 -*-

u'''
******************************************************************************
* 文  件：ht1621x.py
* 概  述：ht1621x芯片驱动文件
* 版  本：V0.11
* 作  者：Robin Chen
* 日  期：2018年5月9日
* 历  史： 日期             编辑           版本         记录
          2018年5月9日    Robin Chen    V0.10       创建文件
          2018年5月11日   Robin Chen    V0.11       将所有命令以二进制字符串的形式列了出来
******************************************************************************'''

from machine import Pin
from time import sleep_ms,sleep_us,sleep


# 引脚定义,启动上拉电阻
CS = Pin("A0",Pin.OUT,Pin.PULL_UP)      # 低电平有效
RD = Pin("A1",Pin.OUT,Pin.PULL_UP)      # 低电平有效
WR = Pin("B0",Pin.OUT,Pin.PULL_UP)      # 低电平有效
DATA = Pin("B1",Pin.OUT,Pin.PULL_UP)    # 高低电平均有效


# 命令清单
# -------------------------
# 功能符号(标志字)
FLAG_CMD        = '100'  # 命令
FLAG_READ       = '110'  # 只读RAM
FLAG_WRITE      = '101'  # 只写RAM
FLAG_MODIFY     = '101'  # 读和写RAM(即修改RAM)READ-MODIFY-WRITE

# 液晶控制
CMD_LCDON       = '000000110'  # 打开LCD偏压发生器
CMD_LCDOFF      = '000000100'  # 关闭LCD偏压发生器   （上电时默认设置）

#系统控制
CMD_SYSEN       = '000000010'  # 打开系统振荡器
CMD_SYSDIS      = '000000000'  # 关半系统振荡器和LCD偏压发生器 （上电时默认设置）

#Bias与COM设置，即偏置电压与COM端,当前参数根据液晶的资料文件进行选择，比如1/4DUTY,1/3BIAL，则选择"B3C4"
# 1/2偏压设置
CMD_B2C2        = '001000000'	 # 2COM,1/2 bias
CMD_B2C3        = '001001000'	 # 3COM,1/2 bias
CMD_B2C4        = '001010000'	 # 4COM,1/2 bias

# 1/3偏压设置
CMD_B3C2        = '001000010'	 # 2COM,1/3 bias
CMD_B3C3        = '001001010'	 # 3COM,1/3 bias
CMD_B3C4        = '001010010'	 # 4COM,1/3 bias

# 时钟设置
CMD_RC256K      = '000110000'  # 系统时钟源，片内RC振荡器   （上电时默认设置）
CMD_EXT256K     = '000111000'  # 系统时钟源，外部时钟
CMD_XTAL32K     = '000101000'  # 系统时钟源（晶振）

# 时基设置
CMD_TIMER_EN    = '000001100'  # 时基输出使能
CMD_TIMER_DIS   = '000001000'  # 时基输出失效
CMD_CLR_TIMER   = '000011000'  # 时基发生器清零

# WDT设置
CMD_WDT_DIS     = '000001010'  # WDT溢出标志输出失效，禁用看门狗
CMD_WDT_EN      = '000001110'  # WDT溢出标志输出有效，启用看门狗
CMD_CLR_WDT     = '000011100'  # 清除WDT状态

# 声音输出设置
CMD_TONE2K      = '011000000'  # 设置声音频率输出为2KHz
CMD_TONE4K      = '010000000'  # 设置声音频率输出为4KHz
CMD_TONEON      = '000010010'   # 打开声音输出
CMD_TONEOFF     = '000010000'   # 关闭声音输出   （上电时默认设置）

# 时基/WDT输出设置
CMD_F1          = '101000000'  # 时基/WDT时钟输出:1Hz | WDT超时标志后: 4s
CMD_F2          = '101000010'  # 时基/WDT时钟输出:2Hz | WDT超时标志后: 2s
CMD_F4          = '101000100'  # 时基/WDT时钟输出:4Hz | WDT超时标志后: 1s
CMD_F8          = '101000110'  # 时基/WDT时钟输出:8Hz | WDT超时标志后: 1/2s
CMD_F16         = '101001000'  # 时基/WDT时钟输出:16Hz | WDT超时标志后: 1/4s
CMD_F32         = '101001010'  # 时基/WDT时钟输出:32Hz | WDT超时标志后: 1/8s
CMD_F64         = '101001100'  # 时基/WDT时钟输出:64Hz | WDT超时标志后: 1/16s
CMD_F128        = '101001110'  # 时基/WDT时钟输出:128Hz | WDT超时标志后: 1/32s   （上电时默认设置）

# IRQ设置
CMD_IRQ_DIS     = '100000000'  # 使IRQ输出失效   （上电时默认设置）
CMD_IRQ_EN      = '100010000'  # 使IRQ输出有效

# 工作模式设置
CMD_TEST        = '111000000'  # 测试模式
CMD_NORMAL      = '111000110'  # 普通模式   （上电时默认设置）

#默认设置清单
u'''----------------------------------------
|  CMD_LCDOFF   |  LCD偏压发生器关闭       |
|  CMD_SYSDIS   |  系统振荡器关闭          |
|  CMD_RC256K   |  使能RC振荡器           | 
|  CMD_TONEOFF  |  声音通道关闭            |   
|  CMD_F128     |  时基/WDT时钟输出为128Hz |
|  CMD_IRQ_DIS  |  IRQ输出关闭            |
|  CMD_NORMAL   |  系统设置为默认工作模式    |
-----------------------------------------'''
# -------------- 结束 -----------------


u'''
*************************************************************************
* 功   能：发送数据
* 说   明：将数据转化时序波形
* 输入参数：
          da: 需要写入的数据
* 输出参数：None
* 返 回 值：
          True
**************************************************************************'''
def _wrData(da):
    for i in da:
        WR.off()
        DATA.value(int(i))
        sleep_us(4)
        WR.on()
        sleep_us(4)
    return True


u'''
*************************************************************************
* 功   能：写命令
* 说   明：
* 输入参数：
          cmd: str | 
* 输出参数：None
* 返 回 值：True
**************************************************************************'''
def HT1621xWrCmd(cmd):
    CS.off()
    sleep_us(4)
    _wrData(FLAG_CMD)
    _wrData(cmd)
    CS.on()
    sleep_us(4)
    return True


u'''
*************************************************************************
* 功   能：指定地址写单个数据
* 说   明：
* 输入参数：
          addr: 数据地址 | str | hex | 0x00~0x1F | eg. 0x00
          data: 数据列表 | list| hex | 0x00~0x0F | eg: 0x00
* 输出参数：None
* 返 回 值：
**************************************************************************'''
def HT1621xWrOneData(addr,data):
    ad = bin(addr^(1<<6))[3:]   # 将16进制值转化为6位二进制字符串
    da = bin(data^(1<<4))[3:]   # 将16进制值转化为4位二进制字符串
    CS.off()
    sleep_us(4)
    _wrData(FLAG_WRITE)
    _wrData(ad)
    _wrData(da)
    CS.on()
    sleep_us(4)
    return True


u'''
*************************************************************************
* 功   能：指定地址连续写多个数据
* 说   明：
* 输入参数：
          addr: 数据起始地址 | str | hex | 0x00~0x1F | eg. 0x00
          data: 数据列表    | list| hex | 0x00~0x0F | eg: [0x00,0x0F,0x0A]
* 输出参数：None
* 返 回 值：True
**************************************************************************'''
def HT1621xWrAllData(addr,data):
    ad = bin(addr^(1<<6))[3:]   # 将16进制值转化为6位二进制字符串
    CS.off()
    sleep_us(4)
    _wrData(FLAG_WRITE)         # 写命令
    _wrData(ad)                 # 写地址
    for da in data:
        dat = bin(da ^ (1 << 4))[3:]   # 将16进制值转化为4位二进制字符串
        _wrData(dat)            # 写数据
    CS.on()
    sleep_us(4)
    return True


u'''*************************************************************************
* 功   能：显示所有显示字段
* 说   明：
* 输入参数：
          nbit: 数据起始地址 | str | hex | 0x00~0x1F | eg. 0x00
          data: 数据列表    | list| hex | 0x00~0x0F | eg: 0x00
* 输出参数：None
* 返 回 值：True
**************************************************************************'''
def ALLSHOW(addr,nbit):
    data = []
    for i in range(nbit):
        data.append(0x0F)
    HT1621xWrAllData(addr,data)
    return True


u'''*************************************************************************
* 功   能：清除屏幕全部显示
* 说   明：
* 输入参数：
          addr: 数据起始地址 | str | hex | 0x00~0x1F | eg. 0x00
          data: 数据列表    | list| hex | 0x00~0x0F | eg: 0x00
* 输出参数：None
* 返 回 值：True
**************************************************************************'''
def ALLCLEAR(addr,nbit):
    data = []
    for i in range(nbit):
        data.append(0x00)
    HT1621xWrAllData(addr,data)
    return True

u'''
*************************************************************************
* 功   能：液晶初建化
* 说   明：根据当前配置，打开或关闭一些功能
* 输入参数：None
* 输出参数：None
* 返 回 值：
**************************************************************************'''
def lcdinit():
    CS.on()
    WR.on()
    RD.on()
    DATA.on()
    sleep(3)
    HT1621xWrCmd(CMD_B3C4)
    HT1621xWrCmd(CMD_RC256K)
    HT1621xWrCmd(CMD_SYSDIS)
    HT1621xWrCmd(CMD_WDT_DIS)
    HT1621xWrCmd(CMD_TONE4K)
    HT1621xWrCmd(CMD_SYSEN)
    HT1621xWrCmd(CMD_NORMAL)
    HT1621xWrCmd(CMD_TONEON)
    sleep(1)
    HT1621xWrCmd(CMD_TONEOFF)
    HT1621xWrCmd(CMD_LCDON)
    return True
