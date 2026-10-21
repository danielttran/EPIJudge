#include <chrono>
#include <fstream>
#include <iostream>
#include <iterator>
#include <sstream>
#include <tuple>
#include "test_framework/json.h"
using json = nlohmann::json;
#include "solution.cpp"

struct ContractError : std::runtime_error { using std::runtime_error::runtime_error; };
struct NeedChoice { int lower, upper; };
void check(bool condition, const std::string& message = "The result violates the bank contract.") {
    if (!condition) throw ContractError(message);
}
std::vector<LinkedListNode*> listNodes(LinkedListNode* head) {
    std::vector<LinkedListNode*> nodes;
    std::unordered_set<LinkedListNode*> seen;
    while (head) {
        check(seen.insert(head).second, "Output list contains a cycle.");
        nodes.push_back(head); head = head->Next;
    }
    return nodes;
}
std::vector<BinaryTreeNode*> treeNodes(BinaryTreeNode* root) {
    std::vector<BinaryTreeNode*> nodes, pending;
    std::unordered_set<BinaryTreeNode*> seen;
    if (root) pending.push_back(root);
    while (!pending.empty()) {
        auto node = pending.back(); pending.pop_back();
        check(seen.insert(node).second, "Input must remain a tree.");
        nodes.push_back(node);
        if (node->Left) pending.push_back(node->Left);
        if (node->Right) pending.push_back(node->Right);
    }
    return nodes;
}
LinkedListNode* readList(const json& raw) {
    LinkedListNode* head = nullptr;
    for (auto i = raw.rbegin(); i != raw.rend(); ++i) head = new LinkedListNode(i->get<int>(), head);
    return head;
}
BinaryTreeNode* readTree(const json& raw) {
    if (raw.empty()) return nullptr;
    auto root = new BinaryTreeNode(raw[0].get<int>());
    std::vector<BinaryTreeNode*> nodes{root};
    size_t position = 1;
    for (size_t i = 0; i < nodes.size(); ++i) {
        auto node = nodes[i];
        if (position < raw.size() && !raw[position].is_null()) {
            node->Left = new BinaryTreeNode(raw[position].get<int>()); nodes.push_back(node->Left);
        }
        ++position;
        if (position < raw.size() && !raw[position].is_null()) {
            node->Right = new BinaryTreeNode(raw[position].get<int>()); nodes.push_back(node->Right);
        }
        ++position;
    }
    return root;
}
std::vector<GraphNode*> readGraph(const json& raw) {
    std::vector<GraphNode*> nodes;
    for (size_t i = 0; i < raw.size(); ++i) nodes.push_back(new GraphNode("v" + std::to_string(i)));
    for (size_t i = 0; i < raw.size(); ++i)
        for (const auto& target : raw[i]) nodes[i]->Neighbors.insert(nodes.at(target.get<int>()));
    return nodes;
}
std::vector<Meeting*> readMeetings(const json& raw) {
    std::vector<Meeting*> meetings;
    for (const auto& row : raw) meetings.push_back(new Meeting(row[0].get<int>(), row[1].get<int>()));
    return meetings;
}
Rectangle* readRect(const json& raw) {
    return new Rectangle(raw[0].get<int>(), raw[1].get<int>(), raw[2].get<int>(), raw[3].get<int>());
}
std::vector<CakeType*> readCakes(const json& raw) {
    std::vector<CakeType*> cakes;
    for (const auto& row : raw) cakes.push_back(new CakeType(row[0].get<int>(), row[1].get<long long>()));
    return cakes;
}
std::vector<char> readChars(const json& raw) {
    auto text = raw.get<std::string>(); return {text.begin(), text.end()};
}
json dump(LinkedListNode* head) {
    json out = json::array(); for (auto node : listNodes(head)) out.push_back(node->Value); return out;
}
json dump(Rectangle* rectangle) {
    check(rectangle != nullptr, "Return a rectangle object.");
    return json::array({rectangle->LeftX, rectangle->BottomY, rectangle->Width, rectangle->Height});
}
json dump(const std::vector<Meeting*>& meetings) {
    json out = json::array();
    for (auto meeting : meetings) {
        check(meeting != nullptr, "A result meeting is null.");
        out.push_back(json::array({meeting->StartTime, meeting->EndTime}));
    }
    return out;
}
json dump(const std::vector<FilePaths>& paths) {
    json out = json::array();
    for (const auto& pair : paths) out.push_back(json::array({pair.OriginalPath, pair.DuplicatePath}));
    return out;
}
json dump(const std::vector<char>& characters) { return std::string(characters.begin(), characters.end()); }
template <typename T> json dump(const std::optional<T>& value) { return value ? json(*value) : json(nullptr); }
template <typename T> json dump(const T& value) { return json(value); }

