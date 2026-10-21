function eliminateDuplicate(names) {
  return [...new Set(names.map((name) => name[0]))];
}

module.exports = { eliminateDuplicate };
