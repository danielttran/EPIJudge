'use strict';
class HashTable {
  constructor(capacity) {
    this.buckets = Array(capacity).fill(null);
  }
  index(key) {
    if (typeof key === "number") return (key >>> 0) % this.buckets.length;
    const text = String(key);
    let hash = 2166136261;
    for (let i = 0; i < text.length; ++i)
      hash = Math.imul(hash ^ text.charCodeAt(i), 16777619) >>> 0;
    return hash % this.buckets.length;
  }
  find(key) {
    for (let node = this.buckets[this.index(key)]; node !== null; node = node.next)
      if (node.key === key) return node;
    return null;
  }
  Put(key, value) {
    const node = this.find(key);
    if (node !== null) {
      node.value = value;
      return;
    }
    const slot = this.index(key);
    this.buckets[slot] = { key, value, next: this.buckets[slot] };
  }
  Get(key) {
    const node = this.find(key);
    if (node === null) throw new RangeError("missing");
    return node.value;
  }
  Contains(key) {
    return this.find(key) !== null;
  }
  Remove(key) {
    const slot = this.index(key);
    let previous = null,
      node = this.buckets[slot];
    while (node !== null) {
      if (node.key === key) {
        if (previous === null) this.buckets[slot] = node.next;
        else previous.next = node.next;
        return true;
      }
      previous = node;
      node = node.next;
    }
    return false;
  }
}
