function optimumTaskAssignment(task_durations) {
  const values = task_durations.slice().sort((a, b) => a - b),
    result = [];
  for (let i = 0; i < Math.floor(values.length / 2); i++)
    result.push([values[i], values[values.length - 1 - i]]);
  return result;
}

module.exports = { optimumTaskAssignment };
