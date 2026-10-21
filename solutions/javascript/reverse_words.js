function reverseWords(s) {
  const text = s.split("").reverse();
  for (let start = 0; start < text.length; ) {
    if (text[start] === " ") {
      start++;
      continue;
    }
    let end = start;
    while (end < text.length && text[end] !== " ") end++;
    for (let l = start, r = end - 1; l < r; l++, r--)
      [text[l], text[r]] = [text[r], text[l]];
    start = end;
  }
  return text.join("");
}

module.exports = { reverseWords };
