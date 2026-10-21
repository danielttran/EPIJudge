public class Solution
{
    public void GroupByAge(List<(int Age, string Name)> people)
    {
        var groups = new Dictionary<int, List<(int Age, string Name)>>();
        foreach (var person in people)
        {
            if (!groups.TryGetValue(person.Age, out var group))
                groups.Add(person.Age, group = new());
            group.Add(person);
        }
        int index = 0;
        foreach (var group in groups.Values)
            foreach (var person in group)
                people[index++] = person;
    }
}
