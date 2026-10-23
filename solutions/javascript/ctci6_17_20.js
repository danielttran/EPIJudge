'use strict';
function ContinuousMedians(values) {
  class Heap {
    constructor(before) {
      this.data = [];
      this.before = before;
    }
    push(value) {
      const data = this.data;
      data.push(value);
      let index = data.length - 1;
      while (index > 0) {
        const parent = Math.floor((index - 1) / 2);
        if (!this.before(data[index], data[parent])) break;
        [data[index], data[parent]] = [data[parent], data[index]];
        index = parent;
      }
    }
    pop() {
      const data = this.data,
        result = data[0],
        last = data.pop();
      if (data.length !== 0) {
        data[0] = last;
        let index = 0;
        while (2 * index + 1 < data.length) {
          let child = 2 * index + 1;
          if (child + 1 < data.length && this.before(data[child + 1], data[child])) ++child;
          if (!this.before(data[child], data[index])) break;
          [data[index], data[child]] = [data[child], data[index]];
          index = child;
        }
      }
      return result;
    }
  }
  const lower = new Heap((a, b) => a > b),
    upper = new Heap((a, b) => a < b),
    medians = [];
  for (const value of values) {
    if (lower.data.length === 0 || value <= lower.data[0]) lower.push(value);
    else upper.push(value);
    if (lower.data.length > upper.data.length + 1) upper.push(lower.pop());
    else if (upper.data.length > lower.data.length) lower.push(upper.pop());
    medians.push(
      lower.data.length > upper.data.length ? lower.data[0] : (lower.data[0] + upper.data[0]) / 2,
    );
  }
  return medians;
}

module.exports = {ContinuousMedians};
