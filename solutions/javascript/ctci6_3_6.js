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
class AnimalShelter {
  constructor() {
    this._heads = [null, null];
    this._tails = [null, null];
    this._order = 0;
    this._count = 0;
  }
  _oldest() {
    if (this._heads[0] === null) return 1;
    if (this._heads[1] === null) return 0;
    return this._heads[0].order < this._heads[1].order ? 0 : 1;
  }
  _take(slot) {
    const entry = this._heads[slot];
    if (entry === null) return null;
    this._heads[slot] = entry.next;
    if (this._heads[slot] === null) this._tails[slot] = null;
    --this._count;
    return entry.value;
  }
  Enqueue(animal) {
    let slot;
    if (animal.Species === "dog") slot = 0;
    else if (animal.Species === "cat") slot = 1;
    else throw new BankError("species");
    const entry = { value: animal, order: this._order++, next: null };
    if (this._tails[slot] === null) this._heads[slot] = entry;
    else this._tails[slot].next = entry;
    this._tails[slot] = entry;
    ++this._count;
  }
  DequeueAny() {
    return this._take(this._oldest());
  }
  DequeueDog() {
    return this._take(0);
  }
  DequeueCat() {
    return this._take(1);
  }
  Peek() {
    return this._heads[this._oldest()]?.value ?? null;
  }
  Size() {
    return this._count;
  }
}

module.exports = {BankError,IntStack,Animal,AnimalShelter};
