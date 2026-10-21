#include <algorithm>
#include <deque>
#include <functional>
#include <memory>
#include <numeric>
#include <queue>
#include <random>
#include <stdexcept>
#include <string>
#include <tuple>
#include <unordered_map>
#include <unordered_set>
#include <vector>
#include "list_node.h"
#include "test_framework/generic_test.h"
#include "test_framework/test_failure.h"
#include "test_framework/timed_executor.h"
#include "test_framework/random_sequence_checker.h"

// Original implementation authored for EPI Practice from its public contract.
std::vector<int> SortKIncreasingDecreasingArray(const std::vector<int>& values) {
  std::vector<int> sorted=values;
  std::sort(sorted.begin(),sorted.end());
  return sorted;
}

int main(int argc, char* argv[]) {
  std::vector<std::string> arguments(argv+1, argv+argc);
  std::vector<std::string> parameters{"A"};
  return GenericTestMain(arguments,"sort_increasing_decreasing_array.cc","sort_increasing_decreasing_array.tsv",&SortKIncreasingDecreasingArray,DefaultComparator{},parameters);
}
