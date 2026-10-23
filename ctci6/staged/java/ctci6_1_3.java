import java.util.*;
class Solution {
    public void Urlify(char[] buffer, int trueLength) {
        int write = buffer.length - 1;
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
}
