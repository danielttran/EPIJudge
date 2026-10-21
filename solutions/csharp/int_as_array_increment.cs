public class Solution
{
    public List<int> PlusOne(List<int> A)
    {
        var result = new List<int>(A);
        int index = result.Count - 1;
        while (index >= 0 && result[index] == 9)
            result[index--] = 0;
        if (index >= 0)
            result[index]++;
        else
            result.Insert(0, 1);
        return result;
    }
}
