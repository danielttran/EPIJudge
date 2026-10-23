'use strict';
class BitArray { Size(){throw new Error("Provided by the judge");} FetchBit(index,column){throw new Error("Provided by the judge");} }
function MissingNumberBits(numbers) {
  let current = Array.from({ length: numbers.Size() }, (_, i) => i),
    answer = 0,
    column = 0;
  while (current.length && column < 32) {
    const zeros = [],
      ones = [];
    for (const index of current) (numbers.FetchBit(index, column) === 0 ? zeros : ones).push(index);
    if (zeros.length <= ones.length) current = zeros;
    else {
      answer |= 1 << column;
      current = ones;
    }
    ++column;
  }
  return answer;
}
