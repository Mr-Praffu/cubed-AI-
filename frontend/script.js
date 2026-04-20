function addMessage(text, className) {
    const chatBox = document.getElementById("chat-box");

    const div = document.createElement("div");
    div.className = `message ${className}`;
    div.innerText = text;

    chatBox.appendChild(div);

    chatBox.scrollTop = chatBox.scrollHeight;
}

function handleKey(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}

async function sendMessage() {
    const input = document.getElementById("user-input");
    const message = input.value.trim();

    if (!message) return;

    addMessage(message, "user");
    input.value = "";

    // typing indicator
    addMessage("Typing...", "bot");

    try {
        const response = await fetch("http://127.0.0.1:8000/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message })
        });

        const data = await response.json();

        // remove "Typing..."
        const chatBox = document.getElementById("chat-box");
        chatBox.removeChild(chatBox.lastChild);

        addMessage(data.reply || "Error", "bot");

    } catch (err) {
        addMessage("Server error", "bot");
    }
}