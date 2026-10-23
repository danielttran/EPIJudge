'use strict';
function BinaryFraction(number) {
  if (number <= 0 || number >= 1) return "ERROR";
  const digits = [];
  for (let i = 0; i < 31; ++i) {
    number *= 2;
    const bit = number >= 1;
    digits.push(bit ? "1" : "0");
    if (bit) --number;
    if (number === 0) return "." + digits.join("");
  }
  return "ERROR";
}

module.exports = {BinaryFraction};
