// create get the room name 
const roomName = JSON.parse(document.getElementById('room-name').textContent); 
const chatLog = document.querySelector('#chat-log');

//if chatLog is empty
if (!chatLog.hasChildNodes()) {

    const emptyText = document.createElement('div')
    emptyText.id = 'emptyText'
    emptyText.innerText = 'No Messages'
    emptyText.className = 'emptyText'
    chatLog.appendChild(emptyText)
}

// create a web socket
const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
);

//when we get a message
chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    // document.querySelector('#chat-log').value += (data.message + '\n');  //adding to the chat logs

    //creating a child element to add new message to the chat logs 
    const messageElement = document.createElement('div')
    const userId = data.userId
    const loggedInUserId = JSON.parse(document.getElementById('user-id').textContent); 
    messageElement.innerText = data.message

    //checking whether the message belong to logged-in user or not
    if (userId === loggedInUserId) {
        messageElement.classList.add('message', 'sender')
    } else {
        messageElement.classList.add('message', 'receiver')
    }
    // messageElement.className = 'message'
    chatLog.appendChild(messageElement)

    if (document.querySelector('#emptyText')) {
        document.querySelector('#emptyText').remove()
    }
};

//when the socket gets closed 
chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};


document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;

    //sending the message through the chat socket
    chatSocket.send(JSON.stringify({
        'message': message
    }));
    messageInputDom.value = '';
};