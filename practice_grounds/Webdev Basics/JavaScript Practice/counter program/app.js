// Counter app

// HTML elements as constants as they are fixed
const decreaseButton = document.getElementById("decreaseBtn");
const resetButton = document.getElementById("reset");
const increaseButton = document.getElementById("increaseBtn");
const countLabel = document.getElementById("countLabel");

// count as variable as it will contain the restult
let count = 0;

// Increase function
increaseButton.onclick = function(){
    count ++; // Adds 1
    countLabel.textContent = count; // sets countLabel content to the value stored in count variable
}
// STOP FORGETTING THE ;;;;;;;;;;;;;;;

// Decrease function
decreaseButton.onclick = function(){
    count --; // removes 1
    countLabel.textContent = count; // sets countLabel content to the value stored in count variable
}

// Reset function
resetButton.onclick = function(){
    count = 0; // sets count back to 0
    countLabel.textContent = count; // sets countLabel content to the value stored in count variable
}