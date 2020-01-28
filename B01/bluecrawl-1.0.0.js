/**


                   GNU LESSER GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.


  This version of the GNU Lesser General Public License incorporates
the terms and conditions of version 3 of the GNU General Public
License, supplemented by the additional permissions listed below.

  0. Additional Definitions.

  As used herein, "this License" refers to version 3 of the GNU Lesser
General Public License, and the "GNU GPL" refers to version 3 of the GNU
General Public License.

  "The Library" refers to a covered work governed by this License,
other than an Application or a Combined Work as defined below.

  An "Application" is any work that makes use of an interface provided
by the Library, but which is not otherwise based on the Library.
Defining a subclass of a class defined by the Library is deemed a mode
of using an interface provided by the Library.

  A "Combined Work" is a work produced by combining or linking an
Application with the Library.  The particular version of the Library
with which the Combined Work was made is also called the "Linked
Version".

  The "Minimal Corresponding Source" for a Combined Work means the
Corresponding Source for the Combined Work, excluding any source code
for portions of the Combined Work that, considered in isolation, are
based on the Application, and not on the Linked Version.

  The "Corresponding Application Code" for a Combined Work means the
object code and/or source code for the Application, including any data
and utility programs needed for reproducing the Combined Work from the
Application, but excluding the System Libraries of the Combined Work.

  1. Exception to Section 3 of the GNU GPL.

  You may convey a covered work under sections 3 and 4 of this License
without being bound by section 3 of the GNU GPL.

  2. Conveying Modified Versions.

  If you modify a copy of the Library, and, in your modifications, a
facility refers to a function or data to be supplied by an Application
that uses the facility (other than as an argument passed when the
facility is invoked), then you may convey a copy of the modified
version:

   a) under this License, provided that you make a good faith effort to
   ensure that, in the event an Application does not supply the
   function or data, the facility still operates, and performs
   whatever part of its purpose remains meaningful, or

   b) under the GNU GPL, with none of the additional permissions of
   this License applicable to that copy.

  3. Object Code Incorporating Material from Library Header Files.

  The object code form of an Application may incorporate material from
a header file that is part of the Library.  You may convey such object
code under terms of your choice, provided that, if the incorporated
material is not limited to numerical parameters, data structure
layouts and accessors, or small macros, inline functions and templates
(ten or fewer lines in length), you do both of the following:

   a) Give prominent notice with each copy of the object code that the
   Library is used in it and that the Library and its use are
   covered by this License.

   b) Accompany the object code with a copy of the GNU GPL and this license
   document.

  4. Combined Works.

  You may convey a Combined Work under terms of your choice that,
taken together, effectively do not restrict modification of the
portions of the Library contained in the Combined Work and reverse
engineering for debugging such modifications, if you also do each of
the following:

   a) Give prominent notice with each copy of the Combined Work that
   the Library is used in it and that the Library and its use are
   covered by this License.

   b) Accompany the Combined Work with a copy of the GNU GPL and this license
   document.

   c) For a Combined Work that displays copyright notices during
   execution, include the copyright notice for the Library among
   these notices, as well as a reference directing the user to the
   copies of the GNU GPL and this license document.

   d) Do one of the following:

       0) Convey the Minimal Corresponding Source under the terms of this
       License, and the Corresponding Application Code in a form
       suitable for, and under terms that permit, the user to
       recombine or relink the Application with a modified version of
       the Linked Version to produce a modified Combined Work, in the
       manner specified by section 6 of the GNU GPL for conveying
       Corresponding Source.

       1) Use a suitable shared library mechanism for linking with the
       Library.  A suitable mechanism is one that (a) uses at run time
       a copy of the Library already present on the user's computer
       system, and (b) will operate properly with a modified version
       of the Library that is interface-compatible with the Linked
       Version.

   e) Provide Installation Information, but only if you would otherwise
   be required to provide such information under section 6 of the
   GNU GPL, and only to the extent that such information is
   necessary to install and execute a modified version of the
   Combined Work produced by recombining or relinking the
   Application with a modified version of the Linked Version. (If
   you use option 4d0, the Installation Information must accompany
   the Minimal Corresponding Source and Corresponding Application
   Code. If you use option 4d1, you must provide the Installation
   Information in the manner specified by section 6 of the GNU GPL
   for conveying Corresponding Source.)

  5. Combined Libraries.

  You may place library facilities that are a work based on the
Library side by side in a single library together with other library
facilities that are not Applications and are not covered by this
License, and convey such a combined library under terms of your
choice, if you do both of the following:

   a) Accompany the combined library with a copy of the same work based
   on the Library, uncombined with any other library facilities,
   conveyed under the terms of this License.

   b) Give prominent notice with the combined library that part of it
   is a work based on the Library, and explaining where to find the
   accompanying uncombined form of the same work.

  6. Revised Versions of the GNU Lesser General Public License.

  The Free Software Foundation may publish revised and/or new versions
of the GNU Lesser General Public License from time to time. Such new
versions will be similar in spirit to the present version, but may
differ in detail to address new problems or concerns.

  Each version is given a distinguishing version number. If the
Library as you received it specifies that a certain numbered version
of the GNU Lesser General Public License "or any later version"
applies to it, you have the option of following the terms and
conditions either of that published version or of any later version
published by the Free Software Foundation. If the Library as you
received it does not specify a version number of the GNU Lesser
General Public License, you may choose any version of the GNU Lesser
General Public License ever published by the Free Software Foundation.

  If the Library as you received it specifies that a proxy can decide
whether future versions of the GNU Lesser General Public License shall
apply, that proxy's public statement of acceptance of any version is
permanent authorization for you to choose that version for the
Library.


  ____________ __    ____  _             ____                    _
 / / __ ) \ \ \\ \  | __ )| |_   _  ___ / ___|_ __ __ ___      _| |
| ||  _ \| | | |\ \ |  _ \| | | | |/ _ \ |   | '__/ _` \ \ /\ / / |
| || |_) | | | |/ / | |_) | | |_| |  __/ |___| | | (_| |\ V  V /| |
| ||____/| | | /_/  |____/|_|\__,_|\___|\____|_|  \__,_| \_/\_/ |_|
 \_\    /_/_/_/
	for Frida (Android)
	by Keith Makan @IOActive

	- simple frida script for interacting with and dumping info from bluetooth device objects and sockets
	- I left a little bit of breathing room for those who want to do other cool stuff

_device_t = new Object();
_device_t._name="";
_device_t._address="";
_device_t._class="";
_device_t._type="";
_device_t._bond="";

*/
/** should design a better console graphics library **/

