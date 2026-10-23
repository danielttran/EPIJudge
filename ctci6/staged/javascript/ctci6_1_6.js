'use strict';
function Compress(text) {
  const parts = [];
  for (let start = 0; start < text.length; ) {
    let end = start + 1;
    while (end < text.length && text[end] === text[start]) ++end;
    parts.push(text[start], String(end - start));
    start = end;
  }
  const output = parts.join("");
  return output.length < text.length ? output : text;
}
