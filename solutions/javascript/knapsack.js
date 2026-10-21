function optimumSubjectToCapacity(items, capacity) {
  const best = Array(capacity + 1).fill(0);
  for (const [weight, value] of items)
    for (let available = capacity; available >= weight; available--)
      best[available] = Math.max(
        best[available],
        best[available - weight] + value,
      );
  return best[capacity];
}

module.exports = { optimumSubjectToCapacity };
