'use strict';
class BankError extends Error { constructor(code) { super(code); this.Code=code; } }
class TwoStackQueue {
  constructor() {
    this._newest = [];
    this._oldest = [];
  }
  _shift() {
    if (!this._oldest.length) while (this._newest.length) this._oldest.push(this._newest.pop());
  }
  Add(value) {
    this._newest.push(value);
  }
  Remove() {
    this._shift();
    if (!this._oldest.length) throw new BankError("empty");
    return this._oldest.pop();
  }
  Peek() {
    this._shift();
    if (!this._oldest.length) throw new BankError("empty");
    return this._oldest.at(-1);
  }
  Size() {
    return this._newest.length + this._oldest.length;
  }
}
