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
class ThreeStacks {
  constructor(capacity) {
    if (capacity < 1 || capacity > 256) throw new BankError("capacity");
    this._capacity = capacity;
    this._values = Array(3 * capacity).fill(0);
    this._sizes = [0, 0, 0];
  }
  _check(stack) {
    if (stack < 0 || stack >= 3) throw new BankError("index");
  }
  Push(stack, value) {
    this._check(stack);
    if (this._sizes[stack] === this._capacity) throw new BankError("full");
    this._values[stack * this._capacity + this._sizes[stack]] = value;
    ++this._sizes[stack];
  }
  Pop(stack) {
    this._check(stack);
    if (!this._sizes[stack]) throw new BankError("empty");
    --this._sizes[stack];
    return this._values[stack * this._capacity + this._sizes[stack]];
  }
  Peek(stack) {
    this._check(stack);
    if (!this._sizes[stack]) throw new BankError("empty");
    return this._values[stack * this._capacity + this._sizes[stack] - 1];
  }
  IsEmpty(stack) {
    this._check(stack);
    return this._sizes[stack] === 0;
  }
  IsFull(stack) {
    this._check(stack);
    return this._sizes[stack] === this._capacity;
  }
}

module.exports = {BankError,IntStack,Animal,ThreeStacks};
