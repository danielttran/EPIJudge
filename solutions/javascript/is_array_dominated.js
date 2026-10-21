function validPlacementExists(team0, team1) {
  if (team0.length !== team1.length) return false;
  const front = team0.slice().sort((a, b) => a - b),
    back = team1.slice().sort((a, b) => a - b);
  for (let i = 0; i < front.length; i++) if (front[i] >= back[i]) return false;
  return true;
}

module.exports = { validPlacementExists };
