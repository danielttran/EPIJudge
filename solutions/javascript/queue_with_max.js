class QueueWithMax {
  constructor() {
    this.values = [];
    this.head = 0;
    this.candidates = [];
    this.first = 0;
  }
  enqueue(value) {
    this.values.push(value);
    while (
      this.candidates.length > this.first &&
      this.candidates.at(-1) < value
    )
      this.candidates.pop();
    this.candidates.push(value);
  }
  dequeue() {
    if (this.head === this.values.length) throw new RangeError("Empty queue");
    const value = this.values[this.head++];
    if (this.candidates[this.first] === value) this.first++;
    if (this.head > 1024 && this.head * 2 > this.values.length) {
      this.values = this.values.slice(this.head);
      this.head = 0;
    }
    if (this.first > 1024 && this.first * 2 > this.candidates.length) {
      this.candidates = this.candidates.slice(this.first);
      this.first = 0;
    }
    return value;
  }
  max() {
    if (this.head === this.values.length) throw new RangeError("Empty queue");
    return this.candidates[this.first];
  }
}
module.exports = { QueueWithMax };
