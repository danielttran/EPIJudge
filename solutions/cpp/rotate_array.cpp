#include <algorithm>
#include <string>
#include <vector>

#include "test_framework/generic_test.h"
#include "test_framework/timed_executor.h"

void RotateArray(int rotate_amount, std::vector<int>* A) {
  if (A->empty()) return;
  const long long length = static_cast<long long>(A->size());
  const auto shift = static_cast<std::vector<int>::difference_type>(
      (static_cast<long long>(rotate_amount) % length + length) % length);
  std::reverse(A->begin(), A->end());
  std::reverse(A->begin(), A->begin() + shift);
  std::reverse(A->begin() + shift, A->end());
}

std::vector<int> RotateArrayWrapper(TimedExecutor& executor, std::vector<int> A,
                                    int rotate_amount) {
  executor.Run([&A, rotate_amount] { RotateArray(rotate_amount, &A); });
  return A;
}

int main(int argc, char* argv[]) {
  std::vector<std::string> arguments(argv + 1, argv + argc);
  std::vector<std::string> parameters{"executor", "A", "rotate_amount"};
  return GenericTestMain(arguments, "rotate_array.cc", "rotate_array.tsv",
                         &RotateArrayWrapper, DefaultComparator{}, parameters);
}
