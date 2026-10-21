public class Solution
{
    public List<int> Multiply(List<int> num1, List<int> num2)
    {
        if (num1.Count == 0 || num2.Count == 0)
            return new List<int> { 0 };
        bool negative = (num1[0] < 0) != (num2[0] < 0);
        var digits = new int[num1.Count + num2.Count];
        for (int i = num1.Count - 1; i >= 0; i--)
            for (int j = num2.Count - 1; j >= 0; j--)
            {
                int value = digits[i + j + 1] + Math.Abs(num1[i]) * Math.Abs(num2[j]);
                digits[i + j + 1] = value % 10;
                digits[i + j] += value / 10;
            }
        int first = 0;
        while (first + 1 < digits.Length && digits[first] == 0)
            first++;
        var result = digits.Skip(first).ToList();
        if (negative && result[0] != 0)
            result[0] = -result[0];
        return result;
    }
}
