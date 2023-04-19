[toc]

# Pixel4平替：OnePlus7刷NetHunter(android10) 指南

## Intro

## 为什么要用OnePlus7这个设备
1. Kali Nethunter官方支持一加7
2. OnePlus7是属于一加前几代机型,价格不高,性能上相当于Pixel4代
3. OnePlus7拥有高通9008的救砖模式,这个机器不管怎么折腾都可以恢复.
    >> 救砖模式是高通CPU提供的特性
4. OnePlus7在xda上面拥有众多的三方rom包，随便玩


本篇基于一加7手机，在性能上相当于Pixel四代手机。运行环境是安卓10。本文中用到的附件等位于百度盘中：链接：https://pan.baidu.com/s/1gtmCfqfQmEX5JvMZtvUH7w 提取码：euuo 

该系列为学员优秀作品系列，附件apk、代码等位于我的项目中，大家可以自取：

[https://github.com/r0ysue/AndroidSecurityStudy](20230403https://github.com/r0ysue/AndroidSecurityStudy)

## 刷机是玄学,怎么做才科学
1. 刷机需要测试各个版本的工具,很多时候不是你步骤错了,可能仅仅是使用的工具包版本不对
方案:提供下面步骤用到的所有工具包,在附件里面
2. 系统版本,OnePlus的系统版本众多,会影响结果,可能bootloader都解锁不了(这里有个伤心的故事)
方案:提供刷机固件包,从头开始,这样肯定行

## 开始刷机
### 下载安装高通驱动

1. 安装高通9008驱动,驱动名称:"QDLoader_HS-USB_Driver_64bit_Setup.exe"
+ 安装
![11](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023041811.png)
![12](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023041812.png)
![13](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023041813.png)
![14](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023041814.png)
![15](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023041815.png)
+ 用管理员权限打开cmd,输入命令开启测试模式,然后重启电脑
```
bcdedit /set testsigning on
```
+ 检查测试模式是否打开,重启后电脑桌面右下角出现下图所示就是成功,可继续下一步

![19](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023041819.png)

### 刷入固件包

1. 电脑解压固件包guacamoleb_14_P.32_210127.zip,
   ![20](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023041820.png)
2. 启动软件MsmDownloadTool V4.0.exe
   ![21](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023041821.png)
3. 点击start,等待手机进入edl模式
   ![22](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023041822.png)
4. 手机进入edl模式,MsmDownloadTool会自动输入android 10系统
+ 方式1:手机关机,数据线连接电脑,然后同时按住音量上键和下键
+ 方式2: 如果手机还可以开机,还可以连接adb
```
adb reboot edl
```
![23](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023041823.png)
5. 等待系统刷入,进入简单设置下
![24](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023041824.jpg)

### 解锁手机bootloader

1. 打开手机开发者模式, 开启adb调试
![2](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/202304182.jpg)
2.  开启oem解锁
![1](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/202304181.jpg)
3.  使用命令,进入fastboot模式
```
adb reboot bootloader
```
4.  使用命令解锁
```
fastboot oem unlock
```
  ![24](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023041824.png)

5. 选择"UNLOCK THE BOOTLOADER",等待重启,进入,重新设置usb调试和开发者模式
  
  ![18](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023041818.jpg)

### 刷入twrp

1. 重启手机到fastboot模式
```
adb reboot bootloader
```
2. 刷入twrp
```
fastboot boot twrp.img
```
![25](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023041825.png)

3. 这里安装完就直接进入revovery模式,twrp系统中,
4. 操作界面选择 Advanced->Flash Current TWRP

![26](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023041826.jpg)

4. 操作界面选择 Wipe->Format Data->输入yes

![27](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023041827.jpg)

5. 这时候不要重启

### 刷入Magisk

1. Advanced->ADB Sideload->Swipe to Start Sideload
![28](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023041828.jpg)
![29](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023041829.jpg)
![30](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023041830.jpg)
2. 输入命令,刷入Magisk.zip
![32](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023041832.png)
![31](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023041831.jpg)

### 刷入Disable_Dm-Verity_ForceEncrypt_11.02.2020.zip

1. Advanced->ADB Sideload->Swipe to Start Sideload
2. 刷入Disable_Dm-Verity_ForceEncrypt_11.02.2020.zip,出现Select Option的时候,按音量+键
![33](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023041833.png)
![34](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023041834.png)
3. 重启,进入设置,其中有个设置选"无"
![35](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023041835.jpg)

### 刷入nethunter

1. 重启到fastboot模式,然后音量键-进入recovery模式,重新进入twrp
![36](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023041836.jpg)

2. Advanced->ADB Sideload->Swipe to Start Sideload
3. 输入命令,刷入"kernel-nethunter-2021.3-oneplus7-oos-ten.zip"
```
adb sideload kernel-nethunter-2021.3-oneplus7-oos-ten.zip 
```
4. Advanced->ADB Sideload->Swipe to Start Sideload
5. 输入命令,输入"nethunter-2022.1-oneplus7-oos-ten-kalifs-full.zip "
```
adb sideload nethunter-2022.1-oneplus7-oos-ten-kalifs-full.zip 
```
![38](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023041838.png)
![39](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023041839.jpg)
![40](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023041840.jpg)
![41](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023041841.jpg)

### 安装一个magisk
1. 输入命令安装magisk.app
```
adb install magisk.app
```
![44](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023041844.png)
![45](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023041845.jpg)

### 初始化Nethunter
1. 联wifi,修改时间
2. 打开图中红圈得nethunter
   ![46](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023041846.jpg)
3. 点击kali Chroot Manager
   ![47](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023041847.jpg)
4. 点击START KALI CHROOT
   ![48](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023041848.jpg)
5. 成功
   ![49](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023041849.jpg)
6. 验证,打开命令行窗口,输入命令
   ```
   apt update
   ```
   ![50](http://www.dtasecurity.cn:20080/IMAGE/OFFLINE/2023041850.jpg)
   