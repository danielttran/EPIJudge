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
std::shared_ptr<ListNode<int>> ListPivoting(const std::shared_ptr<ListNode<int>>& head,int pivot) {
  std::shared_ptr<ListNode<int>> heads[3],tails[3];
  auto node=head;
  while (node) {
    auto next=node->next;
    node->next=nullptr;
    int group=node->data<pivot?0:node->data==pivot?1:2;
    if (tails[group]) tails[group]->next=node; else heads[group]=node;
    tails[group]=node;
    node=next;
  }
  std::shared_ptr<ListNode<int>> result,tail;
  for (int group=0;group<3;++group) if (heads[group]) {
    if (tail) tail->next=heads[group]; else result=heads[group];
    tail=tails[group];
  }
  return result;
}
void VerifyPivot(TimedExecutor& executor,const std::shared_ptr<ListNode<int>>& head,int pivot) {
  std::unordered_map<ListNode<int>*,int> originals;
  for (auto node=head;node;node=node->next) originals.emplace(node.get(),node->data);
  auto result=executor.Run([&]{return ListPivoting(head,pivot);});
  std::unordered_set<ListNode<int>*> seen;
  int previous=-1;
  for (auto node=result;node;node=node->next) {
    auto original=originals.find(node.get());
    if (original==originals.end() || original->second!=node->data || !seen.insert(node.get()).second) throw TestFailure("Node identity, value or cycle violation");
    int group=node->data<pivot?0:node->data==pivot?1:2;
    if (group<previous) throw TestFailure("Pivot partitions out of order");
    previous=group;
  }
  if (seen.size()!=originals.size()) throw TestFailure("Lost list nodes");
}

int main(int argc, char* argv[]) {
  std::vector<std::string> arguments(argv+1, argv+argc);
  std::vector<std::string> parameters{"executor","l","x"};
  return GenericTestMain(arguments,"pivot_list.cc","pivot_list.tsv",&VerifyPivot,DefaultComparator{},parameters);
}
