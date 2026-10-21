public class Solution
{
    public List<List<int>> ComputeTowerHanoi(int numRings)
    {
        var moves = new List<List<int>>();
        void Transfer(int count, int from, int to, int spare)
        {
            if (count == 0)
                return;
            Transfer(count - 1, from, spare, to);
            moves.Add(new List<int> { from, to });
            Transfer(count - 1, spare, to, from);
        }
        Transfer(numRings, 0, 1, 2);
        return moves;
    }
}
