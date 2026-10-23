'use strict';
class LRUCache {
  constructor(capacity) {
    this.capacity = capacity;
    this.entries = new Map();
  }
  Get(key) {
    if (!this.entries.has(key)) return null;
    const value = this.entries.get(key);
    this.entries.delete(key);
    this.entries.set(key, value);
    return value;
  }
  Set(key, value) {
    this.entries.delete(key);
    this.entries.set(key, value);
    if (this.entries.size > this.capacity) this.entries.delete(this.entries.keys().next().value);
  }
}

module.exports = {LRUCache};
