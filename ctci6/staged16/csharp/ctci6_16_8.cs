using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public string EnglishInteger(int value)
    {
        if (value == 0)
            return "Zero";
        string[] small = { "Zero",    "One",     "Two",       "Three",    "Four",
                           "Five",    "Six",     "Seven",     "Eight",    "Nine",
                           "Ten",     "Eleven",  "Twelve",    "Thirteen", "Fourteen",
                           "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen" },
                 tens = { "",      "",      "Twenty",  "Thirty", "Forty",
                          "Fifty", "Sixty", "Seventy", "Eighty", "Ninety" },
                 scales = { "", "Thousand", "Million", "Billion" };
        long magnitude = value;
        if (magnitude < 0)
            magnitude = -magnitude;
        List<string> groups = new List<string>();
        int scale = 0;
        while (magnitude > 0)
        {
            int chunk = (int)(magnitude % 1000);
            if (chunk != 0)
            {
                List<string> words = new List<string>();
                if (chunk >= 100)
                {
                    words.Add(small[chunk / 100]);
                    words.Add("Hundred");
                    chunk %= 100;
                }
                if (chunk >= 20)
                {
                    words.Add(tens[chunk / 10]);
                    chunk %= 10;
                }
                if (chunk != 0)
                    words.Add(small[chunk]);
                if (scale != 0)
                    words.Add(scales[scale]);
                groups.Add(string.Join(" ", words));
            }
            magnitude /= 1000;
            ++scale;
        }
        groups.Reverse();
        return (value < 0 ? "Negative " : "") + string.Join(" ", groups);
    }
}
