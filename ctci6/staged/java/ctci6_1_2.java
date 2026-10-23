import java.util.*;
class Solution {
    public boolean CheckPermutation(String first, String second) {
        if (first.length() != second.length()) return false;
        int[] counts = new int[128];
        for (int i = 0; i < first.length(); ++i) ++counts[first.charAt(i)];
        for (int i = 0; i < second.length(); ++i) {
            int code = second.charAt(i);
            --counts[code];
            if (counts[code] < 0) return false;
        }
        return true;
    }
}
