import time
import frida

def my_message_handler(message, payload):
    print(message)
    print(payload)


device = frida.get_usb_device()
#pid = device.spawn(["com.r0ysue.a0512demo02"])
# pid  = 28450
# device.resume
# time.sleep(1)
print(device.get_frontmost_application())
session = device.attach(device.get_frontmost_application().pid)
with open("10.js") as f :
    script = session.create_script(f.read())
script.on("message", my_message_handler)
script.load()

command = ""
while 1 ==1 :
    command = input("Enter Command:")
    if command == "1":
        break
    elif command == "2":
        print(script.exports.callsecretfunction())