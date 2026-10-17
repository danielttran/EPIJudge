using EpiJudge.TestFramework;

// Intentionally simple reference implementations for exercising the adapters.
// These are audit fixtures, not the practice editor's starter solutions.
public class AlgorithmFixture
{
    public int FindMissingElement(List<int> stream) { var set=stream.ToHashSet(); int i=0; while(set.Contains(i)) i++; return i; }
    public void Rearrange(List<int> values) { values.Sort(); for(int i=1;i+1<values.Count;i+=2) (values[i],values[i+1])=(values[i+1],values[i]); }
    public void EvenOdd(List<int> values) => values.Sort((x,y)=>(x&1).CompareTo(y&1));
    public void DutchFlagPartition(int pivot,List<int> values) { int p=values[pivot]; values.Sort((x,y)=>x.CompareTo(p).CompareTo(y.CompareTo(p))); }
    public void GroupByAge(List<(int Age,string Name)> people) => people.Sort((x,y)=>x.Age.CompareTo(y.Age));
    public List<int> GrayCode(int bits) => Enumerable.Range(0,1<<bits).Select(x=>x^(x>>1)).ToList();
    public List<List<int>> ComputeTowerHanoi(int rings)
    {
        var moves=new List<List<int>>();
        void Move(int n,int from,int to,int spare) { if(n==0)return; Move(n-1,from,spare,to); moves.Add([from,to]); Move(n-1,spare,to,from); }
        Move(rings,0,1,2); return moves;
    }
    public bool ValidPlacementExists(List<int> first,List<int> second) => first.Order().Zip(second.Order()).All(x=>x.First<x.Second);
    public List<string> DecomposeIntoDictionaryWords(string domain,HashSet<string> dictionary)
    {
        var previous=Enumerable.Repeat(-1,domain.Length+1).ToArray(); previous[0]=0;
        for(int i=1;i<=domain.Length;i++) for(int j=0;j<i;j++) if(previous[j]>=0 && dictionary.Contains(domain[j..i])) { previous[i]=j;break; }
        if(previous[^1]<0) return [];
        var result=new List<string>(); for(int i=domain.Length;i>0;i=previous[i]) result.Add(domain[previous[i]..i]); result.Reverse(); return result;
    }
    public int SearchEntryEqualToItsIndex(List<int> values) { for(int i=0;i<values.Count;i++) if(values[i]==i)return i; return -1; }
    public int FindAmpleCity(List<int> gallons,List<int> distances)
    {
        long tank=0; int start=0;
        for(int i=0;i<gallons.Count;i++) { tank+=20L*gallons[i]-distances[i]; if(tank<0) { start=i+1;tank=0; } }
        return start%gallons.Count;
    }
    public string Encoding(string text)
    {
        var output=new System.Text.StringBuilder();
        for(int i=0;i<text.Length;) { int j=i+1; while(j<text.Length && text[j]==text[i])j++; output.Append(j-i).Append(text[i]);i=j; } return output.ToString();
    }
    public string Decoding(string text)
    {
        var output=new System.Text.StringBuilder(); int count=0;
        foreach(char c in text) if(char.IsDigit(c)) count=count*10+c-'0'; else { output.Append(c,count);count=0; } return output.ToString();
    }
    public string IntToString(int value) => value.ToString(System.Globalization.CultureInfo.InvariantCulture);
    public int StringToInt(string text) => int.Parse(text,System.Globalization.CultureInfo.InvariantCulture);
    public virtual ListNode<int>? ListPivoting(ListNode<int>? head,int pivot)
    {
        var nodes=EpiJudge.Runner.JudgeAdapters.Nodes(head).OrderBy(n=>n.Data.CompareTo(pivot)).ToList();
        for(int i=0;i<nodes.Count;i++) nodes[i].Next=i+1<nodes.Count?nodes[i+1]:null; return nodes.FirstOrDefault();
    }
    public ListNode<int>? HasCycle(ListNode<int>? head)
    {
        var seen=new HashSet<ListNode<int>>(); while(head is not null) { if(!seen.Add(head))return head; head=head.Next; } return null;
    }
    public ListNode<int>? OverlappingLists(ListNode<int>? first,ListNode<int>? second)
    {
        var seen=EpiJudge.Runner.JudgeAdapters.Nodes(first).ToHashSet(); return EpiJudge.Runner.JudgeAdapters.Nodes(second).FirstOrDefault(seen.Contains);
    }
    public virtual PostingListNode? CopyPostingsList(PostingListNode? head)
    {
        var map=new Dictionary<PostingListNode,PostingListNode>();
        PostingListNode? Copy(PostingListNode? n) { if(n is null)return null; if(map.TryGetValue(n,out var found))return found; var node=new PostingListNode(n.Order);map[n]=node; node.Next=Copy(n.Next);node.Jump=Copy(n.Jump);return node; }
        return Copy(head);
    }
    public virtual GraphVertex CloneGraph(GraphVertex graph)
    {
        var map=new Dictionary<GraphVertex,GraphVertex>(); var queue=new Queue<GraphVertex>(); map[graph]=new(graph.Label);queue.Enqueue(graph);
        while(queue.TryDequeue(out var n)) foreach(var e in n.Edges) { if(!map.ContainsKey(e)) { map[e]=new(e.Label);queue.Enqueue(e); } map[n].Edges.Add(map[e]); } return map[graph];
    }
    public BinaryTreeNode<int>? BuildBstFromSortedDoublyList(BinaryTreeNode<int>? head,int count)
    {
        var nodes=new List<BinaryTreeNode<int>>(); for(var n=head;n is not null;n=n.Right)nodes.Add(n);
        BinaryTreeNode<int>? Build(int l,int r) { if(l>=r)return null; int mid=l+(r-l)/2;var n=nodes[mid];n.Left=Build(l,mid);n.Right=Build(mid+1,r);return n; } return Build(0,count);
    }
    public virtual void SolveSudoku(List<List<int>> board)
    {
        int n=board.Count,w=(int)Math.Sqrt(n);
        bool Fill()
        {
            int row=-1,col=-1; List<int>? choices=null;
            for(int r=0;r<n;r++) for(int c=0;c<n;c++) if(board[r][c]==0)
            {
                var possible=Enumerable.Range(1,n).Where(v=>!board[r].Contains(v) && !board.Any(line=>line[c]==v)
                    && !Enumerable.Range(0,n).Any(i=>board[r/w*w+i/w][c/w*w+i%w]==v)).ToList();
                if(possible.Count==0)return false;
                if(choices is null || possible.Count<choices.Count) { row=r;col=c;choices=possible; }
            }
            if(choices is null)return true;
            foreach(int v in choices) { board[row][col]=v;if(Fill())return true; } board[row][col]=0;return false;
        }
        if(!Fill())throw new Exception("Unsolvable audit puzzle.");
    }
    public int NonuniformRandomNumberGeneration(List<int> values,List<double> probabilities)
    {
        double r=Random.Shared.NextDouble(); for(int i=0;i<values.Count-1;i++) { r-=probabilities[i];if(r<0)return values[i]; } return values[^1];
    }
    public int UniformRandom(int lower,int upper) => (int)Random.Shared.NextInt64(lower,(long)upper+1);
    public List<int> ComputeRandomPermutation(int n) { var result=Enumerable.Range(0,n).ToList();RandomSampling(n,result);return result; }
    public List<int> RandomSubset(int n,int k) => ComputeRandomPermutation(n).Take(k).ToList();
    public void RandomSampling(int k,List<int> values) { for(int i=0;i<k;i++) { int j=Random.Shared.Next(i,values.Count);(values[i],values[j])=(values[j],values[i]); } }
    public List<int> OnlineRandomSample(List<int> stream,int k) { RandomSampling(k,stream);return stream.Take(k).ToList(); }
    public BinaryTreeNode<int>? BuildMinHeightBstFromSortedArray(List<int> values)
    {
        BinaryTreeNode<int>? Build(int l,int r) { if(l>=r)return null;int m=l+(r-l)/2;return new(values[m]) {Left=Build(l,m),Right=Build(m+1,r)}; } return Build(0,values.Count);
    }
    public BinaryTreeNode<int>? BstToDoublyLinkedList(BinaryTreeNode<int>? tree)
    {
        var nodes=new List<BinaryTreeNode<int>>();
        void Visit(BinaryTreeNode<int>? n) { if(n is null)return;Visit(n.Left);nodes.Add(n);Visit(n.Right); } Visit(tree);
        for(int i=0;i<nodes.Count;i++) { nodes[i].Left=i>0?nodes[i-1]:null;nodes[i].Right=i+1<nodes.Count?nodes[i+1]:null; } return nodes.FirstOrDefault();
    }
    public void ConstructRightSibling(BinaryTreeNode<int>? root)
    {
        var q=new Queue<BinaryTreeNode<int>>();if(root is not null)q.Enqueue(root);
        while(q.Count>0) { int size=q.Count;BinaryTreeNode<int>? prev=null;while(size-->0) { var n=q.Dequeue();if(prev is not null)prev.Next=n;prev=n;if(n.Left is not null)q.Enqueue(n.Left);if(n.Right is not null)q.Enqueue(n.Right); }prev!.Next=null; }
    }
    public virtual List<(int,int)> SearchMaze(List<List<int>> maze,(int,int) start,(int,int) end)
    {
        var previous=new Dictionary<(int,int),(int,int)> {[start]=start};var q=new Queue<(int,int)>();q.Enqueue(start);
        while(q.TryDequeue(out var current))
        {
            if(current==end) { var path=new List<(int,int)>(); for(var p=end;;p=previous[p]) { path.Add(p);if(p==start)break; }path.Reverse();return path; }
            foreach(var (dr,dc) in new[] {(0,1),(0,-1),(1,0),(-1,0)}) { var next=(current.Item1+dr,current.Item2+dc);if(next.Item1>=0 && next.Item1<maze.Count && next.Item2>=0 && next.Item2<maze[next.Item1].Count && maze[next.Item1][next.Item2]==0 && previous.TryAdd(next,current))q.Enqueue(next); }
        }
        return [];
    }
    public (int,int) FindSmallestSubarrayCoveringSet(List<string> paragraph,HashSet<string> keywords)
    {
        var counts=new Dictionary<string,int>();int covered=0,start=0;var best=(-1,int.MaxValue/2);
        for(int end=0;end<paragraph.Count;end++)
        {
            string word=paragraph[end];if(keywords.Contains(word)) { if(counts.GetValueOrDefault(word)==0)covered++;counts[word]=counts.GetValueOrDefault(word)+1; }
            while(covered==keywords.Count && start<=end) { if(end-start<best.Item2-best.Item1)best=(start,end);word=paragraph[start++];if(keywords.Contains(word) && --counts[word]==0)covered--; }
        }
        return best;
    }
    public (int,int) FindSmallestSequentiallyCoveringSubset(List<string> paragraph,List<string> keywords)
    {
        var starts=Enumerable.Repeat(-1,keywords.Count).ToArray();var best=(-1,int.MaxValue/2);
        for(int i=0;i<paragraph.Count;i++) for(int k=keywords.Count-1;k>=0;k--) if(paragraph[i]==keywords[k])
        {
            if(k==0)starts[0]=i;else if(starts[k-1]>=0)starts[k]=starts[k-1];
            if(k==keywords.Count-1 && starts[k]>=0 && i-starts[k]<best.Item2-best.Item1)best=(starts[k],i);
        }
        return best;
    }
}

