using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public bool OneAway(string first, string second)
    {
        int n = first.Length, m = second.Length;
        if (n - m > 1 || m - n > 1)
            return false;
        int i = 0, j = 0;
        bool used = false;
        while (i < n && j < m)
        {
            if (first[i] == second[j])
            {
                ++i;
                ++j;
            }
            else
            {
                if (used)
                    return false;
                used = true;
                if (n >= m)
                    ++i;
                if (m >= n)
                    ++j;
            }
        }
        return true;
    }
}
