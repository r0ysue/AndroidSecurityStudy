setImmediate(function () {
    if (ObjC.available) {
        Interceptor.attach(ObjC.classes["ViewController"]["- buttonClick:"].implementation, {
            onEnter: function (args) {
                const x0 = new ObjC.Object(args[0]);
                console.log("x0 => " + x0.toString() + ' (' + x0.$className + ')')
                console.log("current theLabel value is => ", JSON.stringify(x0.$ivars), "---------\n\n\t\n")
                var newString = ObjC.classes.NSString.stringWithUTF8String_(Memory.allocUtf8String("aaaa"))
                console.log(JSON.stringify((ObjC.Object(x0.$ivars["_theLabel"]).$ownMethods)));
                ObjC.Object(x0.$ivars["_theLabel"]).setText_(newString);

                // console.log("")
            }, onLeave: function (ret) {
                console.log("ret => ", ret)
            }
        })

        const specifier = {
            class: ObjC.classes['ViewController'],
            subclasses: true,  // don't skip subclasses
        };

        ObjC.choose(specifier, {
            onMatch: function (ins) {
                console.log("found ins => ", ins)
                console.log("ivars => ", JSON.stringify(ins.$ivars["_theLabel"].toString()))
                console.log("methods => ", ins.$ownMethods)
                var doit = new NativeFunction(Module.findExportByName(null, 'do_it'), 'pointer', [])
                console.log("doit result => ", doit().readCString())
            }, onComplete() {
                console.log("Search Completed!")
            }

        });
    }
})

function callSecretFunc() {
    return (new NativeFunction(Module.findExportByName(null, 'do_it'), 'pointer', []))().readCString()
}


rpc.exports = {
    callsecretfunction: callSecretFunc
};