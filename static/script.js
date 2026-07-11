const chatBox = document.getElementById("chatBox");

const question = document.getElementById("question");

const sendBtn = document.getElementById("sendBtn");

sendBtn.onclick = sendQuestion;

question.addEventListener("keypress", function(e){

    if(e.key==="Enter"){

        sendQuestion();

    }

});

async function sendQuestion(){

    const text = question.value.trim();

    if(text==="") return;

    chatBox.innerHTML += `

    <div class="user-message">

        ${text}

    </div>

    `;

    question.value="";

    chatBox.innerHTML += `

    <div class="bot-message loading" id="loading">

        AI is thinking...

    </div>

    `;

    chatBox.scrollTop=chatBox.scrollHeight;

    const response = await fetch("/chat",{

        method:"POST",

        headers:{

            "Content-Type":"application/json"

        },

        body:JSON.stringify({

            question:text

        })

    });

    const data = await response.json();

    document.getElementById("loading").remove();

   chatBox.innerHTML += `

<div class="bot-message">

    ${data.answer}

</div>

`;



    chatBox.scrollTop=chatBox.scrollHeight;

}
