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
std::vector<double> OnlineMedian(std::vector<int>::const_iterator first,
                                const std::vector<int>::const_iterator& last) {
  std::priority_queue<int> lower;
  std::priority_queue<int,std::vector<int>,std::greater<int>> upper;
  std::vector<double> result;
  for (;first!=last;++first) {
    lower.push(*first);
    upper.push(lower.top());lower.pop();
    if (upper.size()>lower.size()) {lower.push(upper.top());upper.pop();}
    result.push_back(lower.size()>upper.size()?static_cast<double>(lower.top()):
        (static_cast<double>(lower.top())+upper.top())/2.0);
  }
  return result;
}
std::vector<double> ComputeMedians(const std::vector<int>& values) {
  return OnlineMedian(values.begin(),values.end());
}

int main(int argc,char* argv[]) {
  std::vector<std::string> arguments(argv+1,argv+argc);
  std::vector<std::string> parameters{"sequence"};
  return GenericTestMain(arguments,"online_median.cc","online_median.tsv",&ComputeMedians,DefaultComparator{},parameters);
}
