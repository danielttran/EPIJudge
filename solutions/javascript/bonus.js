function calculateBonus(productivity) {
  const n = productivity.length,
    bonuses = Array(n).fill(1);
  for (let i = 1; i < n; i++)
    if (productivity[i] > productivity[i - 1]) bonuses[i] = bonuses[i - 1] + 1;
  for (let i = n - 2; i >= 0; i--)
    if (productivity[i] > productivity[i + 1])
      bonuses[i] = Math.max(bonuses[i], bonuses[i + 1] + 1);
  return bonuses.reduce((sum, value) => sum + value, 0);
}

module.exports = { calculateBonus };
