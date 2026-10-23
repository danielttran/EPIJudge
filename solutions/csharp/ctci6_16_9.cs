using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public int AdditionOnlyArithmetic(int first, int second, string operation)
    {
        int Opposite(int value)
        {
            int step = value < 0 ? 1 : -1, result = 0;
            while (value != 0)
            {
                value += step;
                result += step;
            }
            return result;
        }
        if (operation == "subtract")
            return first + Opposite(second);
        if (operation == "multiply")
        {
            int count = second < 0 ? Opposite(second) : second,
                addend = second < 0 ? Opposite(first) : first, result = 0;
            while (count > 0)
            {
                result += addend;
                count += -1;
            }
            return result;
        }
        int remaining = first < 0 ? Opposite(first) : first,
            divisor = second < 0 ? Opposite(second) : second, remove = Opposite(divisor),
            step = (first < 0) == (second < 0) ? 1 : -1, quotient = 0;
        while (remaining + remove >= 0)
        {
            remaining += remove;
            quotient += step;
        }
        return quotient;
    }
}
