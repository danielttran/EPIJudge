using System.Diagnostics;
using System.Reflection;
using System.Text.Json;
using EpiJudge.Runner;

namespace EpiJudge.Tests;

public sealed class JavascriptHarnessTests
{
    private static Problem Problem(string id) => new ProblemCatalog().Find(id)!;

    private static async Task<JsonElement[]> Run(Problem problem, string code, string input)
    {
        var directory = Path.Combine(Path.GetTempPath(), "epi-js-harness-" + Guid.NewGuid().ToString("N"));
        Directory.CreateDirectory(directory);
        try
        {
            var create = typeof(SubmissionRunner).GetMethod("CreateJsHarness", BindingFlags.NonPublic | BindingFlags.Static)!;
            await File.WriteAllTextAsync(Path.Combine(directory, "harness.js"), (string)create.Invoke(null, [problem])!);
            await File.WriteAllTextAsync(Path.Combine(directory, "solution.js"), code);
            using var process = new Process
            {
                StartInfo = new ProcessStartInfo(NodeLocator.FindNode())
                {
                    WorkingDirectory = directory,
                    RedirectStandardInput = true,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    UseShellExecute = false,
                    CreateNoWindow = true
                }
            };
            process.StartInfo.ArgumentList.Add("harness.js");
            process.Start();
            var output = process.StandardOutput.ReadToEndAsync();
            var error = process.StandardError.ReadToEndAsync();
            using var timeout = new CancellationTokenSource(TimeSpan.FromSeconds(25));
            await process.StandardInput.WriteAsync(input.AsMemory(), timeout.Token);
            process.StandardInput.Close();
            try { await process.WaitForExitAsync(timeout.Token); }
            catch (OperationCanceledException) { process.Kill(entireProcessTree: true); throw; }
            Assert.True(process.ExitCode == 0, await error);
            return JsonSerializer.Deserialize<JsonElement[]>(await output)!;
        }
        finally { Directory.Delete(directory, recursive: true); }
    }

    private static void Valid(JsonElement row)
    {
        Assert.Equal(JsonValueKind.Null, row.GetProperty("error").ValueKind);
        Assert.False(row.GetProperty("validationFailed").GetBoolean(), row.GetProperty("validationMessage").ToString());
    }

    private static void Invalid(JsonElement row)
    {
        Assert.Equal(JsonValueKind.Null, row.GetProperty("error").ValueKind);
        Assert.True(row.GetProperty("validationFailed").GetBoolean());
    }

    [Fact]
    public async Task Signed64BitInputsAndOutputsRemainExactWhileSafeInputsKeepNumberCompatibility()
    {
        var problem = Problem("swap_bits") with { JsInvocation = "identity", ArgumentTypes = ["long"] };
        var rows = await Run(problem, "exports.identity=x=>{if((x===7)!==(typeof x==='number'))throw Error('wrong type');return x;};",
            "[[7],[9007199254740993],[9223372036854775807],[-9223372036854775808]]");
        Assert.Equal(new[] { "7", "9007199254740993", "9223372036854775807", "-9223372036854775808" },
            rows.Select(row => row.GetProperty("actual").GetRawText()));
        Assert.All(rows, Valid);
    }

    [Fact]
    public async Task NestedGrammarDistinguishesLongFromFloatBeforeCallingTheSolution()
    {
        var problem = Problem("count_bits") with
        {
            JsInvocation = "identity", ArgumentTypes = ["array(tuple(long, float))"], ResultType = "array(tuple(long, float))"
        };
        var rows = await Run(problem,
            "exports.identity=x=>{if(typeof x[0][0]!=='bigint'||typeof x[0][1]!=='number')throw Error('wrong type');return x;};",
            "[[[[9007199254740993,1000000000000000000000000]]]]");
        Valid(rows[0]);
        Assert.Equal("9007199254740993", rows[0].GetProperty("actual")[0][0].GetRawText());
        Assert.Equal(1e24, rows[0].GetProperty("actual")[0][1].GetDouble());
    }

    [Fact]
    public async Task NodeTypesExistDuringModuleLoadingAndPlainNewTreesSerializeByContract()
    {
        var rows = await Run(Problem("bst_from_preorder"),
            "const node=new BinaryTreeNode(1); const list=new ListNode(2); const posting=new PostingListNode(3); const graph=new GraphVertex(4); exports.rebuildBstFromPreorder=()=>({data:2,left:{data:1},right:{data:3}});",
            "[[[2,1,3]]]");
        Valid(rows[0]); Assert.Equal("[2,1,3]", rows[0].GetProperty("actual").GetRawText());
    }

