"""Independent iterative graph traversal and queue-based indegree elimination."""

def body(ref,language):
    if ref=='4.1':
        if language=='python':return '''if start == target:
    return True
adjacent = [[] for _ in range(nodeCount)]
for source, destination in edges:
    adjacent[source].append(destination)
visited = [False] * nodeCount
visited[start] = True
queue = [start]
head = 0
while head < len(queue):
    node = queue[head]
    head += 1
    for neighbor in adjacent[node]:
        if not visited[neighbor]:
            if neighbor == target:
                return True
            visited[neighbor] = True
            queue.append(neighbor)
return False'''
        if language=='javascript':return 'if(start===target)return true;const adjacent=Array.from({length:nodeCount},()=>[]),visited=new Array(nodeCount).fill(false),queue=[start];for(const [source,destination] of edges)adjacent[source].push(destination);visited[start]=true;for(let head=0;head<queue.length;++head)for(const neighbor of adjacent[queue[head]])if(!visited[neighbor]){if(neighbor===target)return true;visited[neighbor]=true;queue.push(neighbor);}return false;'
        if language=='cpp':return 'if(start==target)return true;std::vector<std::vector<int>> adjacent(nodeCount);for(const auto& edge:edges)adjacent[edge[0]].push_back(edge[1]);std::vector<bool> visited(nodeCount,false);std::vector<int> queue{start};visited[start]=true;for(size_t head=0;head<queue.size();++head)for(int neighbor:adjacent[queue[head]])if(!visited[neighbor]){if(neighbor==target)return true;visited[neighbor]=true;queue.push_back(neighbor);}return false;'
        if language=='csharp':return 'if(start==target)return true;var adjacent=new List<int>[nodeCount];for(int i=0;i<nodeCount;++i)adjacent[i]=new List<int>();foreach(var edge in edges)adjacent[edge[0]].Add(edge[1]);bool[] visited=new bool[nodeCount];var queue=new List<int>{start};visited[start]=true;for(int head=0;head<queue.Count;++head)foreach(int neighbor in adjacent[queue[head]])if(!visited[neighbor]){if(neighbor==target)return true;visited[neighbor]=true;queue.Add(neighbor);}return false;'
        return 'if(start==target)return true;List<List<Integer>> adjacent=new ArrayList<>();for(int i=0;i<nodeCount;++i)adjacent.add(new ArrayList<>());for(int[] edge:edges)adjacent.get(edge[0]).add(edge[1]);boolean[] visited=new boolean[nodeCount];List<Integer> queue=new ArrayList<>();queue.add(start);visited[start]=true;for(int head=0;head<queue.size();++head)for(int neighbor:adjacent.get(queue.get(head)))if(!visited[neighbor]){if(neighbor==target)return true;visited[neighbor]=true;queue.add(neighbor);}return false;'
    if ref!='4.7':raise ValueError(ref)
    if language=='python':return """adjacent = [[] for _ in range(projectCount)]
indegree = [0] * projectCount
for before, after in dependencies:
    adjacent[before].append(after)
    indegree[after] += 1
order = [i for i in range(projectCount) if indegree[i] == 0]
head = 0
while head < len(order):
    project = order[head]
    head += 1
    for dependent in adjacent[project]:
        indegree[dependent] -= 1
        if indegree[dependent] == 0:
            order.append(dependent)
return order if len(order) == projectCount else []"""
    if language=='javascript':return 'const adjacent=Array.from({length:projectCount},()=>[]),indegree=new Array(projectCount).fill(0),order=[];for(const [before,after] of dependencies){adjacent[before].push(after);++indegree[after];}for(let i=0;i<projectCount;++i)if(indegree[i]===0)order.push(i);for(let head=0;head<order.length;++head)for(const dependent of adjacent[order[head]]){--indegree[dependent];if(indegree[dependent]===0)order.push(dependent);}return order.length===projectCount?order:[];'
    if language=='cpp':return 'std::vector<std::vector<int>> adjacent(projectCount);std::vector<int> indegree(projectCount,0),order;for(const auto& edge:dependencies){adjacent[edge[0]].push_back(edge[1]);++indegree[edge[1]];}for(int i=0;i<projectCount;++i)if(indegree[i]==0)order.push_back(i);for(size_t head=0;head<order.size();++head)for(int dependent:adjacent[order[head]]){--indegree[dependent];if(indegree[dependent]==0)order.push_back(dependent);}if(order.size()!=static_cast<size_t>(projectCount))return {};return order;'
    if language=='csharp':return 'var adjacent=new List<int>[projectCount];for(int i=0;i<projectCount;++i)adjacent[i]=new List<int>();int[] indegree=new int[projectCount];foreach(var edge in dependencies){adjacent[edge[0]].Add(edge[1]);++indegree[edge[1]];}var order=new List<int>();for(int i=0;i<projectCount;++i)if(indegree[i]==0)order.Add(i);for(int head=0;head<order.Count;++head)foreach(int dependent in adjacent[order[head]]){--indegree[dependent];if(indegree[dependent]==0)order.Add(dependent);}return order.Count==projectCount?order.ToArray():[];'
    return 'List<List<Integer>> adjacent=new ArrayList<>();for(int i=0;i<projectCount;++i)adjacent.add(new ArrayList<>());int[] indegree=new int[projectCount];for(int[] edge:dependencies){adjacent.get(edge[0]).add(edge[1]);++indegree[edge[1]];}List<Integer> order=new ArrayList<>();for(int i=0;i<projectCount;++i)if(indegree[i]==0)order.add(i);for(int head=0;head<order.size();++head)for(int dependent:adjacent.get(order.get(head))){--indegree[dependent];if(indegree[dependent]==0)order.add(dependent);}if(order.size()!=projectCount)return new int[0];int[] result=new int[projectCount];for(int i=0;i<projectCount;++i)result[i]=order.get(i);return result;'

