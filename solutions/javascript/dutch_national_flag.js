function dutchFlagPartition(pivotIndex, values) {
  const pivot = values[pivotIndex];
  let smaller = 0,
    current = 0,
    larger = values.length;
  while (current < larger) {
    if (values[current] < pivot) {
      [values[smaller], values[current]] = [values[current], values[smaller]];
      smaller++;
      current++;
    } else if (values[current] === pivot) current++;
    else {
      larger--;
      [values[current], values[larger]] = [values[larger], values[current]];
    }
  }
}

module.exports = { dutchFlagPartition };
