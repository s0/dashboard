//alert("asd");

if ("WebSocket" in window) {

    var ws = new WebSocket("ws://localhost:8888/?Id=123456789");

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
