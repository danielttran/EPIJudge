#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <cstdint>
#include <functional>
#include <utility>
#include <unordered_map>
#include <unordered_set>
class Solution {
 public:
  std::vector<std::string> WordTransformation(const std::string& start, const std::string& stop,
                                              const std::vector<std::string>& dictionary) {
    std::unordered_set<std::string> words(dictionary.begin(), dictionary.end());
    std::unordered_map<std::string, std::string> previous{{start, ""}};
    std::vector<std::string> queue{start};
    for (size_t head = 0; head < queue.size(); ++head) {
      std::string word = queue[head];
      if (word == stop) {
        std::vector<std::string> path;
        for (std::string current = stop; !current.empty(); current = previous.at(current))
          path.push_back(current);
        std::reverse(path.begin(), path.end());
        return path;
      }
      for (size_t position = 0; position < word.size(); ++position) {
        std::string candidate = word;
        for (char letter = 'a'; letter <= 'z'; ++letter) {
          if (letter == word[position])
            continue;
          candidate[position] = letter;
          if (words.count(candidate) && !previous.count(candidate)) {
            previous[candidate] = word;
            queue.push_back(candidate);
          }
        }
      }
    }
    return {};
  }
};
