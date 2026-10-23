'use strict';
class BankError extends Error { constructor(code) { super(code); this.Code=code; } }
class MinStack {
  constructor() {
    this._top = null;
  }
  Push(value) {
    const minimum = this._top === null ? value : Math.min(value, this._top.minimum);
    this._top = { value, minimum, next: this._top };
  }
  Pop() {
    if (this._top === null) throw new BankError("empty");
    const value = this._top.value;
    this._top = this._top.next;
    return value;
  }
  Peek() {
    if (this._top === null) throw new BankError("empty");
    return this._top.value;
  }
  GetMin() {
    if (this._top === null) throw new BankError("empty");
    return this._top.minimum;
  }
  IsEmpty() {
    return this._top === null;
  }
}
