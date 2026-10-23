import java.util.*;
class Solution {
    public boolean IsUnique(String text) {
        boolean[] seen = new boolean[128];
        for (int i = 0; i < text.length(); ++i) {
            int code = text.charAt(i);
            if (seen[code]) return false;
            seen[code] = true;
        }
        return true;
    }
}
