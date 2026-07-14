// Test api calling with quotes API

const welcomeMessage = document.getElementById("welcomeMessage");
const connectBtn = document.getElementById("connectBtn");
const submitQuoteIdBtn = document.getElementById("submitQuoteIdBtn");
const quoteId = document.getElementById("quoteId");
const quoteOutput = document.getElementById("quoteOutput");

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

submitQuoteIdBtn.onclick = function(){
     fetch(`http://127.0.0.1:8000/quotes/${quoteId}`)
    .then(response => {

        if(!response.ok){
            throw new Error("The resource you tried to access does not exist");
        }
        return response.json();

    })
    .then(data => quoteOutput.textContent = data)
    .catch(error => console.error(error));
}