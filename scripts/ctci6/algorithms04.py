"""Independent iterative graph traversal and lexical indegree elimination."""

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
