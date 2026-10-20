using System.Reflection;
using System.Text.Json;
using System.Diagnostics;

internal sealed class ContractError(string message) : Exception(message);
internal static class Harness
{
    static readonly JsonSerializerOptions Json = new() { IncludeFields = true };
    static void Check(bool ok, string message = "The result violates the problem contract.") { if (!ok) throw new ContractError(message); }
    static object? Call(object target, string name, params object?[] args)
    {
        try { return target.GetType().GetMethod(name)!.Invoke(target,args); }
        catch(TargetInvocationException ex) { throw ex.InnerException ?? ex; }
    }
    static object New(string name) => Activator.CreateInstance(Assembly.GetExecutingAssembly().GetType(name)!)!;
    static List<ListNode> ListNodes(ListNode? head)
    {
        var nodes=new List<ListNode>(); var seen=new HashSet<ListNode>(ReferenceEqualityComparer.Instance);
        while(head is not null) { Check(seen.Add(head),"Output list contains a cycle."); nodes.Add(head);head=head.next; }
        return nodes;
    }
    static List<object> Nodes(object? root,string kind)
    {
        if(kind=="list") return ListNodes((ListNode?)root).Cast<object>().ToList();
        if(kind=="lists") return ((ListNode?[])root!).SelectMany(ListNodes).Cast<object>().ToList();
        if(kind is not ("tree" or "graph")) return [];
        var result=new List<object>();var seen=new HashSet<object>(ReferenceEqualityComparer.Instance);var q=new Stack<object>();
        if(root is not null)q.Push(root);
        while(q.TryPop(out var n))
        {
            if(!seen.Add(n)) {Check(kind=="graph","Tree contains a cycle or shared child.");continue;}
            result.Add(n);
            if(n is Node g) foreach(var c in g.neighbors)q.Push(c);
            else if(n is TreeNode t) {if(t.left is not null)q.Push(t.left);if(t.right is not null)q.Push(t.right);}
        }
        return result;
    }
    static int Val(object n) => n switch {ListNode l=>l.val,TreeNode t=>t.val,Node g=>g.val,_=>throw new InvalidOperationException()};
    static object?[] Links(object n) => n switch {ListNode l=>[l.next],TreeNode t=>[t.left,t.right],Node g=>g.neighbors.Cast<object?>().ToArray(),_=>[]};
    static object? Load(JsonElement v,string kind)
    {
        if(kind=="list") {ListNode? head=null;foreach(var n in v.EnumerateArray().Reverse())head=new(n.GetInt32(),head);return head;}
        if(kind=="lists") return v.EnumerateArray().Select(row=>(ListNode?)Load(row,"list")).ToArray();
        if(kind=="tree")
        {
            var values=v.EnumerateArray().ToArray();if(values.Length==0)return null;
            var root=new TreeNode(values[0].GetInt32());var q=new Queue<TreeNode>();q.Enqueue(root);int i=1;
            while(q.TryDequeue(out var n))
            {
                if(i<values.Length && values[i].ValueKind!=JsonValueKind.Null){n.left=new(values[i].GetInt32());q.Enqueue(n.left);}i++;
                if(i<values.Length && values[i].ValueKind!=JsonValueKind.Null){n.right=new(values[i].GetInt32());q.Enqueue(n.right);}i++;
            }
            return root;
        }
        if(kind=="graph")
        {
            var rows=v.EnumerateArray().ToArray();var nn=rows.Select((_,i)=>new Node(i+1)).ToArray();
            for(int i=0;i<nn.Length;i++)nn[i].neighbors=rows[i].EnumerateArray().Select(c=>nn[c.GetInt32()-1]).ToList();
            return nn.FirstOrDefault();
        }
        return kind switch {"i"=>v.GetInt32(),"l"=>v.GetInt64(),"s"=>v.GetString(),"b"=>v.GetBoolean(),
            "ai"=>v.Deserialize<int[]>(),"as"=>v.Deserialize<string[]>(),"aai"=>v.Deserialize<int[][]>(),
            "aas"=>v.Deserialize<string[][]>(),"ab"=>v.Deserialize<bool[]>(),"ad"=>v.Deserialize<double[]>(),_=>throw new InvalidOperationException(kind)};
    }
    static object? Dump(object? value,string kind)
    {
        if(kind=="list")return ListNodes((ListNode?)value).Select(n=>n.val).ToArray();
        if(kind=="tree_node")return (value as TreeNode)?.val;
        if(kind=="tree")
        {
            Nodes(value,"tree");var result=new List<int?>();var q=new Queue<TreeNode?>();if(value is not null)q.Enqueue((TreeNode)value);
            while(q.TryDequeue(out var n)){result.Add(n?.val);if(n is not null){q.Enqueue(n.left);q.Enqueue(n.right);}}
            while(result.Count>0 && result[^1] is null)result.RemoveAt(result.Count-1);return result;
        }
        if(kind=="graph")
        {
            var nn=Nodes(value,"graph").Cast<Node>().OrderBy(n=>n.val).ToArray();
            Check(nn.Select(n=>n.val).SequenceEqual(Enumerable.Range(1,nn.Length)),"Graph labels must remain unique and contiguous.");
            return nn.Select(n=>n.neighbors.Select(c=>c.val).Order().ToArray()).ToArray();
        }
        return value;
    }
    static object? Execute(JsonElement raw)
    {
        var args=Kinds.Select((kind,i)=>Load(raw[i],kind)).ToArray();
        var original=args.SelectMany((v,i)=>Nodes(v,Kinds[i])).ToArray();
        var snapshot=new Dictionary<object,int>(ReferenceEqualityComparer.Instance);foreach(var n in original)snapshot[n]=Val(n);
        var originalLinks=new Dictionary<object,object?[]>(ReferenceEqualityComparer.Instance);foreach(var n in original)originalLinks[n]=Links(n);
        var rows=Mode=="matrix_inplace"?((int[][])args[0]!).ToArray():[];
        var before=Mode is "tree_codec" or "graph_clone"?JsonSerializer.Serialize(Dump(args[0],Kinds[0]),Json):null;
        object? actual;
        if(Mode=="list_cycle")
        {
            var nn=ListNodes((ListNode?)args[0]);int pos=raw[1].GetInt32();if(pos>=0)nn[^1].next=nn[pos];var edges=nn.Select(n=>n.next).ToArray();
            actual=Call(New("Solution"),Method,args);Check(nn.Select((n,i)=>ReferenceEquals(n.next,edges[i])).All(v=>v),"Cycle detection must preserve links.");
            Check(nn.All(n=>n.val==snapshot[n]),"Cycle detection must preserve values.");
        }
        else if(Mode=="strings_codec") actual=Call(New("Codec"),"Decode",Call(New("Codec"),"Encode",args[0]));
        else if(Mode=="tree_codec") actual=Call(New("Codec"),"Deserialize",Call(New("Codec"),"Serialize",args[0]));
        else if(Mode is "trie" or "dictionary" or "median")
        {
            var obj=New(Class);var operations=(string[])args[0]!;var values=(Array)args[1]!;var results=new List<object?>();
            for(int i=0;i<operations.Length;i++)
            {
                var op=operations[i];var name=char.ToUpperInvariant(op[0])+op[1..];
                var result=Call(obj,name,op=="findMedian"?[]:[values.GetValue(i)]);
                if(op is not ("insert" or "addWord" or "addNum"))results.Add(result);
            }
            actual=results;
        }
        else {actual=Call(New("Solution"),Method,args);if(Mode is "matrix_inplace" or "list_reorder")actual=args[0];}
        if(Mode=="matrix_inplace")Check(rows.Length==((int[][])args[0]!).Length && rows.Select((row,i)=>ReferenceEquals(row,((int[][])args[0]!)[i])).All(v=>v),"Preserve each row object.");
        if(Mode is "list_reuse" or "list_remove" or "list_reorder" or "tree_inplace" or "tree_node" or "tree_codec" or "graph_clone")
        {
            var kind=Mode.StartsWith("list_",StringComparison.Ordinal)?"list":Mode=="graph_clone"?"graph":"tree";
            var after=Mode=="tree_node"?(actual is null?new List<object>():[actual]):Nodes(actual,kind);
            bool Same(IEnumerable<object> expected) => new HashSet<object>(expected,ReferenceEqualityComparer.Instance).SetEquals(after);
            if(Mode=="list_remove")Check(Same(original.Where((_,i)=>i!=original.Length-(int)args[1]!)),"Remove exactly the requested original node.");
            else if(Mode is "list_reuse" or "list_reorder" or "tree_inplace")Check(Same(original),"Reuse exactly the original nodes.");
            else if(Mode=="tree_node")Check(actual is not null && snapshot.ContainsKey(actual),"Return an original tree node.");
            else {Check(after.All(n=>!snapshot.ContainsKey(n)),"Copy shares original nodes.");Check(JsonSerializer.Serialize(Dump(args[0],Kinds[0]),Json)==before,"Preserve original structure.");Check(original.All(n=>kind=="graph"?Links(n).Length==originalLinks[n].Length&&new HashSet<object?>(Links(n),ReferenceEqualityComparer.Instance).SetEquals(originalLinks[n]):Links(n).SequenceEqual(originalLinks[n],ReferenceEqualityComparer.Instance)),"Preserve original node links.");}
            Check(original.All(n=>Val(n)==snapshot[n]),"Preserve original node values.");
            if(Mode=="tree_inplace")Check(ReferenceEquals(actual,args[0]),"Return the original root.");
        }
        return Dump(actual,Output);
    }
    static void Main()
    {
        var results=new List<object>();using var document=JsonDocument.Parse(File.ReadAllText("cases.json"));
        foreach(var raw in document.RootElement.EnumerateArray())
        {
            var clock=Stopwatch.StartNew();object? actual=null;string? error=null;bool validationFailed=false;var stdout=Console.Out;
            try{Console.SetOut(TextWriter.Null);actual=Execute(raw);}catch(ContractError){validationFailed=true;}catch(Exception ex){error=ex.GetType().Name+": "+ex.Message;}finally{Console.SetOut(stdout);}
            results.Add(new{actual,error,validationFailed,elapsedMs=clock.Elapsed.TotalMilliseconds});
        }
        File.WriteAllText("results.json",JsonSerializer.Serialize(results,Json));
    }
// CONFIGURATION
}
