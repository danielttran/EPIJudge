using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public List<string> GetValidIpAddress(string s)
    {
        var output = new List<string>();
        if (s.Length < 4 || s.Length > 12)
            return output;
        bool Valid(string part) => part.Length > 0 && part.Length <= 3 && (part.Length == 1 || part[0] != '0') && int.Parse(part, System.Globalization.CultureInfo.InvariantCulture) <= 255;
        for (int a = 1; a <= 3 && a < s.Length; a++)
            for (int b = a + 1; b <= a + 3 && b < s.Length; b++)
                for (int c = b + 1; c <= b + 3 && c < s.Length; c++)
                {
                    string first = s[..a], second = s[a..b], third = s[b..c], fourth = s[c..];
                    if (Valid(first) && Valid(second) && Valid(third) && Valid(fourth))
                        output.Add(first + "." + second + "." + third + "." + fourth);
                }
        return output;
    }
}
