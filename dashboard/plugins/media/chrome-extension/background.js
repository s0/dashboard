var ws = null,
    next_tab_id = 0,
    tabs = {};

function ws_send(obj){
    if(ws !== null && ws.readyState === 1){
        ws.send(JSON.stringify(obj))
        return;
    }

    if ("WebSocket" in window) {

        ws = new WebSocket("ws://localhost:8888/");

        console.debug(ws)

        ws.onopen = function() {
            console.debug("connected");
            ws.send(JSON.stringify(obj))
        };
        ws.onmessage = function (evt) {
            var msg = JSON.parse(evt.data);
            if(msg.tab_id in tabs)
                tabs[msg.tab_id](msg)
            else
                console.debug("Unknown tab id: ", msg);
        };
        ws.onclose = function() {
            console.debug("Connection is closed...");
        };
    } else {
        console.debug("WebSocket NOT supported by your Browser!");
    }
}

chrome.runtime.onConnect.addListener(function(port) {

    var tab_id = next_tab_id++;

    console.log("New tab")

    port.onDisconnect.addListener(function(){
        var msg = {action: "del_tab", tab_id: tab_id}
        console.log("chrome --> dashboard", msg)
        ws_send(msg)
    })

    // Handle chrome --> dashboard messages
    port.onMessage.addListener(function(msg) {
        msg.tab_id = tab_id
        console.log("chrome[" + tab_id + "] --> dashboard", msg)
        ws_send(msg)
    })

    // Handle dashboard --> chrome messages
    tabs[tab_id] = function(msg){
        console.log("dashboard --> chrome[" + tab_id + "]", msg)
        port.postMessage(msg)
    }
});
