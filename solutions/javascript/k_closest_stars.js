function findClosestKStars(stars, k) {
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
  const selected = new Heap((a, b) => b - a);
  for (const [x, y, z] of stars) {
    selected.push(x * x + y * y + z * z);
    if (selected.size > k) selected.pop();
  }
  const result = [];
  while (selected.size) result.push(Math.sqrt(selected.pop()));
  return result;
}

module.exports = { findClosestKStars };
