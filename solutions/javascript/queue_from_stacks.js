class QueueFromStacks {
  constructor() {
    this.incoming = [];
    this.outgoing = [];
  }
  enqueue(value) {
    this.incoming.push(value);
  }
  dequeue() {
    if (!this.outgoing.length)
      while (this.incoming.length) this.outgoing.push(this.incoming.pop());
    if (!this.outgoing.length) throw new RangeError("Empty queue");
    return this.outgoing.pop();
  }
}
module.exports = { QueueFromStacks };
