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
function SortStack(stack) {
  const spare = new IntStack();
  while (!stack.IsEmpty()) {
    const value = stack.Pop();
    while (!spare.IsEmpty() && spare.Peek() > value) stack.Push(spare.Pop());
    spare.Push(value);
  }
  while (!spare.IsEmpty()) stack.Push(spare.Pop());
}

module.exports = {BankError,IntStack,Animal,SortStack};
