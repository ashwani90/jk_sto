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
    let chat_room_id = document.getElementById("chat_room_id").value;
    let chat_user_id = document.getElementById("chat_user_id").value;
    let data_url = window.main_url+"api/get_messages/";
        $.get({url: data_url, success: (result) => {
            
            if (result.success) { 
                console.log(result.messages);
                let messages = result.messages;
                for (let i=0;i<messages.length;i++) {
                    let sent = '';
                    let msgt = messages[i].message;
                    if (messages[i].user_id == chat_user_id) {
                        sent = `<div class="chat-box-body-send">
                                <p>${msgt}</p>
                                <span>12:00</span>
                            </div>`;
                            
                    } else {
                        sent = `<div class="chat-box-body-receive">
                            <p>${msgt}</p>
                            <span>12:00</span>
                        </div>`;
                    }
                    $("#chat-box-content").append(sent);
                }
            } 
        }})
    
    let socket = new WebSocket(
        `ws://127.0.0.1:8000/ws/users/3/chat/`
      );
      
      $("#send-message").click(() => {
        // let message = $("#message-input").val();
        let msgt = document.getElementById("message-input").value;
        
        const msg = {
            action: "message",
            message: document.getElementById("message-input").value,
            user: chat_user_id,
            date: Date.now(),
            roomId: chat_room_id
          };
        let sent = `<div class="chat-box-body-send">
                    <p>${msgt}</p>
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
            action: "message",
            message: document.getElementById("message-input").value,
            user: chat_user_id,
            date: Date.now(),
            roomId: chat_room_id
          };
          socket.send(JSON.stringify(msg));
      };
      socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.message && data.user != chat_user_id) {
            let msgt = data.message;
            let sent = `<div class="chat-box-body-receive">
                    <p>${msgt}</p>
                    <span>12:00</span>
                </div>`;
            $("#chat-box-content").append(sent);
        }
        
      };
})