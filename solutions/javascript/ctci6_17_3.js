'use strict';
class RandomSource {static Draw=(lower,upper)=>{throw new Error("Provided by the judge");};static GetRandom(lower,upper){return RandomSource.Draw(lower,upper);}}
function RandomSubset(values, count) {
  const reservoir = values.slice(0, count);
  if (count === 0) return reservoir;
  for (let index = count; index < values.length; ++index) {
    const slot = RandomSource.GetRandom(0, index);
    if (slot < count) reservoir[slot] = values[index];
  }
  return reservoir;
}

module.exports = {RandomSource,RandomSubset};
