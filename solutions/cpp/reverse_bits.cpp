#include <string>
#include <vector>
#include "test_framework/generic_test.h"

// Original implementation for EPI Practice: reverse every bit of the 64-bit word.
unsigned long long ReverseBits(unsigned long long value) {
  unsigned long long result = 0;
  for (int bit = 0; bit < 64; ++bit) {
    result = (result << 1) | (value & 1ULL);
    value >>= 1;
  }
  return result;
}

int main(int argc, char* argv[]) {
  std::vector<std::string> arguments(argv + 1, argv + argc);
  std::vector<std::string> parameters{"x"};
  return GenericTestMain(arguments, "reverse_bits.cc", "reverse_bits.tsv",
                         &ReverseBits, DefaultComparator{}, parameters);
}
