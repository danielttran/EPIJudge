#include <algorithm>
#include <deque>
#include <functional>
#include <memory>
#include <numeric>
#include <queue>
#include <random>
#include <stdexcept>
#include <string>
#include <tuple>
#include <unordered_map>
#include <unordered_set>
#include <vector>
#include "list_node.h"
#include "test_framework/generic_test.h"
#include "test_framework/test_failure.h"
#include "test_framework/timed_executor.h"
#include "test_framework/random_sequence_checker.h"

// Original implementation authored for EPI Practice from its public contract.
std::shared_ptr<ListNode<int>> ZippingLinkedList(const std::shared_ptr<ListNode<int>>& head) {
  if (!head || !head->next) return head;
  auto middle=head, fast=head;
  while (fast->next && fast->next->next) { middle=middle->next; fast=fast->next->next; }
  auto current=middle->next;
  middle->next=nullptr;
  std::shared_ptr<ListNode<int>> reversed;
  while (current) { auto next=current->next; current->next=reversed; reversed=current; current=next; }
  auto first=head;
  while (reversed) {
    auto firstNext=first->next, secondNext=reversed->next;
    first->next=reversed; reversed->next=firstNext;
    first=firstNext; reversed=secondNext;
  }
  return head;
}

int main(int argc, char* argv[]) {
  std::vector<std::string> arguments(argv+1, argv+argc);
  std::vector<std::string> parameters{"L"};
  return GenericTestMain(arguments,"zip_list.cc","zip_list.tsv",&ZippingLinkedList,DefaultComparator{},parameters);
}
