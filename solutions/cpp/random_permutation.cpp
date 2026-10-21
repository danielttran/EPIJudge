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
std::vector<int> ComputeRandomPermutation(int n) {
  std::vector<int> result(n);std::iota(result.begin(),result.end(),0);
  static thread_local std::mt19937_64 random(std::random_device{}());
  for(int index=0;index<n;++index) {
    int selected=std::uniform_int_distribution<int>(index,n-1)(random);
    std::swap(result[index],result[selected]);
  }
  return result;
}
int FactorialValue(int n) {int result=1;for(int value=2;value<=n;++value)result*=value;return result;}
int PermutationRank(const std::vector<int>& values) {
  int rank=0;
  for(int i=0;i<static_cast<int>(values.size());++i) {
    int smaller=0;for(int j=i+1;j<static_cast<int>(values.size());++j) if(values[j]<values[i])++smaller;
    rank+=smaller*FactorialValue(static_cast<int>(values.size())-i-1);
  }
  return rank;
}
void VerifyPermutation(TimedExecutor& executor,int n) {
  auto Trial=[&]() {
    std::vector<int> samples;samples.reserve(1000000);
    executor.Run([&]{
      for(int trial=0;trial<1000000;++trial) {
        auto values=ComputeRandomPermutation(n),sorted=values;
        std::sort(sorted.begin(),sorted.end());
        if(static_cast<int>(sorted.size())!=n) throw TestFailure("Incorrect permutation size");
        for(int i=0;i<n;++i) if(sorted[i]!=i) throw TestFailure("Incorrect permutation membership");
        samples.push_back(PermutationRank(values));
      }
    });
    return test_framework::CheckSequenceIsUniformlyRandom(samples,FactorialValue(n),0.01);
  };
  test_framework::RunFuncWithRetries(Trial);
}

int main(int argc, char* argv[]) {
  std::vector<std::string> arguments(argv+1, argv+argc);
  std::vector<std::string> parameters{"executor","n"};
  return GenericTestMain(arguments,"random_permutation.cc","random_permutation.tsv",&VerifyPermutation,DefaultComparator{},parameters);
}
