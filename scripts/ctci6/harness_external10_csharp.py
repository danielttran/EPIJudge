"""Disk-backed private models with exact live-record accounting."""
CORE=r'''
sealed class ExternalContext10:IDisposable {
public readonly string Root;public readonly int Limit,IoLimit,FileLimit;public readonly List<ExternalFile10> Files=new();public readonly ExternalFile10 Input;public bool Active;public int Live,Peak,Reads,Writes,Creates,Streams,MaxStreams;
public static void Check(bool ok,string message){if(!ok)throw new InvalidOperationException(message);}
public ExternalContext10(string[] lines,int limit){Limit=limit;int power=1,log=0;while(power<Math.Max(1,lines.Length)){power<<=1;log++;}IoLimit=8*lines.Length*(log+2)+128;FileLimit=4*lines.Length+64;Root=Path.Combine(Directory.GetCurrentDirectory(),".ctci-external-"+Guid.NewGuid().ToString("N"));Directory.CreateDirectory(Root);string path=Path.Combine(Root,"input");File.WriteAllLines(path,lines,Encoding.ASCII);Input=new ExternalFile10(this,path,true);Files.Add(Input);}
public void ReadTick(){if(Active)Check(++Reads<=IoLimit,"External file I/O budget exceeded");}public void WriteTick(){if(Active)Check(++Writes<=IoLimit,"External file I/O budget exceeded");}
public void Opened(){Streams++;MaxStreams=Math.Max(MaxStreams,Streams);Check(Streams<=16,"Close completed file streams before opening more");}public void Closed(){Streams--;}
public LineRecord Acquire(string text){Check(Live<Limit,"Live record buffer limit exceeded");Live++;Peak=Math.Max(Peak,Live);return new ExternalRecord10(this,text);}
public void Dispose(){Active=false;foreach(var file in Files)file.Close();if(Directory.Exists(Root))Directory.Delete(Root,true);}
}
sealed class ExternalRecord10(ExternalContext10 owner,string text):LineRecord {
public readonly ExternalContext10 Owner=owner;public string Text=text;public bool Alive=true;
public void Valid()=>ExternalContext10.Check(Alive,"Record was already consumed or released");
public override int CompareTo(LineRecord other){Valid();ExternalContext10.Check(other is ExternalRecord10 record&&ReferenceEquals(record.Owner,Owner),"Compare only records from this workspace");var actual=(ExternalRecord10)other;actual.Valid();return string.CompareOrdinal(Text,actual.Text);}
public override void Release(){Valid();Alive=false;Text=string.Empty;Owner.Live--;}
}
sealed class ExternalFile10(ExternalContext10 owner,string path,bool readOnly):TextFile {
public readonly ExternalContext10 Owner=owner;public readonly string PathName=path;public readonly bool ReadOnly=readOnly;public bool Deleted;private StreamReader? reader;private StreamWriter? writer;
private void Valid()=>ExternalContext10.Check(!Deleted,"File was deleted");
public override LineRecord? ReadLine(){Valid();Owner.ReadTick();writer?.Flush();if(reader is null){Owner.Opened();reader=new StreamReader(PathName,Encoding.ASCII,false);}string? text=reader.ReadLine();return text is null?null:Owner.Acquire(text);}
public override void Rewind(){Valid();writer?.Flush();if(reader is not null){reader.Dispose();reader=null;Owner.Closed();}}
public override void AppendLine(LineRecord record){Valid();ExternalContext10.Check(!ReadOnly,"Input file is read-only");ExternalContext10.Check(record is ExternalRecord10 actual&&ReferenceEquals(actual.Owner,Owner),"Write only a live owned record");var value=(ExternalRecord10)record;value.Valid();Owner.WriteTick();if(writer is null){Owner.Opened();writer=new StreamWriter(PathName,true,Encoding.ASCII);}writer.WriteLine(value.Text);value.Release();}
public override void Close(){if(reader is not null){reader.Dispose();reader=null;Owner.Closed();}if(writer is not null){writer.Dispose();writer=null;Owner.Closed();}}
}
sealed class ExternalWorkspace10(ExternalContext10 owner):TextWorkspace {
public override TextFile CreateFile(){ExternalContext10.Check(++owner.Creates<=owner.FileLimit,"Temporary-file creation budget exceeded");string path=Path.Combine(owner.Root,owner.Creates.ToString(System.Globalization.CultureInfo.InvariantCulture));File.WriteAllText(path,string.Empty,Encoding.ASCII);var file=new ExternalFile10(owner,path,false);owner.Files.Add(file);return file;}
public override void DeleteFile(TextFile file){ExternalContext10.Check(file is ExternalFile10 actual&&ReferenceEquals(actual.Owner,owner)&&owner.Files.Contains(actual)&&!actual.ReadOnly&&!actual.Deleted,"Delete only a live workspace temporary file");var target=(ExternalFile10)file;target.Close();File.Delete(target.PathName);target.Deleted=true;}
}
static class ExternalAudit10 {
public static object Run(JsonElement row){var args=row.GetProperty("arguments");string[] lines=JsonSerializer.Deserialize<string[]>(args[0].GetRawText())!;using var context=new ExternalContext10(lines,args[1].GetInt32());TextFile result;context.Active=true;try{result=new Solution_10_6().SortExternalFile(context.Input,context.Limit,new ExternalWorkspace10(context));}finally{context.Active=false;}ExternalContext10.Check(result is ExternalFile10 actual&&ReferenceEquals(actual.Owner,context)&&context.Files.Contains(actual)&&!actual.Deleted,"Return a live input/workspace file, not an in-memory replacement");ExternalContext10.Check(context.Live==0,"Consume or release every record before returning");var output=(ExternalFile10)result;output.Close();context.Input.Close();string[] contents=File.ReadAllLines(output.PathName,Encoding.ASCII);bool preserved=File.ReadAllLines(context.Input.PathName,Encoding.ASCII).SequenceEqual(lines);return new {actual=contents,mutationOk=preserved,ownedResult=true,peakRecords=context.Peak,liveRecords=context.Live,reads=context.Reads,writes=context.Writes,createdFiles=context.Creates,maxStreams=context.MaxStreams};}
}
'''
INSIDE='static object ExecuteExternal10(JsonElement row)=>ExternalAudit10.Run(row);\n'
