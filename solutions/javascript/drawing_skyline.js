function computeSkyline(buildings) {
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
  const changes = new Map();
  function add(position, height, delta) {
    if (!changes.has(position)) changes.set(position, []);
    changes.get(position).push([height, delta]);
  }
  for (const [left, right, height] of buildings) {
    add(left, height, 1);
    add(right + 1, height, -1);
  }
  const counts = new Map(),
    heights = new Heap((a, b) => b - a),
    result = [];
  let previous = null,
    currentHeight = 0;
  for (const position of [...changes.keys()].sort((a, b) => a - b)) {
    if (previous !== null && previous < position) {
      const left = previous,
        right = position - 1,
        last = result.at(-1);
      if (last && last[2] === currentHeight && last[1] + 1 === left)
        last[1] = right;
      else result.push([left, right, currentHeight]);
    }
    for (const [height, delta] of changes.get(position)) {
      const count = (counts.get(height) || 0) + delta;
      if (count === 0) counts.delete(height);
      else counts.set(height, count);
      if (delta > 0) heights.push(height);
    }
    while (heights.size && !counts.has(heights.peek())) heights.pop();
    currentHeight = heights.size ? heights.peek() : 0;
    previous = position;
  }
  return result;
}

module.exports = { computeSkyline };