    [Fact]
    public async Task TreeInputsHaveParentLinksAndInitializedSubtreeSizes()
    {
        var rows = await Run(Problem("kth_node_in_tree"),
            "exports.findKthNodeBinaryTree=(tree,k)=>{if(tree.size!==4||tree.left.size!==2||tree.left.parent!==tree||tree.left.right.parent!==tree.left)throw Error('broken input');return tree.data;};",
            "[[[8,3,11,null,5],3]]");
        Valid(rows[0]); Assert.Equal(8, rows[0].GetProperty("actual").GetInt32());
    }

    [Theory]
    [InlineData("alternating_array", "exports.rearrange=a=>a.fill(0);", "[[[3,1,2]]]")]
    [InlineData("even_odd_array", "exports.evenOdd=a=>a.fill(0);", "[[[3,1,2]]]")]
    [InlineData("dutch_national_flag", "exports.dutchFlagPartition=(p,a)=>a.fill(0);", "[[[3,1,2],1]]")]
    public async Task InPlaceOrderingCannotDiscardTheOriginalElements(string id, string source, string input)
        => Invalid((await Run(Problem(id), source, input))[0]);

    [Fact]
    public async Task DutchFlagReceivesPivotBeforeTheArrayAndValidatesAllPartitions()
    {
        var rows = await Run(Problem("dutch_national_flag"),
            "exports.dutchFlagPartition=(pivot,a)=>{if(pivot!==1)throw Error('argument order');a.sort((x,y)=>x-y);};",
            "[[[3,1,2],1]]");
        Valid(rows[0]); Assert.True(rows[0].GetProperty("actual").GetBoolean());
    }

    [Fact]
    public async Task GrayCodeRequiresOneBitTransitionsAndValidMembers()
    {
        var valid = await Run(Problem("gray_code"), "exports.grayCode=()=>[0,1,3,2];", "[[2]]");
        Valid(valid[0]);
        Invalid((await Run(Problem("gray_code"), "exports.grayCode=()=>[0,3,1,2];", "[[2]]"))[0]);
        Invalid((await Run(Problem("gray_code"), "exports.grayCode=()=>[0,1,3,6];", "[[2]]"))[0]);
    }

    [Fact]
    public async Task CyclicAndSharedChildTreesAreRejectedWithoutHanging()
    {
        Invalid((await Run(Problem("bst_from_preorder"), "exports.rebuildBstFromPreorder=()=>{const root={data:1};root.left=root;return root;};", "[[[1]]]"))[0]);
        Invalid((await Run(Problem("bst_from_preorder"), "exports.rebuildBstFromPreorder=()=>{const node={data:1};return {data:2,left:node,right:node};};", "[[[2,1,1]]]"))[0]);
        Invalid((await Run(Problem("reverse_list"), "exports.reverseList=head=>{head.next=head;return head;};", "[[[1]]]"))[0]);
    }

    [Fact]
    public async Task CycleEntryRequiresIdentityAndPreservesTheOriginalCycle()
    {
        const string good = "exports.hasCycle=head=>{const seen=new Set();while(head){if(seen.has(head))return head;seen.add(head);head=head.next;}return null;};";
        Assert.All(await Run(Problem("is_list_cyclic"), good, "[[[1,2,3],2],[[4,5],-1]]"), Valid);
        Invalid((await Run(Problem("is_list_cyclic"), "exports.hasCycle=()=>new ListNode(2);", "[[[1,2,3],2]]"))[0]);
        Invalid((await Run(Problem("is_list_cyclic"), "exports.hasCycle=head=>{const entry=head.next;head.next=null;return entry;};", "[[[1,2,3],2]]"))[0]);
    }

    [Theory]
    [InlineData("do_terminated_lists_overlap", "[[[1],[2],[3,4]]]")]
    [InlineData("do_lists_overlap", "[[[1],[2],[3,4],2,-1]]")]
    public async Task OverlapRequiresAnActuallySharedNode(string id, string input)
    {
        const string good = "exports.overlappingLists=(a,b)=>{const seen=new Set();while(a&&!seen.has(a)){seen.add(a);a=a.next;}const visited=new Set();while(b&&!visited.has(b)){if(seen.has(b))return b;visited.add(b);b=b.next;}return null;};";
        Valid((await Run(Problem(id), good, input))[0]);
        Invalid((await Run(Problem(id), "exports.overlappingLists=()=>new ListNode(3);", input))[0]);
    }

