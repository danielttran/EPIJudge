'use strict';
function Calculate(expression) {
  let total = 0,
    term = 0,
    operator = "+",
    index = 0;
  while (index < expression.length) {
    let number = 0;
    while (index < expression.length && expression[index] >= "0" && expression[index] <= "9") {
      number = number * 10 + expression.charCodeAt(index) - 48;
      ++index;
    }
    if (operator === "+") {
      total += term;
      term = number;
    } else if (operator === "-") {
      total += term;
      term = -number;
    } else if (operator === "*") term *= number;
    else term /= number;
    if (index < expression.length) operator = expression[index++];
  }
  return total + term;
}

module.exports = {Calculate};
