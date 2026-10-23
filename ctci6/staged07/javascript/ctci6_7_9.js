'use strict';
class CircularArray {
  constructor(initialValues) {
    this.items = initialValues.slice();
    this.head = 0;
  }
  checkIndex(index) {
    if (index < 0 || index >= this.items.length) throw new RangeError("index");
  }
  Get(index) {
    this.checkIndex(index);
    return this.items[(this.head + index) % this.items.length];
  }
  Set(index, value) {
    this.checkIndex(index);
    this.items[(this.head + index) % this.items.length] = value;
  }
  Rotate(shift) {
    const size = this.items.length;
    if (size === 0) return;
    const step = ((shift % size) + size) % size;
    this.head = (this.head + step) % size;
  }
  *[Symbol.iterator]() {
    for (let index = 0; index < this.items.length; ++index)
      yield this.items[(this.head + index) % this.items.length];
  }
}
