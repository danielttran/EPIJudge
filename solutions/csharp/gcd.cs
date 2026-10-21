public class Solution
{
    public long Gcd(long x, long y)
    {
        while (y != 0)
            (x, y) = (y, x % y);
        return x;
    }
}
