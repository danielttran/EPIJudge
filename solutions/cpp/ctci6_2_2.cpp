#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <unordered_set>
struct LinkedListNode { int Value; LinkedListNode* Next; explicit LinkedListNode(int value, LinkedListNode* next=nullptr):Value(value),Next(next){} };
class Solution {
 public:
  LinkedListNode* KthToLast(LinkedListNode* head, int k) {
    if (k <= 0)
      return nullptr;
    LinkedListNode* lead = head;
    for (int i = 0; i < k; ++i) {
      if (lead == nullptr)
        return nullptr;
      lead = lead->Next;
    }
    LinkedListNode* follow = head;
    while (lead != nullptr) {
      lead = lead->Next;
      follow = follow->Next;
    }
    return follow;
  }
};
