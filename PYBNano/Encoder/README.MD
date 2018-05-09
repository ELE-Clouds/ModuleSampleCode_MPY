<table style="width:50%" class="t_table" cellspacing="0" cellpadding="0"><tbody><tr>
<td align="center"> 参数</td>
<td align="center">类型
</td>
<td align="center"> 值</td>
<td valign="top">默认值
</td><td align="center"> 描述</td>
<td align="center"> 备注</td>
</tr>
<tr>
<td> pin_clk</td>
<td align="center">string</td>
<td align="center">引脚名</td>
<td valign="top">
</td><td> 与编码器CLK接口相连</td>
<td> </td>
</tr>
<tr>
<td> pin_dt</td>
<td align="center">string</td>
<td align="center">引脚名
</td>
<td valign="top">
</td><td> 与编码器DT接口相连</td>
<td> </td>
</tr>
<tr>
<td> pin_mode</td>
<td> int</td>
<td><div align="center">None(PULL_None)
</div><div align="center">1(PULL_UP)
</div><div align="center">2(PULL_DOWN)</div></td>
<td valign="top">None                     
</td><td>连接引脚模式
</td>
<td>引脚若处于上拉模式，则可不接+电源
</td>
</tr>
<tr>
<td> clicks</td>
<td>int
</td>
<td> </td>
<td valign="top">1
</td><td> 点击</td>
<td> 具体功能和用法不详</td>
</tr>
<tr>
<td> min_val</td>
<td> int</td>
<td> </td>
<td valign="top">0
</td><td> 编码最小值</td>
<td> </td>
</tr>
<tr>
<td> max_val</td>
<td> int</td>
<td> </td>
<td valign="top">100
</td><td> 编码最大值</td>
<td> </td>
</tr>
<tr>
<td> accel</td>
<td> int</td>
<td> </td>
<td valign="top">0
</td><td> 旋转加速</td>
<td> 具体功能和用法不详</td>
</tr>
<tr>
<td> reverse</td>
<td> bool</td>
<td> True
False
</td>
<td valign="top">False
</td><td> 反向（下向+1，反向-1）</td>
<td> </td>
</tr>
</tbody></table>