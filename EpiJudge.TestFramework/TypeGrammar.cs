using System.Text.RegularExpressions;

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

        if (TryInner(grammar, "binary_tree", out var treeInner))
        {
            return IsGenericType(type, typeof(BinaryTreeNode<>), out var valueType) &&
                IsCompatible(treeInner, valueType);
        }

        if (TryInner(grammar, "linked_list", out var listInner))
        {
            return IsGenericType(type, typeof(ListNode<>), out var valueType) &&
                IsCompatible(listInner, valueType);
        }

        if (TryTuple(grammar, out var tupleTypes))
        {
            var tupleType = type.IsGenericType ? type.GetGenericTypeDefinition() : null;
            var argumentTypes = type.IsGenericType ? type.GetGenericArguments() : Array.Empty<Type>();
            var expectedDefinition = tupleTypes.Length switch
            {
                2 => typeof(ValueTuple<,>),
                3 => typeof(ValueTuple<,,>),
                4 => typeof(ValueTuple<,,,>),
                _ => null,
            };
            return tupleType == expectedDefinition && argumentTypes.Length == tupleTypes.Length &&
                tupleTypes.Select((part, index) => IsCompatible(part, argumentTypes[index])).All(value => value);
        }

        return false;
    }

    private static bool IsGenericType(Type type, Type genericDefinition, out Type valueType)
    {
        if (type.IsGenericType && type.GetGenericTypeDefinition() == genericDefinition)
        {
            valueType = type.GetGenericArguments()[0];
            return true;
        }
        valueType = typeof(void);
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

    private static bool TryTuple(string value, out string[] parts)
    {
        if (!value.StartsWith("tuple(", StringComparison.Ordinal) || !value.EndsWith(')'))
        {
            parts = Array.Empty<string>();
            return false;
        }

        var inner = value[6..^1];
        var depth = 0;
        var start = 0;
        var parsed = new List<string>();
        for (var index = 0; index < inner.Length; ++index)
        {
            if (inner[index] == '(') ++depth;
            else if (inner[index] == ')') --depth;
            else if (inner[index] == ',' && depth == 0)
            {
                parsed.Add(inner[start..index]);
                start = index + 1;
            }
        }
        parsed.Add(inner[start..]);
        parts = parsed.ToArray();
        return parts.Length is >= 2 and <= 4;
    }

    private static string RemoveComment(string value)
    {
        return Regex.Replace(value, @"\s*\[[^\]]*\]", string.Empty).Trim();
    }
}
