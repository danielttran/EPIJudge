import java.util.*;
class Solution {
    public boolean IsRotation(String first, String second) {
        if (first.length() == 0 || first.length() != second.length()) return false;
        return (first + first).contains(second);
    }
}
