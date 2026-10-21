function addInterval(disjoint_intervals, new_interval) {
  const result = [];
  let index = 0;
  new_interval = new_interval.slice();
  while (
    index < disjoint_intervals.length &&
    disjoint_intervals[index][1] < new_interval[0]
  )
    result.push(disjoint_intervals[index++]);
  while (
    index < disjoint_intervals.length &&
    disjoint_intervals[index][0] <= new_interval[1]
  ) {
    const next = disjoint_intervals[index++];
    new_interval = [
      Math.min(new_interval[0], next[0]),
      Math.max(new_interval[1], next[1]),
    ];
  }
  result.push(new_interval);
  while (index < disjoint_intervals.length)
    result.push(disjoint_intervals[index++]);
  return result;
}

module.exports = { addInterval };
