#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
class BitArray { public: virtual int Size()=0; virtual int FetchBit(int index,int column)=0; virtual ~BitArray()=default; };
class Solution {
 public:
  int MissingNumberBits(BitArray& numbers) {
    std::vector<int> current;
    for (int i = 0; i < numbers.Size(); ++i)
      current.push_back(i);
    int answer = 0, column = 0;
    while (!current.empty() && column < 32) {
      std::vector<int> zeros, ones;
      for (int index : current)
        (numbers.FetchBit(index, column) == 0 ? zeros : ones).push_back(index);
      if (zeros.size() <= ones.size())
        current = std::move(zeros);
      else {
        answer |= 1 << column;
        current = std::move(ones);
      }
      ++column;
    }
    return answer;
  }
};
