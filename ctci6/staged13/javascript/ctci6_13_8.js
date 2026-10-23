'use strict';
class FairCoinSource {Next(){throw new Error("Provided by the judge");}}
function RandomSubset(values, coins) {
  return values.filter((value) => coins.Next());
}
