$(function() {
    // When we're using HTTPS, use WSS too.
    // var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    // var chatsock = new ReconnectingWebSocket('http://' + window.location.host + "/chat/");
    
    // chatsock.onmessage = function(message) {
    //     var data = JSON.parse(message.data);
    //     var chat = $("#chat")
    //     var ele = $('<tr></tr>')
    //     console.log(data)
    //     ele.append(
    //         $("<td></td>").text(data.owner)
    //     )
    //     ele.append(
    //         $("<td></td>").text(data.timestamp)
    //     )
    //     ele.append(
    //         $("<td></td>").text(data.user)
    //     )
    //     ele.append(
    //         $("<td></td>").text(data.msg)
    //     )
        
    //     chat.append(ele)
    // };
   
    $("#chatform").on("submit", function(event) {
        var message = {
            command: "send",
            message: $('#message').val(),
            character: parseInt(document.getElementById("mySelect").value)
        }
        var data_url = 'http://' + window.location.host + "/chat_send/";
        $.get({url: data_url, data: message, success: (result) => {
            
            if (result.success) {
               console.log(result);
            } 
        }})
        // chatsock.send(JSON.stringify(message));
        $("#message").val('').focus();
        return false;
    });
    console.log("hello main");
     // Helpful debugging
    // chatsock.onopen = function () {
    //     console.log("hello open");
    //     console.log("Connected to chat socket");
    // };
    // chatsock.onclose = function () {
    //     console.log("hello close");
    //     console.log("Disconnected from chat socket");
    // }
});