"""Independent generic offset collection with actual native iterators."""
def body(ref,language):
    if ref!='7.9':raise ValueError(ref)
    return {
'csharp':'''public class CircularArray<T>:IEnumerable<T> {
    private readonly T[] items;
    private int head;
    public CircularArray(T[] initialValues){items=initialValues.ToArray();}
    private void CheckIndex(int index){if(index<0||index>=items.Length)throw new ArgumentOutOfRangeException(nameof(index));}
    public T Get(int index){CheckIndex(index);return items[(head+index)%items.Length];}
    public void Set(int index,T value){CheckIndex(index);items[(head+index)%items.Length]=value;}
    public void Rotate(int shift){if(items.Length==0)return;int step=shift%items.Length;if(step<0)step+=items.Length;head=(head+step)%items.Length;}
    public IEnumerator<T> GetEnumerator(){for(int index=0;index<items.Length;++index)yield return items[(head+index)%items.Length];}
    System.Collections.IEnumerator System.Collections.IEnumerable.GetEnumerator()=>GetEnumerator();
}''',
'java':'''class CircularArray<T> implements Iterable<T> {
    private final ArrayList<T> items;
    private int head;
    public CircularArray(List<T> initialValues){items=new ArrayList<>(initialValues);}
    private void checkIndex(int index){if(index<0||index>=items.size())throw new IndexOutOfBoundsException("index");}
    public T Get(int index){checkIndex(index);return items.get((head+index)%items.size());}
    public void Set(int index,T value){checkIndex(index);items.set((head+index)%items.size(),value);}
    public void Rotate(int shift){if(items.isEmpty())return;head=(head+Math.floorMod(shift,items.size()))%items.size();}
    public Iterator<T> iterator(){return new Iterator<T>(){private int cursor;public boolean hasNext(){return cursor<items.size();}public T next(){if(!hasNext())throw new NoSuchElementException();return Get(cursor++);}};}
}''',
'cpp':'''template<class T> class CircularArray {
    std::vector<T> items;
    int head=0;
    void checkIndex(int index)const{if(index<0||index>=static_cast<int>(items.size()))throw std::out_of_range("index");}
public:
    explicit CircularArray(const std::vector<T>& initialValues):items(initialValues){}
    T Get(int index)const{checkIndex(index);return items[(head+index)%items.size()];}
    void Set(int index,const T& value){checkIndex(index);items[(head+index)%items.size()]=value;}
    void Rotate(int shift){if(items.empty())return;int size=static_cast<int>(items.size()),step=shift%size;if(step<0)step+=size;head=(head+step)%size;}
    class const_iterator {
        const CircularArray* owner=nullptr;
        std::size_t cursor=0;
    public:
        using value_type=T;
        using difference_type=std::ptrdiff_t;
        using reference=typename std::vector<T>::const_reference;
        using pointer=void;
        using iterator_category=std::input_iterator_tag;
        const_iterator()=default;
        const_iterator(const CircularArray* owner,std::size_t cursor):owner(owner),cursor(cursor){}
        reference operator*()const{return owner->items[(owner->head+cursor)%owner->items.size()];}
        const_iterator& operator++(){++cursor;return *this;}
        const_iterator operator++(int){auto previous=*this;++*this;return previous;}
        bool operator==(const const_iterator& other)const{return owner==other.owner&&cursor==other.cursor;}
        bool operator!=(const const_iterator& other)const{return !(*this==other);}
    };
    const_iterator begin()const{return const_iterator(this,0);}
    const_iterator end()const{return const_iterator(this,items.size());}
};''',
'python':'''_T=TypeVar("_T")
class CircularArray(Generic[_T]):
    def __init__(self,initialValues: list[_T]):
        self._items=initialValues.copy()
        self._head=0
    def _check_index(self,index: int) -> None:
        if index<0 or index>=len(self._items):
            raise IndexError(index)
    def Get(self,index: int) -> _T:
        self._check_index(index)
        return self._items[(self._head+index)%len(self._items)]
    def Set(self,index: int,value: _T) -> None:
        self._check_index(index)
        self._items[(self._head+index)%len(self._items)]=value
    def Rotate(self,shift: int) -> None:
        if self._items:
            self._head=(self._head+shift)%len(self._items)
    def __iter__(self) -> Iterator[_T]:
        for index in range(len(self._items)):
            yield self._items[(self._head+index)%len(self._items)]
''',
'javascript':'''class CircularArray {
    constructor(initialValues){this.items=initialValues.slice();this.head=0;}
    checkIndex(index){if(index<0||index>=this.items.length)throw new RangeError("index");}
    Get(index){this.checkIndex(index);return this.items[(this.head+index)%this.items.length];}
    Set(index,value){this.checkIndex(index);this.items[(this.head+index)%this.items.length]=value;}
    Rotate(shift){const size=this.items.length;if(size===0)return;const step=((shift%size)+size)%size;this.head=(this.head+step)%size;}
    *[Symbol.iterator](){for(let index=0;index<this.items.length;++index)yield this.items[(this.head+index)%this.items.length];}
}'''}[language]

_previous_body=body
def body(ref,language):
    if ref=='7.12':
        from algorithms_hash07 import body as run
        return run(language)
    return _previous_body(ref,language)

_generic_previous_body=body
def body(ref,language):
    if ref=='7.6':
        from algorithms_jigsaw07 import body as run
        return run(language)
    return _generic_previous_body(ref,language)

_jigsaw_previous_body=body
def body(ref,language):
    if ref=='7.10':
        from algorithms_mines07 import body as run
        return run(language)
    return _jigsaw_previous_body(ref,language)

_mines_previous_body=body
def body(ref,language):
    if ref=='7.8':
        from algorithms_othello07 import body as run
        return run(language)
    return _mines_previous_body(ref,language)
