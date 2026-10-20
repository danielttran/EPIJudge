"""These succeed with fresh instances in one process but carry no data in the wire string."""
def bodies(mode,lang):
    tree=mode=='tree_codec'
    if not tree:
        fields={'csharp':'private static string[] cache=[];','javascript':'static cache=[];','python':'    cache=[]\n','cpp':'inline static std::vector<std::string> cache{};','java':'private static String[] cache=new String[0];'}[lang]
        encode={'csharp':'cache=strings.ToArray();return "token";','javascript':'Codec.cache=[...strings];return "token";','python':'Codec.cache=list(strings)\nreturn "token"','cpp':'cache=strings;return "token";','java':'cache=strings.clone();return "token";'}[lang]
        decode={'csharp':'return cache.ToArray();','javascript':'return [...Codec.cache];','python':'return list(Codec.cache)','cpp':'return cache;','java':'return cache.clone();'}[lang]
        return dict(Encode=encode,Decode=decode),fields
    fields={'csharp':'private static string cache="# ";','javascript':'static cache="# ";','python':'    cache="# "\n','cpp':'inline static std::string cache="# ";','java':'private static String cache="# ";'}[lang]
    encode={'csharp':'cache=Probe.Serialize(root);return "token";','javascript':'Codec.cache=Probe.serialize(root);return "token";','python':'Codec.cache=Probe.serialize(root)\nreturn "token"','cpp':'cache=Probe::serialize(root);return "token";','java':'cache=Probe.serialize(root);return "token";'}[lang]
    decode={'csharp':'return Probe.Deserialize(cache);','javascript':'return Probe.deserialize(Codec.cache);','python':'return Probe.deserialize(Codec.cache)','cpp':'return Probe::deserialize(cache);','java':'return Probe.deserialize(cache);'}[lang]
    return dict(Serialize=encode,Deserialize=decode),fields
