'use strict';
function ReSpace(text, dictionary) {
  const words = new Set(dictionary);
  let maximum = 0;
  for (const word of words) maximum = Math.max(maximum, word.length);
  const cost = new Array(text.length + 1).fill(0),
    previous = new Array(text.length + 1).fill(0);
  for (let end = 1; end <= text.length; ++end) {
    cost[end] = cost[end - 1] + 1;
    previous[end] = end - 1;
    for (let length = 1; length <= maximum && length <= end; ++length) {
      const start = end - length;
      if (words.has(text.slice(start, end)) && cost[start] < cost[end]) {
        cost[end] = cost[start];
        previous[end] = start;
      }
    }
  }
  const result = [];
  for (let end = text.length; end > 0; end = previous[end])
    result.push(text.slice(previous[end], end));
  return result.reverse();
}
