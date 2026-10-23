"""Independent separate-chaining tables using language hash/equality primitives."""
def body(language):
    return {
'csharp':'''public class HashTable<K,V> where K:notnull {
    private sealed class Node(K key,V value,Node? next){public readonly K Key=key;public V Value=value;public Node? Next=next;}
    private readonly Node?[] buckets;
    public HashTable(int capacity){buckets=new Node?[capacity];}
    private int Index(K key)=>(int)((uint)EqualityComparer<K>.Default.GetHashCode(key)%(uint)buckets.Length);
    private Node? Find(K key){for(var node=buckets[Index(key)];node is not null;node=node.Next)if(EqualityComparer<K>.Default.Equals(node.Key,key))return node;return null;}
    public void Put(K key,V value){var node=Find(key);if(node is not null){node.Value=value;return;}int index=Index(key);buckets[index]=new Node(key,value,buckets[index]);}
    public V Get(K key){var node=Find(key);if(node is null)throw new KeyNotFoundException();return node.Value;}
    public bool Contains(K key)=>Find(key) is not null;
    public bool Remove(K key){int index=Index(key);Node? previous=null;var node=buckets[index];while(node is not null){if(EqualityComparer<K>.Default.Equals(node.Key,key)){if(previous is null)buckets[index]=node.Next;else previous.Next=node.Next;return true;}previous=node;node=node.Next;}return false;}
}''',
'java':'''class HashTable<K,V> {
    private static class Node<K,V>{final K key;V value;Node<K,V> next;Node(K key,V value,Node<K,V> next){this.key=key;this.value=value;this.next=next;}}
    private final ArrayList<Node<K,V>> buckets;
    public HashTable(int capacity){buckets=new ArrayList<>(Collections.nCopies(capacity,null));}
    private int index(K key){return Math.floorMod(key.hashCode(),buckets.size());}
    private Node<K,V> find(K key){for(var node=buckets.get(index(key));node!=null;node=node.next)if(Objects.equals(node.key,key))return node;return null;}
    public void Put(K key,V value){var node=find(key);if(node!=null){node.value=value;return;}int slot=index(key);buckets.set(slot,new Node<>(key,value,buckets.get(slot)));}
    public V Get(K key){var node=find(key);if(node==null)throw new NoSuchElementException();return node.value;}
    public boolean Contains(K key){return find(key)!=null;}
    public boolean Remove(K key){int slot=index(key);Node<K,V> previous=null;var node=buckets.get(slot);while(node!=null){if(Objects.equals(node.key,key)){if(previous==null)buckets.set(slot,node.next);else previous.next=node.next;return true;}previous=node;node=node.next;}return false;}
}''',
'cpp':'''template<class K,class V> class HashTable {
    struct Node {K key;V value;Node* next;Node(K key,V value,Node* next):key(std::move(key)),value(std::move(value)),next(next){}};
    std::vector<Node*> buckets;
    std::size_t index(const K& key)const{return std::hash<K>{}(key)%buckets.size();}
    Node* find(const K& key)const{for(Node* node=buckets[index(key)];node;node=node->next)if(std::equal_to<K>{}(node->key,key))return node;return nullptr;}
public:
    explicit HashTable(int capacity):buckets(capacity,nullptr){}
    HashTable(const HashTable&)=delete;
    HashTable& operator=(const HashTable&)=delete;
    ~HashTable(){for(Node* node:buckets)while(node){Node* next=node->next;delete node;node=next;}}
    void Put(const K& key,const V& value){if(Node* node=find(key)){node->value=value;return;}auto slot=index(key);buckets[slot]=new Node(key,value,buckets[slot]);}
    V Get(const K& key)const{Node* node=find(key);if(!node)throw std::out_of_range("missing");return node->value;}
    bool Contains(const K& key)const{return find(key)!=nullptr;}
    bool Remove(const K& key){Node** link=&buckets[index(key)];while(*link&&!std::equal_to<K>{}((*link)->key,key))link=&(*link)->next;if(!*link)return false;Node* removed=*link;*link=removed->next;delete removed;return true;}
};''',
'python':'''_K=TypeVar("_K",bound=Hashable)
_V=TypeVar("_V")
class HashTable(Generic[_K,_V]):
    class _Node:
        def __init__(self,key,value,next_node):
            self.key=key
            self.value=value
            self.next=next_node
    def __init__(self,capacity: int):
        self._buckets=[None]*capacity
    def _index(self,key: _K) -> int:
        return hash(key)%len(self._buckets)
    def _find(self,key: _K):
        node=self._buckets[self._index(key)]
        while node is not None:
            if node.key==key:
                return node
            node=node.next
        return None
    def Put(self,key: _K,value: _V) -> None:
        node=self._find(key)
        if node is not None:
            node.value=value
            return
        slot=self._index(key)
        self._buckets[slot]=HashTable._Node(key,value,self._buckets[slot])
    def Get(self,key: _K) -> _V:
        node=self._find(key)
        if node is None:
            raise KeyError(key)
        return node.value
    def Contains(self,key: _K) -> bool:
        return self._find(key) is not None
    def Remove(self,key: _K) -> bool:
        slot=self._index(key)
        previous=None
        node=self._buckets[slot]
        while node is not None:
            if node.key==key:
                if previous is None:
                    self._buckets[slot]=node.next
                else:
                    previous.next=node.next
                return True
            previous=node
            node=node.next
        return False
''',
'javascript':'''class HashTable {
    constructor(capacity){this.buckets=Array(capacity).fill(null);}
    index(key){if(typeof key==='number')return (key>>>0)%this.buckets.length;const text=String(key);let hash=2166136261;for(let i=0;i<text.length;++i)hash=Math.imul(hash^text.charCodeAt(i),16777619)>>>0;return hash%this.buckets.length;}
    find(key){for(let node=this.buckets[this.index(key)];node!==null;node=node.next)if(node.key===key)return node;return null;}
    Put(key,value){const node=this.find(key);if(node!==null){node.value=value;return;}const slot=this.index(key);this.buckets[slot]={key,value,next:this.buckets[slot]};}
    Get(key){const node=this.find(key);if(node===null)throw new RangeError("missing");return node.value;}
    Contains(key){return this.find(key)!==null;}
    Remove(key){const slot=this.index(key);let previous=null,node=this.buckets[slot];while(node!==null){if(node.key===key){if(previous===null)this.buckets[slot]=node.next;else previous.next=node.next;return true;}previous=node;node=node.next;}return false;}
}'''}[language]
