'use strict';
class ResourceLock {Lock(){throw new Error('Provided native resource lock');}Unlock(){throw new Error('Provided native resource lock');}}
class LockPool {Get(resource){throw new Error('Provided stable native lock pool');}}
class DeadlockFreeLocks {
  constructor(resourceCount, pool) {
    this.count = resourceCount;
    this.pool = pool;
    this.orders = Array.from({ length: 4 }, () => []);
    this.next = Array(4).fill(0);
  }
  Declare(owner, order) {
    if (owner < 0 || owner >= 4) return false;
    const seen = Array(this.count).fill(false);
    for (const resource of order) {
      if (resource < 0 || resource >= this.count || seen[resource]) return false;
      seen[resource] = true;
    }
    const reach = Array.from({ length: this.count }, () => Array(this.count).fill(false));
    for (let candidate = 0; candidate < 4; ++candidate) {
      const path = candidate === owner ? order : this.orders[candidate];
      for (let i = 1; i < path.length; ++i) reach[path[i - 1]][path[i]] = true;
    }
    for (let middle = 0; middle < this.count; ++middle)
      for (let first = 0; first < this.count; ++first)
        for (let second = 0; second < this.count; ++second)
          reach[first][second] =
            reach[first][second] || (reach[first][middle] && reach[middle][second]);
    for (let i = 0; i < this.count; ++i) if (reach[i][i]) return false;
    this.orders[owner] = order.slice();
    this.next[owner] = 0;
    return true;
  }
  GetLock(owner, resource) {
    if (owner < 0 || owner >= 4) return null;
    const path = this.orders[owner],
      position = this.next[owner];
    if (position === path.length || path[position] !== resource) return null;
    ++this.next[owner];
    return this.pool.Get(resource);
  }
}
