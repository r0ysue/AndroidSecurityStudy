# Android Application Security Study
安卓应用安全学习


# 进Frida群

加微信：r0ysue（备注：进frida群）

---

# FRIDA

主要是接前文没能写完的部分：https://github.com/hookmaster/frida-all-in-one

### FRIDA脚本篇

- [FRIDA脚本系列（一）入门篇：在安卓8.1上dump蓝牙接口和实例](https://github.com/hookmaster/frida-all-in-one/tree/master/04.FRIDA-SCRIPTS/FRIDA%E8%84%9A%E6%9C%AC%E7%B3%BB%E5%88%97%EF%BC%88%E4%B8%80%EF%BC%89%E5%85%A5%E9%97%A8%E7%AF%87%EF%BC%9A%E5%9C%A8%E5%AE%89%E5%8D%938.1%E4%B8%8Adump%E8%93%9D%E7%89%99%E6%8E%A5%E5%8F%A3%E5%92%8C%E5%AE%9E%E4%BE%8B)
- [FRIDA脚本系列（二）成长篇：动静态结合逆向WhatsApp](https://github.com/hookmaster/frida-all-in-one/tree/master/04.FRIDA-SCRIPTS/FRIDA%E8%84%9A%E6%9C%AC%E7%B3%BB%E5%88%97%EF%BC%88%E4%BA%8C%EF%BC%89%E6%88%90%E9%95%BF%E7%AF%87%EF%BC%9A%E5%8A%A8%E9%9D%99%E6%80%81%E7%BB%93%E5%90%88%E9%80%86%E5%90%91WhatsApp)
- [FRIDA脚本系列（三）超神篇：百度AI“调教”抖音AI](https://github.com/hookmaster/frida-all-in-one/tree/master/04.FRIDA-SCRIPTS/FRIDA%E8%84%9A%E6%9C%AC%E7%B3%BB%E5%88%97%EF%BC%88%E4%B8%89%EF%BC%89%E8%B6%85%E7%A5%9E%E7%AF%87%EF%BC%9A%E7%99%BE%E5%BA%A6AI%E2%80%9C%E8%B0%83%E6%95%99%E2%80%9D%E6%8A%96%E9%9F%B3AI)
- [FRIDA脚本系列（四）更新篇：几个主要机制的大更新](https://www.anquanke.com/post/id/177597)

### FRIDA API篇

- [rpc、Process、Module、Memory使用方法及示例](https://www.anquanke.com/post/id/195215)
- [Java、Interceptor、NativePointer(Function/Callback)使用方法及示例](https://www.anquanke.com/post/id/195869)
- [Frida Java Hook 详解（安卓9）：代码及示例（上）](https://mp.weixin.qq.com/s/2BdX-rtAu8WZuzY3pK94NQ)

### FRIDA HOOK 网络通信组件

- 抓包、HTTP(s)、SSL pinning bypass
- 抓包、SOCKET(TCP/UDP)、包解密

### FRIDA HOOK JNI 、SO

- 静态注册与动态注册
- 枚举与拦截Exports/Imports
- 拦截JNIEnv与主动调用
- so地址hook与主动调用

### FRIDA辅助分析OLLVM

- FRIDA+IDA双开调试
- FRIDA Native 花式hook
- FRIDA主动调用确定数据流
