class Harness
{
    static readonly JsonElement Config = JsonDocument.Parse(@"CONFIG_VALUE").RootElement.Clone();
    static Exception Unwrap(Exception error)
    {
        while (error is TargetInvocationException invocation && invocation.InnerException is not null) error = invocation.InnerException;
        return error;
    }
    static object Execute(JsonElement row)
    {
        string reference = row.GetProperty("ref").GetString()!;
        var args = row.GetProperty("arguments");
SORT_BRANCH_START
        if (reference == "3.5")
        {
            var stack = new IntStack();
            foreach (var value in args[0].EnumerateArray()) stack.Push(value.GetInt32());
            new Solution().SortStack(stack);
            var output = new List<int>();
            while (!stack.IsEmpty())
            {
                output.Add(stack.Pop());
                if (output.Count > args[0].GetArrayLength()) return new { actual = output, mutationOk = false };
            }
            return new { actual = output, mutationOk = true };
        }
SORT_BRANCH_END
        var operations = args[0]; var arguments = args[1]; var config = Config.GetProperty(reference);
        var type = typeof(Harness).Assembly.GetType(config.GetProperty("cls").GetString()!)!;
        object? instance = null;
        var outputs = new List<object?>(); bool valid = true;
        var animals = new List<(Animal Value, int Id, string Species)>();
        for (int i = 0; i < operations.GetArrayLength(); i++)
        {
            string op = operations[i].GetString()!;
            try
            {
                object?[] parameters = op == "Enqueue" ? [] : arguments[i].EnumerateArray().Select(value => (object?)value.GetInt32()).ToArray();
                if (i == 0) { instance = Activator.CreateInstance(type, parameters); outputs.Add(null); continue; }
                if (op == "Enqueue")
                {
                    var animal = new Animal(arguments[i][0].GetInt32(), arguments[i][1].GetString()!);
                    animals.Add((animal, animal.Id, animal.Species)); parameters = [animal];
                }
                var value = type.GetMethod(op)!.Invoke(instance, parameters);
                string kind = config.GetProperty("methods").GetProperty(op).GetString()!;
                if (kind == "animal" && value is not null)
                {
                    if (value is not Animal a || !animals.Any(original => ReferenceEquals(original.Value, a))) { valid = false; value = new { invalidIdentity = true }; }
                    else value = a.Id;
                }
                else if (kind == "void") { if (value is not null) valid = false; value = null; }
                else if (kind == "i" && value is not int) { valid = false; value = new { invalidReturn = "integer" }; }
                else if (kind == "b" && value is not bool) { valid = false; value = new { invalidReturn = "boolean" }; }
                outputs.Add(value);
            }
            catch (Exception error)
            {
                if (Unwrap(error) is BankError bank) outputs.Add(new { error = bank.Code });
                else throw;
            }
        }
        valid &= animals.All(a => a.Value.Id == a.Id && a.Value.Species == a.Species);
        return new { actual = outputs, mutationOk = valid };
    }
    static void Main()
    {
        using var data = JsonDocument.Parse(File.ReadAllText("cases.json")); var results = new List<object>();
        foreach (var row in data.RootElement.EnumerateArray())
        {
            try { results.Add(Execute(row)); }
            catch (Exception error) { results.Add(new { error = Unwrap(error).ToString() }); }
        }
        File.WriteAllText("results.json", JsonSerializer.Serialize(results));
    }
}
