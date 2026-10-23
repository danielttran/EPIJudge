using System;
using System.Collections.Generic;
using System.Text;
public abstract class BitArray { public abstract int Size(); public abstract int FetchBit(int index,int column); }
public class Solution
{
    public int MissingNumberBits(BitArray numbers)
    {
        var current = new List<int>();
        for (int i = 0; i < numbers.Size(); ++i)
            current.Add(i);
        int answer = 0, column = 0;
        while (current.Count > 0 && column < 32)
        {
            var zeros = new List<int>();
            var ones = new List<int>();
            foreach (int index in current)
                (numbers.FetchBit(index, column) == 0 ? zeros : ones).Add(index);
            if (zeros.Count <= ones.Count)
                current = zeros;
            else
            {
                answer |= 1 << column;
                current = ones;
            }
            column++;
        }
        return answer;
    }
}
