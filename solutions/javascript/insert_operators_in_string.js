function expressionSynthesis(digits, target) {
  target = BigInt(target);
  function search(index, total, last) {
    if (index === digits.length) return total === target;
    let value = 0n;
    for (let end = index; end < digits.length; end++) {
      value = value * 10n + BigInt(digits[end]);
      if (index === 0) {
        if (search(end + 1, value, value)) return true;
      } else if (
        search(end + 1, total + value, value) ||
        search(end + 1, total - last + last * value, last * value)
      )
        return true;
    }
    return false;
  }
  return digits.length > 0 && search(0, 0n, 0n);
}

module.exports = { expressionSynthesis };
