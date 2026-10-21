function searchMaze(maze, start, end) {
  const white = ([r, c]) =>
      r >= 0 &&
      r < maze.length &&
      c >= 0 &&
      c < maze[r].length &&
      maze[r][c] === 0,
    key = ([r, c]) => r + "," + c;
  if (!white(start) || !white(end)) return [];
  const previous = new Map([[key(start), null]]),
    cells = new Map([[key(start), start]]),
    pending = [start];
  for (let head = 0; head < pending.length; head++) {
    const cell = pending[head];
    if (key(cell) === key(end)) {
      const path = [];
      for (let at = key(end); at !== null; at = previous.get(at))
        path.push(cells.get(at));
      return path.reverse();
    }
    for (const [dr, dc] of [
      [1, 0],
      [-1, 0],
      [0, 1],
      [0, -1],
    ]) {
      const next = [cell[0] + dr, cell[1] + dc],
        id = key(next);
      if (white(next) && !previous.has(id)) {
        previous.set(id, key(cell));
        cells.set(id, next);
        pending.push(next);
      }
    }
  }
  return [];
}

module.exports = { searchMaze };
