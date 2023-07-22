setImmediate(() => {
    console.log("hello world!r0ysue! ObjC => ", ObjC.available)
    const resolver = new ApiResolver('objc');
    const matches = resolver.enumerateMatches('*[* isEqualToString:*]');
    matches.forEach((match) => {
        console.log(JSON.stringify(match))
        Interceptor.attach(match.address, {
            onEnter: function (args) {
                this.change = false;
                const receiver = new ObjC.Object(args[0]);
                console.log("receiver is => ", receiver.$className, "  => ", receiver.toString());

                if (receiver.toString().indexOf("aaaabbbb") >= 0) {
                    this.change = true;
                    console.log("need change")
                    const { NSString } = ObjC.classes;
                    var newString = NSString.stringWithString_("aaaabbbb");
                    args[2] = newString;
                }
            }, onLeave: function (ret) {
                console.log("ret=>", ret)
                // if(this.change){
                //     ret.replace(new NativePointer(0x1))
                // }        
            }
        })
        // const ViewController = ObjC.classes.ViewController; /* macOS */
        // const buttonClick = ViewController['- buttonClick:'];
        // const oldImpl = buttonClick.implementation;
        // buttonClick.implementation = ObjC.implement(buttonClick, (handle, selector,args) => {
        //     console.log("handle selecter args => ",handle,selector,args)
        //     console.log(Thread.backtrace(this.context, Backtracer.FUZZY).map(DebugSymbol.fromAddress).join("\n\t"))
        //     oldImpl(handle, selector,args);
        // });
    })
})