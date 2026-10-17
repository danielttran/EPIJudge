using System.Text.Json;
using System.Text.Json.Serialization;

namespace EpiJudge.TestFramework;

internal sealed class ValueTupleConverterFactory : JsonConverterFactory
{
    public override bool CanConvert(Type typeToConvert)
    {
        if (!typeToConvert.IsGenericType) return false;
        var definition = typeToConvert.GetGenericTypeDefinition();
        return definition == typeof(ValueTuple<,>) ||
            definition == typeof(ValueTuple<,,>) ||
            definition == typeof(ValueTuple<,,,>);
    }

    public override JsonConverter CreateConverter(Type typeToConvert, JsonSerializerOptions options)
    {
        var arguments = typeToConvert.GetGenericArguments();
        var converterDefinition = arguments.Length switch
        {
            2 => typeof(ValueTuple2Converter<,>),
            3 => typeof(ValueTuple3Converter<,,>),
            4 => typeof(ValueTuple4Converter<,,,>),
            _ => throw new NotSupportedException($"Unsupported tuple arity: {arguments.Length}"),
        };
        return (JsonConverter)Activator.CreateInstance(converterDefinition.MakeGenericType(arguments), nonPublic: true)!;
    }

    private sealed class ValueTuple2Converter<T1, T2> : JsonConverter<(T1, T2)>
    {
        public override (T1, T2) Read(ref Utf8JsonReader reader, Type typeToConvert, JsonSerializerOptions options)
        {
            var values = ReadTuple(ref reader, 2);
            return (values[0].Deserialize<T1>(options)!, values[1].Deserialize<T2>(options)!);
        }

        public override void Write(Utf8JsonWriter writer, (T1, T2) value, JsonSerializerOptions options)
        {
            writer.WriteStartArray();
            JsonSerializer.Serialize(writer, value.Item1, options);
            JsonSerializer.Serialize(writer, value.Item2, options);
            writer.WriteEndArray();
        }
    }

    private sealed class ValueTuple3Converter<T1, T2, T3> : JsonConverter<(T1, T2, T3)>
    {
        public override (T1, T2, T3) Read(ref Utf8JsonReader reader, Type typeToConvert, JsonSerializerOptions options)
        {
            var values = ReadTuple(ref reader, 3);
            return (values[0].Deserialize<T1>(options)!, values[1].Deserialize<T2>(options)!,
                values[2].Deserialize<T3>(options)!);
        }

        public override void Write(Utf8JsonWriter writer, (T1, T2, T3) value, JsonSerializerOptions options)
        {
            writer.WriteStartArray();
            JsonSerializer.Serialize(writer, value.Item1, options);
            JsonSerializer.Serialize(writer, value.Item2, options);
            JsonSerializer.Serialize(writer, value.Item3, options);
            writer.WriteEndArray();
        }
    }

    private sealed class ValueTuple4Converter<T1, T2, T3, T4> : JsonConverter<(T1, T2, T3, T4)>
    {
        public override (T1, T2, T3, T4) Read(ref Utf8JsonReader reader, Type typeToConvert, JsonSerializerOptions options)
        {
            var values = ReadTuple(ref reader, 4);
            return (values[0].Deserialize<T1>(options)!, values[1].Deserialize<T2>(options)!,
                values[2].Deserialize<T3>(options)!, values[3].Deserialize<T4>(options)!);
        }

        public override void Write(Utf8JsonWriter writer, (T1, T2, T3, T4) value, JsonSerializerOptions options)
        {
            writer.WriteStartArray();
            JsonSerializer.Serialize(writer, value.Item1, options);
            JsonSerializer.Serialize(writer, value.Item2, options);
            JsonSerializer.Serialize(writer, value.Item3, options);
            JsonSerializer.Serialize(writer, value.Item4, options);
            writer.WriteEndArray();
        }
    }

    private static JsonElement[] ReadTuple(ref Utf8JsonReader reader, int arity)
    {
        using var document = JsonDocument.ParseValue(ref reader);
        if (document.RootElement.ValueKind != JsonValueKind.Array)
            throw new JsonException("Tuple values must be serialized as JSON arrays.");
        var values = document.RootElement.EnumerateArray().ToArray();
        if (values.Length != arity)
            throw new JsonException($"Expected {arity} tuple values, got {values.Length}.");
        return values;
    }
}

internal sealed class BinaryTreeNodeConverterFactory : JsonConverterFactory
{
    public override bool CanConvert(Type typeToConvert) =>
        typeToConvert.IsGenericType && typeToConvert.GetGenericTypeDefinition() == typeof(BinaryTreeNode<>);

