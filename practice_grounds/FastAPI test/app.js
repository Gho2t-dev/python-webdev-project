// Test api calling with quotes API

const welcomeMessage = document.getElementById("welcomeMessage");
const connectBtn = document.getElementById("connectBtn");
const showAll = document.getElementById("showAll");

connectBtn.onclick = function(){
    fetch("http://127.0.0.1:8000/")
    .then(response => {

        if(!response.ok){
            throw new Error("The resource you tried to access does not exist");
        }
        return response.json();

    })
    .then(data => welcomeMessage.textContent = data.Message)
    .catch(error => console.error(error));
}

showAll.onclick = function(){
    fetch("http://127.0.0.1:8000/quotes", {method: "GET"})
    .then(response => {

        if(!response.ok){ // check if the response is NOT ok
            throw new Error("The resource you tried to access does not exist");
        }
        return response.json(); //turn the response into a js object

    })
    .then(data => console.log(data))
    .catch(error => console.error(error));
}