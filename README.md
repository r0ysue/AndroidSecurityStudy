# Android Application Security Study
安卓应用安全学习


# 进Frida&&FART群

加微信：r0ysue（备注：进FridaFart群）

---

# 工具相关update

> 部分链接为知识星球、小鹅通等收费链接，不喜勿入

|工具|更新|
|:-:|:-|
|Fart|- [《Fart8终极版》](https://aistk.xet.tech/s/1mMFrK)：仅Nexus5x、Pixel1(XL)支持刷入<br/>- [《Fart12脱壳王》](https://alq.xet.tech/s/1hGLBF)：1. Fart10升级到Fart12，脱一二代壳依旧so easy ！ 2. 无root，及对抗所有大厂的检测指纹 3. (todo)直接用的内核模块syscall hook，无视eBPF的高版本限制 4. (todo)内置Frida过检测方案<br/>- jadx-gui定制版自动修复二代壳：报Fart脱壳王课程赠送|
|r0env|- [介绍文章：r0env：打造年轻人的第一套安卓逆向环境！](https://mp.weixin.qq.com/s/gBdcaAx8EInRXPUGeJ5ljQ)<br/>- [r0env之两小时完整使用视频](https://www.bilibili.com/video/BV1qQ4y1R7wW)<br/>- [r0env2011](https://t.zsxq.com/10LsaUoNU)（很多人跟我要r0env2021的分享，因为里面带DDMS、hyperpwn等等）<br/>- [r0env2022](https://appli0n8byd8759.h5.xiaoeknow.com)（店铺首页轮播图第五张）<br/>- todo：M芯片版r0env...现在不做主要因为还不成熟|
|Frida|- [《安卓Frida逆向与抓包实战》签名版](https://aistk.xet.tech/s/3DLQvC)<br/>- [《Frida逆向与协议分析》签名版](https://aistk.xet.tech/s/14e51G)<br/>- [todo：《安卓Frida应用SO逆向分析实战》签名版预售](https://aistk.xet.tech/s/2fdcLP)|
|KernelSU|- [Pixel3](https://t.zsxq.com/10boFCXni)<br/>- [Pixel4](https://t.zsxq.com/10QjuMgHG)<br/>- [Pixel4上的安卓13与KernelSU证书导入与抓包全套验证ok](https://t.zsxq.com/10OHT2S48)、[视频版](https://www.bilibili.com/video/BV1M8411Z7rC)<br/>- [Pixel5](https://t.zsxq.com/10V5Ah2yK)<br/>- [小米8：也一起解决了小米机器自编译boot后导致wifi无法使用的问题](https://t.zsxq.com/10Tjnbwz7)<br/>- [Pixel5](https://t.zsxq.com/10V5Ah2yK)<br/>- [一加7](https://t.zsxq.com/101F2paxn)|
|云手机|- [rock5b](https://t.zsxq.com/10BP2JODa)、[一开多安卓云手机 原生支持frida hook so](https://www.bilibili.com/video/BV1XY4y1m7NZ)<br/>- [orangepi5：几百块的云手机套装](https://t.zsxq.com/107aZE2fL)|
|iOS|- 越狱：iOS12：[最高版本也能越狱的iPhone6](https://t.zsxq.com/10bB9dEvt)、[《两百元成本的iOS逆向环境搭建》](https://t.zsxq.com/10v9zKkvv)<br/>- 抓包：[https://t.zsxq.com/10WVReMbd](https://t.zsxq.com/10WVReMbd)、https://t.zsxq.com/10lQkInqh<br/>- 越狱：iOS14-16：iPhoneX|

PS：[以上手机、硬件、图书等下单地址（卖手机处点击查看更多）](https://appli0n8byd8759.h5.xiaoeknow.com)


---

# 《FRIDA系列文章》

## A.环境准备和入门篇

- [01.Android环境准备：谷歌原版镜像8.1、TWRP、Magisk root](FRIDA/A01/README.md)
- [02.一篇文章带你领悟frida的精髓（基于安卓8.1）](FRIDA/A02/README.md)（代码已更新：20200512，具体见文件夹压缩包）

## B.FRIDA脚本篇

- [01.FRIDA脚本系列（一）入门篇：在安卓8.1上dump蓝牙接口和实例](FRIDA/B01/README.md)
- [02.FRIDA脚本系列（二）成长篇：动静态结合逆向WhatsApp](FRIDA/B02/README.md)
- [03.FRIDA脚本系列（三）超神篇：百度AI“调教”抖音AI](FRIDA/B03/README.md)
- [04.FRIDA脚本系列（四）更新篇：几个主要机制的大更新](FRIDA/B04/README.md)

## C.FRIDA API篇

- [01.FRIDA-API使用篇：rpc、Process、Module、Memory使用方法及示例](https://www.anquanke.com/post/id/195215)
- [02.FRIDA-API使用篇：Java、Interceptor、NativePointer(Function/Callback)使用方法及示例](https://www.anquanke.com/post/id/195869)
- [03.Frida Java Hook 详解（安卓9）：代码及示例（上）](https://mp.weixin.qq.com/s/2BdX-rtAu8WZuzY3pK94NQ)
- [04.Frida Java Hook 详解（安卓9）：代码及示例（下）](https://mp.weixin.qq.com/s/heK_r0zXo_6_RoA37yPtGQ)

## D.实用FRIDA篇

- [01.实用FRIDA进阶：内存漫游、`hook anywhere`、抓包](https://www.anquanke.com/post/id/197657)
- [02.实用FRIDA进阶：脱壳、自动化、实用问题集锦](https://www.anquanke.com/post/id/197670)
- 03.实用FRIDA进阶：主动调用，密码克星

---

# 《FART系列文章》

## 源码系列

- [2020年安卓源码编译指南及`FART`脱壳机谷歌全设备镜像发布](https://www.anquanke.com/post/id/199898)
- [FART源码解析及编译镜像支持到Pixel2(xl)](https://www.anquanke.com/post/id/201896)（链接：https://pan.baidu.com/s/1zAYliYbkagdUUsykww_L4g 提取码：vv5u）
- [`XPOSED`魔改一：获取特征](FART/xposed1.md)

> `Kali Linux`虚拟机下载种子在`FART/`文件夹中

## OPPOSRC：来自高纬的对抗系列

- [来自高纬的对抗①：定制ART解释器脱所有一二代壳](https://mp.weixin.qq.com/s/3tjY_03aLeluwXZGgl3ftw)  （[附件](FART/H1/attachment)）
- [来自高纬的对抗②：魔改XPOSED过框架检测(上)](https://mp.weixin.qq.com/s/c97zoTxRrEeYLvD8YwIUVQ)
- [来自高纬的对抗③：魔改XPOSED过框架检测(下)](https://mp.weixin.qq.com/s/YAMCrQSi0LFJGNIwB9qHDA)（[附件1](https://t.zsxq.com/eQR3fMf)、[附件2](https://t.zsxq.com/BqFAIEu)）
- [来自高纬的对抗④：定制安卓内核过反调试](https://mp.weixin.qq.com/s/CC40CwUS6jwNTc_by1zPlA)(附件:链接：https://pan.baidu.com/s/1zAYliYbkagdUUsykww_L4g 提取码：vv5u])
- [来自高纬的对抗⑤：替换安卓内核并解封Linux命令和环境](https://mp.weixin.qq.com/s/PIiGZKW6oQnOAwlCqvcU0g)（[附件](https://t.zsxq.com/jqNZrrr)）

## 进击的Coder：精品连载

- [安卓 App 逆向课程一之环境配置](https://mp.weixin.qq.com/s/YyDP_Lfk7kxOZf7F5SViLw)
- [精品连载丨安卓 App 逆向课程之二逆向神器 frida 的介绍](https://mp.weixin.qq.com/s/5LpaRY1O9br1ZnRNA-gH6Q)
- [精品连载丨安卓 App 逆向课程之三 frida 注入 Okhttp 抓包上篇](https://mp.weixin.qq.com/s/F_UGRoAsfDW4SAa7cXMKrg)
- [精品连载丨安卓 App 逆向课程之四 frida 注入 Okhttp 抓包中篇](https://mp.weixin.qq.com/s/PICqN6K_LFGHkjyiXkPzUw)
- [精品连载丨安卓 App 逆向课程之五 frida 注入 Okhttp 抓包下篇](https://mp.weixin.qq.com/s/SBEKXSO6LrFYsO5pOtfxJA)

##  各种合集：

- [《常见Java层反调试技术之root检测方式总结》](Student/001)
- [《挑战不用macOS逆向iOS APP》之两百元成本的iOS逆向环境搭建](Student/002)
- [《Pixel1代平替：一加3手机刷入KaliNethunter解封完整Linux命令环境》](Student/003)
- [《Pixel4平替：OnePlus7刷NetHunter(android10) 指南》](Student/004)
- [《挑战不用macOS逆向iOS APP》之ObjC语法、iOS应用开发、及Objection自动化hook入门](Student/005)
- [《Frida前置知识:iOS/ObjC语法进阶及其ARM汇编实现》](Student/006)
- [《Frida hook/invoke iOS以及内存搜刮和黑盒调用》](Student/007)