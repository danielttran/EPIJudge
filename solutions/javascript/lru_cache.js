class LruCache {
  constructor(capacity) {
    this.limit = capacity;
    this.entries = new Map();
  }
  lookup(isbn) {
    if (!this.entries.has(isbn)) return -1;
    const price = this.entries.get(isbn);
    this.entries.delete(isbn);
    this.entries.set(isbn, price);
    return price;
  }
  insert(isbn, price) {
    if (this.entries.has(isbn)) {
      this.lookup(isbn);
      return;
    }
    if (this.limit <= 0) return;
    if (this.entries.size === this.limit)
      this.entries.delete(this.entries.keys().next().value);
    this.entries.set(isbn, price);
  }
  erase(isbn) {
    return this.entries.delete(isbn);
  }
}
module.exports = { LruCache };
