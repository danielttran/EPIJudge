"""Independent iterative BST updates and one-rank selection, with private caches."""

def body(language):
    if language=='python':return '''class RandomBst:
    class _SizedNode(RandomNode):
        def __init__(self,value: int):
            super().__init__(value)
            self.Size = 1

    def __init__(self):
        self.Root: RandomNode | None = None

    def Insert(self,value: int) -> None:
        added = RandomBst._SizedNode(value)
        if self.Root is None:
            self.Root = added
            return
        path = []
        node = self.Root
        while True:
            path.append(node)
            if value <= node.Data:
                if node.Left is None:
                    node.Left = added
                    break
                node = node.Left
            else:
                if node.Right is None:
                    node.Right = added
                    break
                node = node.Right
        for ancestor in path:
            ancestor.Size += 1

    def Find(self,value: int) -> RandomNode | None:
        node = self.Root
        while node is not None:
            if value == node.Data:
                return node
            node = node.Left if value < node.Data else node.Right
        return None

    def Delete(self,value: int) -> bool:
        path = []
        node = self.Root
        while node is not None and node.Data != value:
            path.append(node)
            node = node.Left if value < node.Data else node.Right
        if node is None:
            return False
        if node.Left is not None and node.Right is not None:
            path.append(node)
            successor = node.Right
            while successor.Left is not None:
                path.append(successor)
                successor = successor.Left
            node.Data = successor.Data
            node = successor
        replacement = node.Left if node.Left is not None else node.Right
        if not path:
            self.Root = replacement
        else:
            parent = path[-1]
            if parent.Left is node:
                parent.Left = replacement
            else:
                parent.Right = replacement
        for ancestor in path:
            ancestor.Size -= 1
        return True

    def GetRandomNode(self) -> RandomNode | None:
        if self.Root is None:
            return None
        rank = RandomSource.GetRandom(0,self.Root.Size-1)
        node = self.Root
        while node is not None:
            left_size = 0 if node.Left is None else node.Left.Size
            if rank < left_size:
                node = node.Left
            elif rank == left_size:
                return node
            else:
                rank -= left_size+1
                node = node.Right
        return None
'''
    if language=='javascript':return '''class RandomBst {
  static SizedNode = class extends RandomNode {constructor(value){super(value);this.Size=1;}};
  constructor(){this.Root=null;}
  Insert(value){const added=new RandomBst.SizedNode(value);if(this.Root===null){this.Root=added;return;}const path=[];let node=this.Root;while(true){path.push(node);if(value<=node.Data){if(node.Left===null){node.Left=added;break;}node=node.Left;}else{if(node.Right===null){node.Right=added;break;}node=node.Right;}}for(const ancestor of path)++ancestor.Size;}
  Find(value){let node=this.Root;while(node!==null){if(value===node.Data)return node;node=value<node.Data?node.Left:node.Right;}return null;}
  Delete(value){const path=[];let node=this.Root;while(node!==null&&node.Data!==value){path.push(node);node=value<node.Data?node.Left:node.Right;}if(node===null)return false;if(node.Left!==null&&node.Right!==null){path.push(node);let successor=node.Right;while(successor.Left!==null){path.push(successor);successor=successor.Left;}node.Data=successor.Data;node=successor;}const replacement=node.Left!==null?node.Left:node.Right;if(path.length===0)this.Root=replacement;else{const parent=path[path.length-1];if(parent.Left===node)parent.Left=replacement;else parent.Right=replacement;}for(const ancestor of path)--ancestor.Size;return true;}
  GetRandomNode(){if(this.Root===null)return null;let rank=RandomSource.GetRandom(0,this.Root.Size-1),node=this.Root;while(node!==null){const leftSize=node.Left===null?0:node.Left.Size;if(rank<leftSize)node=node.Left;else if(rank===leftSize)return node;else{rank-=leftSize+1;node=node.Right;}}return null;}
}'''
    if language=='csharp':return '''public class RandomBst {
    private sealed class SizedNode(int value):RandomNode(value) {public int Size=1;}
    public RandomNode? Root {get;private set;}
    private static int Size(RandomNode? node)=>node is null?0:((SizedNode)node).Size;
    public void Insert(int value){var added=new SizedNode(value);if(Root is null){Root=added;return;}var path=new List<RandomNode>();var node=Root;while(true){path.Add(node);if(value<=node.Data){if(node.Left is null){node.Left=added;break;}node=node.Left;}else{if(node.Right is null){node.Right=added;break;}node=node.Right;}}foreach(var ancestor in path)((SizedNode)ancestor).Size++;}
    public RandomNode? Find(int value){var node=Root;while(node is not null){if(value==node.Data)return node;node=value<node.Data?node.Left:node.Right;}return null;}
    public bool Delete(int value){var path=new List<RandomNode>();var node=Root;while(node is not null&&node.Data!=value){path.Add(node);node=value<node.Data?node.Left:node.Right;}if(node is null)return false;if(node.Left is not null&&node.Right is not null){path.Add(node);var successor=node.Right;while(successor.Left is not null){path.Add(successor);successor=successor.Left;}node.Data=successor.Data;node=successor;}var replacement=node.Left??node.Right;if(path.Count==0)Root=replacement;else{var parent=path[^1];if(ReferenceEquals(parent.Left,node))parent.Left=replacement;else parent.Right=replacement;}foreach(var ancestor in path)((SizedNode)ancestor).Size--;return true;}
    public RandomNode? GetRandomNode(){if(Root is null)return null;int rank=RandomSource.GetRandom(0,Size(Root)-1);var node=Root;while(node is not null){int leftSize=Size(node.Left);if(rank<leftSize)node=node.Left;else if(rank==leftSize)return node;else{rank-=leftSize+1;node=node.Right;}}return null;}
}'''
    if language=='java':return '''class RandomBst {
    private static final class SizedNode extends RandomNode {int Size=1;SizedNode(int value){super(value);}}
    public RandomNode Root;
    private static int size(RandomNode node){return node==null?0:((SizedNode)node).Size;}
    public void Insert(int value){var added=new SizedNode(value);if(Root==null){Root=added;return;}var path=new ArrayList<RandomNode>();RandomNode node=Root;while(true){path.add(node);if(value<=node.Data){if(node.Left==null){node.Left=added;break;}node=node.Left;}else{if(node.Right==null){node.Right=added;break;}node=node.Right;}}for(var ancestor:path)((SizedNode)ancestor).Size++;}
    public RandomNode Find(int value){RandomNode node=Root;while(node!=null){if(value==node.Data)return node;node=value<node.Data?node.Left:node.Right;}return null;}
    public boolean Delete(int value){var path=new ArrayList<RandomNode>();RandomNode node=Root;while(node!=null&&node.Data!=value){path.add(node);node=value<node.Data?node.Left:node.Right;}if(node==null)return false;if(node.Left!=null&&node.Right!=null){path.add(node);RandomNode successor=node.Right;while(successor.Left!=null){path.add(successor);successor=successor.Left;}node.Data=successor.Data;node=successor;}RandomNode replacement=node.Left!=null?node.Left:node.Right;if(path.isEmpty())Root=replacement;else{RandomNode parent=path.get(path.size()-1);if(parent.Left==node)parent.Left=replacement;else parent.Right=replacement;}for(var ancestor:path)((SizedNode)ancestor).Size--;return true;}
    public RandomNode GetRandomNode(){if(Root==null)return null;int rank=RandomSource.GetRandom(0,size(Root)-1);RandomNode node=Root;while(node!=null){int leftSize=size(node.Left);if(rank<leftSize)node=node.Left;else if(rank==leftSize)return node;else{rank-=leftSize+1;node=node.Right;}}return null;}
}'''
    return '''class RandomBst {
    struct SizedNode final:RandomNode {int Size=1;explicit SizedNode(int value):RandomNode(value){}};
    static int size(RandomNode* node){return node==nullptr?0:static_cast<SizedNode*>(node)->Size;}
public:
    RandomNode* Root=nullptr;
    RandomBst()=default;
    RandomBst(const RandomBst&)=delete;
    RandomBst& operator=(const RandomBst&)=delete;
    ~RandomBst(){std::vector<RandomNode*> pending;if(Root!=nullptr)pending.push_back(Root);while(!pending.empty()){auto node=pending.back();pending.pop_back();if(node->Left!=nullptr)pending.push_back(node->Left);if(node->Right!=nullptr)pending.push_back(node->Right);delete node;}Root=nullptr;}
    void Insert(int value){auto added=new SizedNode(value);if(Root==nullptr){Root=added;return;}std::vector<RandomNode*> path;auto node=Root;while(true){path.push_back(node);if(value<=node->Data){if(node->Left==nullptr){node->Left=added;break;}node=node->Left;}else{if(node->Right==nullptr){node->Right=added;break;}node=node->Right;}}for(auto ancestor:path)++static_cast<SizedNode*>(ancestor)->Size;}
    RandomNode* Find(int value){auto node=Root;while(node!=nullptr){if(value==node->Data)return node;node=value<node->Data?node->Left:node->Right;}return nullptr;}
    bool Delete(int value){std::vector<RandomNode*> path;auto node=Root;while(node!=nullptr&&node->Data!=value){path.push_back(node);node=value<node->Data?node->Left:node->Right;}if(node==nullptr)return false;if(node->Left!=nullptr&&node->Right!=nullptr){path.push_back(node);auto successor=node->Right;while(successor->Left!=nullptr){path.push_back(successor);successor=successor->Left;}node->Data=successor->Data;node=successor;}auto replacement=node->Left!=nullptr?node->Left:node->Right;if(path.empty())Root=replacement;else{auto parent=path.back();if(parent->Left==node)parent->Left=replacement;else parent->Right=replacement;}for(auto ancestor:path)--static_cast<SizedNode*>(ancestor)->Size;delete node;return true;}
    RandomNode* GetRandomNode(){if(Root==nullptr)return nullptr;int rank=RandomSource::GetRandom(0,size(Root)-1);auto node=Root;while(node!=nullptr){int leftSize=size(node->Left);if(rank<leftSize)node=node->Left;else if(rank==leftSize)return node;else{rank-=leftSize+1;node=node->Right;}}return nullptr;}
};'''
