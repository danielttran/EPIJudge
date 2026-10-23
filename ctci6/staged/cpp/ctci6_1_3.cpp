#include <algorithm>
#include <array>
#include <string>
#include <vector>
class Solution {
public:
    void Urlify(std::vector<char>& buffer, int trueLength) {
        int write = static_cast<int>(buffer.size()) - 1;
        for (int read = trueLength - 1; read >= 0; --read) {
            char current = buffer[read];
            if (current == ' ') {
                buffer[write--] = '0';
                buffer[write--] = '2';
                buffer[write--] = '%';
            } else {
                buffer[write--] = current;
            }
        }
    }
};
