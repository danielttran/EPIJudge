using System;
using System.Collections.Generic;
using System.Text;
public class Solution
{
    public int[] ScoreMasterMind(string guess, string secret)
    {
        int[] remaining = new int[4];
        int hits = 0, pseudoHits = 0;
        for (int i = 0; i < 4; ++i)
        {
            if (guess[i] == secret[i])
                ++hits;
            else
                ++remaining["RGBY".IndexOf(secret[i])];
        }
        for (int i = 0; i < 4; ++i)
        {
            if (guess[i] == secret[i])
                continue;
            int color = "RGBY".IndexOf(guess[i]);
            if (remaining[color] > 0)
            {
                --remaining[color];
                ++pseudoHits;
            }
        }
        return [hits, pseudoHits];
    }
}
