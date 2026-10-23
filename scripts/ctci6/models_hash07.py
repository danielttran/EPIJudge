"""Generic hash-table APIs retain concrete value returns without null ambiguity."""
SIGNATURE={
'csharp':'class HashTable<K,V> where K:notnull; HashTable(int capacity); void Put(K key,V value); V Get(K key); bool Remove(K key); bool Contains(K key)',
'java':'HashTable<K,V>(int capacity); void Put(K key,V value); V Get(K key); boolean Remove(K key); boolean Contains(K key)',
'cpp':'template<class K,class V> HashTable<K,V>(int capacity); void Put(const K& key,const V& value); V Get(const K& key) const; bool Remove(const K& key); bool Contains(const K& key) const',
'python':'HashTable[K,V](capacity: int); Put(key: K,value: V) -> None; Get(key: K) -> V; Remove(key: K) -> bool; Contains(key: K) -> bool',
'javascript':'new HashTable(capacity); Put(key,value); Get(key); Remove(key) -> boolean; Contains(key) -> boolean'}
def neutral(language):
    return {
'csharp':'public class HashTable<K,V> where K:notnull {public HashTable(int capacity){}public void Put(K key,V value){}public V Get(K key)=>throw new KeyNotFoundException();public bool Remove(K key)=>false;public bool Contains(K key)=>false;}',
'java':'class HashTable<K,V> {public HashTable(int capacity){}public void Put(K key,V value){}public V Get(K key){throw new NoSuchElementException();}public boolean Remove(K key){return false;}public boolean Contains(K key){return false;}}',
'cpp':'template<class K,class V> class HashTable {public:explicit HashTable(int capacity){}void Put(const K& key,const V& value){}V Get(const K& key)const{throw std::out_of_range("missing");}bool Remove(const K& key){return false;}bool Contains(const K& key)const{return false;}};',
'python':'_K=TypeVar("_K",bound=Hashable)\n_V=TypeVar("_V")\nclass HashTable(Generic[_K,_V]):\n    def __init__(self,capacity: int):\n        pass\n    def Put(self,key: _K,value: _V) -> None:\n        pass\n    def Get(self,key: _K) -> _V:\n        raise KeyError(key)\n    def Remove(self,key: _K) -> bool:\n        return False\n    def Contains(self,key: _K) -> bool:\n        return False\n',
'javascript':'class HashTable {constructor(capacity){}Put(key,value){}Get(key){throw new RangeError("missing");}Remove(key){return false;}Contains(key){return false;}}'}[language]
