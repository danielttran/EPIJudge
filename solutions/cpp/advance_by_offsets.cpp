#include <algorithm>
#include <vector>

#include "test_framework/generic_test.h"

using std::max;
using std::vector;

bool CanReachEnd(const vector<int>& max_advance_steps) {
  if (max_advance_steps.empty()) return true;
  const std::size_t destination = max_advance_steps.size() - 1;
  std::size_t reachable = 0;
  for (std::size_t position = 0; position <= destination; ++position) {
    if (position > reachable) return false;
    const auto jump = static_cast<std::size_t>(max_advance_steps[position]);
    // Test against the remaining distance before adding the offset.
    if (jump >= destination - position) return true;
    reachable = std::max(reachable, position + jump);
  }
  return false;
}

int main(int argc, char* argv[]) {
  std::vector<std::string> args{argv + 1, argv + argc};
  std::vector<std::string> param_names{"max_advance_steps"};
  return GenericTestMain(args, "advance_by_offsets.cc",
                         "advance_by_offsets.tsv", &CanReachEnd,
                         DefaultComparator{}, param_names);
}
