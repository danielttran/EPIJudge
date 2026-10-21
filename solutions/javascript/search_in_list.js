function searchList(L, key) {
  for (let node = L; node; node = node.next) if (node.data === key) return key;
  return -1;
}

module.exports = { searchList };
