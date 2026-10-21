function countInversions(A) {
  const values = A.slice(),
    temporary = Array(A.length);
  function sort(start, end) {
    if (end - start <= 1) return 0;
    const middle = start + Math.floor((end - start) / 2);
    let count = sort(start, middle) + sort(middle, end),
      i = start,
      j = middle,
      out = start;
    while (i < middle || j < end) {
      if (j === end || (i < middle && values[i] <= values[j]))
        temporary[out++] = values[i++];
      else {
        temporary[out++] = values[j++];
        count += middle - i;
      }
    }
    for (let p = start; p < end; p++) values[p] = temporary[p];
    return count;
  }
  return sort(0, values.length);
}

module.exports = { countInversions };