public class CreditsFixture
{
    private readonly Dictionary<string,int> values=[];
    public void Initialize()=>values.Clear();
    public void Insert(string id,int credit)=>values[id]=credit;
    public bool Remove(string id)=>values.Remove(id);
    public int Lookup(string id)=>values.GetValueOrDefault(id,-1);
    public void AddAll(int amount) { foreach(var id in values.Keys.ToArray())values[id]+=amount; }
    public string Max()=>values.Count==0?"":values.MaxBy(x=>x.Value).Key;
}
public class QueueFixture
{
    private readonly Queue<int> values=[];
    public void Initialize()=>values.Clear();
    public void Initialize(int capacity)=>values.Clear();
    public void Enqueue(int value)=>values.Enqueue(value);
    public int Dequeue()=>values.Dequeue();
    public int Size()=>values.Count;
    public int Max()=>values.Max();
}
public class StackFixture
{
    private readonly Stack<int> values=[];
    public void Initialize()=>values.Clear();
    public void Push(int value)=>values.Push(value);
    public int Pop()=>values.Pop();
    public bool Empty()=>values.Count==0;
    public int Max()=>values.Max();
}
public class LruFixture
{
    private readonly LinkedList<(int Key,int Price)> entries=[];
    private int capacity;
    public void Initialize(int size) { entries.Clear();capacity=size; }
    private LinkedListNode<(int Key,int Price)>? Find(int key) { for(var n=entries.First;n is not null;n=n.Next)if(n.Value.Key==key)return n;return null; }
    public int Lookup(int key) { var n=Find(key);if(n is null)return -1;int price=n.Value.Price;entries.Remove(n);entries.AddLast(n);return price; }
    public void Insert(int key,int price) { var n=Find(key);if(n is not null) { entries.Remove(n);entries.AddLast(n);return; }if(entries.Count==capacity)entries.RemoveFirst();entries.AddLast((key,price)); }
    public bool Erase(int key) { var n=Find(key);if(n is null)return false;entries.Remove(n);return true; }
}
public sealed class BrokenFixture : AlgorithmFixture
{
    public override ListNode<int>? ListPivoting(ListNode<int>? head,int pivot) { for(var node=head;node is not null;node=node.Next)node.Data=0;return head; }
    public override PostingListNode? CopyPostingsList(PostingListNode? head)=>head;
    public override GraphVertex CloneGraph(GraphVertex graph)=>graph;
    public override void SolveSudoku(List<List<int>> board) { }
    public new void Rearrange(List<int> values) { }
    public override List<(int,int)> SearchMaze(List<List<int>> maze,(int,int) start,(int,int) end)=>[start,end];
    public new int NonuniformRandomNumberGeneration(List<int> values,List<double> probabilities)=>values[0];
    public new int UniformRandom(int lower,int upper)=>lower;
    public new List<int> ComputeRandomPermutation(int n)=>Enumerable.Range(0,n).ToList();
    public new List<int> RandomSubset(int n,int k)=>Enumerable.Range(0,k).ToList();
    public new void RandomSampling(int k,List<int> values) { }
    public new List<int> OnlineRandomSample(List<int> values,int k)=>values.Take(k).ToList();
}

public sealed class MutatingPostingFixture : AlgorithmFixture
{
    public override PostingListNode? CopyPostingsList(PostingListNode? head)
    {
        for(var node=head;node is not null;node=node.Next)node.Order+=100;
        return base.CopyPostingsList(head);
    }
}
