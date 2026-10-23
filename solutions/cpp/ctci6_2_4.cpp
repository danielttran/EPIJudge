#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <unordered_set>
struct LinkedListNode { int Value; LinkedListNode* Next; explicit LinkedListNode(int value, LinkedListNode* next=nullptr):Value(value),Next(next){} };
class Solution {
 public:
  LinkedListNode* Partition(LinkedListNode* head, int pivot) {
    LinkedListNode* smallHead = nullptr;
    LinkedListNode* smallTail = nullptr;
    LinkedListNode* largeHead = nullptr;
    LinkedListNode* largeTail = nullptr;
    LinkedListNode* current = head;
    while (current != nullptr) {
      LinkedListNode* next = current->Next;
      current->Next = nullptr;
      if (current->Value < pivot) {
        if (smallTail == nullptr)
          smallHead = current;
        else
          smallTail->Next = current;
        smallTail = current;
      } else {
        if (largeTail == nullptr)
          largeHead = current;
        else
          largeTail->Next = current;
        largeTail = current;
      }
      current = next;
    }
    if (smallHead == nullptr)
      return largeHead;
    smallTail->Next = largeHead;
    return smallHead;
  }
};
