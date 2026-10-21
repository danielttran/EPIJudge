#include <cstdint>
#include <string>
#include <vector>

#include "test_framework/generic_test.h"

// Original EPI Practice algorithm: the right boundary is exclusive, avoiding
// an empty-array subtraction while still allowing both choices to use one
// index.
bool HasTwoSum(const std::vector<int>& A, int t) {
  std::size_t left = 0, end = A.size();
  while (left < end) {
    std::int64_t actual = static_cast<std::int64_t>(A[left]) + A[end - 1];
    if (actual == static_cast<std::int64_t>(t)) return true;
    if (actual < t)
      ++left;
    else
      --end;
  }
  return false;
}
int main(int argc, char* argv[]) {
  std::vector<std::string> arguments(argv + 1, argv + argc);
  std::vector<std::string> parameters{"A", "t"};
  return GenericTestMain(arguments, "two_sum.cc", "two_sum.tsv", &HasTwoSum,
                         DefaultComparator{}, parameters);
}
