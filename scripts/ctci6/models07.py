"""Full generic state classes expose native iteration instead of fake row APIs."""
from models08 import header as base_header
SIGNATURE={
'csharp':'CircularArray<T>(T[] initialValues); T Get(int index); void Set(int index,T value); void Rotate(int shift); IEnumerable<T>',
'java':'CircularArray<T>(List<T> initialValues); T Get(int index); void Set(int index,T value); void Rotate(int shift); Iterable<T>',
'cpp':'template<class T> CircularArray<T>(const std::vector<T>& initialValues); T Get(int index) const; void Set(int index,const T& value); void Rotate(int shift); begin() const; end() const',
'python':'CircularArray(initialValues: list[T]); Get(index: int) -> T; Set(index: int,value: T) -> None; Rotate(shift: int) -> None; __iter__() -> Iterator[T]',
'javascript':'new CircularArray(initialValues); Get(index); Set(index,value); Rotate(shift); [Symbol.iterator]()'}
def declare(spec,language,body,class_name='Solution'):
    if language=='python':body='from typing import Generic,TypeVar,Iterator\n'+body
    return SIGNATURE[language],body

def header(ref,language):
    return base_header(ref,language)+('' if language=='python' else '#include <iterator>\n#include <stdexcept>\n' if language=='cpp' else '')

def neutral(spec,language):
    return {
'csharp':'public class CircularArray<T>:IEnumerable<T> {public CircularArray(T[] initialValues){}public T Get(int index)=>throw new ArgumentOutOfRangeException(nameof(index));public void Set(int index,T value){throw new ArgumentOutOfRangeException(nameof(index));}public void Rotate(int shift){}public IEnumerator<T> GetEnumerator()=>Enumerable.Empty<T>().GetEnumerator();System.Collections.IEnumerator System.Collections.IEnumerable.GetEnumerator()=>GetEnumerator();}',
'java':'class CircularArray<T> implements Iterable<T> {public CircularArray(List<T> initialValues){}public T Get(int index){throw new IndexOutOfBoundsException();}public void Set(int index,T value){throw new IndexOutOfBoundsException();}public void Rotate(int shift){}public Iterator<T> iterator(){return Collections.emptyIterator();}}',
'cpp':'template<class T> class CircularArray {std::vector<T> empty;public:explicit CircularArray(const std::vector<T>& initialValues){}T Get(int index)const{throw std::out_of_range("index");}void Set(int index,const T& value){throw std::out_of_range("index");}void Rotate(int shift){}auto begin()const{return empty.begin();}auto end()const{return empty.end();}};',
'python':'_T=TypeVar("_T")\nclass CircularArray(Generic[_T]):\n    def __init__(self,initialValues: list[_T]):\n        pass\n    def Get(self,index: int) -> _T:\n        raise IndexError(index)\n    def Set(self,index: int,value: _T) -> None:\n        raise IndexError(index)\n    def Rotate(self,shift: int) -> None:\n        pass\n    def __iter__(self) -> Iterator[_T]:\n        return iter([])\n',
'javascript':'class CircularArray {constructor(initialValues){}Get(index){throw new RangeError("index");}Set(index,value){throw new RangeError("index");}Rotate(shift){}*[Symbol.iterator](){}}'}[language]
