class CircularQueue {
  constructor(capacity = 1) {
    this.buffer = Array(Math.max(1, capacity)).fill(0);
    this.head = 0;
    this.count = 0;
  }
  enqueue(value) {
    if (this.count === this.buffer.length) {
      const larger = Array(this.buffer.length * 2).fill(0);
      for (let i = 0; i < this.count; i++)
        larger[i] = this.buffer[(this.head + i) % this.buffer.length];
      this.buffer = larger;
      this.head = 0;
    }
    this.buffer[(this.head + this.count) % this.buffer.length] = value;
    this.count++;
  }
  dequeue() {
    if (!this.count) throw new RangeError("Empty queue");
    const value = this.buffer[this.head];
    this.head = (this.head + 1) % this.buffer.length;
    this.count--;
    return value;
  }
  size() {
    return this.count;
  }
}
module.exports = { CircularQueue };
