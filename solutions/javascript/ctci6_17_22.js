'use strict';
function WordTransformation(start, stop, dictionary) {
  const words = new Set(dictionary),
    previous = new Map([[start, null]]),
    queue = [start];
  for (let head = 0; head < queue.length; ++head) {
    const word = queue[head];
    if (word === stop) {
      const path = [];
      for (let current = stop; current !== null; current = previous.get(current))
        path.push(current);
      return path.reverse();
    }
    for (let position = 0; position < word.length; ++position)
      for (let code = 97; code <= 122; ++code) {
        const letter = String.fromCharCode(code);
        if (letter === word[position]) continue;
        const candidate = word.slice(0, position) + letter + word.slice(position + 1);
        if (words.has(candidate) && !previous.has(candidate)) {
          previous.set(candidate, word);
          queue.push(candidate);
        }
      }
  }
  return [];
}

module.exports = {WordTransformation};
