public class Solution
{
    public bool ValidPlacementExists(List<int> team0, List<int> team1)
    {
        if (team0.Count != team1.Count)
            return false;
        var front = team0.Order().ToArray();
        var back = team1.Order().ToArray();
        for (int i = 0; i < front.Length; i++)
        if (front[i] >= back[i])
            return false;
        return true;
    }
}