    [Fact]
    public async Task PostingCopiesMustBeDisjointAndPreserveTheOriginalValuesAndLinks()
    {
        const string good = "exports.copyPostingsList=head=>{const nodes=[],map=new Map();for(let p=head;p;p=p.next){nodes.push(p);map.set(p,new PostingListNode(p.order));}for(const p of nodes){map.get(p).next=map.get(p.next)||null;map.get(p).jump=map.get(p.jump)||null;}return map.get(head)||null;};";
        Valid((await Run(Problem("copy_posting_list"), good, "[[[[1,2],[2,1]]]]"))[0]);
        Invalid((await Run(Problem("copy_posting_list"), "exports.copyPostingsList=head=>head;", "[[[[1,-1]]]]"))[0]);
        const string corrupt = "exports.copyPostingsList=head=>{const copy=new PostingListNode(head.order);head.order=99;return copy;};";
        Invalid((await Run(Problem("copy_posting_list"), corrupt, "[[[[1,-1]]]]"))[0]);
    }

    [Fact]
    public async Task GraphCopiesMustBeDisjointPreserveDuplicateEdgesAndNotModifyTheOriginal()
    {
        const string good = "exports.cloneGraph=root=>{const map=new Map([[root,new GraphVertex(root.label)]]),q=[root];for(let i=0;i<q.length;i++){const node=q[i];for(const edge of node.edges){if(!map.has(edge)){map.set(edge,new GraphVertex(edge.label));q.push(edge);}map.get(node).edges.push(map.get(edge));}}return map.get(root);};";
        Valid((await Run(Problem("graph_clone"), good, "[[2,[[0,1],[0,1],[1,0]]]]"))[0]);
        Invalid((await Run(Problem("graph_clone"), "exports.cloneGraph=root=>root;", "[[1,[[0,0]]]]"))[0]);
        Invalid((await Run(Problem("graph_clone"), "exports.cloneGraph=root=>{const copy=new GraphVertex(0);root.label=9;return copy;};", "[[1,[]]]"))[0]);
    }

    [Fact]
    public async Task StableListSortMustKeepOriginalNodesAndRelativeOrderOfTies()
    {
        const string good = "exports.stableSortList=head=>{const nodes=[];for(let p=head;p;p=p.next)nodes.push(p);nodes.sort((a,b)=>a.data-b.data);for(let i=0;i<nodes.length;i++)nodes[i].next=nodes[i+1]||null;return nodes[0]||null;};";
        Valid((await Run(Problem("sort_list"), good, "[[[2,1,2]]]"))[0]);
        Invalid((await Run(Problem("sort_list"), "exports.stableSortList=head=>new ListNode(1,new ListNode(2,new ListNode(2)));", "[[[2,1,2]]]"))[0]);
        const string reverseTies = "exports.stableSortList=head=>{const a=head,b=head.next,c=b.next;b.next=c;c.next=a;a.next=null;return b;};";
        Invalid((await Run(Problem("sort_list"), reverseTies, "[[[2,1,2]]]"))[0]);
    }

    [Fact]
    public async Task ContainerConstructorMarkersResetStateInsideOneCase()
    {
        const string good = "exports.StackWithMax=class{constructor(){this.a=[];}push(x){this.a.push(x);}pop(){return this.a.pop();}max(){return Math.max(...this.a);}empty(){return this.a.length===0;}};";
        const string operations = "[[[[\"Stack\",0],[\"push\",-3],[\"push\",-3],[\"pop\",-3],[\"max\",-3],[\"Stack\",0],[\"empty\",1]]]]";
        Valid((await Run(Problem("stack_with_max"), good, operations))[0]);
        const string bad = "const a=[];exports.StackWithMax=class{push(x){a.push(x);}pop(){return a.pop();}max(){return Math.max(...a);}empty(){return a.length===0;}};";
        Invalid((await Run(Problem("stack_with_max"), bad, operations))[0]);
    }

    [Fact]
    public async Task RightSiblingLinksCannotReplaceOriginalChildren()
    {
        const string good = "exports.constructRightSibling=root=>{if(!root)return;let level=[root];while(level.length){const next=[];for(let i=0;i<level.length;i++){level[i].next=level[i+1]||null;if(level[i].left)next.push(level[i].left);if(level[i].right)next.push(level[i].right);}level=next;}};";
        Valid((await Run(Problem("tree_right_sibling"), good, "[[[1,2,3]]]"))[0]);
        Invalid((await Run(Problem("tree_right_sibling"), "exports.constructRightSibling=root=>{root.left=null;root.right=null;};", "[[[1,2,3]]]"))[0]);
    }

