function plusOne(A) {
  const result = A.slice();
  let index = result.length - 1;
  while (index >= 0 && result[index] === 9) result[index--] = 0;
  if (index >= 0) result[index]++;
  else result.unshift(1);
  return result;
}

module.exports = { plusOne };
