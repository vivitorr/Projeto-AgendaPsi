const divMessage = document.querySelector(".alert");

const msg = "Conta criada!";

(function (win, doc){
    "use strict";

    const message = document.createElement("div");
    message.classList.add("message");
    message.innerText = msg;
    divMessage.appendChild(message);

    setTimeout(()=>{
        message.style.display = "none";
    }, 4000);
})(window, document)