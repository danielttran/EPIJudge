function encoding(text) {
  const output = [];
  for (let start = 0; start < text.length; ) {
    let end = start + 1;
    while (end < text.length && text[end] === text[start]) end++;
    output.push(String(end - start), text[start]);
    start = end;
  }
  return output.join("");
}
function decoding(encoded) {
  const output = [];
  let count = 0;
  for (const c of encoded) {
    if (c >= "0" && c <= "9") count = count * 10 + Number(c);
    else {
      output.push(c.repeat(count));
      count = 0;
    }
  }
  return output.join("");
}
module.exports = { encoding, decoding };
