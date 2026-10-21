function multiply(num1, num2) {
  if (!num1.length || !num2.length) return [0];
  const negative = num1[0] < 0 !== num2[0] < 0,
    digits = Array(num1.length + num2.length).fill(0);
  for (let i = num1.length - 1; i >= 0; i--)
    for (let j = num2.length - 1; j >= 0; j--) {
      const value = digits[i + j + 1] + Math.abs(num1[i]) * Math.abs(num2[j]);
      digits[i + j + 1] = value % 10;
      digits[i + j] += Math.floor(value / 10);
    }
  let first = 0;
  while (first + 1 < digits.length && digits[first] === 0) first++;
  const result = digits.slice(first);
  if (negative && result[0] !== 0) result[0] = -result[0];
  return result;
}

module.exports = { multiply };
