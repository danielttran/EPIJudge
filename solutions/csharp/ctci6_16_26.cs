using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public double Calculate(string expression)
    {
        double total = 0, term = 0;
        char op = '+';
        int index = 0;
        while (index < expression.Length)
        {
            int number = 0;
            while (index < expression.Length && expression[index] >= '0' &&
                   expression[index] <= '9')
            {
                number = number * 10 + expression[index] - '0';
                index++;
            }
            if (op == '+')
            {
                total += term;
                term = number;
            }
            else if (op == '-')
            {
                total += term;
                term = -number;
            }
            else if (op == '*')
                term *= number;
            else
                term /= number;
            if (index < expression.Length)
                op = expression[index++];
        }
        return total + term;
    }
}
