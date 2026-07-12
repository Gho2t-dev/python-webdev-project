// While loops repeat certain code until a condition is true

let username = "";

while(username === "" || username === null){
    username = window.prompt("Enter a username");
}

console.log(`Welcome ${username}`);