using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public int SparseSearch(string[] words, string target)
    {
        if (target.Length == 0)
            return -1;
        int low = 0, high = words.Length - 1;
        while (low <= high)
        {
            int middle = low + (high - low) / 2;
            if (words[middle].Length == 0)
            {
                int left = middle - 1, right = middle + 1;
                while (true)
                {
                    if (left < low && right > high)
                        return -1;
                    if (right <= high && !(words[right].Length == 0))
                    {
                        middle = right;
                        break;
                    }
                    if (left >= low && !(words[left].Length == 0))
                    {
                        middle = left;
                        break;
                    }
                    --left;
                    ++right;
                }
            }
            int comparison = StringComparer.Ordinal.Compare(words[middle], target);
            if (comparison == 0)
                return middle;
            if (comparison < 0)
                low = middle + 1;
            else
                high = middle - 1;
        }
        return -1;
    }
}
