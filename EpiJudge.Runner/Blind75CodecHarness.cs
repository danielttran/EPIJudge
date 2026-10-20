namespace EpiJudge.Runner;

// A new object alone still shares static/module memory. A fresh decoding process
// proves that the encoded string carries the data, while the encoder checks its
// input structure before that process exits.
internal static class Blind75CodecHarness
{
    internal static string Isolate(string source, string mode, string language)
    {
        var tree = mode == "tree_codec";
        var encode = tree ? "Serialize" : "Encode";
        var decode = tree ? "Deserialize" : "Decode";
        var lowerEncode = char.ToLowerInvariant(encode[0]) + encode[1..];
        var lowerDecode = char.ToLowerInvariant(decode[0]) + decode[1..];
        switch (language)
        {
            case "csharp":
                source = source.Replace("var args=Kinds.Select", $$"""
                    var codecPhase=File.ReadAllText("codec-phase.txt");
                    if(codecPhase=="decode")return Dump(Call(New("Codec"),"{{decode}}",raw[0].GetString()),Output);
                    var args=Kinds.Select
                    """);
                return source.Replace("object? actual;", $$"""
                    if(codecPhase=="encode")
                    {
                        var encoded=Call(New("Codec"),"{{encode}}",args[0]);
                        Check(encoded is string,"Encode must return a string.");
                        if(Mode=="tree_codec")
                        {
                            Check(JsonSerializer.Serialize(Dump(args[0],Kinds[0]),Json)==before,"Preserve the original tree.");
                            Check(original.All(n=>Val(n)==snapshot[n]&&Links(n).SequenceEqual(originalLinks[n],ReferenceEqualityComparer.Instance)),"Preserve original nodes and links.");
                        }
                        return encoded;
                    }
                    object? actual;
                    """);
            case "java":
                source = source.Replace("Object[] args=new Object[KINDS.length];", $$"""
                    String codecPhase=Files.readString(Path.of("codec-phase.txt"),StandardCharsets.UTF_8);
                    if(codecPhase.equals("decode"))return dump(call(fresh("Codec"),"{{lowerDecode}}",raw.get(0).asString()),OUTPUT);
                    Object[] args=new Object[KINDS.length];
                    """);
                return source.Replace("Object actual;", $$"""
                    if(codecPhase.equals("encode")){
                      Object encoded=call(fresh("Codec"),"{{lowerEncode}}",args[0]);check(encoded instanceof String,"Encode must return a string.");
                      if(MODE.equals("tree_codec")){
                        check(dump(args[0],KINDS[0]).toString().equals(before),"Preserve the original tree.");
                        for(Object n:original){check(val(n)==snapshot.get(n),"Preserve values.");List<Object>now=links(n),old=originalLinks.get(n);check(now.size()==old.size(),"Preserve links.");for(int i=0;i<now.size();i++)check(now.get(i)==old.get(i),"Preserve links.");}
                      }return dump(encoded,"");
                    }
                    Object actual;
                    """);
            case "javascript":
                source = source.Replace("function execute(raw) {", $$"""
                    function execute(raw) {
                      const codecPhase=fs.readFileSync('codec-phase.txt','utf8');
                      if(codecPhase==='decode')return dump(new user.Codec().{{lowerDecode}}(raw[0]),OUTPUT);
                    """);
                return source.Replace("let actual;", $$"""
                    if(codecPhase==='encode'){
                      const encoded=new user.Codec().{{lowerEncode}}(args[0]);check(typeof encoded==='string','Encode must return a string.');
                      if(MODE==='tree_codec'){
                        check(JSON.stringify(dump(args[0],KINDS[0]))===before,'Preserve the original tree.');
                        check(original.every(n=>n.val===snapshot.get(n)&&[n.left,n.right].every((v,i)=>v===originalLinks.get(n)[i])),'Preserve original nodes and links.');
                      }return encoded;
                    }
                    let actual;
                    """);
            case "python":
                var pyEncode = tree ? "serialize" : "encode";
                var pyDecode = tree ? "deserialize" : "decode";
                source = source.Replace("def execute(raw):\n", $$"""
                    def execute(raw):
                        with open('codec-phase.txt',encoding='utf-8') as phase_file: codec_phase=phase_file.read()
                        if codec_phase=='decode': return dump(user.Codec().{{pyDecode}}(raw[0]),OUTPUT)
                    """ + "\n");
                return source.Replace("    if mode=='list_cycle':", $$"""
                        if codec_phase=='encode':
                            encoded=user.Codec().{{pyEncode}}(args[0])
                            check(isinstance(encoded,str),'Encode must return a string.')
                            if mode=='tree_codec':
                                check(dump(args[0],KINDS[0])==before,'Preserve the original tree.')
                                check(all(n.val==snapshot[id(n)] and all(x is y for x,y in zip((n.left,n.right),original_links[id(n)])) for n in original),'Preserve original nodes and links.')
                            return encoded
                        if mode=='list_cycle':
                    """);
            default:
                source = source.Replace("json execute(const json& raw){", $$"""
                    json execute(const json& raw){
                    std::ifstream phaseInput("codec-phase.txt");std::string codecPhase;phaseInput>>codecPhase;
                    if(codecPhase=="decode")return dump(Codec().{{decode}}(raw[0].get<std::string>()));
                    """);
                var target = tree ? "auto actual=Codec().Deserialize(Codec().Serialize(a0));" : "auto actual=Codec().Decode(Codec().Encode(a0));";
                var preservation = tree ? "check(dump(a0)==before,\"Preserve the original tree.\");for(auto n:original)check(n->val==snapshot.at(n)&&std::make_pair(n->left,n->right)==originalLinks.at(n),\"Preserve original nodes and links.\");" : "";
                return source.Replace(target, $$"""
                    if(codecPhase=="encode"){auto encoded=Codec().{{encode}}(a0);{{preservation}}return json(encoded);}
                    {{target}}
                    """);
        }
    }
}
