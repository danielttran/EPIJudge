'use strict';
function MostPopulatedYear(people) {
  const changes = Array(102).fill(0);
  for (const [birth, death] of people) {
    ++changes[birth - 1900];
    --changes[death - 1900 + 1];
  }
  let alive = 0,
    best = 0,
    answer = 1900;
  for (let offset = 0; offset < 101; ++offset) {
    alive += changes[offset];
    if (alive > best) {
      best = alive;
      answer = 1900 + offset;
    }
  }
  return answer;
}
