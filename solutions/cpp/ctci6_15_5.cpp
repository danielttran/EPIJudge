#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
class SyncContext {public:virtual void Wait(int gate)=0;virtual void Signal(int gate)=0;virtual void Work()=0;protected:virtual ~SyncContext()=default;};
class Solution {
 public:
  void RunOrdered(int role, SyncContext& context) {
    if (role > 0)
      context.Wait(role - 1);
    context.Work();
    if (role < 2)
      context.Signal(role);
  }
};
