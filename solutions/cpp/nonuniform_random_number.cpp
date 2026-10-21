#include <cmath>
#include <functional>
#include <random>
#include <string>
#include <unordered_map>
#include <vector>
#include "test_framework/generic_test.h"
#include "test_framework/random_sequence_checker.h"
#include "test_framework/test_failure.h"
#include "test_framework/timed_executor.h"

// Original EPI Practice algorithm: draw once and consume cumulative mass.
int NonuniformRandomNumberGeneration(const std::vector<int>& values,
                                     const std::vector<double>& probabilities) {
  static thread_local std::mt19937_64 random(std::random_device{}());
  double remaining = std::uniform_real_distribution<double>(0.0,1.0)(random);
  for (std::size_t index=0; index+1<values.size(); ++index) {
    remaining -= probabilities[index];
    if (remaining < 0) return values[index];
  }
  return values.back();
}

// Retain the complete million-draw statistical check and its original 5σ bounds.
void VerifyWeightedDraw(TimedExecutor& executor,const std::vector<int>& values,
                        const std::vector<double>& probabilities) {
  auto Trial = [&]() {
    constexpr int draws=1000000;
    std::unordered_map<int,int> observed;
    executor.Run([&] {
      for (int draw=0;draw<draws;++draw)
        ++observed[NonuniformRandomNumberGeneration(values,probabilities)];
    });
    for (std::size_t index=0;index<values.size();++index) {
      double probability=probabilities[index];
      if (draws*probability<50 || draws*(1.0-probability)<50) continue;
      double sigma=std::sqrt(draws*probability*(1.0-probability));
      if (std::abs(observed[values[index]]-draws*probability)>5*sigma) return false;
    }
    return true;
  };
  test_framework::RunFuncWithRetries(Trial);
}
int main(int argc,char* argv[]) {
  std::vector<std::string> arguments(argv+1,argv+argc);
  std::vector<std::string> parameters{"executor","values","probabilities"};
  return GenericTestMain(arguments,"nonuniform_random_number.cc",
                         "nonuniform_random_number.tsv",&VerifyWeightedDraw,
                         DefaultComparator{},parameters);
}
