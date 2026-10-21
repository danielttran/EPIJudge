public class Solution
{
    public (int, int) FindDuplicateMissing(List<int> A)
    {
        var seen = new bool[A.Count];
        int duplicate = -1;
        foreach (int value in A)
        {
            if (seen[value])
                duplicate = value;
            seen[value] = true;
        }
        for (int value = 0; value < seen.Length; value++)
            if (!seen[value])
                return (duplicate, value);
        throw new ArgumentException("The input must contain one duplicate and one missing value.");
    }
}