    public override JsonConverter CreateConverter(Type typeToConvert, JsonSerializerOptions options) =>
        (JsonConverter)Activator.CreateInstance(
            typeof(BinaryTreeNodeConverter<>).MakeGenericType(typeToConvert.GetGenericArguments()), nonPublic: true)!;

    private sealed class BinaryTreeNodeConverter<T> : JsonConverter<BinaryTreeNode<T>>
    {
        public override BinaryTreeNode<T>? Read(ref Utf8JsonReader reader, Type typeToConvert, JsonSerializerOptions options)
        {
            using var document = JsonDocument.ParseValue(ref reader);
            if (document.RootElement.ValueKind != JsonValueKind.Array)
                throw new JsonException("Binary trees must be serialized as level-order JSON arrays.");
            var values = document.RootElement.EnumerateArray().ToArray();
            if (values.Length == 0 || values[0].ValueKind == JsonValueKind.Null) return null;

            var root = NewNode(values[0], options);
            var queue = new Queue<BinaryTreeNode<T>>();
            queue.Enqueue(root);
            var index = 1;
            while (queue.Count > 0 && index < values.Length)
            {
                var parent = queue.Dequeue();
                if (index < values.Length && values[index].ValueKind != JsonValueKind.Null)
                {
                    parent.Left = NewNode(values[index], options);
                    parent.Left.Parent = parent;
                    queue.Enqueue(parent.Left);
                }
                ++index;
                if (index < values.Length && values[index].ValueKind != JsonValueKind.Null)
                {
                    parent.Right = NewNode(values[index], options);
                    parent.Right.Parent = parent;
                    queue.Enqueue(parent.Right);
                }
                ++index;
            }
            return root;
        }

        public override void Write(Utf8JsonWriter writer, BinaryTreeNode<T> value, JsonSerializerOptions options)
        {
            if (value is null)
            {
                writer.WriteStartArray();
                writer.WriteEndArray();
                return;
            }

            var values = new List<BinaryTreeNode<T>?>();
            var queue = new Queue<BinaryTreeNode<T>?>();
            queue.Enqueue(value);
            while (queue.Count > 0)
            {
                var node = queue.Dequeue();
                values.Add(node);
                if (node is not null)
                {
                    queue.Enqueue(node.Left);
                    queue.Enqueue(node.Right);
                }
            }
            while (values.Count > 0 && values[^1] is null) values.RemoveAt(values.Count - 1);

            writer.WriteStartArray();
            foreach (var node in values)
            {
                if (node is null) writer.WriteNullValue();
                else JsonSerializer.Serialize(writer, node.Data, options);
            }
            writer.WriteEndArray();
        }

        private static BinaryTreeNode<T> NewNode(JsonElement value, JsonSerializerOptions options) =>
            new(value.Deserialize<T>(options)!);
    }
}

internal sealed class ListNodeConverterFactory : JsonConverterFactory
{
    public override bool CanConvert(Type typeToConvert) =>
        typeToConvert.IsGenericType && typeToConvert.GetGenericTypeDefinition() == typeof(ListNode<>);

    public override JsonConverter CreateConverter(Type typeToConvert, JsonSerializerOptions options) =>
        (JsonConverter)Activator.CreateInstance(
            typeof(ListNodeConverter<>).MakeGenericType(typeToConvert.GetGenericArguments()), nonPublic: true)!;

    private sealed class ListNodeConverter<T> : JsonConverter<ListNode<T>>
    {
        public override ListNode<T>? Read(ref Utf8JsonReader reader, Type typeToConvert, JsonSerializerOptions options)
        {
            var values = JsonSerializer.Deserialize<List<T>>(ref reader, options) ?? [];
            ListNode<T>? head = null;
            ListNode<T>? tail = null;
            foreach (var value in values)
            {
                var node = new ListNode<T>(value);
                if (head is null) head = node;
                else tail!.Next = node;
                tail = node;
            }
            return head;
        }

        public override void Write(Utf8JsonWriter writer, ListNode<T> value, JsonSerializerOptions options)
        {
            writer.WriteStartArray();
            var visited = new HashSet<ListNode<T>>(ReferenceEqualityComparer.Instance);
            for (var node = value; node is not null; node = node.Next)
            {
                if (!visited.Add(node)) throw new JsonException("Cannot serialize a cyclic linked list.");
                JsonSerializer.Serialize(writer, node.Data, options);
            }
            writer.WriteEndArray();
        }
    }
}
