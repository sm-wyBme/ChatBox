document.querySelector('#room-name-input').focus();
document.querySelector('#room-name-input').onkeyup = function (e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#room-name-submit').click();
    }
};

document.querySelector('#room-name-submit').onclick = function (e) {
    var roomName = document.querySelector('#room-name-input').value;
    if (roomName == "") {
        alert('Room Name Cannot be Empty');
    } else {
        window.location.pathname = '/chat/' + roomName + '/';        
    }
};