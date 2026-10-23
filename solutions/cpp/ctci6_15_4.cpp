#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
class ResourceLock {public:virtual void Lock()=0;virtual void Unlock()=0;protected:virtual ~ResourceLock()=default;};
class LockPool {public:virtual ResourceLock* Get(int resource)=0;protected:virtual ~LockPool()=default;};
class DeadlockFreeLocks {
  int count;
  LockPool& pool;
  std::array<std::vector<int>, 4> orders;
  std::array<std::size_t, 4> next{};

 public:
  DeadlockFreeLocks(int resourceCount, LockPool& pool) : count(resourceCount), pool(pool) {
  }
  bool Declare(int owner, const std::vector<int>& order) {
    if (owner < 0 || owner >= 4)
      return false;
    std::vector<bool> seen(count, false);
    for (int resource : order) {
      if (resource < 0 || resource >= count || seen[resource])
        return false;
      seen[resource] = true;
    }
    std::vector<std::vector<bool>> reach(count, std::vector<bool>(count, false));
    for (int candidate = 0; candidate < 4; ++candidate) {
      const auto& path = candidate == owner ? order : orders[candidate];
      for (std::size_t i = 1; i < path.size(); ++i)
        reach[path[i - 1]][path[i]] = true;
    }
    for (int middle = 0; middle < count; ++middle)
      for (int first = 0; first < count; ++first)
        for (int second = 0; second < count; ++second)
          reach[first][second] =
              reach[first][second] || (reach[first][middle] && reach[middle][second]);
    for (int i = 0; i < count; ++i)
      if (reach[i][i])
        return false;
    orders[owner] = order;
    next[owner] = 0;
    return true;
  }
  ResourceLock* GetLock(int owner, int resource) {
    if (owner < 0 || owner >= 4)
      return nullptr;
    const auto& path = orders[owner];
    if (next[owner] == path.size() || path[next[owner]] != resource)
      return nullptr;
    ++next[owner];
    return pool.Get(resource);
  }
};
