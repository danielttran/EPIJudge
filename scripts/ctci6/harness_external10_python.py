"""Real disk streams with consumable record leases and enforced I/O budgets."""
CORE=r'''
def executeExternal10(row):
    import os
    import tempfile
    lines,limit,placeholder=row['arguments']
    class ContractError(Exception):pass
    def check(ok,message):
        if not ok:raise ContractError(message)
    class Context:
        def __init__(self,root):
            self.root=root;self.files=[];self.active=False;self.live=self.peak=self.reads=self.writes=self.creates=self.streams=self.max_streams=0
            self.io_limit=8*len(lines)*((max(1,len(lines))-1).bit_length()+2)+128
        def tick(self,name):
            if self.active:
                value=getattr(self,name)+1;setattr(self,name,value)
                check(value<=self.io_limit,'External file I/O budget exceeded')
        def opened(self):
            self.streams+=1;self.max_streams=max(self.max_streams,self.streams)
            check(self.streams<=16,'Close completed file streams before opening more')
        def closed(self):self.streams-=1
        def acquire(self,text):
            check(self.live<limit,'Live record buffer limit exceeded')
            self.live+=1;self.peak=max(self.peak,self.live)
            return Record(self,text)
    class Record(LineRecord):
        def __init__(self,owner,text):self.owner=owner;self.text=text;self.alive=True
        def valid(self):check(self.alive,'Record was already consumed or released')
        def CompareTo(self,other):
            self.valid();check(type(other) is Record and other.owner is self.owner,'Compare only records from this workspace');other.valid()
            return (self.text>other.text)-(self.text<other.text)
        def Release(self):
            self.valid();self.alive=False;self.text=None;self.owner.live-=1
    class File(TextFile):
        def __init__(self,owner,path,readonly):self.owner=owner;self.path=path;self.readonly=readonly;self.deleted=False;self.reader=self.writer=None
        def valid(self):check(not self.deleted,'File was deleted')
        def ReadLine(self):
            self.valid();self.owner.tick('reads')
            if self.writer is not None:self.writer.flush()
            if self.reader is None:self.owner.opened();self.reader=open(self.path,'r',encoding='ascii',newline='')
            text=self.reader.readline()
            return None if text=='' else self.owner.acquire(text[:-1] if text.endswith('\n') else text)
        def Rewind(self):
            self.valid()
            if self.writer is not None:self.writer.flush()
            if self.reader is not None:self.reader.close();self.reader=None;self.owner.closed()
        def AppendLine(self,record):
            self.valid();check(not self.readonly,'Input file is read-only')
            check(type(record) is Record and record.owner is self.owner,'Write only a live owned record');record.valid();self.owner.tick('writes')
            if self.writer is None:self.owner.opened();self.writer=open(self.path,'a',encoding='ascii',newline='')
            self.writer.write(record.text+'\n');record.Release()
        def Close(self):
            if self.reader is not None:self.reader.close();self.reader=None;self.owner.closed()
            if self.writer is not None:self.writer.close();self.writer=None;self.owner.closed()
    class Workspace(TextWorkspace):
        def __init__(self,owner):self.owner=owner
        def CreateFile(self):
            self.owner.creates+=1;check(self.owner.creates<=4*len(lines)+64,'Temporary-file creation budget exceeded')
            path=os.path.join(self.owner.root,str(self.owner.creates));open(path,'w').close();result=File(self.owner,path,False);self.owner.files.append(result);return result
        def DeleteFile(self,file):
            check(type(file) is File and file.owner is self.owner and any(file is actual for actual in self.owner.files) and not file.readonly and not file.deleted,'Delete only a live workspace temporary file')
            file.Close();os.remove(file.path);file.deleted=True
    with tempfile.TemporaryDirectory(prefix='.ctci-external-',dir='.') as root:
        context=Context(root);input_path=os.path.join(root,'input')
        with open(input_path,'w',encoding='ascii',newline='') as initial:
            for line in lines:initial.write(line+'\n')
        input_file=File(context,input_path,True);context.files.append(input_file)
        try:
            context.active=True
            try:result=SortExternalFile(input_file,limit,Workspace(context))
            finally:context.active=False
            check(type(result) is File and result.owner is context and any(result is file for file in context.files) and not result.deleted,'Return a live input/workspace file, not an in-memory replacement')
            check(context.live==0,'Consume or release every record before returning')
            result.Close();input_file.Close()
            with open(result.path,'r',encoding='ascii',newline='') as stream:actual=[line[:-1] if line.endswith('\n') else line for line in stream]
            with open(input_path,'r',encoding='ascii',newline='') as stream:preserved=[line[:-1] if line.endswith('\n') else line for line in stream]
            return dict(actual=actual,mutationOk=preserved==lines,ownedResult=True,peakRecords=context.peak,liveRecords=context.live,reads=context.reads,writes=context.writes,createdFiles=context.creates,maxStreams=context.max_streams)
        finally:
            for file in context.files:file.Close()
'''
