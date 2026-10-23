using System;
using System.Collections.Generic;
using System.Text;
public class Solution {
    public bool IsRotation(string first, string second) {
        if (first.Length == 0 || first.Length != second.Length) return false;
        return (first + first).Contains(second, StringComparison.Ordinal);
    }
}
