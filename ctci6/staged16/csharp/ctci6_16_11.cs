using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public int[] DivingBoardLengths(int planks, int shorter, int longer)
    {
        if (shorter == longer)
            return [planks * shorter];
        int[] result = new int[planks + 1];
        for (int count = 0; count <= planks; ++count)
            result[count] = planks * shorter + count * (longer - shorter);
        return result;
    }
}
