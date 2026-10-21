#include <algorithm>
#include <cstdint>
#include <ostream>
#include <string>
#include <tuple>
#include <vector>

#include "test_framework/fmt_print.h"
#include "test_framework/generic_test.h"
#include "test_framework/serialization_traits.h"

struct Rect {
  int x, y, width, height;
};

// Original EPI Practice algorithm: intersect closed projections using wide
// edges.
bool IsIntersect(const Rect& first, const Rect& second) {
  std::int64_t right =
      std::min(static_cast<std::int64_t>(first.x) + first.width,
               static_cast<std::int64_t>(second.x) + second.width);
  std::int64_t top =
      std::min(static_cast<std::int64_t>(first.y) + first.height,
               static_cast<std::int64_t>(second.y) + second.height);
  return std::max(first.x, second.x) <= right &&
         std::max(first.y, second.y) <= top;
}
Rect IntersectRectangle(const Rect& first, const Rect& second) {
  int left = std::max(first.x, second.x);
  int bottom = std::max(first.y, second.y);
  std::int64_t right =
      std::min(static_cast<std::int64_t>(first.x) + first.width,
               static_cast<std::int64_t>(second.x) + second.width);
  std::int64_t top =
      std::min(static_cast<std::int64_t>(first.y) + first.height,
               static_cast<std::int64_t>(second.y) + second.height);
  if (left > right || bottom > top) return {0, 0, -1, -1};
  return {left, bottom, static_cast<int>(right - left),
          static_cast<int>(top - bottom)};
}
bool operator==(const Rect& first, const Rect& second) {
  return first.x == second.x && first.y == second.y &&
         first.width == second.width && first.height == second.height;
}
namespace test_framework {
template <>
struct SerializationTrait<Rect> : UserSerTrait<Rect, int, int, int, int> {
  static std::vector<std::string> GetMetricNames(const std::string& argument) {
    return {FmtStr("height({})", argument), FmtStr("width({})", argument)};
  }
  static std::vector<int> GetMetrics(const Rect& rectangle) {
    return {rectangle.height, rectangle.width};
  }
};
}  // namespace test_framework
std::ostream& operator<<(std::ostream& output, const Rect& rectangle) {
  return PrintTo(output, std::make_tuple(rectangle.x, rectangle.y,
                                         rectangle.width, rectangle.height));
}
int main(int argc, char* argv[]) {
  std::vector<std::string> arguments(argv + 1, argv + argc);
  std::vector<std::string> parameters{"r1", "r2"};
  return GenericTestMain(arguments, "rectangle_intersection.cc",
                         "rectangle_intersection.tsv", &IntersectRectangle,
                         DefaultComparator{}, parameters);
}
