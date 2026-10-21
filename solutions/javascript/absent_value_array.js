function findMissingElement(stream) {
  const present = new Set(stream);
  let candidate = 0;
  while (present.has(candidate)) candidate++;
  return candidate;
}

module.exports = { findMissingElement };
