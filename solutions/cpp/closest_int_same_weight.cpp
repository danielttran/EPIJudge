#include <algorithm>
#include <climits>
#include <functional>
#include <limits>
#include <queue>
#include <stdexcept>
#include <string>
#include <vector>
#include "test_framework/generic_test.h"

// Original EPI Practice implementation using the displayed native contract.
unsigned long long ClosestIntSameBitCount(unsigned long long value) {
  for (int bit=0;bit<63;++bit)
    if (((value>>bit)&1ULL)!=((value>>(bit+1))&1ULL))
      return value^(1ULL<<bit)^(1ULL<<(bit+1));
  throw std::invalid_argument("No different same-weight unsigned word exists");
}

int main(int argc,char* argv[]) {
  std::vector<std::string> arguments(argv+1,argv+argc);
  std::vector<std::string> parameters{"x"};
  return GenericTestMain(arguments,"closest_int_same_weight.cc","closest_int_same_weight.tsv",&ClosestIntSameBitCount,DefaultComparator{},parameters);
}
