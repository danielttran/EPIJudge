function phoneMnemonic(phone_number) {
  const letters = [
      "0",
      "1",
      "ABC",
      "DEF",
      "GHI",
      "JKL",
      "MNO",
      "PQRS",
      "TUV",
      "WXYZ",
    ],
    result = [],
    word = Array(phone_number.length);
  function visit(i) {
    if (i === word.length) {
      result.push(word.join(""));
      return;
    }
    for (const c of letters[Number(phone_number[i])]) {
      word[i] = c;
      visit(i + 1);
    }
  }
  visit(0);
  return result;
}

module.exports = { phoneMnemonic };
