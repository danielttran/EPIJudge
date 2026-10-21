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
std::shared_ptr<ListNode<int>> MergeParts(std::shared_ptr<ListNode<int>> a,std::shared_ptr<ListNode<int>> b) {
  auto dummy=std::make_shared<ListNode<int>>(0), tail=dummy;
  while (a && b) {
    auto& source=a->data<=b->data?a:b;
    tail->next=source; source=source->next; tail=tail->next;
  }
  tail->next=a?a:b;
  return dummy->next;
}
std::shared_ptr<ListNode<int>> StableSortList(std::shared_ptr<ListNode<int>> head) {
  if (!head || !head->next) return head;
  auto middle=head, fast=head->next;
  while (fast && fast->next) { middle=middle->next; fast=fast->next->next; }
  auto second=middle->next; middle->next=nullptr;
  return MergeParts(StableSortList(head),StableSortList(second));
}

int main(int argc, char* argv[]) {
  std::vector<std::string> arguments(argv+1, argv+argc);
  std::vector<std::string> parameters{"L"};
  return GenericTestMain(arguments,"sort_list.cc","sort_list.tsv",&StableSortList,DefaultComparator{},parameters);
}
