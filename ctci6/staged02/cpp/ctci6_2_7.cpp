#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <unordered_set>
struct LinkedListNode { int Value; LinkedListNode* Next; explicit LinkedListNode(int value, LinkedListNode* next=nullptr):Value(value),Next(next){} };
class Solution {
 public:
  LinkedListNode* FindIntersection(LinkedListNode* first, LinkedListNode* second) {
    LinkedListNode* p = first;
    LinkedListNode* q = second;
    while (p != q) {
      p = p == nullptr ? second : p->Next;
      q = q == nullptr ? first : q->Next;
    }
    return p;
  }
};
