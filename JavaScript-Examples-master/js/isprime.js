function isPrimeFocus(where) {
    var buttonEl = document.getElementById("is-prime-button");
    buttonEl.innerHTML = "Is Prime?";
    buttonEl.style.backgroundColor = "LightBlue";
}
function isPrimeClick(where) {
    var inputEl = document.getElementById("number");
    var numStr = inputEl.value;
    var number = parseInt(numStr);

    var answer;
    var color;
    if (isNaN(number)) {
        answer = "¿%^@!?";
        color = "Yellow";
    } else if (isPrime(number)) {
        answer = "\u2713";  // checkmark
        color = "LawnGreen";
    } else {
        answer = "\u2A02";  // X symbol
        color = "Red";
    }
    var buttonEl = document.getElementById("is-prime-button");
    buttonEl.innerHTML = answer;
    buttonEl.style.backgroundColor = color;
}

function isPrime(x) {
    if (x <= 1) return false;
    for (var i = 2; i < x; i++) {
        if (x % i == 0) {
            return false;
        }
    }
    return true;
}

