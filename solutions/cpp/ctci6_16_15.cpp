#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
class Solution {
 public:
  std::vector<int> ScoreMasterMind(const std::string& guess, const std::string& secret) {
    int remaining[4] = {};
    int hits = 0, pseudoHits = 0;
    for (int i = 0; i < 4; ++i) {
      if (guess[i] == secret[i])
        ++hits;
      else
        ++remaining[static_cast<int>(std::string("RGBY").find(secret[i]))];
    }
    for (int i = 0; i < 4; ++i) {
      if (guess[i] == secret[i])
        continue;
      int color = static_cast<int>(std::string("RGBY").find(guess[i]));
      if (remaining[color] > 0) {
        --remaining[color];
        ++pseudoHits;
      }
    }
    return {hits, pseudoHits};
  }
};