function infoCursor(){

	return "\033[2m";
}
function lightGrayCursor(){
	return "\033[37m";
}

function lightGreenCursor(){
	return "\033[92m";
}
function greenCursor(){
	return "\033[32m";
}

function lightCyanCursor(){
	return "\033[96m"
}
function lightBlueCursor(){
	return "\033[94m"
}
function cyanCursor(){
	return "\033[36m"
}
function blueCursor(){
	return "\033[34m"
}
function closeCursor(){
	return "\033[0m"
}

_device_list = [] //array of _device_t objects

function add_new_device(_device_instance){

	var _bluetoothDevice = _device_instance;
	var _bluetoothDevice_address = _bluetoothDevice.getAddress();
	var _bluetoothDevice_class = _bluetoothDevice.getBluetoothClass();
	var _bluetoothDevice_bondState = _bluetoothDevice.getBondState();
	var _bluetoothDevice_name = _bluetoothDevice.getName();
	var _bluetoothDevice_type = _bluetoothDevice.getType();


	__device =  new Object();
	__device._address = _bluetoothDevice.getAddress();
	__device._class   = _bluetoothDevice.getBluetoothClass();
	__device._bond    = _bluetoothDevice.getBondState();
	__device._name    = _bluetoothDevice.getName();
	__device._type  	= _bluetoothDevice.getType();
	_device_list.push(__device);

	return __device;
}

function find_device(_address){
	for (var index = 0; index < _device_list.length; index++){
		if (_device_list[index]._address == _address){
			return _device_list[index];
		}
	}
	return undefined;
}

function make_spaces(length,spaces){
	var line_length = spaces;
	var spaces = " ";
	var index = 0;
	for (;index < line_length - length;index++){
		spaces+=" ";
	}
	return spaces;
}

