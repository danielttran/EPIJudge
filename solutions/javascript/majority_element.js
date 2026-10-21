function majoritySearch(stream) {
  let candidate = "",
    balance = 0;
  for (const value of stream) {
    if (!balance) candidate = value;
    balance += value === candidate ? 1 : -1;
  }
  return candidate;
}

module.exports = { majoritySearch };
