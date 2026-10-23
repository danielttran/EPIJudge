import java.util.*;
class Solution {
    public boolean OneAway(String first, String second) {
        int n = first.length(), m = second.length();
        if (n - m > 1 || m - n > 1) return false;
        int i = 0, j = 0;
        boolean used = false;
        while (i < n && j < m) {
            if (first.charAt(i) == second.charAt(j)) { ++i; ++j; }
            else {
                if (used) return false;
                used = true;
                if (n >= m) ++i;
                if (m >= n) ++j;
            }
        }
        return true;
    }
}
