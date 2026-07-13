// Test api calling with quotes API

const welcomeMessage = document.getElementById("welcomeMessage");
const connectBtn = document.getElementById("connectBtn");

connectBtn.onclick = function(){
    fetch("http://127.0.0.1:8000/")
    .then(response => {

        if(!response.ok){
            throw new error("The resource you tried to access does not exist");
        }
        return response.json();

    })
    .then(data => welcomeMessage.textContent = data.Message)
    .catch(error => console.error(error));
}