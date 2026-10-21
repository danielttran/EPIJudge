function intToString(value) {
  const negative = value < 0;
  let remaining = Math.abs(value);
  const reversed = [];
  do {
    reversed.push(String.fromCharCode(48 + (remaining % 10)));
    remaining = Math.floor(remaining / 10);
  } while (remaining);
  if (negative) reversed.push("-");
  return reversed.reverse().join("");
}
function stringToInt(text) {
  let index = 0,
    negative = false,
    value = 0;
  if (text[0] === "-" || text[0] === "+") {
    negative = text[0] === "-";
    index++;
  }
  for (; index < text.length; index++)
    value = value * 10 + text.charCodeAt(index) - 48;
  return negative ? -value : value;
}
module.exports = { intToString, stringToInt };
