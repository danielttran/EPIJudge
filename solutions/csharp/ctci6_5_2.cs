using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public string BinaryFraction(double number)
    {
        if (number <= 0 || number >= 1)
            return "ERROR";
        var result = new StringBuilder(".");
        for (int i = 0; i < 31; ++i)
        {
            number *= 2;
            bool bit = number >= 1;
            result.Append(bit ? '1' : '0');
            if (bit)
                --number;
            if (number == 0)
                return result.ToString();
        }
        return "ERROR";
    }
}
