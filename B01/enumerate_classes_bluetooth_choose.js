function make_spaces(length,spaces){
	var line_length = spaces;
	var spaces = " ";
	var index = 0;
	for (;index < line_length - length;index++){
		spaces+=" ";
	}
	return spaces;
}

function bluetoothDeviceInfo(_device_instance){

	console.log("[*]\tBluetooth device ['"+_device_instance+"']");

	var _bluetoothDevice = _device_instance;
	var _bluetoothDevice_address = _bluetoothDevice.getAddress();
	var _bluetoothDevice_class = _bluetoothDevice.getBluetoothClass();
	var _bluetoothDevice_bondState = _bluetoothDevice.getBondState();
	var _bluetoothDevice_name = _bluetoothDevice.getName();
	var _bluetoothDevice_type = _bluetoothDevice.getType();

	//setPin and other fun still awaits	 - for now sticking to just simple reporting
	_bluetoothDevice = _device_instance;
	spaces = 16;

	console.log("[*]"+"\t- Name"+make_spaces("- Name".length,spaces)+":"+_bluetoothDevice.getName());
	console.log("[*]"+"\t- Address"+make_spaces("- Address".length,spaces)+":"+_bluetoothDevice.getAddress());
	console.log("[*]"+"\t- Device Class"+make_spaces("- Device Class".length,spaces)+":"+_bluetoothDevice.getBluetoothClass());
	console.log("");
	//need to dump data that can be read from this device
}


setTimeout(function (){
  Java.perform(function (){
    console.log("\n[*] enumerating classes...");
    Java.enumerateLoadedClasses({
      onMatch: function(instance){
        if (instance.split(".")[1] == "bluetooth"){
	         console.log("[->]\t"+instance);
	        }
        },
        onComplete: function(){
	         console.log("[*] class enuemration complete");
	        }
    });

    Java.choose("android.bluetooth.BluetoothDevice",{
      onMatch: function (instance){
        console.log("[*] "+" android.bluetooth.BluetoothDevice instance found"+" :=> '"+instance+"'");
        bluetoothDeviceInfo(instance);
      },
      onComplete: function() { console.log("[*] -----");}
    });

  });
});
