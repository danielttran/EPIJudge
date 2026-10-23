'use strict';
function KthMultiple357(k) {
  const values = [1];
  let third = 0,
    fifth = 0,
    seventh = 0;
  for (let i = 0; i < k; ++i) {
    const a = values[third] * 3,
      b = values[fifth] * 5,
      c = values[seventh] * 7,
      value = Math.min(a, b, c);
    values.push(value);
    if (value === a) ++third;
    if (value === b) ++fifth;
    if (value === c) ++seventh;
  }
  return values[k];
}
