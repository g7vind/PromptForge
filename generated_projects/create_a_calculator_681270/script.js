let currentInput = '0';
let previousInput = '';
let operator = null;
let shouldResetDisplay = false;

const display = document.getElementById('display');

function updateDisplay() {
    display.textContent = currentInput;
}

function appendNumber(number) {
    if (shouldResetDisplay) {
        currentInput = number;
        shouldResetDisplay = false;
    } else if (currentInput === '0' && number !== '.') {
        currentInput = number;
    } else {
        currentInput += number;
    }
    updateDisplay();
}

function appendDecimal() {
    if (shouldResetDisplay) {
        currentInput = '0.';
        shouldResetDisplay = false;
    } else if (currentInput.includes('.')) {
        return;
    } else {
        currentInput += '.';
    }
    updateDisplay();
}

function clearCalculator() {
    currentInput = '0';
    previousInput = '';
    operator = null;
    shouldResetDisplay = false;
    updateDisplay();
}

function compute() {
    if (previousInput === null || previousInput === '' || operator === null || operator === '') {
        return;
    }

    const prevNum = parseFloat(previousInput);
    let currentNum = parseFloat(currentInput);

    if (isNaN(currentNum)) {
        currentNum = prevNum;
    }

    let result;
    switch (operator) {
        case '+':
            result = prevNum + currentNum;
            break;
        case '-':
            result = prevNum - currentNum;
            break;
        case '*':
            result = prevNum * currentNum;
            break;
        case '/':
            if (currentNum === 0) {
                alert("Cannot divide by zero!");
                clearCalculator();
                return;
            }
            result = prevNum / currentNum;
            break;
        default:
            return;
    }

    currentInput = result.toString();
    operator = null;
    previousInput = '';
    shouldResetDisplay = true;
    updateDisplay();
}

function chooseOperator(nextOperator) {
    if ((currentInput === '' || currentInput === '0') && previousInput === '') {
        return;
    }

    if (previousInput !== '') {
        compute();
    }

    previousInput = currentInput;
    operator = nextOperator;
    shouldResetDisplay = true;
}

updateDisplay();

const numberButtons = document.querySelectorAll('.number');
numberButtons.forEach(button => {
    button.addEventListener('click', () => {
        appendNumber(button.dataset.value);
    });
});

const decimalButton = document.querySelector('.decimal');
decimalButton.addEventListener('click', () => {
    appendDecimal();
});

const clearButton = document.querySelector('.clear');
clearButton.addEventListener('click', () => {
    clearCalculator();
});

const operatorButtons = document.querySelectorAll('.operator');
operatorButtons.forEach(button => {
    button.addEventListener('click', () => {
        chooseOperator(button.dataset.value);
    });
});

const equalsButton = document.querySelector('.equals');
equalsButton.addEventListener('click', () => {
    compute();
});