'use strict';
function SmallestK(values, k) {
  if (k === 0) return [];
  const heap = values.slice(0, k);
  function down(index) {
    while (true) {
      let child = 2 * index + 1;
      if (child >= heap.length) return;
      if (child + 1 < heap.length && heap[child + 1] > heap[child]) ++child;
      if (heap[index] >= heap[child]) return;
      [heap[index], heap[child]] = [heap[child], heap[index]];
      index = child;
    }
  }
  for (let i = Math.floor(k / 2) - 1; i >= 0; --i) down(i);
  for (let i = k; i < values.length; ++i) {
    if (values[i] < heap[0]) {
      heap[0] = values[i];
      down(0);
    }
  }
  heap.sort((a, b) => a - b);
  return heap;
}

module.exports = {SmallestK};
