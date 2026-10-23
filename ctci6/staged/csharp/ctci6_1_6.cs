using System;
using System.Collections.Generic;
using System.Text;
public class Solution {
    public string Compress(string text) {
        var output = new System.Text.StringBuilder();
        int n = text.Length;
        for (int start = 0; start < n;) {
            int end = start + 1;
            while (end < n && text[end] == text[start]) ++end;
            output.Append(text[start]); output.Append(end - start);
            start = end;
        }
        return output.Length < n ? output.ToString() : text;
    }
}
