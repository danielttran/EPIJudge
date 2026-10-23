#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
class FizzContext {public:virtual void Wait(int gate)=0;virtual void Signal(int gate)=0;virtual void Print(int value)=0;protected:virtual ~FizzContext()=default;};
class Solution {
 public:
  void RunFizzBuzz(int role, int limit, FizzContext& context) {
    auto owner = [](int value) {
      return value % 15 == 0 ? 3 : value % 3 == 0 ? 1 : value % 5 == 0 ? 2 : 0;
    };
    for (int value = 1; value <= limit; ++value) {
      if (owner(value) != role)
        continue;
      context.Wait(role);
      context.Print(value);
      if (value < limit)
        context.Signal(owner(value + 1));
    }
  }
};
