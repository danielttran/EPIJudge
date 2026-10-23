#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
#include <stdexcept>
struct RandomSource { inline static std::function<int(int,int)> Draw=[](int,int)->int{throw std::runtime_error("Provided by the judge");}; static int GetRandom(int lower,int upper){return Draw(lower,upper);} };
class Solution {
 public:
  std::vector<int> RandomSubset(const std::vector<int>& values, int count) {
    std::vector<int> reservoir(values.begin(), values.begin() + count);
    if (count == 0)
      return reservoir;
    for (int index = count; index < static_cast<int>(values.size()); ++index) {
      int slot = RandomSource::GetRandom(0, index);
      if (slot < count)
        reservoir[slot] = values[index];
    }
    return reservoir;
  }
};
