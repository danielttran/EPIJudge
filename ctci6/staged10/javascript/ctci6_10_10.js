'use strict';
class RankTracker {
  constructor() {
    this.root = null;
  }
  Track(value) {
    if (this.root === null) {
      this.root = { value, leftCount: 0, left: null, right: null };
      return;
    }
    let node = this.root;
    while (true) {
      if (value <= node.value) {
        ++node.leftCount;
        if (node.left === null) {
          node.left = { value, leftCount: 0, left: null, right: null };
          return;
        }
        node = node.left;
      } else {
        if (node.right === null) {
          node.right = { value, leftCount: 0, left: null, right: null };
          return;
        }
        node = node.right;
      }
    }
  }
  GetRank(value) {
    let node = this.root,
      skipped = 0;
    while (node !== null) {
      if (value === node.value) return skipped + node.leftCount;
      if (value < node.value) node = node.left;
      else {
        skipped += node.leftCount + 1;
        node = node.right;
      }
    }
    return -1;
  }
}
