function examineBuildingsWithSunset(sequence) {
  const visible = [];
  let maximum = -Infinity;
  for (let i = sequence.length - 1; i >= 0; i--)
    if (sequence[i] > maximum) {
      visible.push(i);
      maximum = sequence[i];
    }
  return visible;
}

module.exports = { examineBuildingsWithSunset };
