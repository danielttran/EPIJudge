function findClosestElementsInSortedArrays(sorted_arrays) {
  class Heap {
    constructor(compare) {
      this.a = [];
      this.compare = compare;
    }
    get size() {
      return this.a.length;
    }
    peek() {
      return this.a[0];
    }
    push(value) {
      const a = this.a;
      a.push(value);
      let i = a.length - 1;
      while (i) {
        const p = Math.floor((i - 1) / 2);
        if (this.compare(a[p], a[i]) <= 0) break;
        [a[p], a[i]] = [a[i], a[p]];
        i = p;
      }
    }
    pop() {
      const a = this.a;
      if (!a.length) throw new RangeError("Empty heap");
      const result = a[0],
        last = a.pop();
      if (a.length) {
        a[0] = last;
        let i = 0;
        for (;;) {
          let c = 2 * i + 1;
          if (c >= a.length) break;
          if (c + 1 < a.length && this.compare(a[c + 1], a[c]) < 0) c++;
          if (this.compare(a[i], a[c]) <= 0) break;
          [a[i], a[c]] = [a[c], a[i]];
          i = c;
        }
      }
      return result;
    }
  }
  if (!sorted_arrays.length) return 0;
  const minima = new Heap((a, b) => a.value - b.value);
  let maximum = -Infinity;
  for (let i = 0; i < sorted_arrays.length; i++) {
    const value = sorted_arrays[i][0];
    minima.push({ array: i, index: 0, value });
    maximum = Math.max(maximum, value);
  }
  let best = Infinity;
  while (minima.size) {
    const entry = minima.pop();
    best = Math.min(best, maximum - entry.value);
    const next = entry.index + 1;
    if (next === sorted_arrays[entry.array].length) break;
    const value = sorted_arrays[entry.array][next];
    maximum = Math.max(maximum, value);
    minima.push({ array: entry.array, index: next, value });
  }
  return best;
}

module.exports = { findClosestElementsInSortedArrays };
