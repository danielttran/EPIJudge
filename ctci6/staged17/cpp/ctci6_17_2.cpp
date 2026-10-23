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
  void Shuffle(std::vector<int>& values) {
    for (int index = static_cast<int>(values.size()) - 1; index > 0; --index) {
      int other = RandomSource::GetRandom(0, index);
      std::swap(values[index], values[other]);
    }
  }
};
