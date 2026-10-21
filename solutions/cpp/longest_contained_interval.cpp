#include <algorithm>
#include <cstdint>
#include <string>
#include <unordered_set>
#include <vector>

#include "test_framework/generic_test.h"

// Original EPI Practice algorithm: consume each component with wide neighbor
// keys.
int LongestContainedRange(const std::vector<int>& A) {
  std::unordered_set<std::int64_t> unused(A.begin(), A.end());
  int best = 0;
  while (!unused.empty()) {
    std::int64_t seed = *unused.begin();
    unused.erase(seed);
    int length = 1;
    for (std::int64_t below = seed - 1; unused.erase(below) != 0; --below)
      ++length;
    for (std::int64_t above = seed + 1; unused.erase(above) != 0; ++above)
      ++length;
    best = std::max(best, length);
  }
  return best;
}
int main(int argc, char* argv[]) {
  std::vector<std::string> arguments(argv + 1, argv + argc);
  std::vector<std::string> parameters{"A"};
  return GenericTestMain(arguments, "longest_contained_interval.cc",
                         "longest_contained_interval.tsv",
                         &LongestContainedRange, DefaultComparator{},
                         parameters);
}