function bluetoothDevice_MajorClassInfo(_majorClass){
	//should probably use bit masks for this right? just return all the matching fields right? naah fuck it, this is javascript
	switch(_majorClass){
		case(1024): return "("+_majorClass+") Audio/Video"; break;
		case(256):  return "("+_majorClass+")  Computer";break; //very very accurate description, very internet of things ready lol
		case(2304): return "("+_majorClass+") Health";break;
		case(1536): return "("+_majorClass+") Imaging";break;
		case(768):  return "("+_majorClass+")  Networking";break;
		case(1280): return "("+_majorClass+") Peripheral";break;
		case(512):  return "("+_majorClass+")  Phone";break;
		case(2048): return "("+_majorClass+") Toy"; break;
		case(7936): return "("+_majorClass+") Uncategorized";break;
		case(1792): return "("+_majorClass+") Wearable";break;
		case(0):     return "Misc [0]";break;
		default: return "unknown ["+_majorClass+"]";break;
	}
}
function findServicesForClass(_class){
	for (var index = 0;index < 3000;index++){
		if (_class.hasService(index)){
			console.log("[*]\t\t--"+bluetoothDevice_ServiceClassInfo(index));
		}
	}

}
function bluetoothGattServiceCharacteristicInfo(_gatt_service){

}
function bluetoothGattServiceInfo(_gatt_service){
	console.log("[t]\t\t UUID: "+services[index].getUUID().toString());
	return;
}
function bluetoothGattServerInfo(_gatt_server){
	//expands on Gatt Services
	//produce a nice print out of the device gatt service and all its descriptors
	//UUID
	//Type
	//InstanceID
	//IncludedServices
	//Dump Characteristics
	try{
		var services = _gatt_server.getServices();

	}
	catch(err){
		console.log("[x]\t\t"+err);
		return;
	}
	for (var index=0;index < services.length;index++){
		console.log("[t]\t\t "+services[index].getUUID().toString());
	}
}
function bluetoothDevice_ServiceClassInfo(_device_class){ //need to rename these but this sthe device class the one elow is te class object in java
	switch (_device_class){
		case(1076): return "("+_device_class+") Audio Video Camcorder"; break;
		case(1056): return "("+_device_class+") Audio Video Car"; break;
		case(1032): return "("+_device_class_+") Audio Video Headphones"; break;
		case(1048): return "("+_device_class_+") Audio Video Hifi Audio"; break;
		case(1044): return "("+_device_class_+") Audio Video Loudspeaker"; break;
		case(1040): return "("+_device_class_+") Audio Video Microphone"; break;
		case(1052): return "("+_device_class_+") Audio Video Portable Audio"; break;
		case(1060): return "("+_device_class_+") Audio Video Set Top Box"; break;
		case(1024): return "("+_device_class_+") Audio Video Uncategorized"; break;
		case(1068): return "("+_device_class_+") Audio Video VCR"; break;
		case(1072): return "("+_device_class_+") Audio Video Video Camera"; break;
		case(1088): return "("+_device_class_+") Audio Video Conferencing"; break;
		case(1084): return "("+_device_class_+") Audio Video Display and Loudspeaker"; break;
		case(1096): return "("+_device_class_+") Audio Video Gaming/Toy";break;
		case(1080): return "("+_device_class_+") Audio Video Monitor"; break;
		case(1028): return "("+_device_class_+") Audio Video Wearable Headset";break;
		case(260): return  "("+_device_class_+") Computer Desktop"; break;
		case(272): return  "("+_device_class_+") Computer Handheld PC PDA"; break;
		case(268): return  "("+_device_class_+") Computer Laptop"; break;
		case(276): return  "("+_device_class_+") Computer Palm Size PC PDA"; break;
		case(264): return  "("+_device_class_+") Computer Server"; break;
		case(256): return  "("+_device_class_+") Computer Uncategorized"; break;
		case(280): return  "("+_device_class_+") Computer Wearable"; break;
		case(2308): return "("+_device_class_+") Health Blood Pressure"; break;
		case(2332): return "("+_device_class_+") Health Data Display"; break;
		case(2320): return "("+_device_class_+") Health Glucose"; break;
		case(2324):return  "("+_device_class_+") Health Pulse Oximeter"; break;
		case(2328): return "("+_device_class_+") Health Pulse Rate"; break;
		case(2312): return "("+_device_class_+") Health Thermometer"; break;
		case(2304): return "("+_device_class_+") Health Uncategorized"; break;
		case(2316): return "("+_device_class_+") Health Weighing"; break;
		case(516): return  "("+_device_class_+") Phone Cellular";break;
		case(520): return  "("+_device_class_+") Phone ISDN"; break;
		case(528): return  "("+_device_class_+") Phone Modem or Gateway";break;
		case(524): return  "("+_device_class_+") Phone Smart";break;
		case(512): return  "("+_device_class_+") Phone Uncategorized";break;
		case(2064): return "("+_device_class_+") Toy Controller";break;
		case(2060): return "("+_device_class_+") Toy Action Figure"; break;
		case(2068): return "("+_device_class_+") Toy Game"; break;
		case(2052): return "("+_device_class_+") Toy Robot"; break; //will we one day have a sub-category for sentient robots? proabaly not anytime soon lol
		case(2048): return "("+_device_class_+") Toy Uncategorized";break;
		case(2056): return "("+_device_class_+") Toy Vehicle";break;
		case(1812): return "("+_device_class_+") Wearable Glasses";break;
		case(1808): return "("+_device_class_+") Wearable Helmet";break;
		case(1804): return "("+_device_class_+") Wearable Jacket";break;
		case(1800): return "("+_device_class_+") Wearable Pager";break;
		case(1792): return "("+_device_class_+") Wearable Uncategorized"; break;
		case(1796): return "("+_device_class_+") Wearable Wrist Watch";break;
		default: return "";break;
	}
	return "";
}
function bluetoothClassInfo(_class){
	//var _bluetoothClass_t = Java.cast("android.bluetooth.BluetoothClass",_class);
	//var _javaInteger = Java.use("java.lang.Integer");
	//var _bluetoothDeviceClassMajor = Java.cast(_javaInteger,_class.getMajorDeviceClass());
	var _bluetoothClass_t = "";
	var _bluetoothDeviceClassMajor = "";
	var _bluetoothDeviceClass = "";

	try{
	var _bluetoothClass_t = _class;
	var _bluetoothDeviceClassMajor = _bluetoothClass_t.getMajorDeviceClass();
	//var _bluetoothDeviceServiceClass = device_service_class;
	//var _bluetoothDeviceHasService = _bluetoothClass_t.hasService(); need some argument for this not sure what yet
	var _bluetoothDeviceClass = _bluetoothClass_t.getDeviceClass();

	}
	catch(err){
		console.log("[x]\t\t"+err);
	}
	//console.log("\t\t[device::class] Major :" + bluetoothDevice_MajorClassInfo(_bluetoothDeviceClassMajor));
	console.log("[*]\t\t"+lightBlueCursor()+"-- Class Major "+closeCursor()+" : "+ bluetoothDevice_MajorClassInfo(_bluetoothDeviceClassMajor));
	//console.log("[*]\t\t"+lightBlueCursor()+"-- Device Class"+closeCursor()+" : "\
	//		+ bluetoothDevice_ServiceClassInfo(_bluetoothDeviceClass));
	//console.log("[*]\t\t"+lightBlueCursor()+"-- Service Class"+closeCursor()+" : "+ _bluetoothDeviceClass);
	//console.log("\t\t[device::class] hasService :"  + _bluetoothDeviceHasService);
	//findServicesForClass(_class);
}

