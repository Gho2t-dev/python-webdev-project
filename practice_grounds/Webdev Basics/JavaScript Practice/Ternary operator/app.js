// a shortcut to if else statements assigns variable based on condtion
// condition ? codeiftrue : codeiffalse;

let age = 22;
let adult = age >= 18 ? "You are over 18" : "You are under 18"
console.log(adult)

let time = 16;
let greeting = time < 12 ? "Good Morning" : "Good Afternoon"
console.log(greeting)

let isStudent = true;
let message = isStudent ? "You are a student" : "You are NOT a student"
console.log(message)

// Very cool

let purchaseAmount = 125;
let discount = purchaseAmount >= 100 ? 10 : 0;
console.log(`Your total is $${purchaseAmount - purchaseAmount * (discount / 100)}`)