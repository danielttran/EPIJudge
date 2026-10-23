#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
class Rand5Source { public: virtual int Next()=0; virtual ~Rand5Source()=default; };
#include <unordered_map>
#include <unordered_set>
class Solution {
 public:
  int UniformSeven(Rand5Source& source) {
    while (true) {
      int first = source.Next();
      int state = 5 * first + source.Next();
      if (state < 21)
        return state % 7;
    }
  }
};
