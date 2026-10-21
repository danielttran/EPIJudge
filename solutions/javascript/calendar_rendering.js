function findMaxSimultaneousEvents(events) {
  const endpoints = [];
  for (const [start, finish] of events) {
    endpoints.push([start, 1], [finish, -1]);
  }
  endpoints.sort((a, b) => a[0] - b[0] || b[1] - a[1]);
  let current = 0,
    maximum = 0;
  for (const [, delta] of endpoints) {
    current += delta;
    maximum = Math.max(maximum, current);
  }
  return maximum;
}

module.exports = { findMaxSimultaneousEvents };
