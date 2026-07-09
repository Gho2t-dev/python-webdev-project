/*

console.log(`hello`)
console.log(`i like pizza`)

//window.alert('warning')

// This is a comment
// Semocolon ; is not neccesary but can cause bugs so better to write it.
document.getElementById('Title').textContent = 'Welcome to my Website';
document.getElementById('TitleParagraph').textContent = 'This is a first JS test'

// Rule: Double/single Quotes ' or "" for strings
// `` for interpolation or multiline strings

// Variablen definieren:
let x;
x = 100;
// OR
let age = 22;
console.log(`You are ${age} years old`);
console.log(typeof age); // get datatype

// Display Variables in my Page
let fullname = "Fabian Harrab";
let age = 22;
let isStudent = true;

document.getElementById("p1").textContent = `My name is ${fullname}`;
document.getElementById("p2").textContent = `I am ${age} old`;
document.getElementById("p3").textContent = `In school? ${isStudent}`;


//How to accept userinput
//Easy Way
let username = window.prompt("Username:");
console.log(username)
*/

//Better way:
let username;
document.getElementById("mySubmit").onclick = function(){
    username = document.getElementById("myText").value;
    document.getElementById("myH1").textContent = `Welcome ${username}`
};

/*
//Type conversion
let age = window.prompt("How old are you?");
age = Number(age);
age += 1;

*/

//