"""Physical files and bounded live payloads; released pointers remain tombstones."""
CORE=r'''
#include <filesystem>
#include <fstream>
#include <memory>
#include <chrono>
struct ExternalFile10;struct ExternalRecord10;
struct ExternalContext10 {
std::filesystem::path root;int limit,ioLimit,fileLimit;bool active=false;int live=0,peak=0,reads=0,writes=0,creates=0,streams=0,maxStreams=0;std::vector<std::unique_ptr<ExternalFile10>> files;std::vector<std::unique_ptr<ExternalRecord10>> records;ExternalFile10* input=nullptr;
static void check(bool ok,const std::string& message){if(!ok)throw std::runtime_error(message);}
ExternalContext10(const std::vector<std::string>& lines,int limit);~ExternalContext10();
void readTick(){if(active)check(++reads<=ioLimit,"External file I/O budget exceeded");}void writeTick(){if(active)check(++writes<=ioLimit,"External file I/O budget exceeded");}void opened(){++streams;maxStreams=std::max(maxStreams,streams);check(streams<=16,"Close completed file streams before opening more");}void closed(){--streams;}
LineRecord* acquire(std::string text);ExternalFile10* owned(TextFile* file);
};
struct ExternalRecord10:LineRecord {
ExternalContext10& owner;std::string text;bool alive=true;ExternalRecord10(ExternalContext10& owner,std::string text):owner(owner),text(std::move(text)){}~ExternalRecord10()override=default;
void valid()const{ExternalContext10::check(alive,"Record was already consumed or released");}
int CompareTo(const LineRecord& other)const override{valid();auto actual=dynamic_cast<const ExternalRecord10*>(&other);ExternalContext10::check(actual&&&actual->owner==&owner,"Compare only records from this workspace");actual->valid();return text.compare(actual->text);}
void Release()override{valid();alive=false;std::string{}.swap(text);--owner.live;}
};
struct ExternalFile10:TextFile {
ExternalContext10& owner;std::filesystem::path path;bool readOnly,deleted=false;std::unique_ptr<std::ifstream> reader;std::unique_ptr<std::ofstream> writer;
ExternalFile10(ExternalContext10& owner,std::filesystem::path path,bool readOnly):owner(owner),path(std::move(path)),readOnly(readOnly){}~ExternalFile10()override{Close();}
void valid()const{ExternalContext10::check(!deleted,"File was deleted");}
LineRecord* ReadLine()override{valid();owner.readTick();if(writer)writer->flush();if(!reader){owner.opened();reader=std::make_unique<std::ifstream>(path,std::ios::binary);ExternalContext10::check(reader->is_open(),"Cannot open owned file");}std::string text;if(!std::getline(*reader,text))return nullptr;return owner.acquire(std::move(text));}
void Rewind()override{valid();if(writer)writer->flush();if(reader){reader.reset();owner.closed();}}
void AppendLine(LineRecord& record)override{valid();ExternalContext10::check(!readOnly,"Input file is read-only");auto actual=dynamic_cast<ExternalRecord10*>(&record);ExternalContext10::check(actual&&&actual->owner==&owner,"Write only a live owned record");actual->valid();owner.writeTick();if(!writer){owner.opened();writer=std::make_unique<std::ofstream>(path,std::ios::binary|std::ios::app);ExternalContext10::check(writer->is_open(),"Cannot open owned file");}*writer<<actual->text<<'\n';ExternalContext10::check(static_cast<bool>(*writer),"Cannot append owned record");actual->Release();}
void Close()override{if(reader){reader.reset();owner.closed();}if(writer){writer.reset();owner.closed();}}
};
ExternalContext10::ExternalContext10(const std::vector<std::string>& lines,int capacity):limit(capacity){int power=1,log=0;while(power<std::max(1,static_cast<int>(lines.size()))){power<<=1;++log;}ioLimit=8*static_cast<int>(lines.size())*(log+2)+128;fileLimit=4*static_cast<int>(lines.size())+64;static unsigned long long serial=0;root=std::filesystem::current_path()/(".ctci-external-"+std::to_string(std::chrono::steady_clock::now().time_since_epoch().count())+"-"+std::to_string(serial++));std::filesystem::create_directory(root);auto path=root/"input";{std::ofstream initial(path,std::ios::binary);for(const auto& line:lines)initial<<line<<'\n';check(static_cast<bool>(initial),"Cannot create owned input file");}auto file=std::make_unique<ExternalFile10>(*this,path,true);input=file.get();files.push_back(std::move(file));}
ExternalContext10::~ExternalContext10(){active=false;for(auto& file:files)file->Close();std::error_code error;std::filesystem::remove_all(root,error);}
LineRecord* ExternalContext10::acquire(std::string text){check(live<limit,"Live record buffer limit exceeded");++live;peak=std::max(peak,live);auto record=std::make_unique<ExternalRecord10>(*this,std::move(text));auto result=record.get();records.push_back(std::move(record));return result;}
ExternalFile10* ExternalContext10::owned(TextFile* file){for(auto& actual:files)if(actual.get()==file)return actual.get();return nullptr;}
struct ExternalWorkspace10:TextWorkspace {
ExternalContext10& owner;explicit ExternalWorkspace10(ExternalContext10& owner):owner(owner){}~ExternalWorkspace10()override=default;
TextFile* CreateFile()override{ExternalContext10::check(++owner.creates<=owner.fileLimit,"Temporary-file creation budget exceeded");auto path=owner.root/std::to_string(owner.creates);{std::ofstream initial(path,std::ios::binary);ExternalContext10::check(static_cast<bool>(initial),"Cannot create owned temporary file");}auto file=std::make_unique<ExternalFile10>(owner,path,false);auto result=file.get();owner.files.push_back(std::move(file));return result;}
void DeleteFile(TextFile& file)override{auto actual=owner.owned(&file);ExternalContext10::check(actual&&!actual->readOnly&&!actual->deleted,"Delete only a live workspace temporary file");actual->Close();std::filesystem::remove(actual->path);actual->deleted=true;}
};
std::vector<std::string> externalReadRaw10(const std::filesystem::path& path){std::ifstream input(path,std::ios::binary);std::vector<std::string> result;std::string text;while(std::getline(input,text))result.push_back(text);return result;}
json executeExternal10(const json& row){const auto& args=row["arguments"];auto lines=args[0].get<std::vector<std::string>>();ExternalContext10 context(lines,args[1].get<int>());ExternalWorkspace10 workspace(context);TextFile* result;context.active=true;try{result=Solution_10_6().SortExternalFile(*context.input,context.limit,workspace);}catch(...){context.active=false;throw;}context.active=false;auto output=context.owned(result);ExternalContext10::check(output&&!output->deleted,"Return a live input/workspace file, not an in-memory replacement");ExternalContext10::check(context.live==0,"Consume or release every record before returning");output->Close();context.input->Close();auto actual=externalReadRaw10(output->path);bool preserved=externalReadRaw10(context.input->path)==lines;return json{{"actual",actual},{"mutationOk",preserved},{"ownedResult",true},{"peakRecords",context.peak},{"liveRecords",context.live},{"reads",context.reads},{"writes",context.writes},{"createdFiles",context.creates},{"maxStreams",context.maxStreams}};}
'''
INSIDE=''
