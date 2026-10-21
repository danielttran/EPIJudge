public class Solution
{
    public int Fibonacci(int n)
    {
        int previous = 0, current = 1;
        for (int i = 0; i < n; i++)
            (previous, current) = (current, previous + current);
        return previous;
    }
}
