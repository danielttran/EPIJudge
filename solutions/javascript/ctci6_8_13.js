'use strict';
function MaximumBoxStackHeight(boxes) {
  const order = Array.from({ length: boxes.length }, (_, i) => i).sort(
      (a, b) => boxes[a][0] - boxes[b][0],
    ),
    heights = Array(boxes.length).fill(0);
  let best = 0;
  for (let i = 0; i < order.length; ++i) {
    const current = order[i];
    heights[i] = boxes[current][1];
    for (let j = 0; j < i; ++j) {
      const top = order[j];
      if (
        boxes[top][0] < boxes[current][0] &&
        boxes[top][1] < boxes[current][1] &&
        boxes[top][2] < boxes[current][2]
      )
        heights[i] = Math.max(heights[i], boxes[current][1] + heights[j]);
    }
    best = Math.max(best, heights[i]);
  }
  return best;
}

module.exports = {MaximumBoxStackHeight};
