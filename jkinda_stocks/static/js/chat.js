$('.chat-button').on('click', function() {
    $('.chat-button').css({
        "display": "none"
    });
    $('.chat-box').css({
        "visibility": "visible"
    });
});
$('.chat-box .chat-box-header p').on('click', function() {
    $('.chat-button').css({
        "display": "block"
    });
    $('.chat-box').css({
        "visibility": "hidden"
    });
}) 
$("#addExtra").on("click", function() {
    $(".modal").toggleClass("show-modal");
}) 
$(".modal-close-button").on("click", function() {
    $(".modal").toggleClass("show-modal");
})

$("#send-message").click(() => {
   /* let message = $("#message-input").val();
    let data = {
        message: message
    };
    let sent = `<div class="chat-box-body-send">
                <p>${message}</p>
                <span>12:00</span>
            </div>`;
            $("#chat-box-content").append(sent);
    $("#message-input").val("");
    // add message to the list
    let data_url = window.main_url+"chat/send/";
    $.post({url: data_url,data:data, success: (result) => {
        if (result.success) {
            
            let reply = `<div class="chat-box-body-receive">
                <p>${result.reply}</p>
                <span>12:00</span>
            </div>`;
            $("#chat-box-content").append(reply);
        } 
    }})*/
})

$(document).ready(function() {
    let socket = new WebSocket(
        `ws://127.0.0.1:8000/ws/users/3/chat/`
      );
      
      $("#send-message").click(() => {
        // let message = $("#message-input").val();
        const msg = {
            type: "message",
            text: document.getElementById("message-input").value,
            id: clientID,
            date: Date.now(),
          };
        let sent = `<div class="chat-box-body-send">
                    <p>${message}</p>
                    <span>12:00</span>
                </div>`;
                $("#chat-box-content").append(sent);
        $("#message-input").val("");
        // add message to the list
        // let data_url = window.main_url+"chat/send/";
        // $.post({url: data_url,data:data, success: (result) => {
        //     if (result.success) {
                
        //         let reply = `<div class="chat-box-body-receive">
        //             <p>${result.reply}</p>
        //             <span>12:00</span>
        //         </div>`;
        //         $("#chat-box-content").append(reply);
        //     } 
        // }})
        socket.send(JSON.stringify(msg));
    })

      socket.onopen = (event) => {
        const msg = {
            type: "message",
            text: document.getElementById("message-input").value,
            id: clientID,
            date: Date.now(),
          };
          socket.send(JSON.stringify(msg));
      };
      socket.onmessage = (event) => {
        console.log(event.data);
      };
})