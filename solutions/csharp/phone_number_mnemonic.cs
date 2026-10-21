using System;
using System.Collections.Generic;
using System.Linq;
using EpiJudge.TestFramework;

public class Solution
{
    public List<string> PhoneMnemonic(string phone_number)
    {
        string[] letters = ["0", "1", "ABC", "DEF", "GHI", "JKL", "MNO", "PQRS", "TUV", "WXYZ"];
        var output = new List<string>();
        var current = new char[phone_number.Length];
        void Expand(int index)
        {
            if (index == current.Length)
            {
                output.Add(new string(current));
                return;
            }
            foreach (char letter in letters[phone_number[index] - '0'])
            {
                current[index] = letter;
                Expand(index + 1);
            }
        }
        Expand(0);
        return output;
    }
}
