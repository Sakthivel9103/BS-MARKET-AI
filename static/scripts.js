async function sendMessage(){
    let input = document.getElementById("userinput");
    let message = input.value;
    if(message.trim() === "") 
        return;
    let chatBox = document.getElementById("chat-box");
    chatBox.innerHTML += `
        <div class="user">${message}</div>
    `;
    input.value = "";
    
    let response = await fetch("/chat",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            message:message
        })
    });
    let data = await response.json();
    chatBox.innerHTML += `
        <div class="bot">${data.reply}</div>
    `;
    chatBox.scrollTop = chatBox.scrollHeight;
} 
function startVoice(){
    let recognition = new webkitSpeechRecognition();
    recognition.lang = "ta-IN";
    let inputBox = document.getElementById("userinput");
    inputBox.placeholder = "🎤 Listening...";
    recognition.start();
    recognition.onstart = function(){
        console.log("Voice recording started");
    };
    recognition.onresult = function(event){
        let voiceText = event.results[0][0].transcript;
        inputBox.value = voiceText;
        inputBox.placeholder = "Type message...";
        sendMessage();
    };
    recognition.onerror = function(event){
        alert("Mic Error: " + event.error);
        inputBox.placeholder = "Type message...";
    };
    recognition.onend = function(){
        inputBox.placeholder = "Type message...";
    };
} 
document.getElementById("userinput")
.addEventListener("keydown", function(event){
    if(event.key === "Enter"){sendMessage();}
});

