using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public int Evaluate(string expression)
    {
        var stack = new Stack<int>();
        foreach (string token in expression.Split(','))
        {
            if (int.TryParse(token, out int value))
            {
                stack.Push(value);
                continue;
            }
            int right = stack.Pop(), left = stack.Pop();
            stack.Push(token switch
            {
                "+" => left + right,
                "-" => left - right,
                "*" => left * right,
                "/" => left / right,
                _ => throw new ArgumentException("Unknown operator.")
            });
        }
        return stack.Pop();
    }
}
