function permutations(A) {
  const result = [];
  function visit(first) {
    if (first === A.length) {
      result.push(A.slice());
      return;
    }
    for (let i = first; i < A.length; i++) {
      [A[first], A[i]] = [A[i], A[first]];
      visit(first + 1);
      [A[first], A[i]] = [A[i], A[first]];
    }
  }
  visit(0);
  return result;
}

module.exports = { permutations };
