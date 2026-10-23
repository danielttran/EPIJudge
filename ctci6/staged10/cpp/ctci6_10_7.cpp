#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
class NumberFile { public: virtual int ReadNext()=0; virtual void Reset()=0; virtual ~NumberFile()=default; };
class Solution {
 public:
  int FindMissingInt(NumberFile& file, bool smallMemory) {
    int block = 0;
    if (smallMemory) {
      std::vector<int> counts(2048);
      int value;
      while ((value = file.ReadNext()) != -1)
        ++counts[value >> 20];
      while (counts[block] == (1 << 20))
        ++block;
      file.Reset();
    }
    std::vector<unsigned char> bitmap(smallMemory ? 1u << 17 : 1u << 28);
    int item;
    while ((item = file.ReadNext()) != -1)
      if (!smallMemory || (item >> 20) == block) {
        int offset = smallMemory ? item & ((1 << 20) - 1) : item;
        bitmap[offset >> 3] |= static_cast<unsigned char>(1 << (offset & 7));
      }
    for (size_t index = 0; index < bitmap.size(); ++index)
      if (bitmap[index] != 255)
        for (int bit = 0; bit < 8; ++bit)
          if ((bitmap[index] & (1 << bit)) == 0)
            return (block << 20) + static_cast<int>(index * 8) + bit;
    return -1;
  }
};
