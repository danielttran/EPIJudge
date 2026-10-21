function rookAttack(A) {
  const rows = new Set(),
    columns = new Set();
  for (let r = 0; r < A.length; r++)
    for (let c = 0; c < A[r].length; c++)
      if (A[r][c] === 0) {
        rows.add(r);
        columns.add(c);
      }
  for (let r = 0; r < A.length; r++)
    for (let c = 0; c < A[r].length; c++)
      if (rows.has(r) || columns.has(c)) A[r][c] = 0;
  return A;
}

module.exports = { rookAttack };
