#include <algorithm>
#include <cmath>
#include <limits>

#include "test_framework/generic_test.h"

using std::abs;
using std::max;
using std::numeric_limits;

enum class Ordering { kSmaller, kEqual, kLarger };

Ordering Compare(double a, double b);

double SquareRoot(double x) {
    if (x == 0) return 0;
    double low = 0, high = std::max(1.0, x);
    for (int step = 0; step < 1100; ++step) {
      double middle = low + (high - low) / 2;
      if (middle == low || middle == high) break;
      if (middle <= x / middle) low = middle;
      else high = middle;
    }
    return low + (high - low) / 2;
  }

Ordering Compare(double a, double b) {
  // Uses normalization for precision problem.
  double diff = (a - b) / max(abs(a), abs(b));
  return diff < -numeric_limits<double>::epsilon()
             ? Ordering::kSmaller
             : diff > numeric_limits<double>::epsilon() ? Ordering::kLarger
                                                        : Ordering::kEqual;
}

int main(int argc, char* argv[]) {
  std::vector<std::string> args{argv + 1, argv + argc};
  std::vector<std::string> param_names{"x"};
  return GenericTestMain(args, "real_square_root.cc", "real_square_root.tsv",
                         &SquareRoot, DefaultComparator{}, param_names);
}
