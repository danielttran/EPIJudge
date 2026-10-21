import json

from banktypes import HEADER, STATE, TYPE
from specs import ROOT, S

EXT = {"csharp": "cs", "javascript": "js", "python": "py", "cpp": "cpp", "java": "java"}


def method(lang, name, params, result):
    t = TYPE[lang]
    if lang == "csharp":
        return (
            "public "
            + t[result]
            + " "
            + name
            + "("
            + ", ".join(t[k] + " " + n for n, k in params)
            + ")"
        )
    if lang == "java":
        return (
            "public "
            + t[result]
            + " "
            + name
            + "("
            + ", ".join(t[k] + " " + n for n, k in params)
            + ")"
        )
    if lang == "cpp":
        args = []
        for n, k in params:
            ty = t[k]
            if k in ("ai", "as", "graph", "chars", "map", "meetings", "cakes"):
                ty += "&"
            elif k in ("s", "files"):
                ty = "const " + ty + "&"
            args.append(ty + " " + n)
        return t[result] + " " + name + "(" + ", ".join(args) + ")"
    if lang == "python":
        return (
            "def "
            + name
            + "(self"
            + (
                ""
                if not params
                else ", " + ", ".join(n + ": " + t[k] for n, k in params)
            )
            + ") -> "
            + t[result]
            + ":"
        )
    return name + "(" + ", ".join(n for n, k in params) + ")"


def interfaces(spec, lang):
    mode = spec["mode"]
    cls = spec["className"]
    methods = STATE.get(
        mode,
        [
            (
                spec["method"],
                [(p["name"], p["type"]) for p in spec["params"]],
                spec["result"],
            )
        ],
    )
    if mode == "wordcloud":
        return {
            "signature": {
                "csharp": "public WordCloudData(string input); public IDictionary<string,int> WordsToCounts { get; }",
                "java": "WordCloudData(String input); public Map<String,Integer> WordsToCounts;",
                "cpp": "WordCloudData(const string& input); unordered_map<string,int> WordsToCounts;",
                "python": "WordCloudData(input: str); WordsToCounts: dict[str,int]",
                "javascript": "new WordCloudData(input); WordsToCounts: Object<string,number>",
            }[lang],
            "starter": {
                "csharp": "public class WordCloudData { public IDictionary<string,int> WordsToCounts { get; } = new Dictionary<string,int>(); public WordCloudData(string input) { throw new NotImplementedException(); } }",
                "java": 'class WordCloudData { public Map<String,Integer> WordsToCounts=new HashMap<>(); WordCloudData(String input) { throw new UnsupportedOperationException("Implement the constructor"); } }',
                "cpp": 'class WordCloudData { public: unordered_map<string,int> WordsToCounts; explicit WordCloudData(const string& input) { throw logic_error("Implement constructor"); } };',
                "python": 'class WordCloudData:\n    def __init__(self, input: str):\n        self.WordsToCounts: dict[str,int] = {}\n        raise NotImplementedError("Implement the constructor")\n',
                "javascript": 'class WordCloudData { constructor(input) { this.WordsToCounts={}; throw new Error("Implement the constructor"); } }',
            }[lang],
        }
    signatures = [method(lang, *m) for m in methods]
    if lang in ("csharp", "java", "cpp"):
        throw = {
            "csharp": "throw new NotImplementedException();",
            "java": 'throw new UnsupportedOperationException("Implement this method");',
            "cpp": 'throw logic_error("Implement this method");',
        }[lang]
        starter = (
            ("public class " if lang == "csharp" else "class ")
            + cls
            + " {\n"
            + ("public:\n" if lang == "cpp" else "")
            + "\n".join("    " + x + " { " + throw + " }" for x in signatures)
            + "\n}"
            + (";" if lang == "cpp" else "")
            + "\n"
        )
    elif lang == "python":
        starter = (
            "class "
            + cls
            + ":\n"
            + "\n".join(
                "    "
                + x
                + '\n        raise NotImplementedError("Implement this method")\n'
                for x in signatures
            )
        )
    else:
        starter = (
            "class "
            + cls
            + " {\n"
            + "\n".join(
                "    " + x + ' { throw new Error("Implement this method"); }'
                for x in signatures
            )
            + "\n}\n"
        )
    return {"signature": "; ".join(signatures), "starter": starter}


def full_source(spec, lang, body):
    out = HEADER[lang] + body
    if lang == "javascript":
        out += (
            "\nmodule.exports = {"
            + ", ".join(
                [
                    "LinkedListNode",
                    "BinaryTreeNode",
                    "GraphNode",
                    "Meeting",
                    "Rectangle",
                    "CakeType",
                    "FilePaths",
                    "InfinityException",
                    "RandomSource",
                    spec["className"],
                ]
            )
            + "};\n"
        )
    return out


if __name__ == "__main__":
    data = []
    for s in S:
        d = dict(s)
        d["interfaces"] = {l: interfaces(s, l) for l in EXT}
        data.append(d)
    (ROOT / "scripts/interviewcake/interfaces.json").write_text(
        json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    for lang in EXT:
        (ROOT / "scripts/interviewcake" / ("header_" + lang + ".txt")).write_text(
            HEADER[lang].rstrip() + "\n", encoding="utf-8", newline="\n"
        )
