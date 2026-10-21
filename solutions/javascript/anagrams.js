function findAnagrams(dictionary) {
  const groups = new Map();
  for (const word of dictionary) {
    const key = word.split("").sort().join("");
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(word);
  }
  return [...groups.values()].filter((group) => group.length > 1);
}

module.exports = { findAnagrams };
