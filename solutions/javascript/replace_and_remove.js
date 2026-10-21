function replaceAndRemove(size, s) {
  const result = [];
  for (let i = 0; i < size; i++) {
    if (s[i] === "a") result.push("d", "d");
    else if (s[i] !== "b") result.push(s[i]);
  }
  return result;
}

module.exports = { replaceAndRemove };
