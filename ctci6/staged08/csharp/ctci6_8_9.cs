using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public List<string> GenerateParentheses(int pairs)
    {
        char[] buffer = new char[2 * pairs];
        var result = new List<string>();
        void Visit(int opened, int closed)
        {
            int position = opened + closed;
            if (position == buffer.Length)
            {
                result.Add(new string(buffer));
                return;
            }
            if (opened < pairs)
            {
                buffer[position] = '(';
                Visit(opened + 1, closed);
            }
            if (closed < opened)
            {
                buffer[position] = ')';
                Visit(opened, closed + 1);
            }
        }
        Visit(0, 0);
        return result;
    }
}
