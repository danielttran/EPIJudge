#include <algorithm>
#include <array>
#include <string>
#include <vector>
class Solution {
public:
    bool OneAway(const std::string& first, const std::string& second) {
        int n = static_cast<int>(first.size()), m = static_cast<int>(second.size());
        if (n - m > 1 || m - n > 1) return false;
        int i = 0, j = 0;
        bool used = false;
        while (i < n && j < m) {
            if (first[i] == second[j]) { ++i; ++j; }
            else {
                if (used) return false;
                used = true;
                if (n >= m) ++i;
                if (m >= n) ++j;
            }
        }
        return true;
    }
};
