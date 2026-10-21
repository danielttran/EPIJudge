public class Solution
{
    public List<int> GrayCode(int numBits)
    {
        var result = new List<int>(1 << numBits);
        for (int value = 0; value < (1 << numBits); value++)
            result.Add(value ^ (value >> 1));
        return result;
    }
}
