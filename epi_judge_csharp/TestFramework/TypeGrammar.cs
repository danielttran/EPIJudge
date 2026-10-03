namespace EpiJudge.TestFramework;

internal static class TypeGrammar
{
    public static void AssertCompatible(string grammar, Type type)
    {
        grammar = RemoveComment(grammar.Trim());
        if (!IsCompatible(grammar, type))
        {
            throw new InvalidDataException(
                $"TSV type '{grammar}' is incompatible with C# type '{type}'.");
        }
    }

    private static bool IsCompatible(string grammar, Type type)
    {
        if (grammar == "void") return type == typeof(void);
        if (grammar == "bool") return type == typeof(bool);
        if (grammar == "string") return type == typeof(string);
        if (grammar == "int") return type is { } && (type == typeof(short) || type == typeof(int));
        if (grammar == "long") return type == typeof(long);
        if (grammar == "float") return type is { } && (type == typeof(float) || type == typeof(double));

        if (TryInner(grammar, "array", out var arrayInner))
        {
            var elementType = GetSequenceElementType(type);
            return elementType is not null && IsCompatible(arrayInner, elementType);
        }

        if (TryInner(grammar, "set", out var setInner))
        {
            var setInterface = type.GetInterfaces().Append(type)
                .FirstOrDefault(t => t.IsGenericType && t.GetGenericTypeDefinition() == typeof(ISet<>));
            return setInterface is not null && IsCompatible(setInner, setInterface.GetGenericArguments()[0]);
        }

        return false;
    }

    private static Type? GetSequenceElementType(Type type)
    {
        if (type.IsArray) return type.GetElementType();
        var sequence = type.GetInterfaces().Append(type)
            .FirstOrDefault(t => t.IsGenericType && t.GetGenericTypeDefinition() == typeof(IEnumerable<>));
        return sequence?.GetGenericArguments()[0];
    }

    private static bool TryInner(string value, string name, out string inner)
    {
        var prefix = name + "(";
        if (value.StartsWith(prefix, StringComparison.Ordinal) && value.EndsWith(')'))
        {
            inner = value[prefix.Length..^1];
            return true;
        }
        inner = string.Empty;
        return false;
    }

    private static string RemoveComment(string value)
    {
        var bracket = value.IndexOf('[', StringComparison.Ordinal);
        return bracket < 0 ? value : value[..bracket].TrimEnd();
    }
}
