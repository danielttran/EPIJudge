function flipColor(x, y, image) {
  if (!image.length || !image[0].length) return image;
  const old = image[x][y],
    replacement = 1 - old,
    queue = [[x, y]];
  image[x][y] = replacement;
  function add(r, c) {
    if (
      r >= 0 &&
      r < image.length &&
      c >= 0 &&
      c < image[r].length &&
      image[r][c] === old
    ) {
      image[r][c] = replacement;
      queue.push([r, c]);
    }
  }
  for (let head = 0; head < queue.length; head++) {
    const [r, c] = queue[head];
    add(r - 1, c);
    add(r + 1, c);
    add(r, c - 1);
    add(r, c + 1);
  }
  return image;
}

module.exports = { flipColor };
