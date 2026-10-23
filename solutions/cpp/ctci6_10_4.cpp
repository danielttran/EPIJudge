#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
class Listy { public: virtual int ElementAt(int index)=0; virtual ~Listy()=default; };
class Solution {
 public:
  int SearchWithoutSize(Listy& values, int target) {
    if (target <= 0)
      return -1;
    int bound = 1;
    while (true) {
      int value = values.ElementAt(bound);
      if (value == -1 || value >= target)
        break;
      bound *= 2;
    }
    int low = bound / 2, high = bound;
    while (low <= high) {
      int middle = low + (high - low) / 2, value = values.ElementAt(middle);
      if (value == -1 || value > target)
        high = middle - 1;
      else if (value < target)
        low = middle + 1;
      else
        return middle;
    }
    return -1;
  }
};
