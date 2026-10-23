#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <unordered_set>
struct LinkedListNode { int Value; LinkedListNode* Next; explicit LinkedListNode(int value, LinkedListNode* next=nullptr):Value(value),Next(next){} };
class Solution {
 public:
  bool IsPalindrome(LinkedListNode* head) {
    std::vector<int> values;
    for (LinkedListNode* p = head; p != nullptr; p = p->Next)
      values.push_back(p->Value);
    int n = static_cast<int>(values.size());
    for (int i = 0; i < n / 2; ++i)
      if (values[i] != values[n - 1 - i])
        return false;
    return true;
  }
};
