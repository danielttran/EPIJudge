using System;
using System.Collections.Generic;
using System.Text;
public class Solution {
    public bool PalindromePermutation(string text) {
        int[] counts = new int[128];
        for (int i = 0; i < text.Length; ++i) {
            int code = text[i];
            if (code >= 65 && code <= 90) code += 32;
            if (code >= 97 && code <= 122) ++counts[code];
        }
        int odd = 0;
        for (int code = 97; code <= 122; ++code) odd += counts[code] % 2;
        return odd <= 1;
    }
}
