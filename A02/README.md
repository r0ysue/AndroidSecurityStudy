* [一篇文章带你领悟`frida`的精髓（基于安卓8.1）](#一篇文章带你领悟frida的精髓基于安卓81)
	* [`frida`是啥？](#frida是啥)
	* [`frida`为什么这么火？](#frida为什么这么火)
	* [frida实操环境](#frida实操环境)
	* [基本能力Ⅰ：hook参数、修改结果](#基本能力Ⅰ：hook参数-修改结果)
	* [基本能力Ⅱ：参数构造、方法重载、隐藏函数的处理](#基本能力ii参数构造-方法重载-隐藏函数的处理)
	* [中级能力：远程调用](#中级能力远程调用)
	* [高级能力：互联互通、动态修改](#高级能力互联互通-动态修改)
	* [打算做个成套的教程、目录已经想好了](#打算做个成套的教程-目录已经想好了)

# 一篇文章带你领悟`frida`的精髓（基于安卓8.1）

前阵子受[《Xposed模块编写的那些事》](https://www.freebuf.com/articles/terminal/114910.html)这篇文章的帮助很大，感觉有必要写一篇文章来回馈freebuf社区。现在最火爆的又是`frida`，该框架从`Java`层hook到`Native`层hook无所不能，虽然持久化还是要依靠`Xposed`和`hookzz`等开发框架，但是`frida`的动态和灵活对逆向以及自动化逆向的帮助非常巨大。

## `frida`是啥？

首先，`frida`是啥，github目录[Awesome Frida](https://github.com/dweinstein/awesome-frida)这样介绍`frida`的：

>Frida is Greasemonkey for native apps, or, put in more technical terms, it’s a dynamic code instrumentation toolkit. It lets you inject snippets of JavaScript into native apps that run on Windows, Mac, Linux, iOS and Android. Frida is an open source software.

`frida`是平台原生`app`的`Greasemonkey`，说的专业一点，就是一种动态插桩工具，可以插入一些代码到原生`app`的内存空间去，（动态地监视和修改其行为），这些原生平台可以是`Win`、`Mac`、`Linux`、`Android`或者`iOS`。而且`frida`还是开源的。

`Greasemonkey`可能大家不明白，它其实就是`firefox`的一套插件体系，使用它编写的脚本可以直接改变`firefox`对网页的编排方式，实现想要的任何功能。而且这套插件还是外挂的，非常灵活机动。

`frida`也是一样的道理。

## `frida`为什么这么火？

动静态修改内存实现作弊一直是刚需，比如金山游侠，本质上`frida`做的跟它是一件事情。原则上是可以用`frida`把金山游侠，包括`CheatEngine`等“外挂”做出来的。

当然，现在已经不是直接修改内存就可以高枕无忧的年代了。大家也不要这样做，做外挂可是违法行为。

在逆向的工作上也是一样的道理，使用`frida`可以“看到”平时看不到的东西。出于编译型语言的特性，机器码在CPU和内存上执行的过程中，其内部数据的交互和跳转，对用户来讲是看不见的。当然如果手上有源码，甚至哪怕有带调试符号的可执行文件包，也可以使用`gdb`、`lldb`等调试器连上去看。

那如果没有呢？如果是纯黑盒呢？又要对`app`进行逆向和动态调试、甚至自动化分析以及规模化收集信息的话，我们需要的是细粒度的流程控制和代码级的可定制体系，以及不断对调试进行动态纠正和可编程调试的框架，这就是`frida`。

`frida`使用的是`python`、`JavaScript`等“胶水语言”也是它火爆的一个原因，可以迅速将逆向过程自动化，以及整合到现有的架构和体系中去，为你们发布“威胁情报”、“数据平台”甚至“AI风控”等产品打好基础。

![](pic/01.png)

官宣屁屁踢甚至将其`敏捷开发`和`迅速适配到现有架构`的能力作为其核心卖点。

## frida实操环境

主机：

>Host：Macbook Air CPU: i5  Memory:8G
System：Kali Linux 2018.4 （Native，非虚拟机）

客户端：

>client：Nexus 6 shamu CPU：Snapdragon 805 Mem：3G
System：lineage-15.1-20181123-NIGHTLY-shamu，android 8.1

用`kali linux`的原因是工具很全面，权限很单一，只有一个`root`，作为原型开发很好用，否则`python`和`node`的各种权限、环境和依赖实在是烦。用`lineage`因为它有便利的`网络ADB调试`，可以省掉一个`usb`数据线连接的过程。（虽然真实的原因是没钱买新设备，`Nexus 6`[官方](https://developers.google.com/android/images)只支持到`7.1.1`，想上`8.1`只有`lineage`一个选择。）记得需要刷进去一个`lineage`的[`su`包](https://download.lineageos.org/extras)，获取`root`权限，`frida`是需要在`root`权限下运行的。

首先到[官网](https://developer.android.com/studio/releases/platform-tools)下载一个`platform-tools`的linux版本——`SDK Platform-Tools for Linux`，下载解压之后可以直接运行里面的二进制文件，当然也可以把路径加到环境里去。这样`adb`和`fastboot`命令就有了。

然后再将`frida-server`[下载](https://github.com/frida/frida/releases)下来，拷贝到安卓机器里去，使用`root`用户跑起来，保持`adb`的连接不要断开。

```
$ ./adb root # might be required
$ ./adb push frida-server /data/local/tmp/
$ ./adb shell "chmod 755 /data/local/tmp/frida-server"
$ ./adb shell "/data/local/tmp/frida-server &"
```

最后在`kali linux`里安装好`frida`即可，在`kali`里安装`frida`真是太简单了，一句话命令即可，保证不出错。（可能会需要先安装`pip`，也是一句话命令：`curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py`）

```
pip install frida-tools
```

然后用`frida-ps -U`命令连上去，就可以看到正在运行的进程了。

```js
root@kali:~# frida-ps -U
Waiting for USB device to appear...
 PID  Name
----  -----------------------------------------------
 431  ATFWD-daemon
3148  adbd
 391  adspd
2448  android.ext.services
 358  android.hardware.cas@1.0-service
 265  android.hardware.configstore@1.0-service
 359  android.hardware.drm@1.0-service
 360  android.hardware.dumpstate@1.0-service.shamu
 361  android.hardware.gnss@1.0-service
 266  android.hardware.graphics.allocator@2.0-service
 357  android.hidl.allocator@1.0-service
 ...
 ...
 ```

## 基本能力Ⅰ：hook参数、修改结果

先自己写个`app`：

```java
package com.roysue.demo02;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        while (true){

            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }

            fun(50,30);
        }
    }

    void fun(int x , int y ){
        Log.d("Sum" , String.valueOf(x+y));
    }

}
 ```

原理上很简单，就是间隔一秒在控制台输出一下`fun(50,30)`函数的结果，`fun()`这个函数的作用是求和。那最终结果在控制台如下所示。

```
$ adb logcat |grep Sum
11-26 21:26:23.234  3245  3245 D Sum     : 80
11-26 21:26:24.234  3245  3245 D Sum     : 80
11-26 21:26:25.235  3245  3245 D Sum     : 80
11-26 21:26:26.235  3245  3245 D Sum     : 80
11-26 21:26:27.236  3245  3245 D Sum     : 80
11-26 21:26:28.237  3245  3245 D Sum     : 80
11-26 21:26:29.237  3245  3245 D Sum     : 80
```

现在我们来写一段`js`代码，并用`frida-server`将这段代码加载到`com.roysue.demo02`中去，执行其中的`hook`函数。

```
$ nano s1.js
```

```js
console.log("Script loaded successfully ");
Java.perform(function x() {
    console.log("Inside java perform function");
    //定位类
    var my_class = Java.use("com.roysue.demo02.MainActivity");
    console.log("Java.Use.Successfully!");//定位类成功！
    //在这里更改类的方法的实现（implementation）
    my_class.fun.implementation = function(x,y){
        //打印替换前的参数
        console.log( "original call: fun("+ x + ", " + y + ")");
        //把参数替换成2和5，依旧调用原函数
        var ret_value = this.fun(2, 5);
        return ret_value;
    }
});
```

然后我们在`kali`主机上使用一段`python`脚本，将这段`js`脚本“传递”给安卓系统里正在运行的`frida-server`。

```
$ nano loader.py
```

```py
import time
import frida

# 连接安卓机上的frida-server
device = frida.get_usb_device()
# 启动`demo02`这个app
pid = device.spawn(["com.roysue.demo02"])
device.resume(pid)
time.sleep(1)
session = device.attach(pid)
# 加载s1.js脚本
with open("s1.js") as f:
    script = session.create_script(f.read())
script.load()

# 脚本会持续运行等待输入
raw_input()
```

然后得保证`frida-server`正在运行，方法可以是在`kali`主机输入`frida-ps -U`命令，如果安卓机上的进程出现了，则`frida-server`运行良好。

还需要保证`selinux`是关闭的状态，可以在`adb shell`里，`su -`获得`root`权限之后，输入`setenforce 0`命令来获得，在`Settings→About Phone→SELinux status`里看到`Permissive`，说明`selinux`关闭成功。

然后在`kali`主机上输入`python loader.js`，可以观察到安卓机上`com.roysue.demo02`这个`app`马上重启了。然后`$ adb logcat|grep Sum`里的内容也变了。

```
11-26 21:44:47.875  2420  2420 D Sum     : 80
11-26 21:44:48.375  2420  2420 D Sum     : 80
11-26 21:44:48.875  2420  2420 D Sum     : 80
11-26 21:44:49.375  2420  2420 D Sum     : 80
11-26 21:44:49.878  2420  2420 D Sum     : 7
11-26 21:44:50.390  2420  2420 D Sum     : 7
11-26 21:44:50.904  2420  2420 D Sum     : 7
11-26 21:44:51.408  2420  2420 D Sum     : 7
11-26 21:44:51.921  2420  2420 D Sum     : 7
11-26 21:44:52.435  2420  2420 D Sum     : 7
11-26 21:44:52.945  2420  2420 D Sum     : 7
11-26 21:44:53.459  2420  2420 D Sum     : 7
11-26 21:44:53.970  2420  2420 D Sum     : 7
11-26 21:44:54.480  2420  2420 D Sum     : 7
```

在`kali`主机上可以观察到：

```
$ python loader.py
Script loaded successfully
Inside java perform function
Java.Use.Successfully!
original call: fun(50, 30)
original call: fun(50, 30)
original call: fun(50, 30)
original call: fun(50, 30)
original call: fun(50, 30)
original call: fun(50, 30)
original call: fun(50, 30)
original call: fun(50, 30)
original call: fun(50, 30)
```

说明脚本执行成功了，代码也插到`com.roysue.demo02`这个包里去，并且成功执行了，`s1.js`里的代码成功执行了，并且把交互结果传回了`kali`主机上。

## 基本能力Ⅱ：参数构造、方法重载、隐藏函数的处理

我们现在把`app`的代码稍微写复杂一点点：

```java
package com.roysue.demo02;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;

public class MainActivity extends AppCompatActivity {

    private String total = "@@@###@@@";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        while (true){

            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }

            fun(50,30);
            Log.d("ROYSUE.string" , fun("LoWeRcAsE Me!!!!!!!!!"));
        }
    }

    void fun(int x , int y ){
        Log.d("ROYSUE.Sum" , String.valueOf(x+y));
    }

    String fun(String x){
        total +=x;
        return x.toLowerCase();
    }

    String secret(){
        return total;
    }
}
```

`app`运行起来后在使用`logcat`打印出来的日志如下：

```
$ adb logcat |grep ROYSUE
11-26 22:22:35.689  3051  3051 D ROYSUE.Sum: 80
11-26 22:22:35.689  3051  3051 D ROYSUE.string: lowercase me!!!!!!!!!
11-26 22:22:36.695  3051  3051 D ROYSUE.Sum: 80
11-26 22:22:36.696  3051  3051 D ROYSUE.string: lowercase me!!!!!!!!!
11-26 22:22:37.696  3051  3051 D ROYSUE.Sum: 80
11-26 22:22:37.696  3051  3051 D ROYSUE.string: lowercase me!!!!!!!!!
11-26 22:22:38.697  3051  3051 D ROYSUE.Sum: 80
11-26 22:22:38.697  3051  3051 D ROYSUE.string: lowercase me!!!!!!!!!
11-26 22:22:39.697  3051  3051 D ROYSUE.Sum: 80
11-26 22:22:39.698  3051  3051 D ROYSUE.string: lowercase me!!!!!!!!!
```

可以看到`fun()`方法有了重载，在参数是两个`int`的情况下，返回两个`int`之和。在参数为`String`类型之下，则返回字符串的小写形式。

另外，`secret()`函数为隐藏方法，在`app`里没有被直接调用。

这时候如果我们直接使用上一节里面的`js`脚本和`loader.js`来加载的话，肯定会崩溃。为了看到崩溃的信息，我们对`loader.js`做一些处理。

```py
def my_message_handler(message , payload): #定义错误处理
	print message
	print payload
...
script.on("message" , my_message_handler) #调用错误处理
script.load()
```

再运行`$ python loader.py`的话，就会看到如下的错误信息返回：

```
$ python loader.py
Script loaded successfully
Inside java perform function
Java.Use.Successfully!
{u'columnNumber': 1, u'description': u"Error: fun(): has more than one overload, use .overload(<signature>) to choose from:\n\t.overload('java.lang.String')\n\t.overload('int', 'int')", u'fileName': u'frida/node_modules/frida-java/lib/class-factory.js', u'lineNumber': 2233, u'type': u'error', u'stack': u"Error: fun(): has more than one overload, use .overload(<signature>) to choose from:\n\t.overload('java.lang.String')\n\t.overload('int', 'int')\n    at throwOverloadError (frida/node_modules/frida-java/lib/class-factory.js:2233)\n    at frida/node_modules/frida-java/lib/class-factory.js:1468\n    at x (/script1.js:14)\n    at frida/node_modules/frida-java/lib/vm.js:43\n    at M (frida/node_modules/frida-java/index.js:347)\n    at frida/node_modules/frida-java/index.js:299\n    at frida/node_modules/frida-java/lib/vm.js:43\n    at frida/node_modules/frida-java/index.js:279\n    at /script1.js:15"}
None
```

可以看出是一个`throwOverloadError`，这时候就是因为我们没有处理重载，造成的重载处理错误。这个时候就需要我们来处理重载了，在`js`脚本中处理重载是这样写的：

```js
my_class.fun.overload("int" , "int").implementation = function(x,y){
...
my_class.fun.overload("java.lang.String").implementation = function(x){
```

其中参数均为两个`int`的情况下，上一节已经讲过了。参数为`String`类的时候，由于`String`类不是Java基本数据类型，而是`java.lang.String`类型，所以在替换参数的构造上，需要花点心思。

```js
var string_class = Java.use("java.lang.String"); //获取String类型

my_class.fun.overload("java.lang.String").implementation = function(x){
  console.log("*************************************");
  var my_string = string_class.$new("My TeSt String#####"); //new一个新字符串
  console.log("Original arg: " +x );
  var ret =  this.fun(my_string); // 用新的参数替换旧的参数，然后调用原函数获取结果
  console.log("Return value: "+ret);
  console.log("*************************************");
  return ret;
};
```

这样我们对于重载函数的处理就算是ok了。我们到实验里来看下：

```
$ python loader.py
Script loaded successfully
Inside java perform function
original call: fun(50, 30)
*************************************
Original arg: LoWeRcAsE Me!!!!!!!!!
Return value: my test string#####
*************************************
original call: fun(50, 30)
*************************************
Original arg: LoWeRcAsE Me!!!!!!!!!
Return value: my test string#####
*************************************
original call: fun(50, 30)
*************************************
Original arg: LoWeRcAsE Me!!!!!!!!!
Return value: my test string#####
*************************************
```

然后`logcat`打出来的结果也变了。

```
$ adb logcat |grep ROYSUE
11-26 22:23:29.597  3244  3244 D ROYSUE.Sum: 7
11-26 22:23:29.673  3244  3244 D ROYSUE.string: my test string#####
11-26 22:23:30.689  3244  3244 D ROYSUE.Sum: 7
11-26 22:23:30.730  3244  3244 D ROYSUE.string: my test string#####
11-26 22:23:31.740  3244  3244 D ROYSUE.Sum: 7
11-26 22:23:31.789  3244  3244 D ROYSUE.string: my test string#####
11-26 22:23:32.797  3244  3244 D ROYSUE.Sum: 7
11-26 22:23:32.833  3244  3244 D ROYSUE.string: my test string#####
```

最后再说一下隐藏方法的调用，`frida`对其的处理办法跟`Xposed`是非常像的，`Xposed`使用的是`XposedHelpers.findClass("com.example.inner_class_demo.demo",lpparam.classLoader);`方法，直接`findClass`，其实`frida`也非常类似，也是使用的直接到内存里去寻找的方法，也就是`Java.choose(className, callbacks)`函数，通过类名触发回掉函数。

```js
Java.choose("com.roysue.demo02.MainActivity" , {
  onMatch : function(instance){ //该类有多少个实例，该回调就会被触发多少次
    console.log("Found instance: "+instance);
    console.log("Result of secret func: " + instance.secret());
  },
  onComplete:function(){}
});
```

最终运行效果如下：

```
$ python loader.py
Script loaded successfully
Inside java perform function
Found instance: com.roysue.demo02.MainActivity@92d5deb
Result of secret func: @@@###@@@
original call: fun(50, 30)
*************************************
Original arg: LoWeRcAsE Me!!!!!!!!!
Return value: my test string#####
*************************************
original call: fun(50, 30)
*************************************
Original arg: LoWeRcAsE Me!!!!!!!!!
Return value: my test string#####
*************************************
original call: fun(50, 30)
```

这样隐藏方法也被调用起来了。


## 中级能力：远程调用

上一小节中我们在安卓机器上使用`js`脚本调用了隐藏函数`secret()`，它在`app`内虽然没有被任何地方调用，但是仍然被我们的脚本“找到”并且“调用”了起来

这一小节我们要实现的是，不仅要在跑在安卓机上的`js`脚本里调用这个函数，还要可以在`kali`主机上的`py`脚本里，直接调用这个函数。

也就是使用`frida`提供的`RPC`功能（Remote Procedure Call）。

安卓`app`不需要有任何修改，这次我们要修改的是`js`脚本和`py`脚本。

```
$ nano s3.js
```

```js
console.log("Script loaded successfully ");

function callSecretFun() { //定义导出函数
    Java.perform(function () { //找到隐藏函数并且调用
        Java.choose("com.roysue.demo02.MainActivity", {
            onMatch: function (instance) {
                console.log("Found instance: " + instance);
                console.log("Result of secret func: " + instance.secret());
            },
            onComplete: function () { }
        });
    });
}
rpc.exports = {
    callsecretfunction: callSecretFun //把callSecretFun函数导出为callsecretfunction符号，导出名不可以有大写字母或者下划线
};
```

然后我们可以在`kali`主机的`py`脚本里直接调用该函数：

```
$ nano loader3.py
```

```py
import time
import frida

def my_message_handler(message, payload):
    print message
    print payload

device = frida.get_usb_device()
pid = device.spawn(["com.roysue.demo02"])
device.resume(pid)
time.sleep(1)
session = device.attach(pid)
with open("s3.js") as f:
    script = session.create_script(f.read())
script.on("message", my_message_handler)
script.load()

command = ""
while 1 == 1:
    command = raw_input("Enter command:\n1: Exit\n2: Call secret function\nchoice:")
    if command == "1":
        break
    elif command == "2": #在这里调用
        script.exports.callsecretfunction()
```

然后在`kali`主机上我们就可以看到以下的输出：

```
$ python loader3.py
Script loaded successfully
Enter command:
1: Exit
2: Call secret function
choice:2
Found instance: com.roysue.demo02.MainActivity@2eacd80
Result of secret func: @@@###@@@LoWeRcAsE Me!!!!!!!!!LoWeRcAsE Me!!!!!!!!!LoWeRcAsE Me!!!!!!!!!LoWeRcAsE Me!!!!!!!!!
Enter command:
1: Exit
2: Call secret function
choice:2
Found instance: com.roysue.demo02.MainActivity@2eacd80
Result of secret func: @@@###@@@LoWeRcAsE Me!!!!!!!!!LoWeRcAsE Me!!!!!!!!!LoWeRcAsE Me!!!!!!!!!LoWeRcAsE Me!!!!!!!!!LoWeRcAsE Me!!!!!!!!!LoWeRcAsE Me!!!!!!!!!LoWeRcAsE Me!!!!!!!!!
Enter command:
1: Exit
2: Call secret function
choice:2
Found instance: com.roysue.demo02.MainActivity@2eacd80
Result of secret func: @@@###@@@LoWeRcAsE Me!!!!!!!!!LoWeRcAsE Me!!!!!!!!!LoWeRcAsE Me!!!!!!!!!LoWeRcAsE Me!!!!!!!!!LoWeRcAsE Me!!!!!!!!!LoWeRcAsE Me!!!!!!!!!LoWeRcAsE Me!!!!!!!!!LoWeRcAsE Me!!!!!!!!!LoWeRcAsE Me!!!!!!!!!
Enter command:
1: Exit
2: Call secret function
choice:1
```

这样我们就实现了在`kali`主机上直接调用安卓`app`内部的函数的能力。

## 高级能力：互联互通、动态修改

最后我们要实现的功能是，我们不仅仅可以在`kali`主机上调用安卓`app`里的函数。我们还可以把数据从安卓`app`里传递到`kali`主机上，在主机上进行修改，再传递回安卓`app`里面去。

我们编写这样一个`app`，其中最核心的地方在于判断用户是否为`admin`，如果是，则直接返回错误，禁止登陆。如果不是，则把用户和密码上传到服务器上进行验证。

```java
package com.roysue.demo04;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Base64;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {

    EditText username_et;
    EditText password_et;
    TextView message_tv;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);


        password_et = (EditText) this.findViewById(R.id.editText2);
        username_et = (EditText) this.findViewById(R.id.editText);
        message_tv = ((TextView) findViewById(R.id.textView));

        this.findViewById(R.id.button).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                if (username_et.getText().toString().compareTo("admin") == 0) {
                    message_tv.setText("You cannot login as admin");
                    return;
                }
                //hook target
                message_tv.setText("Sending to the server :" + Base64.encodeToString((username_et.getText().toString() + ":" + password_et.getText().toString()).getBytes(), Base64.DEFAULT));

            }
        });

    }
}
```

最终跑起来之后，效果就是这样。

![](pic/02.png)

我们的目标就是在`kali`主机上“得到”输入框输入的内容，并且修改其输入的内容，并且“传输”给安卓机器，使其通过验证。也就是说，我们哪怕输入`admin`的账户和密码，也可以绕过本地校验，进行登陆的操作。

所以最终安卓端的`js`代码的逻辑就是，截取输入，传输给`kali`主机，暂停执行，得到`kali`主机传回的数据之后，继续执行。形成代码如下：

```js
Java.perform(function () {
    var tv_class = Java.use("android.widget.TextView");
    tv_class.setText.overload("java.lang.CharSequence").implementation = function (x) {
        var string_to_send = x.toString();
        var string_to_recv;
        send(string_to_send); // 将数据发送给kali主机的python代码
        recv(function (received_json_object) {
            string_to_recv = received_json_object.my_data
            console.log("string_to_recv: " + string_to_recv);
        }).wait(); //收到数据之后，再执行下去
        return this.setText(string_to_recv);
    }
});
```

`kali`主机端的流程就是，将接受到的`JSON`数据解析，提取出其中的密码部分，然后将用户名替换成`admin`，这样就实现了将`admin`和`pw`发送给“服务器”的结果。

```py
import time
import frida

def my_message_handler(message, payload):
    print message
    print payload
    if message["type"] == "send":
        print message["payload"]
        data = message["payload"].split(":")[1].strip()
        print 'message:', message
        data = data.decode("base64")
        user, pw = data.split(":")
        data = ("admin" + ":" + pw).encode("base64")
        print "encoded data:", data
        script.post({"my_data": data})  # 将JSON对象发送回去
        print "Modified data sent"

device = frida.get_usb_device()
pid = device.spawn(["com.roysue.demo04"])
device.resume(pid)
time.sleep(1)
session = device.attach(pid)
with open("s4.js") as f:
    script = session.create_script(f.read())
script.on("message", my_message_handler)  # 注册消息处理函数
script.load()
raw_input()
```

我们只要输入任意用户名(非admin)+密码，非admin的用户名可以绕过`compareTo`校验，然后`frida`会帮助我们将用户名改成`admin`，最终就是`admin:pw`的组合发送到服务器。

```
$ python loader4.py
Script loaded successfully
{u'type': u'send', u'payload': u'Sending to the server :YWFhYTpiYmJi\n'}
None
Sending to the server :YWFhYTpiYmJi

message: {u'type': u'send', u'payload': u'Sending to the server :YWFhYTpiYmJi\n'}
data: aaaa:bbbb
pw: bbbb
encoded data: YWRtaW46YmJiYg==

Modified data sent
string_to_recv: YWRtaW46YmJiYg==
```

动态修改输入内容就这样实现了。

## 打算做个成套的教程、目录已经想好了

frida『葵花宝典』

第一章.各种环境安装（包括Win、Mac、Ubuntu、ARM机器下的各种环境安装）
第二章.基本案例上手（安卓、iOS、Win、Mac为对象的各种插桩方法）
第三章.frida-tools（frida原生提供的各种工具的使用）
第四章.frida-scripts（各种frida脚本的介绍、使用和总结）
第五章.frida高级应用（安卓hook参数模型的总结、SSL-unpinning模型、iOS应用重打包动态修改等等）
第六章.二次开发基础（frida-API基本使用方法、基于frida的二次开发模型）
第七章.二次开发案例（Fridump、r2frida、brida、Appmon等源码解析和解读）

当然还在酝酿中，大家有想法可以跟我沟通，想要源码的也可以加我。微信&微博：r0ysue

谢谢大家。

参考资料：

- [frida](https://www.frida.re/)
- [dweinstein/awesome-frida](https://github.com/dweinstein/awesome-frida)
- [nluug-2015-frida-putting-the-open-back-into-closed-software](http://slides.com/oleavr/nluug-2015-frida-putting-the-open-back-into-closed-software#/)
- [Frida hooking android](https://11x256.github.io/Frida-hooking-android-part-1/)
- [brida](https://github.com/federicodotta/Brida)
