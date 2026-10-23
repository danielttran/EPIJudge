"""Independent bounded-run generation and streaming binary external merge."""
def body(language):
    return {
'python':'''from functools import cmp_to_key
inputFile.Rewind()
runs=[]
while True:
    chunk=[]
    for _ in range(bufferLimit):
        record=inputFile.ReadLine()
        if record is None:
            break
        chunk.append(record)
    if not chunk:
        break
    chunk.sort(key=cmp_to_key(lambda first,second: first.CompareTo(second)))
    run=workspace.CreateFile()
    for record in chunk:
        run.AppendLine(record)
    run.Close()
    runs.append(run)
inputFile.Close()
if not runs:
    empty=workspace.CreateFile()
    empty.Close()
    return empty
while len(runs)>1:
    merged=[]
    for index in range(0,len(runs),2):
        if index+1==len(runs):
            merged.append(runs[index])
            continue
        left,right=runs[index],runs[index+1]
        left.Rewind()
        right.Rewind()
        output=workspace.CreateFile()
        first,second=left.ReadLine(),right.ReadLine()
        while first is not None or second is not None:
            if second is None or first is not None and first.CompareTo(second)<=0:
                output.AppendLine(first)
                first=left.ReadLine()
            else:
                output.AppendLine(second)
                second=right.ReadLine()
        output.Close()
        left.Close()
        right.Close()
        workspace.DeleteFile(left)
        workspace.DeleteFile(right)
        merged.append(output)
    runs=merged
runs[0].Rewind()
return runs[0]''',
'javascript':'''inputFile.Rewind();
let runs=[];
while(true){const chunk=[];for(let i=0;i<bufferLimit;++i){const record=inputFile.ReadLine();if(record===null)break;chunk.push(record);}if(chunk.length===0)break;chunk.sort((first,second)=>first.CompareTo(second));const run=workspace.CreateFile();for(const record of chunk)run.AppendLine(record);run.Close();runs.push(run);}
inputFile.Close();
if(runs.length===0){const empty=workspace.CreateFile();empty.Close();return empty;}
while(runs.length>1){const merged=[];for(let index=0;index<runs.length;index+=2){if(index+1===runs.length){merged.push(runs[index]);continue;}const left=runs[index],right=runs[index+1];left.Rewind();right.Rewind();const output=workspace.CreateFile();let first=left.ReadLine(),second=right.ReadLine();while(first!==null||second!==null){if(second===null||(first!==null&&first.CompareTo(second)<=0)){output.AppendLine(first);first=left.ReadLine();}else{output.AppendLine(second);second=right.ReadLine();}}output.Close();left.Close();right.Close();workspace.DeleteFile(left);workspace.DeleteFile(right);merged.push(output);}runs=merged;}
runs[0].Rewind();return runs[0];''',
'csharp':'''inputFile.Rewind();
var runs=new List<TextFile>();
while(true){var chunk=new List<LineRecord>();for(int i=0;i<bufferLimit;++i){var record=inputFile.ReadLine();if(record is null)break;chunk.Add(record);}if(chunk.Count==0)break;chunk.Sort((first,second)=>first.CompareTo(second));var run=workspace.CreateFile();foreach(var record in chunk)run.AppendLine(record);run.Close();runs.Add(run);}
inputFile.Close();
if(runs.Count==0){var empty=workspace.CreateFile();empty.Close();return empty;}
while(runs.Count>1){var merged=new List<TextFile>();for(int index=0;index<runs.Count;index+=2){if(index+1==runs.Count){merged.Add(runs[index]);continue;}var left=runs[index];var right=runs[index+1];left.Rewind();right.Rewind();var output=workspace.CreateFile();LineRecord? first=left.ReadLine(),second=right.ReadLine();while(first is not null||second is not null){if(second is null||(first is not null&&first.CompareTo(second)<=0)){output.AppendLine(first!);first=left.ReadLine();}else{output.AppendLine(second);second=right.ReadLine();}}output.Close();left.Close();right.Close();workspace.DeleteFile(left);workspace.DeleteFile(right);merged.Add(output);}runs=merged;}
runs[0].Rewind();return runs[0];''',
'java':'''inputFile.Rewind();
var runs=new ArrayList<TextFile>();
while(true){var chunk=new ArrayList<LineRecord>();for(int i=0;i<bufferLimit;++i){var record=inputFile.ReadLine();if(record==null)break;chunk.add(record);}if(chunk.isEmpty())break;chunk.sort((first,second)->first.CompareTo(second));var run=workspace.CreateFile();for(var record:chunk)run.AppendLine(record);run.Close();runs.add(run);}
inputFile.Close();
if(runs.isEmpty()){var empty=workspace.CreateFile();empty.Close();return empty;}
while(runs.size()>1){var merged=new ArrayList<TextFile>();for(int index=0;index<runs.size();index+=2){if(index+1==runs.size()){merged.add(runs.get(index));continue;}var left=runs.get(index);var right=runs.get(index+1);left.Rewind();right.Rewind();var output=workspace.CreateFile();LineRecord first=left.ReadLine(),second=right.ReadLine();while(first!=null||second!=null){if(second==null||(first!=null&&first.CompareTo(second)<=0)){output.AppendLine(first);first=left.ReadLine();}else{output.AppendLine(second);second=right.ReadLine();}}output.Close();left.Close();right.Close();workspace.DeleteFile(left);workspace.DeleteFile(right);merged.add(output);}runs=merged;}
runs.get(0).Rewind();return runs.get(0);''',
'cpp':'''inputFile.Rewind();
std::vector<TextFile*> runs;
while(true){std::vector<LineRecord*> chunk;for(int i=0;i<bufferLimit;++i){auto record=inputFile.ReadLine();if(!record)break;chunk.push_back(record);}if(chunk.empty())break;std::sort(chunk.begin(),chunk.end(),[](LineRecord* first,LineRecord* second){return first->CompareTo(*second)<0;});TextFile* run=workspace.CreateFile();for(auto record:chunk)run->AppendLine(*record);run->Close();runs.push_back(run);}
inputFile.Close();
if(runs.empty()){TextFile* empty=workspace.CreateFile();empty->Close();return empty;}
while(runs.size()>1){std::vector<TextFile*> merged;for(std::size_t index=0;index<runs.size();index+=2){if(index+1==runs.size()){merged.push_back(runs[index]);continue;}TextFile* left=runs[index];TextFile* right=runs[index+1];left->Rewind();right->Rewind();TextFile* output=workspace.CreateFile();LineRecord* first=left->ReadLine();LineRecord* second=right->ReadLine();while(first||second){if(!second||(first&&first->CompareTo(*second)<=0)){output->AppendLine(*first);first=left->ReadLine();}else{output->AppendLine(*second);second=right->ReadLine();}}output->Close();left->Close();right->Close();workspace.DeleteFile(*left);workspace.DeleteFile(*right);merged.push_back(output);}runs=std::move(merged);}
runs[0]->Rewind();return runs[0];'''}[language]
