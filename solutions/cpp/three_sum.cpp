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
bool HasThreeSum(std::vector<int> values,int target) {
  std::sort(values.begin(),values.end());
  for (int first:values) {
    int left=0,right=static_cast<int>(values.size())-1;
    while (left<=right) {
      long long sum=static_cast<long long>(first)+values[left]+values[right];
      if (sum==target) return true;
      if (sum<target) ++left; else --right;
    }
  }
  return false;
}

int main(int argc, char* argv[]) {
  std::vector<std::string> arguments(argv+1, argv+argc);
  std::vector<std::string> parameters{"A","t"};
  return GenericTestMain(arguments,"three_sum.cc","three_sum.tsv",&HasThreeSum,DefaultComparator{},parameters);
}