auto preserve(BinaryTreeNode* root) {
    auto nodes = treeNodes(root);
    std::vector<std::tuple<int, BinaryTreeNode*, BinaryTreeNode*>> before;
    for (auto node : nodes) before.push_back({node->Value, node->Left, node->Right});
    return [nodes, before]() {
        for (size_t i = 0; i < nodes.size(); ++i)
            check(std::make_tuple(nodes[i]->Value, nodes[i]->Left, nodes[i]->Right) == before[i], "Tree values and links must remain unchanged.");
    };
}
auto preserve(LinkedListNode* head) {
    auto nodes = listNodes(head);
    std::vector<std::pair<int, LinkedListNode*>> before;
    for (auto node : nodes) before.push_back({node->Value, node->Next});
    return [nodes, before]() {
        for (size_t i = 0; i < nodes.size(); ++i)
            check(std::make_pair(nodes[i]->Value, nodes[i]->Next) == before[i], "List values and links must remain unchanged.");
    };
}
auto preserve(Rectangle* rectangle) {
    auto before = dump(rectangle);
    return [rectangle, before]() { check(dump(rectangle) == before, "Rectangle input was modified."); };
}
auto preserve(std::vector<Meeting*>& meetings) {
    auto pointers = meetings;
    std::vector<std::pair<int, int>> values;
    for (auto meeting : pointers) values.push_back({meeting->StartTime, meeting->EndTime});
    return [&meetings, pointers, values]() {
        check(meetings == pointers, "Meeting order or object identity changed.");
        for (size_t i = 0; i < pointers.size(); ++i)
            check(std::make_pair(pointers[i]->StartTime, pointers[i]->EndTime) == values[i], "Meeting fields were modified.");
    };
}
auto preserve(std::vector<CakeType*>& cakes) {
    auto pointers = cakes;
    std::vector<std::pair<int, long long>> values;
    for (auto cake : pointers) values.push_back({cake->Weight, cake->Value});
    return [&cakes, pointers, values]() {
        check(cakes == pointers, "Cake order or object identity changed.");
        for (size_t i = 0; i < pointers.size(); ++i)
            check(std::make_pair(pointers[i]->Weight, pointers[i]->Value) == values[i], "Cake fields were modified.");
    };
}
auto preserve(std::unordered_map<std::string, std::vector<std::string>>& graph) {
    auto before = graph;
    std::unordered_map<std::string, const void*> arrays, data;
    for (const auto& pair : graph) { arrays[pair.first] = &pair.second; data[pair.first] = pair.second.data(); }
    return [&graph, before, arrays, data]() {
        check(graph == before, "Graph adjacency contents changed.");
        for (const auto& pair : graph)
            check(&pair.second == arrays.at(pair.first) && pair.second.data() == data.at(pair.first), "Graph adjacency array identity changed.");
    };
}
template <typename T> auto preserve(T& value) {
    auto before = value;
    return [&value, before]() { check(value == before, "Read-only input was modified."); };
}
std::map<std::string, std::string> filesSnapshot(const std::string& root) {
    std::map<std::string, std::string> snapshot;
    for (const auto& entry : std::filesystem::recursive_directory_iterator(root)) {
        auto relative = std::filesystem::relative(entry.path(), root).generic_string();
        if (entry.is_directory()) snapshot[relative] = "directory";
        else if (entry.is_regular_file()) {
            std::ifstream file(entry.path(), std::ios::binary);
            std::string bytes((std::istreambuf_iterator<char>(file)), std::istreambuf_iterator<char>());
            auto ticks = std::filesystem::last_write_time(entry.path()).time_since_epoch().count();
            snapshot[relative] = std::to_string(ticks) + ":" + bytes;
        }
    }
    return snapshot;
}

