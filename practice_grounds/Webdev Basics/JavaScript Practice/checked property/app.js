// The .checked property determines if a checkbox is active or a radio 
// element is selected

const myCheckbox = document.getElementById("myCheckbox");
const visaBtn = document.getElementById("visaBtn");
const masterCardBtn = document.getElementById("masterCardBtn");
const twintBtn = document.getElementById("twintBtn");
const mySubmit = document.getElementById("mySubmit");
const readyResult = document.getElementById("readyResult");
const paymentType = document.getElementById("paymentType");

mySubmit.onclick = function(){

    if(myCheckbox.checked){
        readyResult.textContent = "You are ready to develop with JavaScript!";
    }
    else{
        readyResult.textContent = "You still need to learn a few things, keep going!";        
    }

    if(visaBtn.checked){
        paymentType.textContent = "You have selected Visa as your prefered way of payment";
    }
    else if(masterCardBtn.checked){
        paymentType.textContent = "You have selected MasterCard as your prefered way of payment";
    }
    else if(twintBtn.checked){
        paymentType.textContent = "You have selected Twint as your prefered way of payment";
    }
    else{
        paymentType.textContent = "You have not selected a prefered way of payment";
    }
}