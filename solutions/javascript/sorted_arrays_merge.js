function mergeSortedArrays(sorted_arrays) {
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
  const candidates = new Heap((a, b) => a.value - b.value),
    result = [];
  for (let i = 0; i < sorted_arrays.length; i++)
    if (sorted_arrays[i].length)
      candidates.push({ array: i, position: 0, value: sorted_arrays[i][0] });
  while (candidates.size) {
    const entry = candidates.pop();
    result.push(entry.value);
    const next = entry.position + 1;
    if (next < sorted_arrays[entry.array].length)
      candidates.push({
        array: entry.array,
        position: next,
        value: sorted_arrays[entry.array][next],
      });
  }
  return result;
}

module.exports = { mergeSortedArrays };
