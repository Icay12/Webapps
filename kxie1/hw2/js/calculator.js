var newValue = 0;
var preValue = 0;
var preOperation = "+";
var preButton = 1; //1:digit 0:operation

function displayChange(x) {
	document.getElementById("display").value = x;
}

function pressDigit(digit) {
	var number = parseInt(digit);
	if(preOperation == "=") {
		newValue = 0;
		preValue = 0;
		preOperation = "+";
	}	
	newValue = newValue*10 + number;
	displayChange(newValue);
	preButton = 1;

}

function  pressOperation(operation) {
	if(preButton == 1) {
		switch(preOperation) {
			case "+":
				preValue = preValue + newValue;
				break;
			case "-":
				preValue = preValue - newValue;
				break;
			case "*":
				preValue = preValue * newValue;
				break;
			case "/":
				if(newValue == 0) {
					preValue = 0;
					operation = "+";
					alert("Can't divide by 0!");
				}
				else
					preValue = parseInt(preValue / newValue);
				break;
			case "=":
				break;
		}
		displayChange(preValue);
		newValue = 0;
		
		if(operation != "=")
			preButton = 0;
	}
	preOperation = operation;

	
	
}

