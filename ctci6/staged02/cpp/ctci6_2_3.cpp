#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <unordered_set>
struct LinkedListNode { int Value; LinkedListNode* Next; explicit LinkedListNode(int value, LinkedListNode* next=nullptr):Value(value),Next(next){} };
class Solution {
 public:
  bool DeleteMiddle(LinkedListNode* target) {
    if (target == nullptr || target->Next == nullptr)
      return false;
    LinkedListNode* successor = target->Next;
    target->Value = successor->Value;
    target->Next = successor->Next;
    return true;
  }
};
