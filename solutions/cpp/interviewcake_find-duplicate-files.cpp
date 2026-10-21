#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <deque>
#include <filesystem>
#include <fstream>
#include <functional>
#include <limits>
#include <map>
#include <optional>
#include <queue>
#include <set>
#include <sstream>
#include <stack>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>
using namespace std;
// Bank-supplied data types and injected randomness; no hidden algorithm helpers.
struct LinkedListNode { int Value; LinkedListNode* Next; LinkedListNode(int value,LinkedListNode* next=nullptr):Value(value),Next(next){} };
struct BinaryTreeNode { int Value; BinaryTreeNode *Left=nullptr,*Right=nullptr; explicit BinaryTreeNode(int value):Value(value){} };
struct GraphNode { string Label; unordered_set<GraphNode*> Neighbors; string Color; explicit GraphNode(string label):Label(move(label)){} };
struct Meeting { int StartTime,EndTime; Meeting(int start,int end):StartTime(start),EndTime(end){} };
struct Rectangle { int LeftX,BottomY,Width,Height; Rectangle(int x=0,int y=0,int width=0,int height=0):LeftX(x),BottomY(y),Width(width),Height(height){} };
struct CakeType { int Weight; long long Value; CakeType(int weight,long long value):Weight(weight),Value(value){} };
struct FilePaths { string OriginalPath,DuplicatePath; };
struct InfinityException:runtime_error { InfinityException():runtime_error("Unbounded optimum"){} };
struct RandomSource {
    inline static function<int(int,int)> Draw=[](int,int)->int{throw runtime_error("Random source must be injected by judge");};
    static int GetRandom(int lower,int upper){return Draw(lower,upper);}
    static int Rand5(){return GetRandom(1,5);} static int Rand7(){return GetRandom(1,7);}
};
class Solution {
    string Fingerprint(const filesystem::path& path) {
        auto size = filesystem::file_size(path);
        uintmax_t last = size > 64 ? size - 64 : 0;
        array<uintmax_t, 3> offsets{0, last / 2, last};
        string key = to_string(size) + ":";
        ifstream file(path, ios::binary);
        for (auto offset : offsets) {
            file.clear();
            file.seekg(static_cast<streamoff>(offset));
            char sample[64];
            file.read(sample, sizeof sample);
            key.append(sample, static_cast<size_t>(file.gcount()));
        }
        return key;
    }
public:
    vector<FilePaths> FindDuplicateFiles(const string& startingDirectory) {
        unordered_map<string, filesystem::path> firstByFingerprint;
        vector<FilePaths> pairs;
        for (const auto& entry : filesystem::recursive_directory_iterator(startingDirectory)) {
            if (!entry.is_regular_file()) continue;
            auto path = filesystem::absolute(entry.path()).lexically_normal();
            string key = Fingerprint(path);
            auto found = firstByFingerprint.find(key);
            if (found == firstByFingerprint.end()) firstByFingerprint.emplace(key, path);
            else {
                auto first = found->second;
                if (filesystem::last_write_time(path) < filesystem::last_write_time(first))
                    pairs.push_back({path.string(), first.string()});
                else pairs.push_back({first.string(), path.string()});
            }
        }
        return pairs;
    }
};
