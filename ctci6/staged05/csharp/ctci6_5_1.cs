using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public int InsertBits(int word, int insert, int low, int high)
    {
        int width = high - low + 1;
        uint mask = width == 32 ? uint.MaxValue : (1u << width) - 1u;
        uint bits = unchecked((uint)word), replacement = unchecked((uint)insert);
        uint result = (bits & ~(mask << low)) | ((replacement & mask) << low);
        return unchecked((int)result);
    }
}
