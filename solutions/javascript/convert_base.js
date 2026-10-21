function convertBase(num_as_string, b1, b2) {
  const digits = "0123456789ABCDEF",
    negative = num_as_string.startsWith("-");
  let value = 0n;
  for (let i = negative ? 1 : 0; i < num_as_string.length; i++)
    value =
      value * BigInt(b1) +
      BigInt(digits.indexOf(num_as_string[i].toUpperCase()));
  if (value === 0n) return "0";
  const result = [];
  while (value > 0n) {
    result.push(digits[Number(value % BigInt(b2))]);
    value /= BigInt(b2);
  }
  if (negative) result.push("-");
  return result.reverse().join("");
}

module.exports = { convertBase };
