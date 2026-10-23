'use strict';
function ArrangePeaksValleys(values) {
  for (let i = 1; i < values.length; i += 2) {
    let best = i;
    if (values[i - 1] > values[best]) best = i - 1;
    if (i + 1 < values.length && values[i + 1] > values[best]) best = i + 1;
    [values[i], values[best]] = [values[best], values[i]];
  }
  return values;
}