function bluetoothBondStateInfo(_type){
	switch(_type){
		case(12): return "("+_type+") Bonded"; break;
		case(11): return "("+_type+") Bonding";break;
		case(10): return "("+_type+") None";break;
		default: return "unknown ["+_type+"]"; break;
	}
	return;
}

function bluetoothConnectionTypeInfo(_type){
	switch(_type){
		case(1): return "("+_type+") L2CAP"; break;
		case(2): return "("+_type+") RFCOMM";break;
		case(3): return "("+_type+") SCO";break;
		default: return "unknown ["+_type+"]"; break;
	}
	return;
}
function bluetoothDeviceTypeInfo(_type){
	switch(_type){
		case(1): return "("+_type+") Classic"; break;
		case(2): return "("+_type+") Low Energy Only (LE Only)";break;
		case(3): return "("+_type+") Dual LE + Classic";break;
		case(0): return "("+_type+") unknown [0]"; break;
		default: return "unknown ["+_type+"]"; break;
	}
	return;
}
function interceptOutputStream(_outputStream_instance){
	_outputStream_instance = Java.use("java.io.OutputStream");
	_outputStream_instance.write = function(_byte){
		console.log("[output stream]> "+_byte);
	}
	_outputStream_instance.write(41);
}
function interceptInputStream(_inputStream_instance){
	_inputStream_instance.read.implementation = function(_byte){
		console.log("[input stream]> "+_byte);
	}
}

