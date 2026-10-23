using System;
using System.Collections.Generic;
using System.Text;
public abstract class NumberFile { public abstract int ReadNext(); public abstract void Reset(); }
public class Solution
{
    public int FindMissingInt(NumberFile file, bool smallMemory)
    {
        int block = 0;
        if (smallMemory)
        {
            var counts = new int[2048];
            int value;
            while ((value = file.ReadNext()) != -1)
                counts[value >> 20]++;
            while (counts[block] == (1 << 20))
                block++;
            file.Reset();
        }
        var bitmap = new byte[smallMemory ? 1 << 17 : 1 << 28];
        int item;
        while ((item = file.ReadNext()) != -1)
            if (!smallMemory || (item >> 20) == block)
            {
                int offset = smallMemory ? item & ((1 << 20) - 1) : item;
                bitmap[offset >> 3] |= (byte)(1 << (offset & 7));
            }
        for (int index = 0; index < bitmap.Length; ++index)
            if (bitmap[index] != 255)
                for (int bit = 0; bit < 8; ++bit)
                    if ((bitmap[index] & (1 << bit)) == 0)
                        return (block << 20) + (index << 3) + bit;
        return -1;
    }
}
