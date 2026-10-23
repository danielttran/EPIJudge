#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <unordered_set>
struct LinkedListNode { int Value; LinkedListNode* Next; explicit LinkedListNode(int value, LinkedListNode* next=nullptr):Value(value),Next(next){} };
class Solution {
 public:
  void RemoveDups(LinkedListNode* head) {
    std::unordered_set<int> seen;
    LinkedListNode* previous = nullptr;
    LinkedListNode* current = head;
    while (current != nullptr) {
      if (!(seen.insert(current->Value).second))
        previous->Next = current->Next;
      else
        previous = current;
      current = current->Next;
    }
  }
};
