function evaluate(expression) {
  const stack = [];
  for (const token of expression.split(",")) {
    if (/^[+-]?\d+$/.test(token)) {
      stack.push(BigInt(token));
      continue;
    }
    const right = stack.pop(),
      left = stack.pop();
    let value;
    switch (token) {
      case "+":
        value = left + right;
        break;
      case "-":
        value = left - right;
        break;
      case "*":
        value = left * right;
        break;
      case "/":
        value = left / right;
        break;
      default:
        throw new Error("Unknown operator");
    }
    stack.push(value);
  }
  return Number(stack.pop());
}

module.exports = { evaluate };