function writeToOutputStream(_outputStream_instance,_bytes){
	_outputStream_instance.write(_bytes);
	_outputStream_instance.flush();

}
function bluetoothInputStreamInfo(_inputStream_instance){
	var availableBytes = _inputStream_instance.available();
	console.log("[*]\t\t- bytes available :"+availableBytes);
}
function bluetoothSocketInfo(_socket_instance){
	console.log("[*]\t"+lightGrayCursor()+"getting info for '"+_socket_instance+"'"+closeCursor());
	var _bluetoothSocket = _socket_instance;
	try{

		var _isConnected = _bluetoothSocket.isConnected();
		var _inputStream = _bluetoothSocket.getInputStream();
		var _outputStream = _bluetoothSocket.getOutputStream();
		var _connectionType = _bluetoothSocket.getConnectionType();
		var _remoteDevice = _bluetoothSocket.getRemoteDevice();

		spaces = 20;
		console.log("[*]\t"+lightGreenCursor()+"- isConnected"+make_spaces("- Connected".length,spaces)+closeCursor()+":"+_isConnected); //add different colors for each connected state
		console.log("[*]\t"+lightGreenCursor()+"- connection type"+make_spaces("- Connection Type".length,spaces)+closeCursor()+":"+bluetoothConnectionTypeInfo(_connectionType)); //different colors for connection state would be cool too

		try{
			console.log("[*]\t"+lightGreenCursor()+"- connected device"+make_spaces("- Connected Device".length,spaces)+closeCursor()+":("+lightCyanCursor()+_remoteDevice.getAddress()+closeCursor()+") '"+greenCursor()+_remoteDevice.getName()+closeCursor()+"'");//definitely want to make this in light blue

		}
		catch(device_error){
			console.log("[x]\t"+lightGrayCursor()+"- conneted device"+make_spaces("- Connected Device".length,spaces)+": device details not available");
		}

		console.log("[*]\t"+lightGreenCursor()+"- InputStream"+make_spaces("- InputStream".length,spaces)+closeCursor()+":"+_inputStream);
		//	bluetoothInputStreamInfo(_inputStream);
		//	interceptInputStream(_inputStream);
		console.log("[*]\t"+lightGreenCursor()+"- OutputStream"+make_spaces("- OuputStream".length,spaces)+closeCursor()+":"+_outputStream);
		//writeToOutputStream(_outputStream,[41,41,41,41,41,41,41,41]);
		//interceptOutputStream(_outputStream);
		console.log("");

	}
	catch(err){
		console.log("\t\t"+err);
		return;
	}

}

function bluetoothServerSocketInfo(_socket_instance){
	console.log("[*]\tgetting info for '"+_socket_instance+"'");
	console.log("\t\t"+_socket_instance.toString());

}

