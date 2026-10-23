'use strict';
function SolveHanoi(disks) {
  const towers = [Array.from({ length: disks }, (_, i) => disks - i), [], []],
    moves = [];
  function transfer(count, source, buffer, destination) {
    if (count === 0) return;
    transfer(count - 1, source, destination, buffer);
    const disk = towers[source].pop();
    towers[destination].push(disk);
    moves.push([disk, source, destination]);
    transfer(count - 1, buffer, source, destination);
  }
  transfer(disks, 0, 1, 2);
  return moves;
}
