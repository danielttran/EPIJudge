'use strict';
function GroupAnagrams(words) {
  const decorated = words.map((word) => ({ key: [...word].sort().join(""), word }));
  decorated.sort((a, b) => (a.key < b.key ? -1 : a.key > b.key ? 1 : 0));
  for (let i = 0; i < words.length; ++i) words[i] = decorated[i].word;
  return words.slice();
}

module.exports = {GroupAnagrams};
