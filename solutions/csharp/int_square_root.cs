public class Solution
{
    public int SquareRoot(int k)
    {
        long low = 0, high = k, result = 0;
        while (low <= high)
        {
            long middle = low + (high - low) / 2;
            if (middle * middle <= k)
            {
                result = middle;
                low = middle + 1;
            }
            else
                high = middle - 1;
        }
        return (int)result;
    }
}
