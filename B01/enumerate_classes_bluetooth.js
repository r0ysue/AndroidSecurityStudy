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
  });
});
