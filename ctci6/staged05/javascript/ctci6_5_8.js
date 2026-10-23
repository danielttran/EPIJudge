'use strict';
function DrawHorizontalLine(screen, width, x1, x2, y) {
  const first = Math.floor(x1 / 8),
    last = Math.floor(x2 / 8),
    row = y * (width / 8);
  for (let byte = first; byte <= last; ++byte) {
    const start = byte === first ? x1 % 8 : 0,
      end = byte === last ? x2 % 8 : 7,
      mask = (255 >>> start) & ((255 << (7 - end)) & 255);
    screen[row + byte] |= mask;
  }
}