function bluetoothDeviceInfo(_device_instance){

	console.log("[*]\tBluetooth device ['"+lightCyanCursor()+_device_instance+closeCursor()+"']");

	var _bluetoothDevice = _device_instance;
	var _bluetoothDevice_address = _bluetoothDevice.getAddress();
	var _bluetoothDevice_class = _bluetoothDevice.getBluetoothClass();
	var _bluetoothDevice_bondState = _bluetoothDevice.getBondState();
	var _bluetoothDevice_name = _bluetoothDevice.getName();
	var _bluetoothDevice_type = _bluetoothDevice.getType();

	//setPin and other fun still awaits	 - for now sticking to just simple reporting
	_bluetoothDevice = _device_instance;
	spaces = 16;

	console.log("[*]"+blueCursor()+"\t- Name"+closeCursor()+make_spaces("- Name".length,spaces)+":"+_bluetoothDevice.getName());
	console.log("[*]"+blueCursor()+"\t- Address"+closeCursor()+make_spaces("- Address".length,spaces)+":"+_bluetoothDevice.getAddress());
	console.log("[*]"+blueCursor()+"\t- Type"+closeCursor()+make_spaces("- Type".length,spaces)+":"+bluetoothDeviceTypeInfo(_bluetoothDevice.getType()));
	console.log("[*]"+blueCursor()+"\t- Device Class"+closeCursor()+make_spaces("- Device Class".length,spaces)+":"+_bluetoothDevice.getBluetoothClass());
	bluetoothClassInfo(_bluetoothDevice.getBluetoothClass());
	console.log("[*]"+blueCursor()+"\t- Bond State"+closeCursor()+make_spaces("- Bond State".length,spaces)+":"+bluetoothBondStateInfo(_bluetoothDevice.getBondState()));
	console.log("");
	//need to dump data that can be read from this device
}
/*
Main Java.perform loop for pulling out the relevant loaded classes and doing stuff with them.
Basic work flow for Frida and android is:
	1. pull objects from live class loader being used by the app
	2. look for classses you want to do stuff with
	3. Either replace them with other functions or pull data from the live objects in memory.

	here i simply target the bluetooth stack of objects because it avoids a tone of bluetooth protocol hacking in some cases.
	Also allows consultants to see the data being pushed out from the app.

**/
VERSION="1.0.0"
setTimeout(function(){
	Java.perform(function(){
		console.log("\n ---------- BlueCrawl : Bluetooth Metadata collector");
		console.log(" v"+VERSION);

		console.log("\n finding loaded bluetooth classes");

		Java.enumerateLoadedClasses({
				onMatch: function(instance){
					if (instance.split(".")[1] == "bluetooth"){
						console.log("[->]\t"+lightBlueCursor()+instance+closeCursor());
					}
				},
				onComplete: function() {}
			});

		Java.choose("android.bluetooth.BluetoothGattServer",{
				onMatch: function (instance){
					console.log("[*] "+infoCursor()+" 	android.bluetooth.BluetoothGattServer instance found"+closeCursor()+" :=> '"+instance+"'");
					bluetoothGattServerInfo(instance);

					/* add_new_device(p_name,p_address,p_class,p_type,p_bond);
				      add_new_device(instance);
					*/
				},
				onComplete: function() { console.log("[*] -----");}
			});

		Java.choose("android.bluetooth.BluetoothGattService",{
				onMatch: function (instance){
					console.log("[*] "+infoCursor()+" 	android.bluetooth.BluetoothGattService instance found"+closeCursor()+" :=> '"+instance+"'");
					bluetoothGattServiceInfo(instance);

					/* add_new_device(p_name,p_address,p_class,p_type,p_bond);
				      add_new_device(instance);
					*/
				},
				onComplete: function() { console.log("[*] -----");}
			});

		 console.log("\n searching loaded classes for 'android.bluetooth.BluetoothSocket'...");
		 Java.choose("android.bluetooth.BluetoothSocket",{
				onMatch: function (instance){
					console.log("[*] "+infoCursor()+"'android.bluetooth.BluetoothSocket' instance found "+closeCursor()+"'"+instance+"'");
					bluetoothSocketInfo(instance);
				},
				onComplete: function() { console.log("[*] -----");}
			});

		  console.log("\n searching loaded classes for 'android.bluetooth.BluetoothServerSocket'...");
		  Java.choose("android.bluetooth.BluetoothServerSocket",{
				onMatch: function (instance){
					console.log("[*] "+infoCursor()+" 'android.bluetooth.BluetoothServerSocket' instance found"+closeCursor()+" '"+instance+"'");
					//bluetoothServerSocketInfo(instance);
				},
				onComplete: function() { console.log("[*] -----");}
			});

	  	  console.log("\n searching loaded classes for 'android.bluetooth.BluetoothDevice'...");
		  Java.choose("android.bluetooth.BluetoothDevice",{
				onMatch: function (instance){
					console.log("[*] "+infoCursor()+" android.bluetooth.BluetoothDevice instance found"+closeCursor()+" :=> '"+instance+"'");
					bluetoothDeviceInfo(instance);

					/* add_new_device(p_name,p_address,p_class,p_type,p_bond);
				      add_new_device(instance);
					*/
				},
				onComplete: function() { console.log("[*] -----");}
			});
	});
},0);
