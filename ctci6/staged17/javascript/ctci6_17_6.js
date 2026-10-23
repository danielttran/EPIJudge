'use strict';
function CountDigitTwos(n) {
  let total = 0;
  for (let place = 1; place <= n; place *= 10) {
    const high = Math.floor(n / (place * 10)),
      digit = Math.floor(n / place) % 10,
      low = n % place;
    total += high * place;
    if (digit === 2) total += low + 1;
    else if (digit > 2) total += place;
  }
  return total;
}
