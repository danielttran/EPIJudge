'use strict';
class Rand5Source {Next(){throw new Error("Provided by the judge");}}
function UniformSeven(source) {
  while (true) {
    const state = 5 * source.Next() + source.Next();
    if (state < 21) return state % 7;
  }
}

module.exports = {Rand5Source,UniformSeven};
