#include <cstdint>
#include <limits>
#include <ostream>
#include <set>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

#include "test_framework/generic_test.h"
#include "test_framework/test_failure.h"

class ClientsCreditsInfo {
 public:
  void Insert(const std::string& client_id, int credit) {
    Remove(client_id);
    const std::int64_t normalized = static_cast<std::int64_t>(credit) - offset_;
    clients_.emplace(client_id, normalized);
    ranking_.emplace(normalized, client_id);
  }

  bool Remove(const std::string& client_id) {
    auto found = clients_.find(client_id);
    if (found == clients_.end()) return false;
    ranking_.erase({found->second, client_id});
    clients_.erase(found);
    return true;
  }

  int Lookup(const std::string& client_id) const {
    const auto found = clients_.find(client_id);
    if (found == clients_.end()) return -1;
    const std::int64_t actual = found->second + offset_;
    if (actual < std::numeric_limits<int>::min() ||
        actual > std::numeric_limits<int>::max()) {
      throw std::overflow_error(
          "The credit does not fit the public int result.");
    }
    return static_cast<int>(actual);
  }

  void AddAll(int amount) { offset_ += static_cast<std::int64_t>(amount); }

  std::string Max() const {
    return ranking_.empty() ? std::string{} : ranking_.rbegin()->second;
  }

 private:
  std::int64_t offset_ = 0;
  std::unordered_map<std::string, std::int64_t> clients_;
  std::set<std::pair<std::int64_t, std::string>> ranking_;
};

struct Operation {
  std::string op;
  std::string s_arg;
  int i_arg;
};

std::ostream& operator<<(std::ostream& output, const Operation& operation) {
  return output << operation.op << '(' << operation.s_arg << ", "
                << operation.i_arg << ')';
}

namespace test_framework {
template <>
struct SerializationTrait<Operation>
    : UserSerTrait<Operation, std::string, std::string, int> {};
}  // namespace test_framework

void ClientsCreditsInfoTester(const std::vector<Operation>& ops) {
  ClientsCreditsInfo credits;
  std::unordered_map<std::string, std::int64_t> expected_credits;
  for (std::size_t index = 0; index < ops.size(); ++index) {
    const Operation& operation = ops[index];
    if (operation.op == "ClientsCreditsInfo") {
      credits = ClientsCreditsInfo{};
      expected_credits.clear();
    } else if (operation.op == "insert") {
      credits.Insert(operation.s_arg, operation.i_arg);
      expected_credits[operation.s_arg] = operation.i_arg;
    } else if (operation.op == "add_all") {
      credits.AddAll(operation.i_arg);
      for (auto& entry : expected_credits) entry.second += operation.i_arg;
    } else if (operation.op == "remove") {
      const int actual = credits.Remove(operation.s_arg) ? 1 : 0;
      expected_credits.erase(operation.s_arg);
      if (actual != operation.i_arg) {
        throw TestFailure("Removal existence differs from its expected result.")
            .WithProperty(PropertyName::COMMAND, operation)
            .WithMismatchInfo(index, operation.i_arg, actual);
      }
    } else if (operation.op == "lookup") {
      const int actual = credits.Lookup(operation.s_arg);
      if (actual != operation.i_arg) {
        throw TestFailure("The client credit differs from its expected result.")
            .WithProperty(PropertyName::COMMAND, operation)
            .WithMismatchInfo(index, operation.i_arg, actual);
      }
    } else if (operation.op == "max") {
      const std::string actual = credits.Max();
      const auto selected = expected_credits.find(actual);
      bool valid = expected_credits.empty() ? actual.empty() : selected != expected_credits.end();
      if (valid && !expected_credits.empty()) {
        for (const auto& entry : expected_credits) {
          if (entry.second > selected->second) valid = false;
        }
      }
      if (!valid) {
        throw TestFailure(
            "Max must return an existing maximal-credit client, or empty when no clients exist.")
            .WithProperty(PropertyName::COMMAND, operation)
            .WithMismatchInfo(index, operation.s_arg, actual);
      }
    } else {
      throw TestFailure("Unknown credit operation: " + operation.op)
          .WithProperty(PropertyName::COMMAND, operation);
    }
  }
}

int main(int argc, char* argv[]) {
  std::vector<std::string> arguments(argv + 1, argv + argc);
  std::vector<std::string> parameters{"ops"};
  return GenericTestMain(arguments, "adding_credits.cc", "adding_credits.tsv",
                         &ClientsCreditsInfoTester, DefaultComparator{},
                         parameters);
}
