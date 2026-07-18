// Test api calling with quotes API

const welcomeMessage = document.getElementById("welcomeMessage");
const APIauthor = document.getElementById("APIauthor");
const connectBtn = document.getElementById("connectBtn");
const submitQuoteIdBtn = document.getElementById("submitQuoteIdBtn");
const quoteId = document.getElementById("quoteId");
const quoteOutput = document.getElementById("quoteOutput");
const quoteAuthor = document.getElementById("quoteAuthor");
const quoteYear = document.getElementById("quoteYear");


connectBtn.onclick = function(){
    fetch("http://127.0.0.1:8000/")
    .then(response => {

        if(!response.ok){
            throw new Error("The resource you tried to access does not exist");
        }
        return response.json();

    })
    .then(
        data => {
            welcomeMessage.textContent = data.Message;
            APIauthor.textContent = "Built buy: " + data.Built_by;
        })
    .catch(error => console.error(error));
}

submitQuoteIdBtn.onclick = function(){
    console.log(typeof quoteId)
    fetch(`http://127.0.0.1:8000/quotes/${quoteId.value}`)
    .then(response => {

        if(!response.ok){
            quoteOutput.textContent = "The Quote you tried to view does not exist";
            quoteAuthor.textContent = "";
            quoteYear.textContent = "";
            throw new Error("The resource you tried to access does not exist");
        }
        return response.json();

    })
    .then(data => { // all the data must be passed in one .then clause as by doing data.quote for example the .then passes that on
    // each .then() passes its return value to the next one. quoteOutput.textContent = data.quote returns the string i assigned
    quoteOutput.textContent = "Quote: " + data.quote;
    quoteAuthor.textContent = "Author: " + data.author;
    quoteYear.textContent = "Year: " + data.year;
    })
    .catch(error => console.error(error));
}