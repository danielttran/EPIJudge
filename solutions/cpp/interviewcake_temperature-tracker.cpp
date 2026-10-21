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
class TempTracker {
    array<int, 111> counts{};
    long long sum = 0;
    int count = 0, minimum = 0, maximum = 0, mode = 0;
public:
    void Insert(int temperature) {
        if (count == 0) minimum = maximum = mode = temperature;
        minimum = min(minimum, temperature);
        maximum = max(maximum, temperature);
        sum += temperature;
        ++count;
        ++counts[temperature];
        if (counts[temperature] > counts[mode]) mode = temperature;
    }
    optional<int> GetMin() { return count ? optional<int>(minimum) : nullopt; }
    optional<int> GetMax() { return count ? optional<int>(maximum) : nullopt; }
    optional<double> GetMean() { return count ? optional<double>(static_cast<double>(sum) / count) : nullopt; }
    optional<int> GetMode() { return count ? optional<int>(mode) : nullopt; }
};
