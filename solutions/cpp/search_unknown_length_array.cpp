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
int BinarySearchUnknownLength(const std::vector<int>& values,int target) {
  int low=0,high=0;
  for (;;) {
    try {if (values.at(high)>=target) break;}
    catch (const std::out_of_range&) {break;}
    low=high+1;
    high=high>(INT_MAX-1)/2?INT_MAX:2*high+1;
  }
  while (low<=high) {
    int middle=low+(high-low)/2;
    try {
      int value=values.at(middle);
      if (value==target) return middle;
      if (value<target) low=middle+1; else high=middle-1;
    } catch (const std::out_of_range&) {high=middle-1;}
  }
  return -1;
}

int main(int argc,char* argv[]) {
  std::vector<std::string> arguments(argv+1,argv+argc);
  std::vector<std::string> parameters{"A","k"};
  return GenericTestMain(arguments,"search_unknown_length_array.cc","search_unknown_length_array.tsv",&BinarySearchUnknownLength,DefaultComparator{},parameters);
}
