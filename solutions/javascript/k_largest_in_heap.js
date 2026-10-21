function kLargestInBinaryHeap(A, k) {
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
  const result = [];
  if (!A.length || !k) return result;
  const candidates = new Heap((a, b) => A[b] - A[a]);
  candidates.push(0);
  while (result.length < k && candidates.size) {
    const index = candidates.pop();
    result.push(A[index]);
    const left = 2 * index + 1,
      right = left + 1;
    if (left < A.length) candidates.push(left);
    if (right < A.length) candidates.push(right);
  }
  return result;
}

module.exports = { kLargestInBinaryHeap };