    [Fact]
    public async Task HanoiValidatesMovesAndSudokuPreservesClues()
    {
        const string hanoi = "exports.computeTowerHanoi=n=>{const out=[];function move(k,a,b,c){if(!k)return;move(k-1,a,c,b);out.push([a,b]);move(k-1,c,b,a);}move(n,0,1,2);return out;};";
        Valid((await Run(Problem("hanoi"), hanoi, "[[3]]"))[0]);
        Invalid((await Run(Problem("hanoi"), "exports.computeTowerHanoi=()=>[[0,1],[0,1]];", "[[2]]"))[0]);
        Invalid((await Run(Problem("sudoku_solve"), "exports.solveSudoku=b=>{b[0][0]=2;};", "[[[[1,2,3,4],[3,4,1,2],[2,1,4,3],[4,3,2,1]]]]"))[0]);
    }

    [Fact]
    public async Task RandomValidationRejectsConstantAndAlternatingOutputs()
    {
        Invalid((await Run(Problem("uniform_random_number"), "exports.uniformRandom=()=>0;", "[[0,1]]"))[0]);
        Invalid((await Run(Problem("uniform_random_number"), "let i=0;exports.uniformRandom=()=>i++%2;", "[[0,1]]"))[0]);
    }

    [Fact]
    public async Task RandomValidationRejectsInvalidSamplesBeforeStatisticalChecks()
    {
        Invalid((await Run(Problem("random_subset"), "exports.randomSubset=()=>[0,0];", "[[4,2]]"))[0]);
        Invalid((await Run(Problem("offline_sampling"), "exports.randomSampling=(k,a)=>{a[0]=a[1];};", "[[1,[1,2,3]]]"))[0]);
    }

    [Theory]
    [InlineData("uniform_random_number", "[[0,3]]")]
    [InlineData("nonuniform_random_number", "[[[10,20],[0.25,0.75]]]")]
    [InlineData("random_permutation", "[[4]]")]
    [InlineData("random_subset", "[[4,2]]")]
    [InlineData("offline_sampling", "[[2,[10,20,30,40]]]")]
    [InlineData("online_sampling", "[[[10,20,30,40],2]]")]
    public async Task ActualRandomAlgorithmsPassTheDistributionAndIndependenceContracts(string id, string input)
    {
        const string source = """
            function shuffle(a){for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;}
            exports.uniformRandom=(a,b)=>a+Math.floor(Math.random()*(b-a+1));
            exports.nonuniformRandomNumberGeneration=(values,p)=>Math.random()<p[0]?values[0]:values[1];
            exports.computeRandomPermutation=n=>shuffle(Array.from({length:n},(_,i)=>i));
            exports.randomSubset=(n,k)=>exports.computeRandomPermutation(n).slice(0,k);
            exports.randomSampling=(k,a)=>{shuffle(a);};
            exports.onlineRandomSample=(a,k)=>{const result=a.slice(0,k);for(let i=k;i<a.length;i++){const j=Math.floor(Math.random()*(i+1));if(j<k)result[j]=a[i];}return result;};
            """;
        Valid((await Run(Problem(id), source, input))[0]);
    }

    [Fact]
    public async Task PrintsCannotCorruptTheProtocolAndRuntimeFailuresDoNotMasqueradeAsWrongAnswers()
    {
        const string prints = "console.log('module output');process.stdout.write('more output');exports.countBits=()=>{console.log('call output');return 1;};";
        var valid = (await Run(Problem("count_bits"), prints, "[[1]]"))[0]; Valid(valid); Assert.Equal(1, valid.GetProperty("actual").GetInt32());
        var failed = (await Run(Problem("count_bits"), "exports.countBits=()=>{throw Error('failure');};", "[[1]]"))[0];
        Assert.False(failed.GetProperty("validationFailed").GetBoolean()); Assert.Contains("failure", failed.GetProperty("error").GetString());
    }

    [Theory]
    [InlineData("+0")]
    [InlineData(" 0 ")]
    [InlineData("00")]
    public async Task DecimalFormattingRetainsTheOriginalCanonicalContract(string formatted)
    {
        var source = "exports.intToString=()=>" + JsonSerializer.Serialize(formatted) + ";exports.stringToInt=()=>0;";
        Invalid((await Run(Problem("string_integer_interconversion"), source, "[[0,\"+0\"]]"))[0]);
    }
}
