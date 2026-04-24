var socket = io();
var nickname = "";

// Elements
const nicknameInput = document.getElementById("nickname");
const joinBtn = document.getElementById("joinBtn");
const messageInput = document.getElementById("message");
const sendBtn = document.getElementById("sendBtn");
const messages = document.getElementById("messages");
const chatArea = document.getElementById("chat-area");
const userList = document.getElementById("user-list");

// ---------------------
// JOIN CHAT
// ---------------------
function joinChat() {
    let name = nicknameInput.value.trim();

    if (!name) {
        alert("Enter nickname first!");
        return;
    }

    nicknameInput.value = "";

    // ADMIN CHECK
    if (name.toLowerCase() === "admin") {
        let pass = prompt("Enter admin password:");

        if (pass !== "1234") {
            alert("Wrong password!");
            return;
        }
    }

    nickname = name;

    socket.emit("join", { nickname: nickname });
    chatArea.style.display = "flex";
}


// ---------------------
// SEND MESSAGE
// ---------------------
function sendMessage() {
    let msg = messageInput.value;

    if (!msg.trim()) return;

    socket.send(msg);
    messageInput.value = "";
}

// ---------------------
// RECEIVE MESSAGE
// ---------------------
socket.on("message", function(data) {
    let name = data.user;
    let text = data.text;

    // -------------------------
    // JOIN / LEAVE
    // -------------------------
    if (text.includes("joined the chat")) {
        let joinName = text.split(" ")[0];

        // add to user list 
        let exists = Array.from(userList.children).some(
            (el) => el.innerText === joinName,
        );

        if (!exists) {
            let userDiv = document.createElement("div");
            userDiv.classList.add("nick");
            userDiv.innerText = joinName;
            userList.appendChild(userDiv);
        }

        // show join message
        let div = document.createElement("div");
        div.classList.add("message", "left");
        div.innerText = text;

        messages.appendChild(div);
        messages.scrollTop = messages.scrollHeight;
        return;
    }

    // -------------------------
    // NORMAL MESSAGE WRAPPER
    // -------------------------
    let wrapper = document.createElement("div");

    wrapper.style.display = "flex";
    wrapper.style.flexDirection = "column";
    wrapper.style.margin = "6px 0";

    if (name === nickname) {
        wrapper.style.alignItems = "flex-end";
    } else {
        wrapper.style.alignItems = "flex-start";
    }

    // -------------------------
    // USERNAME 
    // -------------------------
    let nameDiv = document.createElement("div");
    nameDiv.innerText = name;

    nameDiv.style.fontSize = "13px";
    nameDiv.style.fontWeight = "600";
    nameDiv.style.color = "#075e54";
    nameDiv.style.marginBottom = "3px";

    // -------------------------
    // MESSAGE BUBBLE
    // -------------------------
    let msgDiv = document.createElement("div");
    msgDiv.classList.add("message");

    if (name === nickname) {
        msgDiv.classList.add("right");
    } else {
        msgDiv.classList.add("left");
    }

    msgDiv.innerText = text;

    // -------------------------
    // APPEND
    // -------------------------
    wrapper.appendChild(nameDiv);
    wrapper.appendChild(msgDiv);

    messages.appendChild(wrapper);
    messages.scrollTop = messages.scrollHeight;
});
// ---------------------
// EVENT LISTENERS
// ---------------------

// Join button
joinBtn.addEventListener("click", joinChat);

// Send button
sendBtn.addEventListener("click", sendMessage);

// ENTER 
nicknameInput.addEventListener("keypress", function(e) {
    if (e.key === "Enter") {
        joinChat();
    }
});

// ENTER 
messageInput.addEventListener("keypress", function(e) {
    if (e.key === "Enter") {
        sendMessage();
    }
});