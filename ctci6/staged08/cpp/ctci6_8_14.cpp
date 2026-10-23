#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
class Solution {
 public:
  int CountBooleanParenthesizations(const std::string& expression, bool desired) {
    if (static_cast<int>(expression.size()) == 0)
      return 0;
    int count = (static_cast<int>(expression.size()) + 1) / 2;
    std::vector<std::vector<int>> truth(count, std::vector<int>(count)),
        falsity(count, std::vector<int>(count));
    for (int i = 0; i < count; ++i) {
      truth[i][i] = expression[2 * i] == '1' ? 1 : 0;
      falsity[i][i] = 1 - truth[i][i];
    }
    for (int length = 2; length <= count; ++length) {
      for (int low = 0; low + length <= count; ++low) {
        int high = low + length - 1;
        for (int split = low; split < high; ++split) {
          int lt = truth[low][split], lf = falsity[low][split], rt = truth[split + 1][high],
              rf = falsity[split + 1][high], total = (lt + lf) * (rt + rf);
          char operation = expression[2 * split + 1];
          int trueCount = operation == '&'   ? lt * rt
                          : operation == '|' ? total - lf * rf
                                             : lt * rf + lf * rt;
          truth[low][high] += trueCount;
          falsity[low][high] += total - trueCount;
        }
      }
    }
    return desired ? truth[0][count - 1] : falsity[0][count - 1];
  }
};
