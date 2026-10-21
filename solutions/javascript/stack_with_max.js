class StackWithMax {
  constructor() {
    this.entries = [];
  }
  push(value) {
    this.entries.push([
      value,
      this.entries.length ? Math.max(value, this.entries.at(-1)[1]) : value,
    ]);
  }
  pop() {
    if (!this.entries.length) throw new RangeError("Empty stack");
    return this.entries.pop()[0];
  }
  empty() {
    return !this.entries.length;
  }
  max() {
    if (!this.entries.length) throw new RangeError("Empty stack");
    return this.entries.at(-1)[1];
  }
}
module.exports = { StackWithMax };
