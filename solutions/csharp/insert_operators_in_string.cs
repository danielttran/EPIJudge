public class Solution
{
    public bool ExpressionSynthesis(List<int> digits, int target)
    {
        bool Search(int index, long total, long lastTerm)
        {
            if (index == digits.Count)
                return total == target;
            long value = 0;
            for (int end = index; end < digits.Count; end++)
            {
                value = value * 10 + digits[end];
                if (index == 0)
                {
                    if (Search(end + 1, value, value))
                        return true;
                }
                else if (Search(end + 1, total + value, value) ||
                         Search(end + 1, total - lastTerm + lastTerm * value, lastTerm * value))
                    return true;
            }
            return false;
        }
        return digits.Count > 0 && Search(0, 0, 0);
    }
}
