#pragma once
#include "test_framework/generic_test.h"

// Preserve EPI's native conversions, comparators, and custom problem wrappers.
// Report separately from stdout so debug prints cannot corrupt judge results.
template <typename Function, typename Comparator>
int WebGenericTestMain(const std::vector<std::string>&,
                       const std::string&, const std::string& test_data_file,
                       Function test_func, Comparator comparator,
                       const std::vector<std::string>& param_names,
                       const std::function<void(test_framework::TestConfig&)>& = {}) {
  using namespace test_framework;
  GenericTestHandler<Function, Comparator> handler(test_func, comparator, param_names);
  auto rows = SplitTsvFile("test_data/" + test_data_file);
  handler.ParseSignature(rows.at(0));
  std::ofstream report("native-results.jsonl");
  for (size_t i = 1; i < rows.size(); ++i) {
    auto fields = rows[i];
    fields.pop_back(); // Corpus explanation is not an argument.
    json row = {{"number", i}, {"status", "Accepted"}, {"actual", nullptr}, {"error", nullptr}};
    auto start = std::chrono::steady_clock::now();
    try {
      handler.RunTest(std::chrono::seconds{0}, nullptr, fields);
    } catch (TestFailure& e) {
      row["status"] = "Wrong answer";
      row["error"] = e.GetDescription();
      for (auto property : e.GetProperties()) {
        if (property.Id() == static_cast<int>(PropertyName::RESULT)) {
          std::ostringstream value;
          value << property.Value();
          row["actual"] = value.str().substr(0, 2000);
        }
      }
    } catch (TimeoutException&) {
      row["status"] = "Time limit exceeded";
    } catch (std::exception& e) {
      row["status"] = "Runtime error";
      row["error"] = std::string(e.what()).substr(0, 2000);
    } catch (...) {
      row["status"] = "Runtime error";
      row["error"] = "Unhandled native exception.";
    }
    row["elapsedMs"] = std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - start).count();
    report << row.dump() << std::endl;
  }
  return 0;
}
