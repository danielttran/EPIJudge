#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <unordered_set>
struct LinkedListNode { int Value; LinkedListNode* Next; explicit LinkedListNode(int value, LinkedListNode* next=nullptr):Value(value),Next(next){} };
class Solution {
 public:
  LinkedListNode* AddLists(LinkedListNode* first, LinkedListNode* second,
                           bool mostSignificantFirst) {
    if (mostSignificantFirst) {
      std::vector<int> left, right;
      for (LinkedListNode* scan = first; scan != nullptr; scan = scan->Next)
        left.push_back(scan->Value);
      for (LinkedListNode* scan = second; scan != nullptr; scan = scan->Next)
        right.push_back(scan->Value);
      LinkedListNode* result = nullptr;
      int forwardCarry = 0;
      while (!left.empty() || !right.empty() || forwardCarry != 0) {
        int total = forwardCarry;
        if (!left.empty()) {
          total += left.back();
          left.pop_back();
        }
        if (!right.empty()) {
          total += right.back();
          right.pop_back();
        }
        result = new LinkedListNode(total % 10, result);
        forwardCarry = total / 10;
      }
      return result;
    }
    LinkedListNode dummy(0);
    LinkedListNode* tail = &dummy;
    LinkedListNode* p = first;
    LinkedListNode* q = second;
    int carry = 0;
    while (p != nullptr || q != nullptr || carry != 0) {
      int total = carry;
      if (p != nullptr) {
        total += p->Value;
        p = p->Next;
      }
      if (q != nullptr) {
        total += q->Value;
        q = q->Next;
      }
      tail->Next = new LinkedListNode(total % 10);
      tail = tail->Next;
      carry = total / 10;
    }
    return dummy.Next;
  }
};
