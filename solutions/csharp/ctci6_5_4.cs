using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public int[] SameWeightNeighbors(int number)
    {
        long Successor(long value)
        {
            if (value == 0)
                return -1L;
            long lowest = value & -value, raised = value + lowest;
            if (raised > 2147483647)
                return -1L;
            return raised | (((raised ^ value) / lowest) >> 2);
        }
        long larger = Successor(number), reverse = Successor(2147483647 ^ number),
             smaller = reverse == -1 ? -1 : (2147483647 ^ reverse);
        return new int[] { (int)(smaller), (int)(larger) };
    }
}
