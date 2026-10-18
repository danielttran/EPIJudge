using System.Text.Json;

namespace EpiJudge.TestFramework;

/// <summary>The JSON formats shared by the console and web judges.</summary>
public static class JudgeJson
{
    public static JsonSerializerOptions Options { get; } = Create();
    private static JsonSerializerOptions Create()
    {
        var options = new JsonSerializerOptions { IncludeFields = true };
        options.Converters.Add(new ValueTupleConverterFactory());
        options.Converters.Add(new BinaryTreeNodeConverterFactory());
        options.Converters.Add(new ListNodeConverterFactory());
        return options;
    }
}

public sealed class PostingListNode(int order)
{
    public int Order { get; set; } = order;
    public PostingListNode? Next { get; set; }
    public PostingListNode? Jump { get; set; }
}

public sealed class GraphVertex(int label)
{
    public int Label { get; set; } = label;
    public List<GraphVertex> Edges { get; set; } = [];
}
