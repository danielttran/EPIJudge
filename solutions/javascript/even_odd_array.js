function evenOdd(values) {
  let even = 0;
  for (let unknown = 0; unknown < values.length; unknown++)
    if ((values[unknown] & 1) === 0) {
      [values[even], values[unknown]] = [values[unknown], values[even]];
      even++;
    }
}

module.exports = { evenOdd };
