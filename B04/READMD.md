
<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [FRIDA脚本系列（四）更新篇：几个主要机制的大更新](#frida脚本系列四更新篇几个主要机制的大更新)
  - [进程创建机制大更新](#进程创建机制大更新)
    - [存在的问题：无法为新进程准备参数和环境](#存在的问题无法为新进程准备参数和环境)
    - [问题产生的原因(一)：当初源码中就没有实现](#问题产生的原因一当初源码中就没有实现)
    - [问题产生的原因(二)：`spawn()`的历史遗留问题](#问题产生的原因二spawn的历史遗留问题)
    - [进程创建机制更新(一)：参数、目录、环境均可设置](#进程创建机制更新一参数-目录-环境均可设置)
    - [进程创建机制更新(二)：利用`aux`机制实现平台特定功能](#进程创建机制更新二利用aux机制实现平台特定功能)
  - [子进程插装机制大更新](#子进程插装机制大更新)
    - [存在的问题：子进程多线程机制混乱容易崩](#存在的问题子进程多线程机制混乱容易崩)
    - [解决的方法：引入新的子进程控制`API`：`Child gating`](#解决的方法引入新的子进程控制apichild-gating)
  - [退出(崩溃)消息机制大更新](#退出崩溃消息机制大更新)
    - [存在的问题：程序崩溃时消息来不及发出](#存在的问题程序崩溃时消息来不及发出)
    - [解决的方法：对各大平台的停止进程`API`进行插装](#解决的方法对各大平台的停止进程api进行插装)

<!-- /code_chunk_output -->

## FRIDA脚本系列（四）更新篇：几个主要机制的大更新

最近沉迷学习，无法自拔，还是有一些问题百思不得骑姐，把官网文档又翻了一遍，发现其实最近的几个主要版本，更新还是挺大的，遂花了点时间和功夫，消化吸收下，在这里跟大家分享。

### 进程创建机制大更新

#### 存在的问题：无法为新进程准备参数和环境

当我们使用`Frida Python`的`binding`的时候，一般会这么写：

```
pid = device.spawn(["/bin/cat", "/etc/passwd"])
```

或者在iOS平台上，会这样写：

```
pid = device.spawn(["com.apple.mobilesafari"])
```

目前来看貌似用这个`API`只能这么写，这么写其实是存在很多问题的，比如说没有考虑完整参数列表的问题，或者说新进程的环境是继承自绑定的`host`机环境还是设备`client`环境？再比如想要实现定制功能，比如以关闭`ASLR`模式打开`safari`，这些都没有考虑进去。

#### 问题产生的原因(一)：当初源码中就没有实现

我们先来看看这个`API`在`frida-core`里是如何实现的：

```vala
namespace Frida {
	…
	public class Device : GLib.Object {
		…
		public async uint spawn (string path,
			string[] argv, string[] envp)
			throws Frida.Error;
		public uint spawn_sync (string path,
			string[] argv, string[] envp)
			throws Frida.Error;
	}
	…
}
```

这段代码是用`vala`语言写的，`frida-core`都是用`vala`写的，`vala`看起来跟`C#`很像，并且最终会被编译成`C`代码。从代码可以看出，第一个方法——`spawan`是异步的，调用者调用一遍就可以去干其他事情了，不用等待调用完成，而第二个方法——`spawn_sync`则需要等到调用完全结束并返回。

这两个方法会被编译成如下的C代码：

```c
void frida_device_spawn (FridaDevice * self,
    const gchar * path,
    gchar ** argv, int argv_length,
    gchar ** envp, int envp_length,
    GAsyncReadyCallback callback, gpointer user_data);
guint frida_device_spawn_finish (FridaDevice * self,
    GAsyncResult * result, GError ** error);
guint frida_device_spawn_sync (FridaDevice * self,
    const gchar * path,
    gchar ** argv, int argv_length,
    gchar ** envp, int envp_length,
    GError ** error);
```

前两个函数组成了`spawn()`的过程，首先调用第一个获得一个回调，当获得回调之后就会调用第二个函数——`spawn_finish()`，将回调的返回值将会作为`GAsyncResult`的参数。最终的返回值就是`PID`，当然如果有`error`的话就会返回`error no`。

第三个函数——`spawn_sync()`上面也解释了，是完全同步的，`Frida Python`用的其实就是这个。`Frida nodejs`用的其实是前两个，因为`nodejs`里的绑定默认就是异步的。当然以后其实应该也考虑将`Frida Python`的绑定迁移到异步的模式中来，利用`Python 3.5`版本引入的`async/await`机制。

回到上一小节那两个例子，可以发现其实调用的格式跟我们写的`API`并不完全一致，仔细看源码就会发现，像`envp`字符串列表并没有暴露给上层`API`，如果查看`Frida Python`的绑定过程的话，就可以发现其实后来在绑定里是这样写的：

```
envp = g_get_environ ();
envp_length = g_strv_length (envp);
```

也就是说最终我们传递给`spawn()`函数的是调用者的`Python`环境，这明显是不对的，`host`的`Python`环境跟`client`的`Python`肯定是不一样的，比如像`client`是`iOS`或`Android`的情况。

当然我们在`frida-server`里做了设定，在`spawn()`安卓或者`iOS`的进程的时候，`envp`会被默认忽略掉，这或多或少减少了问题的产生。

#### 问题产生的原因(二)：`spawn()`的历史遗留问题

还有一个问题就是`spawn()`这个古老的`API`的定义——`string[] envp`，这个定义意味着不能为空（如果写成`string[]? envp`的话其实就可以为空了），也就是说其实无法从根本上区别“用默认的环境配置”和“不使用任何环境配置”。

#### 进程创建机制更新(一)：参数、目录、环境均可设置

既然决定要修这个`API`，那就干脆顺便把跟这个`API`相关的问题都来看下：

- 如何给命令提供一些额外的环境参数
- 设置工作目录
- 自定义标准输入流
- 传入平台特定的参数

修正完以上`bug`之后，最终代码会变成下面这样：

```vala
namespace Frida {
	…
	public class Device : GLib.Object {
		…
		public async uint spawn (string program,
			Frida.SpawnOptions? options = null)
			throws Frida.Error;
		public uint spawn_sync (string program,
			Frida.SpawnOptions? options = null)
			throws Frida.Error;
	}
	…
	public class SpawnOptions : GLib.Object {
		public string[]? argv { get; set; }
		public string[]? envp { get; set; }
		public string[]? env { get; set; }
		public string? cwd { get; set; }
		public Frida.Stdio stdio { get; set; }
		public GLib.VariantDict aux { get; }

		public SpawnOptions ();
	}
	…
}
```

最后，我们回到开头的那段示例代码，本来我们是这么写的：

```py
device.spawn(["com.apple.mobilesafari"])
```

现在得这样写了：

```py
device.spawn("com.apple.mobilesafari")
```

第一个参数是要被`spawn`的命令，后面可以加上`argv`的字符串列表，`argv`就会被用来设定参数的命令，比如：

```py
device.spawn("/bin/busybox", argv=["/bin/cat", "/etc/passwd"])
```

如果想要将默认环境替换成自己的设定的话：

```py
device.spawn("/bin/ls", envp={ "CLICOLOR": "1" })
```

只更改环境变量里的一个参数：

```py
device.spawn("/bin/ls", env={ "CLICOLOR": "1" })
```

更改命令的工作目录：

```py
device.spawn("/bin/ls", cwd="/etc")
```

重定向标准输入流：

```py
device.spawn("/bin/ls", stdio="pipe")
```

>`stdin`默认的输入是`inherit`，加上`stdio="pipe"`这个选项之后，就变成管道了。

#### 进程创建机制更新(二)：利用`aux`机制实现平台特定功能

到这里我们几乎覆盖了`spawn()`的所有选项，还剩下最后一个选项——`aux`，该选项的本质是平台特定参数的一个字典。可以用`Python`绑定来设置这个参数，任何无法被前面参数捕获的键值对，都会直接放在命令行的最后面。

比如，打开`Safari`并且通知它去打开特定的`URL`：

```py
device.spawn("com.apple.mobilesafari", url="https://bbs.pediy.com")
```

再比如以关闭`ASLR`的模式执行一个命令：

```py
device.spawn("/bin/ls", aslr="disable")
```

再比如用特定的`Activity`来打开一个安卓的`App`：

```py
spawn("com.android.settings", activity=".SecuritySettings")
```

`aux`机制让命令行可以轻松定制，这可比为每个平台单独写代码方便多了。事实上，底层代码一行都没变 ^.<

最后来看下这个`API`修改完成之后的效果，逗号后面的第二个参数就是带属性的对象，后面无法被是别的参数则全部进`aux`字典。

```js
const pid = await device.spawn('/bin/sh', {
  argv: ['/bin/sh', '-c', 'ls /'],
  env: {
    'BADGER': 'badger-badger-badger',
    'SNAKE': true,
    'MUSHROOM': 42,
  },
  cwd: '/usr',
  stdio: 'pipe',
  aslr: 'auto'
});
```

当然，修改完成之后，子进程的路径、参数和环境都可以置空了，这个置空已经可以区分“用默认的环境配置”和“不使用任何环境配置”了。

### 子进程插装机制大更新

#### 存在的问题：子进程多线程机制混乱容易崩

首先来回顾一下，传统的`fork()`函数本来的操作是这样婶儿的，它会克隆完整的父进程空间给子进程，这个过程通常开销不大，因为有着`copy-on-write`机制，然后将子进程的进程`ID`返回给父进程，将`0`返回给子进程。

而当涉及到多线程的时候，情况就会变得复杂起来，只有调用`fork()`函数的线程，可以“存活”到子进程里面，而如果其他线程碰巧有线程锁，这些锁在子进程里将永远不会被解开。

所以说`App`如果要同时进行多线程和`fork`操作的话，必须得非常谨慎，当然大多数`App`都在`fork`进程时都是使用的单线程设计，可是在注入我们的`frida-gum`之后，该进程就变成了多线程，所以程序经常会崩溃或失去响应。还有一种情况就是拥有共享属性的文件描述符，处理的时候也需要非常非常谨慎。

在这个版本中作者花了大力气，最终解决了这个问题。作者非常鸡冻的宣布，现在`FRIDA`可以检测到即将运行`fork()`函数，临时暂停`FRIDA`的线程，暂停通讯通道，并随着`fork()`的过程一起备份，备份完成之后恢复运行。也就是说在子进程开始运行之前，我们就把想要实施的插装操作应用到子进程上了。

当然不仅仅是`fork()`，还有`execve(), posix_spawn(), CreateProcess()`等系列子进程操作函数，这么说吧，只要是对进程实施的操作，不管是像`execve()`一样替换自身进程的，还是像`posix_spawn()`一样另起一个进程的，都会像`fork()`函数一样，由`FRIDA`先实施好插桩之后，再开始运行。

#### 解决的方法：引入新的子进程控制`API`：`Child gating`

前两个问题主要就是由这个新引入的“子进程控制”的`API`来解决的，我们为拥有`create_script()`方法的`Session`对象全新加入了`enable_child_gating()`和`disable_child_gating()`这两个方法，在不显示调用新`API`的情况下，`Frida`的机制还是会跟从前一样，我们需要手动调用`enable_child_gating()`方法来切换到子进程控制的模式。

进入子进程控制模式之后，所有的子进程都会先暂停，等我们一顿操作完成之后，再对子进程的`PID`调用`resume()`来恢复子进程的运行。`Device`对象有一个叫做`delivered`的信号，我们可以在这个信号上装一个回调`callback`，这样有新的进程被产生出来的时候就会得到通知，得到通知之后立刻对新进程进行插桩等操作即可，然后调用`resume()`函数就可以恢复新进程的运行。`Device`对象还有一个新的`enumerate_pending_children()`的方法，用来列出即将产生的子进程列表，所有即将产生的子进程都会在这个表里，直到用户运行`resume()`函数恢复其运行，或者直接被**kill**掉。

理论讲完了，接下来实际操作一遍。下面是`host`端的`py`代码：

```py
from __future__ import print_function
import frida
from frida.application import Reactor
import threading

class Application(object):
    def __init__(self):
        self._stop_requested = threading.Event()
        self._reactor = Reactor(run_until_return=lambda reactor: self._stop_requested.wait())

        self._device = frida.get_local_device()
        self._sessions = set()

        self._device.on("delivered", lambda child: self._reactor.schedule(lambda: self._on_delivered(child)))

    def run(self):
        self._reactor.schedule(lambda: self._start())
        self._reactor.run()

    def _start(self):
        argv = ["/bin/sh", "-c", "cat /etc/hosts"]
        print("✔ spawn(argv={})".format(argv))
        pid = self._device.spawn(argv)
        self._instrument(pid)

    def _stop_if_idle(self):
        if len(self._sessions) == 0:
            self._stop_requested.set()

    def _instrument(self, pid):
        print("✔ attach(pid={})".format(pid))
        session = self._device.attach(pid)
        session.on("detached", lambda reason: self._reactor.schedule(lambda: self._on_detached(pid, session, reason)))
        print("✔ enable_child_gating()")
        session.enable_child_gating()
        print("✔ create_script()")
        script = session.create_script("""'use strict';

Interceptor.attach(Module.findExportByName(null, 'open'), {
  onEnter: function (args) {
    send({
      type: 'open',
      path: Memory.readUtf8String(args[0])
    });
  }
});
""")
        script.on("message", lambda message, data: self._reactor.schedule(lambda: self._on_message(pid, message)))
        print("✔ load()")
        script.load()
        print("✔ resume(pid={})".format(pid))
        self._device.resume(pid)
        self._sessions.add(session)

    def _on_delivered(self, child):
        print("⚡ delivered: {}".format(child))
        self._instrument(child.pid)

    def _on_detached(self, pid, session, reason):
        print("⚡ detached: pid={}, reason='{}'".format(pid, reason))
        self._sessions.remove(session)
        self._reactor.schedule(self._stop_if_idle, delay=0.5)

    def _on_message(self, pid, message):
        print("⚡ message: pid={}, payload={}".format(pid, message["payload"]))


app = Application()
app.run()

```

然后来运行这段代码：

```sh
$ python3 example.py
✔ spawn(argv=['/bin/sh', '-c', 'cat /etc/hosts'])
✔ attach(pid=42401)
✔ enable_child_gating()
✔ create_script()
✔ load()
✔ resume(pid=42401)
⚡ message: pid=42401,
↪payload={'type': 'open', 'path': '/dev/tty'}
⚡ detached: pid=42401, reason='process-replaced'
⚡ delivered: Child(pid=42401, parent_pid=42401,
↪path="/bin/cat", argv=['cat', '/etc/hosts'],
↪envp=['SHELL=/bin/bash', 'TERM=xterm-256color', …],
↪origin=exec)
✔ attach(pid=42401)
✔ enable_child_gating()
✔ create_script()
✔ load()
✔ resume(pid=42401)
⚡ message: pid=42401,
↪payload={'type': 'open', 'path': '/etc/hosts'}
⚡ detached: pid=42401, reason='process-terminated'
$
```

我们重构了子进程的`hook`机制，也顺便重构了`Android App`的启动机制，移除了之前的`frida-loader-{32,64}.so`，全新的`Zygote`插桩机制会在后台承担所有的子进程控制工作，这也意味着可以对`Zygote`进行任意的插桩工作，当然得记好要调用`enable_child_gating()`来开启这这个功能，对于不需要进行插桩的子进程立即使用`resume()`来恢复其运行。

### 退出(崩溃)消息机制大更新

#### 存在的问题：程序崩溃时消息来不及发出

另外一个一直以来存在的问题就是，当进程快要意外崩溃的时候，进程传给`FRIDA`的`send()`的`API`的数据，可能会来不及发出去，虽然民间也有一种解决的办法就是可以`hook`一些`exit()`或`abort()`函数，然后在`hook`的语句里进行`send()`和`recv().wait()`的`client-host`结对操作，虽然不是很优雅，但针对特定平台也是有效的。

#### 解决的方法：对各大平台的停止进程`API`进行插装

针对程序意外崩溃的情况，`Frida`目前已经可以介入各大系统平台常用的停止进程的`API`，为用户做好进程崩溃时的清理工作，包含把数据发送出去。

有些脚本会把想要输出的数据在本地做个持久化然后定期通过`send()`传出去，这种情况下需要在进程即将崩溃的时候显式地将数据传输出去，我们为这种情况定制了一个`RPC`，导出名为`dispose`：

```js
rpc.exports = {
  dispose: function () {
    send(bufferedData);
  }
};
```

几个大的机制的更新先介绍到这里，应该还会有下一篇，介绍一些小的但是刁钻的，或者是理念式的变化，不要小看这些变化，对于代码来讲，every line matters 。