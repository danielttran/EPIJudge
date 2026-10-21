function decomposeIntoDictionaryWords(domain, dictionary) {
  dictionary = new Set(dictionary);
  const previous = Array(domain.length + 1).fill(-1);
  previous[0] = 0;
  for (let end = 1; end <= domain.length; end++)
    for (let start = 0; start < end; start++)
      if (previous[start] !== -1 && dictionary.has(domain.slice(start, end))) {
        previous[end] = start;
        break;
      }
  if (previous.at(-1) === -1) return [];
  const words = [];
  for (let end = domain.length; end > 0; end = previous[end])
    words.push(domain.slice(previous[end], end));
  return words.reverse();
}

module.exports = { decomposeIntoDictionaryWords };
