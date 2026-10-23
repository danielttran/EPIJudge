#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
class ForkContext {public:virtual void Take(int fork)=0;virtual void Drop(int fork)=0;virtual void Eat()=0;protected:virtual ~ForkContext()=default;};
class Solution {
 public:
  void Dine(int role, int philosophers, int bites, ForkContext& context) {
    int left = role, right = (role + 1) % philosophers, lower = std::min(left, right),
        higher = std::max(left, right);
    for (int bite = 0; bite < bites; ++bite) {
      context.Take(lower);
      context.Take(higher);
      context.Eat();
      context.Drop(higher);
      context.Drop(lower);
    }
  }
};
