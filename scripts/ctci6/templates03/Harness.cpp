json execute(const json& row) {
  std::string ref = row["ref"].get<std::string>(); const auto& args = row["arguments"];
SORT_BRANCH_START
  if (ref == "3.5") {
    IntStack stack; for (const auto& value : args[0]) stack.Push(value.get<int>());
    Solution().SortStack(stack); json output = json::array();
    while (!stack.IsEmpty()) {
      output.push_back(stack.Pop());
      if (output.size() > args[0].size()) return json{{"actual",output},{"mutationOk",false}};
    }
    return json{{"actual",output},{"mutationOk",true}};
  }
SORT_BRANCH_END
  const auto& operations = args[0]; const auto& arguments = args[1];
  json output = json::array(); bool valid = true;
  std::vector<std::unique_ptr<Animal>> owners; std::unordered_set<Animal*> originals;
  STATE_BRANCHES
  return json{{"actual",output},{"mutationOk",valid}};
}
int main() {
  std::ifstream input("cases.json"); json rows; input >> rows; json results = json::array();
  for (const auto& row : rows) {
    try { results.push_back(execute(row)); }
    catch (const std::exception& error) { results.push_back(json{{"error",error.what()}}); }
  }
  std::ofstream("results.json") << results;
}
