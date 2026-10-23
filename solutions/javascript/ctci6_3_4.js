'use strict';
class BankError extends Error { constructor(code) { super(code); this.Code=code; } }
class IntStack {
    constructor() { this._values=[]; }
    Push(value) { this._values.push(value); }
    Pop() { if(!this._values.length) throw new BankError('empty'); return this._values.pop(); }
    Peek() { if(!this._values.length) throw new BankError('empty'); return this._values.at(-1); }
    IsEmpty() { return this._values.length===0; }
}
class Animal { constructor(id,species) { this.Id=id; this.Species=species; Object.freeze(this); } }
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

module.exports = {BankError,IntStack,Animal,TwoStackQueue};
