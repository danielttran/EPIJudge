function lookAndSay(n) {
  let term = "1";
  for (let step = 1; step < n; step++) {
    const next = [];
    for (let first = 0; first < term.length; ) {
      let end = first + 1;
      while (end < term.length && term[end] === term[first]) end++;
      next.push(String(end - first), term[first]);
      first = end;
    }
    term = next.join("");
  }
  return term;
}

module.exports = { lookAndSay };
