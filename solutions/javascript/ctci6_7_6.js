'use strict';
function SolveJigsaw(size, pieces) {
  const count = pieces.length,
    placed = Array(count),
    used = Array(count).fill(false);
  const edge = (index, turn, side) => pieces[index][(side - turn + 4) % 4];
  function search(position) {
    if (position === count) return true;
    const row = Math.floor(position / size),
      column = position % size;
    for (let index = 0; index < count; ++index) {
      if (used[index]) continue;
      for (let turn = 0; turn < 4; ++turn) {
        const values = [0, 1, 2, 3].map((s) => edge(index, turn, s)),
          bounds = [row === 0, column === size - 1, row === size - 1, column === 0];
        if (values.some((v, s) => (v === 0) !== bounds[s])) continue;
        if (row && values[0] !== -edge(...placed[position - size], 2)) continue;
        if (column && values[3] !== -edge(...placed[position - 1], 1)) continue;
        used[index] = true;
        placed[position] = [index, turn];
        if (search(position + 1)) return true;
        used[index] = false;
      }
    }
    return false;
  }
  return search(0) ? placed : [];
}

module.exports = {SolveJigsaw};
