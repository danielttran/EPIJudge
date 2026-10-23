#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
struct RandomNode { int Data; RandomNode* Left=nullptr; RandomNode* Right=nullptr; explicit RandomNode(int data):Data(data){} virtual ~RandomNode()=default; };
#include <stdexcept>
struct RandomSource { inline static std::function<int(int,int)> Draw=[](int,int)->int{throw std::runtime_error("Provided by the judge");}; static int GetRandom(int lower,int upper){return Draw(lower,upper);} };
class RandomBst {
  struct SizedNode final : RandomNode {
    int Size = 1;
    explicit SizedNode(int value) : RandomNode(value) {
    }
  };
  static int size(RandomNode* node) {
    return node == nullptr ? 0 : static_cast<SizedNode*>(node)->Size;
  }

 public:
  RandomNode* Root = nullptr;
  RandomBst() = default;
  RandomBst(const RandomBst&) = delete;
  RandomBst& operator=(const RandomBst&) = delete;
  ~RandomBst() {
    std::vector<RandomNode*> pending;
    if (Root != nullptr)
      pending.push_back(Root);
    while (!pending.empty()) {
      auto node = pending.back();
      pending.pop_back();
      if (node->Left != nullptr)
        pending.push_back(node->Left);
      if (node->Right != nullptr)
        pending.push_back(node->Right);
      delete node;
    }
    Root = nullptr;
  }
  void Insert(int value) {
    auto added = new SizedNode(value);
    if (Root == nullptr) {
      Root = added;
      return;
    }
    std::vector<RandomNode*> path;
    auto node = Root;
    while (true) {
      path.push_back(node);
      if (value <= node->Data) {
        if (node->Left == nullptr) {
          node->Left = added;
          break;
        }
        node = node->Left;
      } else {
        if (node->Right == nullptr) {
          node->Right = added;
          break;
        }
        node = node->Right;
      }
    }
    for (auto ancestor : path)
      ++static_cast<SizedNode*>(ancestor)->Size;
  }
  RandomNode* Find(int value) {
    auto node = Root;
    while (node != nullptr) {
      if (value == node->Data)
        return node;
      node = value < node->Data ? node->Left : node->Right;
    }
    return nullptr;
  }
  bool Delete(int value) {
    std::vector<RandomNode*> path;
    auto node = Root;
    while (node != nullptr && node->Data != value) {
      path.push_back(node);
      node = value < node->Data ? node->Left : node->Right;
    }
    if (node == nullptr)
      return false;
    if (node->Left != nullptr && node->Right != nullptr) {
      path.push_back(node);
      auto successor = node->Right;
      while (successor->Left != nullptr) {
        path.push_back(successor);
        successor = successor->Left;
      }
      node->Data = successor->Data;
      node = successor;
    }
    auto replacement = node->Left != nullptr ? node->Left : node->Right;
    if (path.empty())
      Root = replacement;
    else {
      auto parent = path.back();
      if (parent->Left == node)
        parent->Left = replacement;
      else
        parent->Right = replacement;
    }
    for (auto ancestor : path)
      --static_cast<SizedNode*>(ancestor)->Size;
    delete node;
    return true;
  }
  RandomNode* GetRandomNode() {
    if (Root == nullptr)
      return nullptr;
    int rank = RandomSource::GetRandom(0, size(Root) - 1);
    auto node = Root;
    while (node != nullptr) {
      int leftSize = size(node->Left);
      if (rank < leftSize)
        node = node->Left;
      else if (rank == leftSize)
        return node;
      else {
        rank -= leftSize + 1;
        node = node->Right;
      }
    }
    return nullptr;
  }
};
