//alert("asd");

var next_tab_id = 0;

if ("WebSocket" in window) {

    var ws = new WebSocket("ws://localhost:8888/");

    ws.onopen = function() {
        console.debug("connected");
        ws.send("Message to send");
    };
    ws.onmessage = function (evt) {
        var received_msg = evt.data;
        console.debug("Message is received...");
        console.debug(received_msg);
    };
    ws.onclose = function() {
        console.debug("Connection is closed...");
    };
} else {
    console.debug("WebSocket NOT supported by your Browser!");
}

chrome.runtime.onConnect.addListener(function(port) {

    var tab_id = next_tab_id++;

    console.debug("new tab: " + tab_id)

    port.onDisconnect.addListener(function(){
        console.debug("disconnected")
    })

    port.onMessage.addListener(function(msg) {
        console.log("message received", msg)
        port.postMessage({mmmmsg: "foobar, this is a message"})
  })
});
