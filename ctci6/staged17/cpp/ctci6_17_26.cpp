#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
#include <unordered_map>
class Solution {
 public:
  std::vector<std::vector<int>> SparseSimilarities(const std::vector<int>& documentIds,
                                                   const std::vector<std::vector<int>>& documents) {
    int n = static_cast<int>(documentIds.size());
    std::unordered_map<int, std::vector<int>> postings;
    for (int i = 0; i < n; ++i)
      for (int word : documents[i])
        postings[word].push_back(i);
    std::unordered_map<int, int> intersections;
    for (const auto& entry : postings) {
      const auto& posting = entry.second;
      for (size_t a = 0; a < posting.size(); ++a)
        for (size_t b = a + 1; b < posting.size(); ++b)
          ++intersections[posting[a] * n + posting[b]];
    }
    std::vector<std::vector<int>> result;
    for (const auto& entry : intersections) {
      int left = entry.first / n, right = entry.first % n, count = entry.second,
          a = documentIds[left], b = documentIds[right];
      result.push_back(
          {std::min(a, b), std::max(a, b), count,
           static_cast<int>(documents[left].size() + documents[right].size()) - count});
    }
    std::sort(result.begin(), result.end());
    return result;
  }
};
