
<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [Frida前置知识:iOS/ObjC语法进阶及其ARM汇编实现](#frida前置知识iosobjc语法进阶及其arm汇编实现)
- [1.ObjC类与方法的底层实现逻辑](#1objc类与方法的底层实现逻辑)
  - [(1)基本概念](#1基本概念)
  - [(2)引用关系](#2引用关系)
- [2.ObjC运行时类的结构与消息传递](#2objc运行时类的结构与消息传递)
  - [(1)运行时类结构:](#1运行时类结构)
  - [(2)ObjC中的消息传递:](#2objc中的消息传递)
    - [①SEL](#1sel)
    - [②IMP](#2imp)
    - [③消息机制](#3消息机制)
- [3.ObjC runtime的"反射"->KVC](#3objc-runtime的反射-kvc)
  - [(1)概念](#1概念)
  - [(2)使用](#2使用)
  - [(3)原理概述](#3原理概述)
- [4.ObjC使用AssociatedObject动态为对象添加属性](#4objc使用associatedobject动态为对象添加属性)
  - [(1)概念](#1概念-1)
  - [(2)简单使用](#2简单使用)
- [5.ObjC使用Method Swizzling 进行方法绑定](#5objc使用method-swizzling-进行方法绑定)
  - [(1)概念](#1概念-2)
  - [(2)简单使用](#2简单使用-1)
- [6.ARM架构/指令集/寄存器/编码](#6arm架构指令集寄存器编码)
  - [(1)ARM架构:](#1arm架构)
  - [(2)寄存器:](#2寄存器)
    - [①通用寄存器:](#1通用寄存器)
    - [②特殊寄存器:](#2特殊寄存器)
    - [③处理器状态:](#3处理器状态)
  - [(3)指令集编码:](#3指令集编码)
- [7.ARM64算术/传输/逻辑/地址/移位指令](#7arm64算术传输逻辑地址移位指令)
- [8.栈和方法在ARM64指令集上的实现细节](#8栈和方法在arm64指令集上的实现细节)
  - [(1)栈基础介绍](#1栈基础介绍)
  - [(2).栈相关寄存器](#2栈相关寄存器)
  - [(3).栈帧结构](#3栈帧结构)
- [9.函数调用/参数传递/入栈出栈完整流程](#9函数调用参数传递入栈出栈完整流程)
  - [(1)函数调用逻辑及参数传递](#1函数调用逻辑及参数传递)
  - [(2)OC中的消息机制的汇编代码](#2oc中的消息机制的汇编代码)
- [10.ObjC汇编静态分析与CrackMe动态调试](#10objc汇编静态分析与crackme动态调试)
- [总结](#总结)
- [参考文献](#参考文献)

<!-- /code_chunk_output -->

# Frida前置知识:iOS/ObjC语法进阶及其ARM汇编实现

学习这些语言和汇编的特性，有助于我们后续理解Frida在hook的时候，特定寄存器代表特定的值。比如hook函数的时候，为什么x0代表对象本身，x1代表selector方法名，因为这是由调用约定决定的；再或者我们为什么不用ObjC.implemt去hook，而是Interceptor.attach，因为ObjC其本身就是一个C++的运行时，所以可以采用相同的hook地址的方式。前置的语言学习是学习Frida hook ObjC的理论基础，希望大家可以掌握。

Objective-C语言是一门动态语言，它将很多静态语言在编译和链接时期做的事放到了运行时来处理。这种动态语言的优势在于：我们写代码时能够更具灵活性，如我们可以把消息转发给我们想要的对象，或者随意交换一个方法的实现等。这种特性意味着Objective-C不仅需要一个编译器，还需要一个运行时系统来执行编译的代码。对于Objective-C来说，这个运行时系统就像一个操作系统一样：它让所有的工作可以正常的运行。这个运行时系统即Objc Runtime。Objc Runtime其实是一个Runtime库，它基本上是用C和汇编写的，这个库使得C语言有了面向对象的能力。本篇文章包含以下知识点，大家学完后可以掌握：

>Frida前置知识:iOS/ObjC语法进阶
>- ObjC类与方法的底层实现逻辑
>- ObjC运行时类的结构与消息传递
>- ObjC runtime的"反射"->KVC获取与设置类属性
>- ObjC使用AssociatedObject动态为对象添加属性
>- ObjC使用Method Swizzling 进行方法绑定

>ARM汇编动手实操学习
>- ARM架构/指令集/寄存器/编码
>- ARM64算术/传输/逻辑/地址/移位指令
>- 栈和方法在ARM64指令集上的实现细节
>- 函数调用/参数传递/入栈出栈完整流程
>- ObjC汇编静态分析与CrackMe动态调试


# 1.ObjC类与方法的底层实现逻辑

## (1)基本概念

- 根类:在OC中几乎所有类都继承自NSObject，NSObject类就是根类，根类的父类为nil
- 元类:在我们平时开发中会用到类方法和实例方法，但是在底层的实现中并没有这种区分，实际上都是通过实例方法去查找的，底层为了区分这两种方法，引入元类的概念，然后将实例方法存储在类中，类方法存储在元类中。类的isa指向元类。(所有的类本身就是一个对象)
- 根元类:即为根类NSObject的isa指向的类

## (2)引用关系

![1](/image/1.png)

(3)类的底层实现:

首先写下边的代码然后转为c

```
#import <UIKit/UIKit.h>
@interface MyClass : NSObject

@property NSString *myProperty;

@end
@implementation  MyClass
-(void) myMethod{
    NSLog(@"my method");
}
+(void)myClassMethod{
    NSLog(@"my class method");
}

@end
int main(int argc,char *argv[]){
    @autoreleasepool {
    	[MyClass myClassMethod];
        return 0;
    }
}
```
使用如下命令将其转为C
```
xcrun -sdk iphoneos clang -rewrite-objc -F UIKit -fobjc-arc -arch arm64 ClassAndMethod.m
```

使用VS打开C文件进行分析

搜索我们写的MyClass分别发现其声明及实现

![2](/image/2.png)

![3](/image/3.png)

发现其实现中存在NSObject_IMPL属性，进行搜索

![4](/image/4.png)

可以看到内部其实是一个Class指针，查看其声明发现其是objc_class结构体。

- 第一个属性:isa指针(继承自根类)
- 第二个属性:父类指针

- 第三个属性:用于缓存最近使用的方法。
- 第四个属性:类中实例方法、属性、协议的存储

到这里我们可以看出OC中类结构的基本信息，而objc_class结构体是定义在NSObject.h头文件中它继承自定义在runtime.h头文件中的`_class_t`结构体，下边我们在看一下`_class_t`结构体。

接着我们将代码拉到最后，可以看到定义的类写到了以下section中

![7](/image/7.png)

并在`OBJC_CLASS_SETUP_$_MyClass`方法中对其进行了初始化，这里可以看出，进行初始化时其实是分为元类及类的

![8](/image/8.png)

检索`OBJC_CLASS_$_MyClass`查看其类型发现是`_class_t`结构体

![9](/image/9.png)

结构体定义如下

![10](/image/10.png)

可以看到结构体内属性存在一个`_class_ro_t` 结构体，检索发现其存放及定义内容

![11](/image/11.png)

![12](/image/12.png)

然后分别检索`OBJC_METACLASS_$_MyClass`以及`OBJC_METACLASS_$_MyClass`可以看到以下实现

![14](/image/14.png)

这里的两个RO属性都是readonly只读的在编辑器中确定，继续检索这两个变量查看定义

![15](/image/15.png)

这里已经可以看到方法属性对象方法及类方法的区别，分别保存在元类及类中

继续检索`OBJC_$_INSTANCE_METHODS_MyClass` 及`OBJC_$_CLASS_METHODS_MyClass`看类方法及对象方法

![16](/image/16.png)

可以看到我们自己写的对象方法myMethod及类方法myClassMethod这里可以知道 `_class_t`是类结构，内部包含有方法及属性结构体`_class_ro_t`属性，在实际的实现过程中对一个类分别实现了基于`_class_t`的`OBJC_METACLASS_$_MyClass`以及`OBJC_METACLASS_$_MyClass`分别为类及元类，二者内部又都有基于`_class_ro_t` 结构体的实现`OBJC_$_INSTANCE_METHODS_MyClass` 及`OBJC_$_CLASS_METHODS_MyClass`存放方法及属性。

关于类的继承可总结如下:

isa指向:

- 实例变量的`isa`指向对应的类objc_
- 类的`isa`指向对应的元类
- 元类的`isa`指向根元类
- 根元类的`isa`指向自身

类的继承:

- 类的`superclass`指向父类
- 父类的`superclass`指向根类
- 根类的`superclass`指向`nil`

元类的继承:

- 元类的`superclass`指向对应类的父类的元类
- 父类的元类的`superclass`指向根元类
- 根元类的`superclass`指向根类
- 根类的`superclass`指向`nil`

这里我们的分析过程是Class -->`_class_t`(类结构结构体)-->`_class_ro_t`(类结构内属性方法结构体)-->`_methood_list_t`(类的方法列表)-->`_objc_method`(类内方法对应的结构体，包含名称方法名hash SEL 及方法实际地址IMP)

# 2.ObjC运行时类的结构与消息传递

## (1)运行时类结构:

![48](/image/48.png)

在上边我们已经分析了OC中类的结构，但是其中的class_ro_t却是一个只读结构体，为了实现OC语言的动态性，因此在运行时给类加了一个中间层，下面我们借用AloneMonkey巨佬书的书中的[Demo案例](https://github.com/AloneMonkey/iOSREBook/tree/master/chapter-4/4.3%20%E7%B1%BB%E4%B8%8E%E6%96%B9%E6%B3%95)查看运行时类的结构

![47](/image/47.png)

可以看到类结构中多了一部分名为classReadWrite的结构，这就是增加的可读可写的中间层，原本只读的class_ro_t结构变成了可读可写的class_rw_t的一部分，正是利用这个中间层，实现OC语言的动态性，可以在运行时增加类方法及属性。

---

## (2)ObjC中的消息传递:

首先了解一些基础属性

### ①SEL

SEL又叫选择器，是表示一个方法的`selector`的指针，其定义如下：

![17](/image/17.png)

Objective-C在编译时，会依据每一个方法的名字、参数序列，生成一个唯一的整型标识(`Int`类型的地址)，这个标识就是`SEL`，两个类之间，不管它们是父类与子类的关系，还是之间没有这种关系，只要方法名相同，那么方法的SEL就是一样的。每一个方法都对应着一个`SEL`。所以在Objective-C同一个类(及类的继承体系)中，不能存在2个同名的方法，即使参数类型不同也不行。相同的方法只能对应一个`SEL`。这也就导致Objective-C在处理相同方法名且参数个数相同但类型不同的方法方面的能力很差。

### ②IMP

`IMP`实际上是一个函数指针，指向方法实现的首地址，其定义在Runtime 中如下

![18](/image/18.png)

这个函数使用当前`CPU`架构实现的标准的C调用约定。第一个参数是指向`self`的指针(如果是实例方法，则是类实例的内存地址；如果是类方法，则是指向元类的指针)，第二个参数是方法选择器(`selector`)，接下来是方法的实际参数列表。

通过以上两个变量我们已经明白SEL存放方法名hash过的字符串，而IMP又存放方法的具体地址，当使用Runtime中方法调用方法时又根据self判断其是类方法还是实例方法。那又是如何将二者联系在一起呢？

在代码中检索发现_objc_method 定义内含方法名及地址

![19](/image/19.png)

再结合我们上边查看过的方法列表

![16](/image/16.png)

到这里我们大致了解了方法的存储方式，那实际的方法调用，消息机制是如何实现的呢？

### ③消息机制

直接查看我们编译的代码检索main 函数查看其中方法调用

![20](/image/20.png)

这里可以看到，实际上OC中的方法调用会转化为消息函数objc_msgSend的调用。这个函数将消息接收者和方法名作为其基础参数，如以下所示：

objc_msgSend(receiver, selector, arg1, arg2, ...)

objc_msgSend确定调用方法是进行一个动态查找，具体过程如下:

1.在相应对象的缓存方法列表中查看是否有调用方法(objc_class 的cache,这里可以加快查找速度)

2.如果没找到，在相应对象的方法列表中查找

3.如果还没找到，就在根类指针指向的对象中执行1，2两步

4.如果直到根类中都没有，就进行消息转发，给自己保留处理找不到方法这一状况的机会

以上四步可以归纳为如下图所示

![21](/image/21.png)

当以上方法都查询不到调用方法时进入消息转发机制，消息转发分为三步:动态方法解析，备用接收者，完整转发

5.动态方法解析(其实就是动态换个方法selector)

![24](/image/24.png)

动态添加类有什么好处？当一个类中的方法非常多且有些方法不常用的时候如果直接写了方法,那么这些方法会直接加载到内存,于是内存就很大了,所以我们使用runtime的动态添加方法就不会出现这个问题,只有在运行时才会添加到内存,使用的是class_addMethod方法，具体代码如下:

```
#import <Foundation/Foundation.h>

#import "Person.h"
#import <objc/message.h>

@implementation Person :NSObject
- (void) run {
    NSLog(@"I am run");
    NSLog(@"%s", __func__);
}

+ (BOOL)resolveInstanceMethod:(SEL)sel
{
    // 动态的添加方法实现
    if (sel == @selector(test)) {
        // 获取其他方法 指向method_t的指针
        Method otherMethod = class_getInstanceMethod(self, @selector(run));
 
        // 动态添加test方法的实现
        class_addMethod(self, sel, method_getImplementation(otherMethod), method_getTypeEncoding(otherMethod));
 
        // 返回YES表示有动态添加方法
        return YES;
    }
 
    NSLog(@"%s", __func__);
    return [super resolveInstanceMethod:sel];
}

@end



#import <Foundation/Foundation.h>
#import "test.h"
#import "Person.h"
int main(int argc, const char * argv[]) {
    @autoreleasepool {
        Person *person = [[Person alloc] init];
        [person performSelector:@selector(test)];
    }
    return 0;
}
```

从代码中可以看到Person类中是没有test方法的，但是我们仍然可以调用，这是因为OC的消息转发机制在类及父类中均未找到方法是会进行动态方法解析，会自动调用类的`resolveInstanceMethod`:(或resolveClassMethod:)方法进行动态查找,所以我们可以在resolveInstanceMethod:方法内部使用class_addMethod动态的添加方法实现。

![22](/image/22.png)

方法参数简单介绍:
```
class_addMethod(Class _Nullable cls, SEL _Nonnull name, IMP _Nonnull imp, const char * _Nullable types) 

@cls : 给哪个类对象添加方法
@name ： SEL类型，给哪个方法名添加方法实现
@imp : IMP类型的，要把哪个方法实现添加给给定的方法名
@types ： 就是表示返回值和参数类型的字符串
```

6.备用接收者(其实就是换个执行对象)

![25](/image/25.png)

```
#import <Foundation/Foundation.h>

#import "Person.h"
#import <objc/message.h>
#import "Car.h"
@implementation Person :NSObject
- (void) run {
    NSLog(@"I am run");
    NSLog(@"%s", __func__);
}

+ (BOOL)resolveInstanceMethod:(SEL)sel
{
    // 动态的添加方法实现
    if (sel == @selector(test)) {
        // 获取其他方法 指向method_t的指针
        Method otherMethod = class_getInstanceMethod(self, @selector(run));
 
        // 动态添加test方法的实现
        class_addMethod(self, sel, method_getImplementation(otherMethod), method_getTypeEncoding(otherMethod));
 
        // 返回YES表示有动态添加方法
        return YES;
    }
 
    NSLog(@"%s", __func__);
    return [super resolveInstanceMethod:sel];
}
- (id)forwardingTargetForSelector:(SEL)aSelector {
    //返回能够处理消息的对象
    if (aSelector == @selector(drive)) {
        return [[Car alloc] init];
    }
    return [super forwardingTargetForSelector:aSelector];
}

@end



#import <Foundation/Foundation.h>
#import "Car.h"

@implementation Car : NSObject
-(void)drive{
    NSLog(@"我可以开车");
}

@end



#import <Foundation/Foundation.h>
#import "test.h"
#import "Person.h"
int main(int argc, const char * argv[]) {
    @autoreleasepool {
        Person *person = [[Person alloc] init];
        [person performSelector:@selector(test)];
        [person drive];
    }
    return 0;
}
```

这里我们在Person类中对drive方法只声明不实现，然后写forwardingTargetForSelector方法实现对象的转换，调用有drive方法的Car类，这就是OC消息转发机制中的备用接收者。

![23](/image/23.png)

7.完整转发(我个人理解其实就是在这一步自己决定执行对象和执行方法)

![26](/image/26.png)

写一个`- (NSMethodSignature *)methodSignatureForSelector:(SEL)aSelector`方法只要他返回一个方法签名就会调用你写的另一个函数`- (void)forwardInvocation:(NSInvocation *)anInvocation`，然后你可以自己在这个函数内生成对象，使用这个对象去调用你的这个方法签名代码如下:
```
#import <Foundation/Foundation.h>

#import "Person.h"
#import <objc/message.h>
#import "Car.h"
@implementation Person :NSObject
- (void) run {
    NSLog(@"I am run");
    NSLog(@"%s", __func__);
}

+ (BOOL)resolveInstanceMethod:(SEL)sel
{
    // 动态的添加方法实现
    if (sel == @selector(test)) {
        // 获取其他方法 指向method_t的指针
        Method otherMethod = class_getInstanceMethod(self, @selector(run));
        
        // 动态添加test方法的实现
        class_addMethod(self, sel, method_getImplementation(otherMethod), method_getTypeEncoding(otherMethod));
        
        // 返回YES表示有动态添加方法
        return YES;
    }
    
    NSLog(@"%s", __func__);
    return [super resolveInstanceMethod:sel];
}

- (NSMethodSignature *)methodSignatureForSelector:(SEL)aSelector
{
    if (aSelector == @selector(drive)) {
        // return [NSMethodSignature signatureWithObjCTypes: "v@:"];
        // return [NSMethodSignature signatureWithObjCTypes: "v16@0:8"];
        // 也可以通过调用Car的methodSignatureForSelector方法得到方法签名，这种方式需要car对象有aSelector方法
        return [[[Car alloc] init] methodSignatureForSelector: aSelector];
        
    }
    return [super methodSignatureForSelector:aSelector];
}

//NSInvocation 封装了一个方法调用，包括：方法调用者，方法，方法的参数
//    anInvocation.target 方法调用者
//    anInvocation.selector 方法名
//    [anInvocation getArgument: NULL atIndex: 0]; 获得参数
- (void)forwardInvocation:(NSInvocation *)anInvocation
{
    //   anInvocation中封装了methodSignatureForSelector函数中返回的方法。
    //   此时anInvocation.target 还是person对象，我们需要修改target为可以执行方法的方法调用者。
    //   anInvocation.target = [[Car alloc] init];
    //   [anInvocation invoke];
    [anInvocation invokeWithTarget: [[Car alloc] init]];
}

@end
```

![28](/image/28.png)

总结：

OC中的对象方法调用都是采用消息发送，而所谓消息发送其实是SEL-IMP的查找过程，当我们在类中进行前四步都没找到，那就要进行消息转发，在消息转发中OC提供了三条补救措施，分别是动态方法解析，备用接收者，完整转发。完整流程如下图：

![27](/image/27.png)

# 3.ObjC runtime的"反射"->KVC

## (1)概念

KVC是Key-Value-Coding缩写，意思是键值编码，作用时通过名称访问对象属性，操作方法是由NSObject实现的NSKeyValueCoding协议实现，因此几乎所有对象都支持。

## (2)使用

```
设置值
- (void)setValue:(id)value forKey:(NSString *)key;
- (void)setValue:(id)value forKeyPath:(NSString *)keyPath;
获取值
- (id)valueForKey:(NSString *)key;
- (id)valueForKeyPath:(NSString *)keyPath;
```

案例如下:

```
@interface Dog : NSObject
@property (nonatomic, copy) NSString *name;
@end

#import "dog.h"@implementation Dog

@end


#import "dog.h"
@interface Person2 : NSObject
@property (nonatomic, assign) NSString *name;
@property (nonatomic, assign) NSInteger age;
@property (nonatomic, strong) Dog *dog;
@end

#import "person2.h"
@implementation Person2 : NSObject
@end

#import <Foundation/Foundation.h>
#import "test.h"
#import "Person.h"
#import "person2.h"
int main(int argc, const char * argv[]) {
    @autoreleasepool {
        
        Person2 *person2 = [Person2 new];
        [person2 setValue:@(18) forKey:@"age"];
        NSLog(@"age: %@", [person2 valueForKey:@"age"]);
            
        person2.dog = [Dog new];
        [person2 setValue:@"xiaoHuang" forKeyPath:@"dog.name"];
        NSLog(@"name: %@", [person2 valueForKeyPath:@"dog.name"]);    }
    return 0;
}
```

 ![60](/image/60.png)

## (3)原理概述

设置值:

![50](/image/50.png)

查看文档可以看出设置值分为三步

①有没有set<key> 或者_set<key> 这些方法，如果有的话，优先调用他们，就不再按自己的值设置了的

②检查accesssInstanceVariableDirectly()函数返回值，该函数默认返回值是YES,当然我们可以重写，如果为YES 往下，如果重写了就跳过第二部，直接去第三步，为YES时会检查(`_<key>`),`_is<key>`<key>,is<key> 这几个名字的变量，如果有就给他们赋值顺序第一个，如果没有到第三步

③执行setValue:forUndefinedKey:.这个函数，如果我们不重写那就抛异常结束了，我们可以对其重写

获取值:

取值调用

![57](/image/57.png)

①先看对象内函数，用函数返回值充当值，如果没有就为null

![51](/image/51.png)

![54](/image/54.png)

②第二步和第三步是关于数组和集合的

![58](/image/58.png)

![52](/image/52.png)

④同样会进行函数检查，如果函数返回yes 也会从这些<u>**成员变量**</u>中找值

![53](/image/53.png)

![55](/image/55.png)

# 4.ObjC使用AssociatedObject动态为对象添加属性

## (1)概念

一般情况下，对象在实例化后是不能动态添加属性的，但是在OC中可以通过关联对象(Associated Object)实现我们的需求，具体来说就是新建一个类把两个类关联起来，关联后就可以随时获取该对象

runtime提供了給我们3个API以管理关联对象（存储、获取、移除):

```
//关联对象
void objc_setAssociatedObject(id object, const void *key, id value, objc_AssociationPolicy policy)
//获取关联的对象
id objc_getAssociatedObject(id object, const void *key)
//移除关联的对象
void objc_removeAssociatedObjects(id object)
```

其中的参数

- id object：被关联的对象
- const void *key：关联的key，要求唯一
- id value：关联的对象
- objc_AssociationPolicy policy：内存管理的策略

其中内存管理策略是一个枚举，取值如下

```
typedef OBJC_ENUM(uintptr_t, objc_AssociationPolicy) {
    OBJC_ASSOCIATION_ASSIGN = 0,           /**< Specifies a weak reference to the associated object. */
    OBJC_ASSOCIATION_RETAIN_NONATOMIC = 1, /**< Specifies a strong reference to the associated object. 
                                            *   The association is not made atomically. */
    OBJC_ASSOCIATION_COPY_NONATOMIC = 3,   /**< Specifies that the associated object is copied. 
                                            *   The association is not made atomically. */
    OBJC_ASSOCIATION_RETAIN = 01401,       /**< Specifies a strong reference to the associated object.
                                            *   The association is made atomically. */
    OBJC_ASSOCIATION_COPY = 01403          /**< Specifies that the associated object is copied.
                                            *   The association is made atomically. */
};
```

不同的内存管理策略对应了不同的属性修饰符。

## (2)简单使用

```
#import "MyClass.h"
@interface MyClass ()
{
    NSString * _property;
}
@end

@implementation MyClass

- (instancetype)init
{
    self = [super init];
    if (self) {
        _property = @"AloneMonkey";
    }
    return self;
}

- (void)myMethod{
    NSLog(@"my method");
}

+ (void)classMethod{
    NSLog(@"class method");
}

@end

#import "ViewController.h"
#import "MyClass.h"
#import <objc/runtime.h>

static const void *kAssociatedKey = &kAssociatedKey;

static void *kExampleDoubleKey;

@interface ViewController ()

@end

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view, typically from a nib.
    
    MyClass *myClass = [[MyClass alloc] init];
    
    //KVC
    NSString* property = [myClass valueForKey:@"_property"];
    NSLog(@"property: %@", property);
    
    Ivar ivar = class_getInstanceVariable(objc_getClass("MyClass"), "_property");
    if(ivar){
        NSString* ivarProperty = (__bridge NSString *)(*(void**)((__bridge void*)myClass + ivar_getOffset(ivar)));
        NSLog(@"ivarProperty: %@", ivarProperty);
    }
    
    //AssociatedObject
    
    objc_setAssociatedObject(myClass, kAssociatedKey, @"AssociatedObject1", OBJC_ASSOCIATION_RETAIN_NONATOMIC);
    
    NSString* associatedString = objc_getAssociatedObject(myClass, kAssociatedKey);
    
    NSLog(@"associatedString: %@", associatedString);
    
    objc_setAssociatedObject(myClass, &kExampleDoubleKey, @"AssociatedObject2", OBJC_ASSOCIATION_RETAIN_NONATOMIC);
    
    associatedString = objc_getAssociatedObject(myClass, &kExampleDoubleKey);
    
    NSLog(@"associatedString: %@", associatedString);
    
    objc_setAssociatedObject(myClass, @selector(myProperty), @"AssociatedObject3", OBJC_ASSOCIATION_RETAIN_NONATOMIC);
    
    associatedString = objc_getAssociatedObject(myClass, @selector(myProperty));
    
    NSLog(@"associatedString: %@", associatedString);
}


- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}


@end
```

![61](/image/61.png)



可以看到，我们通过objc_setAssociatedObject方法为MyClass对象关联一个字符串，再通过id objc_getAssociatedObject方法获取其值打印输出，实现为一个对象添加属性

# 5.ObjC使用Method Swizzling 进行方法绑定

## (1)概念

我们在前面了解类结构的时候已经知道了方法对象是由SEL与IMP组成 SEL为方法名称IMP则是方法的具体实现，在OC语言中，Runtime提供了修改IMP的方法和交换两个IMP实现的方法。通过交换两个selector的实现，可以达到在调用A方法时实际调用了B方法，在B方法中可以继续调用A方法的效果，通常把这中操作称为Method Swizzling.

![59](/image/59.png)

## (2)简单使用

这里先补充一点:当一个类被引用进项目时会在main函数执行前先执行load函数

```
@interface MethodSwizzling : NSObject
 
-(void)test1;
-(void)test2;
 
@end

#import <Foundation/Foundation.h>
#import "MethodSwizzling.h"
#import <objc/runtime.h>
 
@implementation MethodSwizzling
 
+ (void)load {
    // 获取test1、test2方法
    Method method_test1 = class_getInstanceMethod(self, @selector(test1));
    Method method_test2 = class_getInstanceMethod(self, @selector(test2));
    // 交换两个方法的实现
    method_exchangeImplementations(method_test1, method_test2);
}
 
-(void)test1 {
    NSLog(@"test1");
}
 
-(void)test2 {
    NSLog(@"test2");
}
 
@end


#import <Foundation/Foundation.h>
#import "test.h"
#import "Person.h"
#import "person2.h"
#import "MethodSwizzling.h"
int main(int argc, const char * argv[]) {
    @autoreleasepool {
        
        MethodSwizzling *obj = [[MethodSwizzling alloc] init];
        [obj test1];
    }
    return 0;
}
```

![60](/image/60.png)

可以看到方法交换后调用test1方法，实际执行函数是test2。



# 6.ARM架构/指令集/寄存器/编码

## (1)ARM架构:

iOS设备和安卓设备的区别在于，android设备在n5x之后建议使用64位架构，而iOS设备则是在18年iOS111时就强制使用64位架构，禁止32位应用上架，因此我们这里只用了解64位架构即可.

体系结构:

A:Applicationtion 体系，就是咱们学习的应用相关。

R:Real-time体系 嵌入式相关。

M:Microcontroller体系，嵌入式相关。

## (2)寄存器:

### ①通用寄存器:

R0~R30是31个通用寄存器，每个寄存器又有两种访问方式

- 64位通用寄存器名为X0~X30
- 32位通用寄存器名为W0~W30

两种访问方式对应关系为Wn表示Xn的低32位，具体如下图所示：

![35](/image/35.png)

通用寄存器X30又用于程序调用的的link register.是一个特殊的寄存器，用于保存函数调用完成时的返回地址。

### ②特殊寄存器:

SP:64位堆栈指针寄存器，可以通过寄存器名WSP 访问堆栈指针最低有效32位

PC:保存当前指令地址的64位程序计数器，程序中不能直接修改PC,只能在分支，异常条目或异常返回时更新。

V0~V31:主要用于浮点数运算，但我们暂时可能也用不到，这里也不展开。

### ③处理器状态:

AArch64通过PSTATE的标志位来保存处理器状态，PSTATE也不是寄存器是进程状态信息的抽象，处理器执行指令时可以读取与设置这些标志位，以这些标志位为依据。以下为PSTATE可以在EL0级别访问的常见标志位

![36](/image/36.png)



## (3)指令集编码:

计算机中存储的都是二进制数据，而我们学习的ARM64指令集肯定也是要转化为二进制数据，比如我们最常见的mov x1 x2 对应的肯定也是要转化为二进制数据存储，所谓的指令集编码就是指令到二进制数据的对应，但其实我们知道我们无论是使用IDA还是lldb进行调试看到最底层也是汇编了，所以这里就不再展开。

# 7.ARM64算术/传输/逻辑/地址/移位指令

ARM64相关指令很多我们可以去 [官网](https://developer.arm.com/documentation/#q=ARMv8-A%20Reference%20Manual&f[navigationhierarchiescontenttype]=Architecture%20Document&cf[navigationhierarchiesproducts]=Architectures)下载官方文档，这里只简单了解一些常见指令。

(1)算术指令:

![29](/image/29.png)

(2)传输指令:

![30](/image/30.png)

(3)逻辑指令:

![31](/image/31.png)

(4)地址指令:

![32](/image/32.png)

(5)移位指令:

![33](/image/33.png)

# 8.栈和方法在ARM64指令集上的实现细节

## (1)栈基础介绍

这里的栈是进程中的一块特殊内存区域，因为我们知道一个进程在运行时都会有属于自己的内存空间，栈就是进程内存空间内一块连续的区域，由编译器自动分配释放，因此一般用来保存一些临时数据，比如局部变量和上下文环境，在操作上类似于数据结构上的栈的操作，有栈顶与栈底，只能在一端操作。

根据栈的增长方向和栈顶指针指向的位置，可以将其分为以下4种类型

- 向高地址方向生长，称为递增堆栈。
- 向低地址方向生长，称为递减堆栈。
- 堆栈指针指向最后压入堆栈的有效数据项，称为满堆栈
- 堆栈指针指向下一个要放入的空位置，成为空堆栈

ARM的堆栈具有后进先出和满递减的特点，如下图所示，将其想象为一个函数栈，有如下特点

![37](/image/37.png)

- 栈中元素按ABCD顺序入栈，按DCBA顺序出栈。
- 栈是向低地址方向生长的
- SP指向栈顶元素，其他元素通过SP+offset 偏移获取

## (2).栈相关寄存器

函数在调用的时候会开辟栈帧，函数参数的传递是通过x0-x7传递的，以下是部分与函数栈帧相关寄存器。

PC寄存器:记录当前执行代码地址

SP寄存器:指向栈帧的指针，在内存操作指令中通过x31寄存器访问。

LR寄存器:指向返回地址，对应寄存器x30

FP寄存器:指向栈帧底部，对应寄存器x29

## (3).栈帧结构

一个栈帧包括以下部分

- 参数区(parameter area):存放调用函数传递的参数。
- 连接区(linkage area):存放调用者(caller)的下一条指令
- 栈帧指针存放区(frame pointer):存放调用函数的栈帧底部
- 寄存器存储区(saved registers area):被调用函数(callee)返回需要恢复的寄存器内容
- 局部存储区(local storage area):用于存放被调用函数(callee)的局部变量

![38](/image/38.png)

# 9.函数调用/参数传递/入栈出栈完整流程

Xcode导入[ArmDemo项目](https://github.com/AloneMonkey/iOSREBook/tree/master/chapter-6/6.3-ARM%E6%B1%87%E7%BC%96/ArmDemo)，这里要注意需要有开发者账号将手机设为调试设备，不然无法attach进程，xcode中的模拟器是X86_64，调试出来的汇编代码不是ARM。另外调试过程中使用xia0LLDB调试工具，安装命令及[介绍地址](https://github.com/4ch12dy/xia0LLDB)如下:

```
git clone https://github.com/4ch12dy/xia0LLDB.git && cd xia0LLDB && ./install.sh
```

1.先看main函数

info -f main 查看main函数地址

dfuc addr查看汇编指令

## (1)函数调用逻辑及参数传递

```
info -f main  查看函数地址及信息
```

![39](/image/39.png)

```
dfuc 查看该地址函数对应汇编代码
```

![40](/image/40.png)

从上述汇编指令可以看到add1函数的调用的参数的传递，add1方法调用共需11个参数，其中前八个参数都是先mov保存到了w0-w7寄存器中然后读取到栈中，而后三个参数则直接使用w8作为中转直接放入栈中，说明函数调用时是用x0-x7传递参数的，但是参数过多时超出个数就直接存放到栈中了

同样的方式查看一个简单函数add2的汇编指令

![40](/image/40.png)

通过分析可以发现方法的调用会开辟新的栈帧空间并对原来栈指针进行保存，方便执行完毕返回原样，现场保存完毕后就是参数的传递及执行完后栈帧空间销毁，跳回原样，具体过程如下:

(1)函数调用前:

1. 开辟新的栈帧空间
2. 保存FP和LR寄存器，以便找到上一个栈帧和返回地址
3. 设置新的FP寄存器
4. 保存子函数会用到的寄存器
5. 保存局部变量或参数

(2)函数调用结束

1. 还原FP和LR寄存器
2. 释放栈帧空间
3. 跳到LR子程序返回

通过上边add2方法的汇编指令我们可以看到，其在传递参数时，不是使用的我们上边所说的x0-x7来传递的参数，这是因为小数是通过d0，d1来传递的参数。

## (2)OC中的消息机制的汇编代码

我们在上边已经了解了OC语言中方法调用时利用消息机制将其转化为objc_msgSend方法的调用该方法调用格式为objc_msgSend(receiver, selector, arg1, arg2, ...)，接下来我们看一看汇编中的实现

![41](/image/41.png)

调试CrackMe，当代码执行到函数调用地址时，我们打印x0，x1寄存器，可以发现x0寄存器存放的是类名，x1寄存器存放方法名，其他参数存储在x2-x7或堆栈中。

# 10.ObjC汇编静态分析与CrackMe动态调试

接下来我们对案例进行简单的汇编分析

先看案例代码如下

![43](/image/43.png)

类方法名下断点

![34](/image/34.png)

进行调试，发现isEqualToString方法

![44](/image/44.png)

继续调试发现theTextField对象，但是其实可以发现，对于这种业务代码，牵扯到库函数的汇编指令会变得格外多，需要分析地方，并不是一个简单的方式，对于初学者来说并不友好，因此这里推荐IDA F5查看伪代码，或者学习之后会更新的frida调试更为方便一些。

![45](/image/45.png)

![46](/image/46.png)

# 总结

学到这里我们明白了ObjC类与方法的底层逻辑，运行时的消息传递原理和过程，动态语言的反射、动态修改等特性，并对调用过程的汇编实现、参数返回值传递等进行了分析，为后续开展frida这款hook框架的编码学习打下了良好的基础。

# 参考文献

- 本文中大部分内容来源于：刘培庆：《iOS应用逆向与安全》 https://github.com/AloneMonkey/iOSREBook
