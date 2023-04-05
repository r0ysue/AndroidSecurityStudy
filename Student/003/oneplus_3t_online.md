[toc]

# Pixel1代平替：一加3手机刷入KaliNethunter解封完整Linux命令环境

# 意义

大家知道在Linux上，我们想要对数据封包进行统计、定位、可视化、分析和转储等，有一系列的工具和软件。这些工具为我们进行网络数据封包的分析和处理提供了无与伦比的支持，可以说有这些工具的存在，没有抓不到的包，如果再结合hook技术，可以说没有解不开的协议。

工具虽好，但是它们的运行都需要一个完整的Linux环境，比如像jnettop/htop/nethogs等需要root权限，像iwlist/aircrack/HID等需要内核驱动支持、监听模式的打开等，Wireshark/Charles/BP会需要桌面环境的支持，在GUI中进行可视化分析。

具体的内容在这篇文章中进行了详细的解释：[《来自高纬的对抗：替换安卓内核并解封Linux命令和环境》](https://mp.weixin.qq.com/s/PIiGZKW6oQnOAwlCqvcU0g)

随着时间的推移，Nexus设备逐渐退出历史舞台，而Kali Nethunter却迟迟不能支持到Pixel设备；此时我们只能退而求其次，选择一加手机，来延续手机上刷入Kali Nethunter解封完整Linux环境的传统。

本篇基于一加3(t)手机，在性能上相当于Pixel一代手机。运行环境是安卓10。本文中用到的附件等位于百度盘中：链接：https://pan.baidu.com/s/1c01pB6JIY6a-25P-855dAA 提取码：e2gn 

该系列为学员优秀作品系列，附件apk、代码等位于我的项目中，大家可以自取：

[https://github.com/r0ysue/AndroidSecurityStudy](20230403https://github.com/r0ysue/AndroidSecurityStudy)



# Intro

1. 为什么要搭建nethunter的环境
  + 工欲善其事,必先利其器.nethunter强大的工具支持,使得工作变得轻松
2. 为什么使用oneplus3T
  + oneplus3T这部机型,lineage,nethunter,twrp都有很好的支持
  + oneplus3T现在的价格很低
  + oneplus3T性能还不错,比nexus 5x的性能强悍很多
3. 为什么写这个刷机文章
   不仅仅是因为这个nethunter的强大和oneplus3t的性价比,更因为是刷机总是出现这样那样的问题,导致失败.经过反复几天测试,得出了一种比较轻松的方式.后面提供了这个刷机过程中用到的所有的工具包
# 刷机前设置
需要开启开发者模式,bootloader解锁,usb调试
如果手机满足这些条件,可以直接进入刷入lineage
## 开启开发者模式
系统版本号(点击多次),一般进入方式都是手机里面,设置->关于手机->版本号
![1](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/202304061.jpg)
![2](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/202304062.jpg)
## 开启usb调试和oem解锁许可
+ 设置->系统->开发者选项
![3](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/202304063.jpg)
![4](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/202304064.jpg)
## 解锁OEM
1. 重启到bootloader
+ 使用adb命令
```
 adb reboot bootloader  
```
+ 手机关机,然后开机键+手机音量下键
![5](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/202304065.png)
![6](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/202304066.jpg)
1. 解锁
```
fastboot oem unlock
```
![7](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/202304067.png)
![8](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/202304068.jpg)
手机出现这个界面以后,选择UNLOCK THE BOOTLOADER(音量上下键可以切换选项,电源键做选择)
等待解锁后自动重启
注意: 解锁重启之后,完成基本设置之后,再次启动开发者模式和usb调试
# 刷入lineage
nethunter官方提供的系统是android10的镜像包,需要输入一个android10的底包,这里选择lineage的系统
## 刷入twrp
1. 重启手机,刷入twrp.img
```
adb reboot bootloader
fastboot flash recovery recovery.img 
```
![9](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/202304069.png)
1. 手机音量上下键,选择recovrey mode进入twrp的系统
![11](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023040611.jpg)
## 清理数据
1. 在twrp中,Wipe->Format Data->输入'yes'->成功之后,back到可以选择Advanced Wipe地方
![12](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023040612.jpg)
![10](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023040610.jpg)
1. Advanced Wipe->勾选全部
![15](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023040615.jpg)

## 输入防护墙的包
1. Advanced->ADB Sideload
![17](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023040617.jpg)
2. 输入命令
```
adb sideload oxygenos-9.0.6-bl-km-5.0.8-firmware-3.zip 
```
![40](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023040640.png)
![41](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023040641.jpg)

## 刷入lineage的包
1. Advanced->ADB Sideload
2. 输入如下命令
```
adb sideload lineage-17.1-20210215-nightly-oneplus3-signed.zip 
```
![42](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023040642.png)
![43](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023040643.jpg)

## 刷入magisk
1. Advanced->ADB Sideload
2. 输入下面命令
```
adb sideload app-release.zip
```
![44](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023040644.png)
![45](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023040645.jpg)
3. 重启
4. 开启开发者模式,usb调试
5. 使用下面命令安装magisk的app
```
adb install app-release.apk 
```
![46](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023040646.png)
![47](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023040647.jpg)
6. 重启,安装magisk之后,第一次需要重启,让配置生效
![48](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023040648.jpg)
7. magisk如上已经安装成功

# 使用Magisk刷入nethunter

1. 传入nethunter的包
```
adb push kalihunter.zip /sdcard/Download
```
![28](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023040628.png)
2. 选择 模块->本地,选择,nethunter的包,等待结束,重启
![29](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023040629.jpg)

# nethunter初始化设置
1. 重启后,连wifi,输入命令,设置时间
```
settings put global captive_portal_http_url https://www.google.cn/generate_204
settings put global captive_portal_https_url https://www.google.cn/generate_204
settings put global ntp_server 1.hk.pool.ntp.org
reboot
```
![30](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023040630.png)

2. 初始化,点击Kali Chroot Manager开始初始化
![31](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023040631.jpg)
![32](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023040632.jpg)
3. 命令窗口可以使用,成功
![33](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023040633.jpg)

# 刷入成功！

可以开启的逆向之旅了！后续还会更新OnePlus系列的Kali Nethunter刷入教程，敬请期待！ 想要直接购买刷好的设备，直接私信肉丝即可，vx：r0ysue 。卖设备还卖教程噢！助您升职加薪！