const inputBox = document.getElementById("user-input");
const sendButton = document.getElementById("send-button");
const chatBox = document.getElementById("chat-box");
inputBox.addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        sendButton.click();
    }
});

sendButton.addEventListener("click", function () {
    const userMessage = inputBox.value;
    inputBox.value = "";

    const userMessageElement = document.createElement("div");
    userMessageElement.classList.add("user-message");
    userMessageElement.textContent = userMessage;
    chatBox.appendChild(userMessageElement);

    fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: userMessage })
    })
        .then(response => response.json())
        .then(data => {
            if (data.reply) {
                const botReply = data.reply;

                const botMessageElement = document.createElement("div")
                botMessageElement.classList.add("bot-message")
                botMessageElement.textContent = botReply;
                chatBox.appendChild(botMessageElement);
                chatBox.scrollTop = chatBox.scrollHeight;
            } else if (data.error) {
                const errorMessageElement = document.createElement("div");
                errorMessageElement.classList.add("bot-message");
                errorMessageElement.textContent = "Error: " + data.error;
                chatBox.appendChild(errorMessageElement);
            }
        })

        .catch(error => {
            console.error(`Error talking to the backend at http://127.0.0.1:5000/chat:)`, error);

            const errorMessageElement = document.createElement("div");
            errorMessageElement.classList.add("bot-message");
            errorMessageElement.textContent = "Sorry, I couldn't connect to the server. Please try again later"
            chatBox.appendChild(errorMessageElement);
        });
});

document.addEventListener('DOMContentLoaded', function () {
    const chatToggle = document.getElementById('chat-toggle');
    const chatContainer = document.getElementById('chat-container');
    const closeChat = document.getElementById('close-chat');
    const inputBox = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");
    const chatBox = document.getElementById("chat-box");

    chatToggle.addEventListener('click', function () {
        if (chatContainer.style.display === 'block') {
            chatContainer.style.display = 'none';
        } else {
            chatContainer.style.display = 'block';
            inputBox.focus();
        }
    });

    closeChat.addEventListener('click', function () {
        chatContainer.style.display = 'none';
    });

    chatContainer.style.display = 'none';

    inputBox.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            sendButton.click();
        }
    });

    sendButton.addEventListener("click", function () {
        const userMessage = inputBox.value;
        if (!userMessage.trim()) return;

        inputBox.value = "";

        const userMessageElement = document.createElement("div");
        userMessageElement.classList.add("user-message");
        userMessageElement.textContent = userMessage;
        chatBox.appendChild(userMessageElement);

        chatBox.scrollTop = chatBox.scrollHeight;

        fetch("http://127.0.0.1:5000/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: userMessage })
        })
            .then(response => response.json())
            .then(data => {
                if (data.reply) {
                    const botMessageElement = document.createElement("div");
                    botMessageElement.classList.add("bot-message");
                    botMessageElement.textContent = data.reply;
                    chatBox.appendChild(botMessageElement);

                    chatBox.scrollTop = chatBox.scrollHeight;
                } else if (data.error) {

                    const errorMessageElement = document.createElement("div");
                    errorMessageElement.classList.add("bot-message");
                    errorMessageElement.textContent = "Error: " + data.error;
                    chatBox.appendChild(errorMessageElement);
                }
            })
            .catch(error => {
                console.error(`Error talking to backend at http://127.0.0.1:5000/chat:`, error);

                const errorMessageElement = document.createElement('div');
                errorMessageElement.classList.add("bot-message");
                errorMessageElement.textContent = "Sorry, I couldn't connect to the server. Please try again later";
                chatBox.appendChild(errorMessageElement);

                chatBox.scrollTop = chatBox.scrollHeight;
            });
    });
});