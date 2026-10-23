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
class SetOfStacks {
  constructor(capacity) {
    if (capacity < 1 || capacity > 256) throw new BankError("capacity");
    this._capacity = capacity;
    this._stacks = [];
  }
  Push(value) {
    if (!this._stacks.length || this._stacks.at(-1).length === this._capacity)
      this._stacks.push([]);
    this._stacks.at(-1).push(value);
  }
  Pop() {
    if (!this._stacks.length) throw new BankError("empty");
    const value = this._stacks.at(-1).pop();
    if (!this._stacks.at(-1).length) this._stacks.pop();
    return value;
  }
  PopAt(index) {
    if (index < 0 || index >= this._stacks.length) throw new BankError("index");
    const value = this._stacks[index].pop();
    for (let i = index; i + 1 < this._stacks.length; ++i)
      this._stacks[i].push(this._stacks[i + 1].shift());
    if (!this._stacks.at(-1).length) this._stacks.pop();
    return value;
  }
  IsEmpty() {
    return this._stacks.length === 0;
  }
}

module.exports = {BankError,IntStack,Animal,SetOfStacks};
