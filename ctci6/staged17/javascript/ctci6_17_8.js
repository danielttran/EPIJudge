'use strict';
function CircusTower(people) {
  if (people.length === 0) return [];
  const order = Array.from({ length: people.length }, (_, i) => i).sort(
      (a, b) => people[a][0] - people[b][0] || people[a][1] - people[b][1] || a - b,
    ),
    length = new Array(order.length).fill(1),
    previous = new Array(order.length).fill(-1);
  let best = 0;
  for (let i = 0; i < order.length; ++i) {
    for (let j = 0; j < i; ++j) {
      const a = people[order[j]],
        b = people[order[i]];
      if (a[0] < b[0] && a[1] < b[1] && length[j] + 1 > length[i]) {
        length[i] = length[j] + 1;
        previous[i] = j;
      }
    }
    if (length[i] > length[best]) best = i;
  }
  const result = [];
  while (best !== -1) {
    result.push(order[best]);
    best = previous[best];
  }
  return result.reverse();
}
