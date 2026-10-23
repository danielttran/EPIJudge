'use strict';
class RandomSource {static Draw=(lower,upper)=>{throw new Error("Provided by the judge");};static GetRandom(lower,upper){return RandomSource.Draw(lower,upper);}}
function Shuffle(values) {
  for (let index = values.length - 1; index > 0; --index) {
    const other = RandomSource.GetRandom(0, index);
    [values[index], values[other]] = [values[other], values[index]];
  }
}
