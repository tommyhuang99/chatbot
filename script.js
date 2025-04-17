

const inputBox = document.getElementById("user-input");
const sendButton = document.getElementById("send-button");
const chatBox= document.getElementById("chat-box");


sendButton.addEventListener("click", function() {
    const userMessage = inputBox.value;
    console.log("User message:", userMessage);
});

const userMessageElement = document.createElement("div");
userMessageElement.classList.add("user-message");
userMessageElement.textContent = userMessage;
chatBox.appendChild(userMessageElement);

inputBox.value="";

