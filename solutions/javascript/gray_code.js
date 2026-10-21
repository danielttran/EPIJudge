function grayCode(numBits) {
  const result = [];
  for (let value = 0; value < 2 ** numBits; value++)
    result.push(value ^ (value >>> 1));
  return result;
}

module.exports = { grayCode };
