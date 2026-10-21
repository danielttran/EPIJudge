function intersectRectangle(r1, r2) {
  const left = Math.max(r1[0], r2[0]),
    bottom = Math.max(r1[1], r2[1]),
    right = Math.min(r1[0] + r1[2], r2[0] + r2[2]),
    top = Math.min(r1[1] + r1[3], r2[1] + r2[3]);
  return left > right || bottom > top
    ? [0, 0, -1, -1]
    : [left, bottom, right - left, top - bottom];
}

module.exports = { intersectRectangle };