_previous_tree_body=body

def body(ref,language):
    if ref=='4.4':
        if language=='python':return '''if root is None:
    return True
heights = {}
stack = [(root, False)]
while stack:
    node, exiting = stack.pop()
    if not exiting:
        stack.append((node, True))
        if node.Right is not None:
            stack.append((node.Right, False))
        if node.Left is not None:
            stack.append((node.Left, False))
    else:
        left = heights.get(node.Left, 0)
        right = heights.get(node.Right, 0)
        if abs(left - right) > 1:
            return False
        heights[node] = 1 + max(left, right)
return True'''
        if language=='javascript':return 'if(root===null)return true;const heights=new Map(),stack=[[root,false]];while(stack.length){const [node,exiting]=stack.pop();if(!exiting){stack.push([node,true]);if(node.Right!==null)stack.push([node.Right,false]);if(node.Left!==null)stack.push([node.Left,false]);}else{const left=heights.get(node.Left)||0,right=heights.get(node.Right)||0;if(Math.abs(left-right)>1)return false;heights.set(node,1+Math.max(left,right));}}return true;'
        if language=='cpp':return 'if(!root)return true;struct Frame{TreeNode* Node;bool Exit;};std::vector<Frame> stack{{root,false}};std::unordered_map<TreeNode*,int> heights;while(!stack.empty()){auto frame=stack.back();stack.pop_back();TreeNode* node=frame.Node;if(!frame.Exit){stack.push_back({node,true});if(node->Right)stack.push_back({node->Right,false});if(node->Left)stack.push_back({node->Left,false});}else{int left=node->Left?heights.at(node->Left):0,right=node->Right?heights.at(node->Right):0;if(left-right>1||right-left>1)return false;heights[node]=1+std::max(left,right);}}return true;'
        if language=='csharp':return 'if(root==null)return true;var heights=new Dictionary<TreeNode,int>();var stack=new Stack<(TreeNode Node,bool Exit)>();stack.Push((root,false));while(stack.Count>0){var frame=stack.Pop();var node=frame.Node;if(!frame.Exit){stack.Push((node,true));if(node.Right!=null)stack.Push((node.Right,false));if(node.Left!=null)stack.Push((node.Left,false));}else{int left=node.Left==null?0:heights[node.Left],right=node.Right==null?0:heights[node.Right];if(Math.Abs(left-right)>1)return false;heights[node]=1+Math.Max(left,right);}}return true;'
        return 'if(root==null)return true;record Frame(TreeNode node,boolean exit){}Map<TreeNode,Integer> heights=new HashMap<>();Deque<Frame> stack=new ArrayDeque<>();stack.push(new Frame(root,false));while(!stack.isEmpty()){var frame=stack.pop();TreeNode node=frame.node();if(!frame.exit()){stack.push(new Frame(node,true));if(node.Right!=null)stack.push(new Frame(node.Right,false));if(node.Left!=null)stack.push(new Frame(node.Left,false));}else{int left=node.Left==null?0:heights.get(node.Left),right=node.Right==null?0:heights.get(node.Right);if(Math.abs(left-right)>1)return false;heights.put(node,1+Math.max(left,right));}}return true;'
    if ref=='4.5':
        if language=='python':return '''stack = [(root, -2147483649, 2147483647)] if root is not None else []
while stack:
    node, lower, upper = stack.pop()
    if node.Data <= lower or node.Data > upper:
        return False
    if node.Right is not None:
        stack.append((node.Right, node.Data, upper))
    if node.Left is not None:
        stack.append((node.Left, lower, node.Data))
return True'''
        if language=='javascript':return 'const stack=root===null?[]:[[root,-2147483649,2147483647]];while(stack.length){const [node,lower,upper]=stack.pop();if(node.Data<=lower||node.Data>upper)return false;if(node.Right!==null)stack.push([node.Right,node.Data,upper]);if(node.Left!==null)stack.push([node.Left,lower,node.Data]);}return true;'
        if language=='cpp':return 'struct Frame{TreeNode* Node;long long Lower,Upper;};std::vector<Frame> stack;if(root)stack.push_back({root,-2147483649LL,2147483647LL});while(!stack.empty()){auto frame=stack.back();stack.pop_back();auto node=frame.Node;if(node->Data<=frame.Lower||node->Data>frame.Upper)return false;if(node->Right)stack.push_back({node->Right,node->Data,frame.Upper});if(node->Left)stack.push_back({node->Left,frame.Lower,node->Data});}return true;'
        if language=='csharp':return 'var stack=new Stack<(TreeNode Node,long Lower,long Upper)>();if(root!=null)stack.Push((root,-2147483649L,2147483647L));while(stack.Count>0){var frame=stack.Pop();var node=frame.Node;if(node.Data<=frame.Lower||node.Data>frame.Upper)return false;if(node.Right!=null)stack.Push((node.Right,node.Data,frame.Upper));if(node.Left!=null)stack.Push((node.Left,frame.Lower,node.Data));}return true;'
        return 'record Frame(TreeNode node,long lower,long upper){}Deque<Frame> stack=new ArrayDeque<>();if(root!=null)stack.push(new Frame(root,-2147483649L,2147483647L));while(!stack.isEmpty()){var frame=stack.pop();TreeNode node=frame.node();if(node.Data<=frame.lower()||node.Data>frame.upper())return false;if(node.Right!=null)stack.push(new Frame(node.Right,node.Data,frame.upper()));if(node.Left!=null)stack.push(new Frame(node.Left,frame.lower(),node.Data));}return true;'
    if ref=='4.6':
        if language=='python':return '''if node is None:
    return None
if node.Right is not None:
    following = node.Right
    while following.Left is not None:
        following = following.Left
    return following
current, parent = node, node.Parent
while parent is not None and current is parent.Right:
    current, parent = parent, parent.Parent
return parent'''
        if language=='javascript':return 'if(node===null)return null;if(node.Right!==null){let following=node.Right;while(following.Left!==null)following=following.Left;return following;}let current=node,parent=node.Parent;while(parent!==null&&current===parent.Right){current=parent;parent=parent.Parent;}return parent;'
        if language=='cpp':return 'if(!node)return nullptr;if(node->Right){auto following=node->Right;while(following->Left)following=following->Left;return following;}TreeNode* current=node;TreeNode* parent=node->Parent;while(parent&&current==parent->Right){current=parent;parent=parent->Parent;}return parent;'
        return 'if(node==null)return null;if(node.Right!=null){var following=node.Right;while(following.Left!=null)following=following.Left;return following;}TreeNode current=node;TreeNode'+('?' if language=='csharp' else '')+' parent=node.Parent;while(parent!=null&&current==parent.Right){current=parent;parent=parent.Parent;}return parent;'
    if ref=='4.8':
        if language=='python':return '''if first is None or second is None:
    return None
depth_first = depth_second = 0
cursor = first
while cursor is not None:
    depth_first += 1
    cursor = cursor.Parent
cursor = second
while cursor is not None:
    depth_second += 1
    cursor = cursor.Parent
while depth_first > depth_second:
    first = first.Parent
    depth_first -= 1
while depth_second > depth_first:
    second = second.Parent
    depth_second -= 1
while first is not second:
    first = first.Parent
    second = second.Parent
return first'''
        if language=='javascript':return 'if(first===null||second===null)return null;let depthFirst=0,depthSecond=0;for(let cursor=first;cursor!==null;cursor=cursor.Parent)++depthFirst;for(let cursor=second;cursor!==null;cursor=cursor.Parent)++depthSecond;while(depthFirst>depthSecond){first=first.Parent;--depthFirst;}while(depthSecond>depthFirst){second=second.Parent;--depthSecond;}while(first!==second){first=first.Parent;second=second.Parent;}return first;'
        if language=='cpp':return 'if(!first||!second)return nullptr;int depthFirst=0,depthSecond=0;for(auto cursor=first;cursor;cursor=cursor->Parent)++depthFirst;for(auto cursor=second;cursor;cursor=cursor->Parent)++depthSecond;while(depthFirst>depthSecond){first=first->Parent;--depthFirst;}while(depthSecond>depthFirst){second=second->Parent;--depthSecond;}while(first!=second){first=first->Parent;second=second->Parent;}return first;'
        if language=='csharp':return 'if(first==null||second==null)return null;int depthFirst=0,depthSecond=0;for(var cursor=first;cursor!=null;cursor=cursor.Parent)++depthFirst;for(var cursor=second;cursor!=null;cursor=cursor.Parent)++depthSecond;while(depthFirst>depthSecond){first=first!.Parent;--depthFirst;}while(depthSecond>depthFirst){second=second!.Parent;--depthSecond;}while(!ReferenceEquals(first,second)){first=first?.Parent;second=second?.Parent;}return first;'
        return 'if(first==null||second==null)return null;int depthFirst=0,depthSecond=0;for(TreeNode cursor=first;cursor!=null;cursor=cursor.Parent)++depthFirst;for(TreeNode cursor=second;cursor!=null;cursor=cursor.Parent)++depthSecond;while(depthFirst>depthSecond){first=first.Parent;--depthFirst;}while(depthSecond>depthFirst){second=second.Parent;--depthSecond;}while(first!=second){first=first.Parent;second=second.Parent;}return first;'
    if ref=='4.12':
        if language=='python':return '''if root is None:
    return 0
prefix = {0: 1}
stack = [(root, 0, False)]
answer = 0
while stack:
    node, running, exiting = stack.pop()
    if exiting:
        prefix[running] -= 1
        if prefix[running] == 0:
            del prefix[running]
        continue
    running += node.Data
    answer += prefix.get(running - target, 0)
    prefix[running] = prefix.get(running, 0) + 1
    stack.append((node, running, True))
    if node.Right is not None:
        stack.append((node.Right, running, False))
    if node.Left is not None:
        stack.append((node.Left, running, False))
return answer'''
        if language=='javascript':return 'if(root===null)return 0;const prefix=new Map([[0,1]]),stack=[[root,0,false]];let answer=0;while(stack.length){let [node,running,exiting]=stack.pop();if(exiting){const count=prefix.get(running)-1;if(count===0)prefix.delete(running);else prefix.set(running,count);continue;}running+=node.Data;answer+=prefix.get(running-target)||0;prefix.set(running,(prefix.get(running)||0)+1);stack.push([node,running,true]);if(node.Right!==null)stack.push([node.Right,running,false]);if(node.Left!==null)stack.push([node.Left,running,false]);}return answer;'
        if language=='cpp':return 'if(!root)return 0;struct Frame{TreeNode* Node;int Sum;bool Exit;};std::vector<Frame> stack{{root,0,false}};std::unordered_map<int,int> prefix{{0,1}};int answer=0;while(!stack.empty()){auto frame=stack.back();stack.pop_back();if(frame.Exit){if(--prefix[frame.Sum]==0)prefix.erase(frame.Sum);continue;}int running=frame.Sum+frame.Node->Data;auto found=prefix.find(running-target);if(found!=prefix.end())answer+=found->second;++prefix[running];stack.push_back({frame.Node,running,true});if(frame.Node->Right)stack.push_back({frame.Node->Right,running,false});if(frame.Node->Left)stack.push_back({frame.Node->Left,running,false});}return answer;'
        if language=='csharp':return 'if(root==null)return 0;var prefix=new Dictionary<int,int>{{0,1}};var stack=new Stack<(TreeNode Node,int Sum,bool Exit)>();stack.Push((root,0,false));int answer=0;while(stack.Count>0){var frame=stack.Pop();if(frame.Exit){if(--prefix[frame.Sum]==0)prefix.Remove(frame.Sum);continue;}int running=frame.Sum+frame.Node.Data;prefix.TryGetValue(running-target,out int count);answer+=count;prefix.TryGetValue(running,out int previous);prefix[running]=previous+1;stack.Push((frame.Node,running,true));if(frame.Node.Right!=null)stack.Push((frame.Node.Right,running,false));if(frame.Node.Left!=null)stack.Push((frame.Node.Left,running,false));}return answer;'
        return 'if(root==null)return 0;record Frame(TreeNode node,int sum,boolean exit){}Map<Integer,Integer> prefix=new HashMap<>();prefix.put(0,1);Deque<Frame> stack=new ArrayDeque<>();stack.push(new Frame(root,0,false));int answer=0;while(!stack.isEmpty()){var frame=stack.pop();if(frame.exit()){int count=prefix.get(frame.sum())-1;if(count==0)prefix.remove(frame.sum());else prefix.put(frame.sum(),count);continue;}int running=frame.sum()+frame.node().Data;answer+=prefix.getOrDefault(running-target,0);prefix.put(running,prefix.getOrDefault(running,0)+1);stack.push(new Frame(frame.node(),running,true));if(frame.node().Right!=null)stack.push(new Frame(frame.node().Right,running,false));if(frame.node().Left!=null)stack.push(new Frame(frame.node().Left,running,false));}return answer;'
    if ref!='4.10':return _previous_tree_body(ref,language)
    if language=='python':return '''if small is None:
    return True
def encode(root):
    tokens = []
    stack = [root]
    while stack:
        node = stack.pop()
        if node is None:
            tokens.append("#")
        else:
            tokens.append("V" + str(node.Data))
            stack.append(node.Right)
            stack.append(node.Left)
    return tokens
text, pattern = encode(large), encode(small)
prefix = [0] * len(pattern)
for index in range(1, len(pattern)):
    matched = prefix[index - 1]
    while matched and pattern[index] != pattern[matched]:
        matched = prefix[matched - 1]
    if pattern[index] == pattern[matched]:
        matched += 1
    prefix[index] = matched
matched = 0
for token in text:
    while matched and token != pattern[matched]:
        matched = prefix[matched - 1]
    if token == pattern[matched]:
        matched += 1
    if matched == len(pattern):
        return True
return False'''
    if language=='javascript':return 'if(small===null)return true;function encode(root){const tokens=[],stack=[root];while(stack.length){const node=stack.pop();if(node===null)tokens.push("#");else{tokens.push("V"+String(node.Data));stack.push(node.Right,node.Left);}}return tokens;}const text=encode(large),pattern=encode(small),prefix=new Array(pattern.length).fill(0);for(let i=1;i<pattern.length;++i){let matched=prefix[i-1];while(matched>0&&pattern[i]!==pattern[matched])matched=prefix[matched-1];if(pattern[i]===pattern[matched])++matched;prefix[i]=matched;}let matched=0;for(const token of text){while(matched>0&&token!==pattern[matched])matched=prefix[matched-1];if(token===pattern[matched])++matched;if(matched===pattern.length)return true;}return false;'
    if language=='cpp':return 'if(!small)return true;auto encode=[](TreeNode* root){std::vector<std::string> tokens;std::vector<TreeNode*> stack{root};while(!stack.empty()){auto node=stack.back();stack.pop_back();if(!node)tokens.push_back("#");else{tokens.push_back("V"+std::to_string(node->Data));stack.push_back(node->Right);stack.push_back(node->Left);}}return tokens;};auto text=encode(large),pattern=encode(small);std::vector<int> prefix(pattern.size(),0);for(size_t i=1;i<pattern.size();++i){int matched=prefix[i-1];while(matched>0&&pattern[i]!=pattern[matched])matched=prefix[matched-1];if(pattern[i]==pattern[matched])++matched;prefix[i]=matched;}int matched=0;for(const auto& token:text){while(matched>0&&token!=pattern[matched])matched=prefix[matched-1];if(token==pattern[matched])++matched;if(matched==static_cast<int>(pattern.size()))return true;}return false;'
    if language=='csharp':return 'if(small==null)return true;List<string> Encode(TreeNode? root){var tokens=new List<string>();var stack=new Stack<TreeNode?>();stack.Push(root);while(stack.Count>0){var node=stack.Pop();if(node==null)tokens.Add("#");else{tokens.Add("V"+node.Data.ToString(System.Globalization.CultureInfo.InvariantCulture));stack.Push(node.Right);stack.Push(node.Left);}}return tokens;}var text=Encode(large);var pattern=Encode(small);int[] prefix=new int[pattern.Count];for(int i=1;i<pattern.Count;++i){int matched=prefix[i-1];while(matched>0&&pattern[i]!=pattern[matched])matched=prefix[matched-1];if(pattern[i]==pattern[matched])++matched;prefix[i]=matched;}int count=0;foreach(string token in text){while(count>0&&token!=pattern[count])count=prefix[count-1];if(token==pattern[count])++count;if(count==pattern.Count)return true;}return false;'
    return 'if(small==null)return true;class Encoder {List<String> encode(TreeNode root){List<String> tokens=new ArrayList<>();List<TreeNode> stack=new ArrayList<>();stack.add(root);while(!stack.isEmpty()){TreeNode node=stack.remove(stack.size()-1);if(node==null)tokens.add("#");else{tokens.add("V"+Integer.toString(node.Data));stack.add(node.Right);stack.add(node.Left);}}return tokens;}}Encoder encoder=new Encoder();List<String> text=encoder.encode(large),pattern=encoder.encode(small);int[] prefix=new int[pattern.size()];for(int i=1;i<pattern.size();++i){int matched=prefix[i-1];while(matched>0&&!pattern.get(i).equals(pattern.get(matched)))matched=prefix[matched-1];if(pattern.get(i).equals(pattern.get(matched)))++matched;prefix[i]=matched;}int matched=0;for(String token:text){while(matched>0&&!token.equals(pattern.get(matched)))matched=prefix[matched-1];if(token.equals(pattern.get(matched)))++matched;if(matched==pattern.size())return true;}return false;'
