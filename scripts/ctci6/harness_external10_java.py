"""Buffered disk I/O and consumable record accounting for Java submissions."""
CORE=r'''
class ExternalContext10 implements AutoCloseable {
final Path root;final int limit,ioLimit,fileLimit;final ArrayList<ExternalFile10> files=new ArrayList<>();final ExternalFile10 input;boolean active;int live,peak,reads,writes,creates,streams,maxStreams;
static void check(boolean ok,String message){if(!ok)throw new IllegalStateException(message);}
ExternalContext10(List<String> lines,int limit){this.limit=limit;int power=1,log=0;while(power<Math.max(1,lines.size())){power<<=1;log++;}ioLimit=8*lines.size()*(log+2)+128;fileLimit=4*lines.size()+64;try{root=Files.createTempDirectory(Path.of("."),".ctci-external-");Path path=root.resolve("input");Files.write(path,lines,StandardCharsets.US_ASCII);input=new ExternalFile10(this,path,true);files.add(input);}catch(IOException error){throw new UncheckedIOException(error);}}
void readTick(){if(active)check(++reads<=ioLimit,"External file I/O budget exceeded");}void writeTick(){if(active)check(++writes<=ioLimit,"External file I/O budget exceeded");}void opened(){streams++;maxStreams=Math.max(maxStreams,streams);check(streams<=16,"Close completed file streams before opening more");}void closed(){streams--;}
LineRecord acquire(String text){check(live<limit,"Live record buffer limit exceeded");live++;peak=Math.max(peak,live);return new ExternalRecord10(this,text);}
public void close(){active=false;for(var file:files)file.Close();try(var paths=Files.walk(root)){paths.sorted(Comparator.reverseOrder()).forEach(path->{try{Files.deleteIfExists(path);}catch(IOException error){throw new UncheckedIOException(error);}});}catch(IOException error){throw new UncheckedIOException(error);}}
}
class ExternalRecord10 extends LineRecord {
final ExternalContext10 owner;String text;boolean alive=true;ExternalRecord10(ExternalContext10 owner,String text){this.owner=owner;this.text=text;}
void valid(){ExternalContext10.check(alive,"Record was already consumed or released");}
public int CompareTo(LineRecord other){valid();ExternalContext10.check(other instanceof ExternalRecord10 record&&record.owner==owner,"Compare only records from this workspace");var record=(ExternalRecord10)other;record.valid();return text.compareTo(record.text);}
public void Release(){valid();alive=false;text="";owner.live--;}
}
class ExternalFile10 extends TextFile {
final ExternalContext10 owner;final Path path;final boolean readOnly;boolean deleted;BufferedReader reader;BufferedWriter writer;
ExternalFile10(ExternalContext10 owner,Path path,boolean readOnly){this.owner=owner;this.path=path;this.readOnly=readOnly;}
void valid(){ExternalContext10.check(!deleted,"File was deleted");}
public LineRecord ReadLine(){valid();owner.readTick();try{if(writer!=null)writer.flush();if(reader==null){owner.opened();reader=Files.newBufferedReader(path,StandardCharsets.US_ASCII);}String text=reader.readLine();return text==null?null:owner.acquire(text);}catch(IOException error){throw new UncheckedIOException(error);}}
public void Rewind(){valid();try{if(writer!=null)writer.flush();if(reader!=null){reader.close();reader=null;owner.closed();}}catch(IOException error){throw new UncheckedIOException(error);}}
public void AppendLine(LineRecord record){valid();ExternalContext10.check(!readOnly,"Input file is read-only");ExternalContext10.check(record instanceof ExternalRecord10 actual&&actual.owner==owner,"Write only a live owned record");var value=(ExternalRecord10)record;value.valid();owner.writeTick();try{if(writer==null){owner.opened();writer=Files.newBufferedWriter(path,StandardCharsets.US_ASCII,StandardOpenOption.APPEND);}writer.write(value.text);writer.newLine();value.Release();}catch(IOException error){throw new UncheckedIOException(error);}}
public void Close(){try{if(reader!=null){reader.close();reader=null;owner.closed();}if(writer!=null){writer.close();writer=null;owner.closed();}}catch(IOException error){throw new UncheckedIOException(error);}}
}
class ExternalWorkspace10 extends TextWorkspace {
final ExternalContext10 owner;ExternalWorkspace10(ExternalContext10 owner){this.owner=owner;}
public TextFile CreateFile(){ExternalContext10.check(++owner.creates<=owner.fileLimit,"Temporary-file creation budget exceeded");Path path=owner.root.resolve(Integer.toString(owner.creates));try{Files.createFile(path);}catch(IOException error){throw new UncheckedIOException(error);}var file=new ExternalFile10(owner,path,false);owner.files.add(file);return file;}
public void DeleteFile(TextFile file){ExternalContext10.check(file instanceof ExternalFile10 actual&&actual.owner==owner&&owner.files.contains(actual)&&!actual.readOnly&&!actual.deleted,"Delete only a live workspace temporary file");var target=(ExternalFile10)file;target.Close();try{Files.delete(target.path);}catch(IOException error){throw new UncheckedIOException(error);}target.deleted=true;}
}
class ExternalAudit10 {
static JsonValue run(JsonObject row){var args=row.get("arguments").asArray();var lines=new ArrayList<String>();for(var line:args.get(0).asArray())lines.add(line.asString());try(var context=new ExternalContext10(lines,args.get(1).asInt())){TextFile result;context.active=true;try{result=new Solution_10_6().SortExternalFile(context.input,context.limit,new ExternalWorkspace10(context));}finally{context.active=false;}ExternalContext10.check(result instanceof ExternalFile10 actual&&actual.owner==context&&context.files.contains(actual)&&!actual.deleted,"Return a live input/workspace file, not an in-memory replacement");ExternalContext10.check(context.live==0,"Consume or release every record before returning");var output=(ExternalFile10)result;output.Close();context.input.Close();try{var actual=new JsonArray();for(String line:Files.readAllLines(output.path,StandardCharsets.US_ASCII))actual.add(line);boolean preserved=Files.readAllLines(context.input.path,StandardCharsets.US_ASCII).equals(lines);return new JsonObject().add("actual",actual).add("mutationOk",preserved).add("ownedResult",true).add("peakRecords",context.peak).add("liveRecords",context.live).add("reads",context.reads).add("writes",context.writes).add("createdFiles",context.creates).add("maxStreams",context.maxStreams);}catch(IOException error){throw new UncheckedIOException(error);}}}
}
'''
INSIDE='static JsonValue executeExternal10(JsonObject row){return ExternalAudit10.run(row);}\n'
