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
std::shared_ptr<ListNode<int>> ReversePart(std::shared_ptr<ListNode<int>> node) {
  std::shared_ptr<ListNode<int>> previous;
  while (node) { auto next=node->next; node->next=previous; previous=node; node=next; }
  return previous;
}
bool IsLinkedListAPalindrome(std::shared_ptr<ListNode<int>> head) {
  if (!head || !head->next) return true;
  auto middle=head, fast=head;
  while (fast->next && fast->next->next) { middle=middle->next; fast=fast->next->next; }
  auto second=ReversePart(middle->next), left=head;
  bool matches=true;
  for (auto right=second; right; right=right->next) {
    if (left->data!=right->data) matches=false;
    left=left->next;
  }
  middle->next=ReversePart(second);
  return matches;
}

int main(int argc, char* argv[]) {
  std::vector<std::string> arguments(argv+1, argv+argc);
  std::vector<std::string> parameters{"L"};
  return GenericTestMain(arguments,"is_list_palindromic.cc","is_list_palindromic.tsv",&IsLinkedListAPalindrome,DefaultComparator{},parameters);
}
