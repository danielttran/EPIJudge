function deleteDuplicates(A) {
  const result = [];
  for (const value of A)
    if (!result.length || result.at(-1) !== value) result.push(value);
  return result;
}

module.exports = { deleteDuplicates };
