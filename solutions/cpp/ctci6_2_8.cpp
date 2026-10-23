#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <unordered_set>
struct LinkedListNode { int Value; LinkedListNode* Next; explicit LinkedListNode(int value, LinkedListNode* next=nullptr):Value(value),Next(next){} };
class Solution {
 public:
  LinkedListNode* FindLoopEntry(LinkedListNode* head) {
    LinkedListNode* slow = head;
    LinkedListNode* fast = head;
    while (fast != nullptr && fast->Next != nullptr) {
      slow = slow->Next;
      fast = fast->Next->Next;
      if (slow == fast)
        break;
    }
    if (fast == nullptr || fast->Next == nullptr)
      return nullptr;
    slow = head;
    while (slow != fast) {
      slow = slow->Next;
      fast = fast->Next;
    }
    return slow;
  }
};
