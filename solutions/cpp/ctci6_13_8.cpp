#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
#include <iterator>
struct FairCoinSource {virtual bool Next()=0;virtual ~FairCoinSource()=default;};
class Solution {
 public:
  std::vector<int> RandomSubset(const std::vector<int>& values, FairCoinSource& coins) {
    std::vector<int> selected;
    std::copy_if(values.begin(), values.end(), std::back_inserter(selected),
                 [&coins](int value) { return coins.Next(); });
    return selected;
  }
};
