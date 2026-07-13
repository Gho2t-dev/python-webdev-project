// Test api calling with quotes API

const connectBtn = document.getElementById("connectBtn");

connectBtn.onclick = function(){
    fetch("http://127.0.0.1:8000/")
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error(error));
}