template <typename Subject, typename Invoke>
json randomCheck(const json& raw, bool shuffle, int maximum, int outcomes, Invoke invoke) {
    std::vector<int> original = shuffle ? raw[0].get<std::vector<int>>() : std::vector<int>{};
    std::map<std::string, double> probabilities;
    struct Branch { std::vector<int> prefix; double weight; };
    std::vector<Branch> pending{{{}, 1.0}};
    double unresolved = 0;
    int branches = 0;
    auto checkBounds = [&](int lower, int upper) {
        check(lower <= upper && (shuffle ? lower >= 0 && upper < std::max(1, static_cast<int>(original.size())) : lower == 1 && upper == maximum), "Unexpected random-source bounds.");
    };
    while (!pending.empty()) {
        check(++branches <= 100000, "Randomized algorithm used too many decision branches.");
        auto branch = pending.back(); pending.pop_back();
        size_t position = 0;
        int draws = 0;
        RandomSource::Draw = [&](int lower, int upper) {
            check(++draws <= 128, "Randomized algorithm exceeded the draw budget."); checkBounds(lower, upper);
            if (position >= branch.prefix.size()) throw NeedChoice{lower, upper};
            int value = branch.prefix[position++];
            check(value >= lower && value <= upper, "Invalid injected random choice."); return value;
        };
        auto array = original;
        try {
            Subject fresh;
            json result = invoke(fresh, array);
            if (shuffle) {
                auto sorted = array, expected = original;
                std::sort(sorted.begin(), sorted.end()); std::sort(expected.begin(), expected.end());
                check(sorted == expected, "Shuffle changed element multiplicities."); result = dump(array);
            } else check(draws > 0 && (outcomes != 7 || draws % 2 == 0) && result.is_number_integer() && result.get<int>() >= 1 && result.get<int>() <= outcomes, "Invalid die result or random-source usage.");
            probabilities[result.dump()] += branch.weight;
        } catch (const NeedChoice& next) {
            int limit = shuffle ? std::max(8, static_cast<int>(original.size()) * 2) : 8;
            if (branch.prefix.size() >= static_cast<size_t>(limit)) unresolved += branch.weight;
            else for (int choice = next.lower; choice <= next.upper; ++choice) {
                auto prefix = branch.prefix; prefix.push_back(choice);
                pending.push_back({std::move(prefix), branch.weight / (next.upper - next.lower + 1)});
            }
        }
    }
    if (shuffle) {
        std::unordered_set<int> distinct(original.begin(), original.end());
        if (distinct.size() == original.size() && original.size() <= 5) {
            int factorial = 1; for (size_t i = 2; i <= original.size(); ++i) factorial *= static_cast<int>(i);
            check(unresolved < 1e-10 && probabilities.size() == static_cast<size_t>(factorial), "Shuffle omits full permutations.");
            for (const auto& entry : probabilities) check(std::abs(entry.second - 1.0 / factorial) < 1e-9, "Shuffle is biased over full permutations.");
        }
    } else {
        check(unresolved < 0.02, "Rejection probability exceeds the bounded exploration.");
        for (int value = 1; value <= outcomes; ++value) {
            double probability = probabilities[std::to_string(value)];
            check(probability <= 1.0 / outcomes + 1e-9 && probability + unresolved >= 1.0 / outcomes - 1e-9, "Die transformation is biased over injected choices.");
        }
    }
    std::uint32_t seed = 0x85ebca6bu;
    std::vector<int> counts(outcomes + 1);
    std::map<std::string, int> seededPermutations;
    constexpr int samples = 4096;
    std::vector<int> pairs(outcomes * outcomes), triples(outcomes * outcomes * outcomes);
    int previous = -1, beforePrevious = -1;
    Subject persistent;
    for (int trial = 0; trial < samples; ++trial) {
        int draws = 0;
        RandomSource::Draw = [&](int lower, int upper) {
            check(++draws <= 128, "Randomized algorithm exceeded the draw budget."); checkBounds(lower, upper);
            if (!shuffle && trial == 0 && draws <= static_cast<int>(raw[0].size())) {
                int forced = raw[0][draws - 1].get<int>();
                check(forced >= lower && forced <= upper, "Forced draw is outside source bounds.");
                return forced;
            }
            seed = seed * 1664525u + 1013904223u;
            return lower + static_cast<int>((static_cast<std::uint64_t>(seed) * static_cast<std::uint32_t>(upper - lower + 1)) >> 32);
        };
        auto array = original;
        json result = invoke(persistent, array);
        if (shuffle) {
            auto sorted = array, expected = original;
            std::sort(sorted.begin(), sorted.end()); std::sort(expected.begin(), expected.end());
            check(sorted == expected && (array.size() <= 1 || draws > 0), "Invalid shuffle or random-source usage.");
            ++seededPermutations[dump(array).dump()];
        } else {
            check(draws > 0 && (outcomes != 7 || draws % 2 == 0) && result.is_number_integer() && result.get<int>() >= 1 && result.get<int>() <= outcomes, "Invalid die result or source usage.");
            int value = result.get<int>() - 1;
            ++counts[value + 1];
            if (previous >= 0) ++pairs[previous * outcomes + value];
            if (beforePrevious >= 0) ++triples[(beforePrevious * outcomes + previous) * outcomes + value];
            beforePrevious = previous; previous = value;
        }
    }
    if (shuffle) {
        std::unordered_set<int> distinct(original.begin(), original.end());
        if (distinct.size() == original.size() && original.size() <= 5) {
            int factorial = 1; for (size_t i = 2; i <= original.size(); ++i) factorial *= static_cast<int>(i);
            check(seededPermutations.size() == static_cast<size_t>(factorial), "Seeded shuffle omits permutations.");
            double expected = static_cast<double>(samples) / factorial, statistic = 0;
            for (const auto& entry : probabilities) {
                double difference = seededPermutations[entry.first] - expected;
                statistic += difference * difference / expected;
            }
            check(statistic <= 4.0 * (factorial - 1) + 80, "Seeded shuffle permutation distribution is biased.");
        }
    } else {
        double expected = static_cast<double>(samples) / outcomes, chiSquared = 0;
        for (int i = 1; i <= outcomes; ++i) chiSquared += (counts[i] - expected) * (counts[i] - expected) / expected;
        check(chiSquared < 40, "Seeded die distribution is biased.");
        auto checkIndependence = [](const std::vector<int>& bins, int observations) {
            double expected = static_cast<double>(observations) / bins.size(), statistic = 0;
            for (int count : bins) statistic += (count - expected) * (count - expected) / expected;
            check(statistic < 4.0 * (bins.size() - 1) + 80, "Seeded die results are dependent across calls.");
        };
        checkIndependence(pairs, samples - 1);
        checkIndependence(triples, samples - 2);
    }
    RandomSource::Draw = [](int, int) -> int { throw std::logic_error("Random source is not active"); };
    return true;
}

// CONFIGURATION

std::string safeError(const char* text) {
    std::string result;
    for (size_t i = 0; text[i] && i < 4096; ++i) {
        unsigned char c = static_cast<unsigned char>(text[i]);
        result.push_back(c >= 32 && c <= 126 ? static_cast<char>(c) : '?');
    }
    return result;
}

int main() {
    std::ifstream input("cases.json"); json rows; input >> rows;
    json results = json::array();
    for (const auto& raw : rows) {
        auto start = std::chrono::steady_clock::now();
        json actual = nullptr, error = nullptr;
        bool invalid = false;
        std::ostringstream suppressed;
        auto output = std::cout.rdbuf(suppressed.rdbuf());
        try { actual = execute(raw); (void)actual.dump(); }
        catch (const ContractError& ex) { invalid = true; actual = nullptr; error = safeError(ex.what()); }
        catch (const std::exception& ex) { actual = nullptr; error = safeError(ex.what()); }
        catch (...) { actual = nullptr; error = "Unknown runtime error."; }
        std::cout.rdbuf(output);
        results.push_back({{"actual", actual}, {"error", error}, {"validationFailed", invalid},
            {"elapsedMs", std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - start).count()}});
    }
    std::ofstream report("results.json"); report << results.dump();
}
