#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
class Solution {
 public:
  std::vector<std::vector<int>> SolveHanoi(int disks) {
    std::array<std::vector<int>, 3> towers;
    for (int disk = disks; disk >= 1; --disk)
      towers[0].push_back(disk);
    std::vector<std::vector<int>> moves;
    std::function<void(int, int, int, int)> transfer = [&](int count, int source, int buffer,
                                                           int destination) {
      if (count == 0)
        return;
      transfer(count - 1, source, destination, buffer);
      int disk = towers[source].back();
      towers[source].pop_back();
      towers[destination].push_back(disk);
      moves.push_back({disk, source, destination});
      transfer(count - 1, buffer, source, destination);
    };
    transfer(disks, 0, 1, 2);
    return moves;
  }
};
