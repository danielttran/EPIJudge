"""Comparable leased records make the external-memory buffer limit observable."""
from models08 import TYPES
API={
'csharp':'''public abstract class LineRecord {public abstract int CompareTo(LineRecord other);public abstract void Release();}
public abstract class TextFile {public abstract LineRecord? ReadLine();public abstract void Rewind();public abstract void AppendLine(LineRecord record);public abstract void Close();}
public abstract class TextWorkspace {public abstract TextFile CreateFile();public abstract void DeleteFile(TextFile file);}
''',
'java':'''abstract class LineRecord {public abstract int CompareTo(LineRecord other);public abstract void Release();}
abstract class TextFile {public abstract LineRecord ReadLine();public abstract void Rewind();public abstract void AppendLine(LineRecord record);public abstract void Close();}
abstract class TextWorkspace {public abstract TextFile CreateFile();public abstract void DeleteFile(TextFile file);}
''',
'cpp':'''struct LineRecord {virtual int CompareTo(const LineRecord& other)const=0;virtual void Release()=0;protected:virtual ~LineRecord()=default;};
struct TextFile {virtual LineRecord* ReadLine()=0;virtual void Rewind()=0;virtual void AppendLine(LineRecord& record)=0;virtual void Close()=0;protected:virtual ~TextFile()=default;};
struct TextWorkspace {virtual TextFile* CreateFile()=0;virtual void DeleteFile(TextFile& file)=0;protected:virtual ~TextWorkspace()=default;};
''',
'python':'''class LineRecord:
    def CompareTo(self,other: "LineRecord") -> int:
        raise RuntimeError("Provided by the judge")
    def Release(self) -> None:
        raise RuntimeError("Provided by the judge")
class TextFile:
    def ReadLine(self) -> LineRecord | None:
        raise RuntimeError("Provided by the judge")
    def Rewind(self) -> None:
        raise RuntimeError("Provided by the judge")
    def AppendLine(self,record: LineRecord) -> None:
        raise RuntimeError("Provided by the judge")
    def Close(self) -> None:
        raise RuntimeError("Provided by the judge")
class TextWorkspace:
    def CreateFile(self) -> TextFile:
        raise RuntimeError("Provided by the judge")
    def DeleteFile(self,file: TextFile) -> None:
        raise RuntimeError("Provided by the judge")
''',
'javascript':'''class LineRecord {CompareTo(other){throw new Error("Provided by the judge");}Release(){throw new Error("Provided by the judge");}}
class TextFile {ReadLine(){throw new Error("Provided by the judge");}Rewind(){throw new Error("Provided by the judge");}AppendLine(record){throw new Error("Provided by the judge");}Close(){throw new Error("Provided by the judge");}}
class TextWorkspace {CreateFile(){throw new Error("Provided by the judge");}DeleteFile(file){throw new Error("Provided by the judge");}}
'''}
for language in TYPES:
    TYPES[language]['textfile']='TextFile&' if language=='cpp' else 'TextFile'
    TYPES[language]['textworkspace']='TextWorkspace&' if language=='cpp' else 'TextWorkspace'
    TYPES[language]['file_result']='TextFile*' if language=='cpp' else 'TextFile'
