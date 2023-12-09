const socket = io();

socket.on("connect", function (s) {
  console.log("connect");
});

socket.on("message", function (data) {
  console.log("receive", data);
  appendMessage(data);
});

socket.on("messages", function (data) {
  console.log("receive", data);
  for (const v of data) {
    appendMessage(v);
  }
});

function appendMessage(data) {
  const time = new Date(data.date).toLocaleTimeString();
  const message = data.message;

  const messageEl = document.createElement("pre");
  messageEl.textContent = `${time}: ${message}`;

  const chat = document.getElementById("chat");
  chat.appendChild(messageEl);
}

function handle_message() {
  const input = document.getElementById("message");
  const message = input.value;
  if (message.length == 0) {
    console.log("message is empty, ignore");
    return false;
  }

  input.value = "";

  const data = {
    date: new Date().toISOString(),
    message: message,
  };
  socket.emit("message", data);
  console.log("send", data);
  return false;
}
