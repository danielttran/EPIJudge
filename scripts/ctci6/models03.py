"""Required error/model APIs; no stack-sorting or shelter logic is supplied."""

from core import HEADERS, TYPES, declaration
from chapter03 import APIS

ERROR = {
    "csharp": "public sealed class BankError : Exception { public string Code { get; } public BankError(string code) : base(code) { Code=code; } }\n",
    "java": "class BankError extends RuntimeException { public final String Code; public BankError(String code) { super(code); Code=code; } }\n",
    "cpp": "struct BankError : std::runtime_error { std::string Code; explicit BankError(std::string code):std::runtime_error(code),Code(std::move(code)){} };\n",
    "python": "class BankError(Exception):\n    def __init__(self, code: str):\n        super().__init__(code)\n        self.Code = code\n",
    "javascript": "class BankError extends Error { constructor(code) { super(code); this.Code=code; } }\n",
}

STACK = {
    "csharp": """public sealed class IntStack {
private readonly Stack<int> values = new();
public void Push(int value) { values.Push(value); }
public int Pop() { if (values.Count==0) throw new BankError("empty"); return values.Pop(); }
public int Peek() { if (values.Count==0) throw new BankError("empty"); return values.Peek(); }
public bool IsEmpty() { return values.Count==0; }
}
""",
    "java": """class IntStack {
private final ArrayDeque<Integer> values = new ArrayDeque<>();
public void Push(int value) { values.push(value); }
public int Pop() { if (values.isEmpty()) throw new BankError("empty"); return values.pop(); }
public int Peek() { if (values.isEmpty()) throw new BankError("empty"); return values.peek(); }
public boolean IsEmpty() { return values.isEmpty(); }
}
""",
    "cpp": """class IntStack {
std::vector<int> values;
public:
void Push(int value) { values.push_back(value); }
int Pop() { if(values.empty()) throw BankError("empty"); int value=values.back(); values.pop_back(); return value; }
int Peek() { if(values.empty()) throw BankError("empty"); return values.back(); }
bool IsEmpty() { return values.empty(); }
};
""",
    "python": """class IntStack:
    def __init__(self):
        self._values = []
    def Push(self, value: int):
        self._values.append(value)
    def Pop(self) -> int:
        if not self._values:
            raise BankError('empty')
        return self._values.pop()
    def Peek(self) -> int:
        if not self._values:
            raise BankError('empty')
        return self._values[-1]
    def IsEmpty(self) -> bool:
        return not self._values
""",
    "javascript": """class IntStack {
    constructor() { this._values=[]; }
    Push(value) { this._values.push(value); }
    Pop() { if(!this._values.length) throw new BankError('empty'); return this._values.pop(); }
    Peek() { if(!this._values.length) throw new BankError('empty'); return this._values.at(-1); }
    IsEmpty() { return this._values.length===0; }
}
""",
}

ANIMAL = {
    "csharp": "public sealed class Animal { public int Id { get; } public string Species { get; } public Animal(int id,string species) { Id=id; Species=species; } }\n",
    "java": "final class Animal { public final int Id; public final String Species; public Animal(int id,String species) { Id=id; Species=species; } }\n",
    "cpp": "struct Animal { const int Id; const std::string Species; Animal(int id,std::string species):Id(id),Species(std::move(species)){} };\n",
    "python": """class Animal:
    def __init__(self, id: int, species: str):
        self._id, self._species = id, species
    @property
    def Id(self) -> int:
        return self._id
    @property
    def Species(self) -> str:
        return self._species
""",
    "javascript": "class Animal { constructor(id,species) { this.Id=id; this.Species=species; Object.freeze(this); } }\n",
}


def header(ref, language):
    prefix = HEADERS[language]
    if language == "cpp":
        prefix += "#include <memory>\n#include <stdexcept>\n#include <utility>\n"
    return (
        prefix
        + ERROR[language]
        + (
            STACK[language]
            if ref == "3.5"
            else ANIMAL[language]
            if ref == "3.6"
            else ""
        )
    )


def type_name(kind, language, result=False):
    if kind == "animal":
        return {
            "csharp": "Animal?" if result else "Animal",
            "java": "Animal",
            "cpp": "Animal*",
            "python": "Animal | None" if result else "Animal",
            "javascript": "Animal",
        }[language]
    return TYPES[language][kind] if language != "javascript" else kind


def method_header(name, params, result, language):
    if language == "python":
        return (
            "def "
            + name
            + "("
            + ", ".join(
                ["self"] + [n + ": " + type_name(t, language) for n, t in params]
            )
            + ") -> "
            + type_name(result, language, True)
            + ":"
        )
    if language == "javascript":
        return name + "(" + ", ".join(n for n, _ in params) + ")"
    return (
        ("public " if language in ("csharp", "java") else "")
        + type_name(result, language, True)
        + " "
        + name
        + "("
        + ", ".join(type_name(t, language) + " " + n for n, t in params)
        + ")"
    )


def declare(spec, language, code, class_name="Solution"):
    if spec["ref"] == "3.5":
        if language in TYPES:
            TYPES[language]["stack"] = {
                "csharp": "IntStack",
                "java": "IntStack",
                "cpp": "IntStack&",
                "python": "IntStack",
            }[language]
        return declaration(spec, language, code, class_name)
    cls, params, methods = APIS[spec["ref"]]
    constructor = (
        cls
        + "("
        + ", ".join(
            n + ": " + t
            if language == "python"
            else n
            if language == "javascript"
            else type_name(t, language) + " " + n
            for n, t in params
        )
        + ")"
    )
    return "; ".join(
        [constructor]
        + [
            method_header(n, p, r, language).removeprefix("public ")
            for n, p, r in methods
        ]
    ), code


def neutral(spec, language):
    if spec["ref"] == "3.5":
        return "pass" if language == "python" else "// Write your solution here."
    cls, params, methods = APIS[spec["ref"]]
    bodies = []
    for name, arguments, result in methods:
        value = (
            "None"
            if language == "python" and result == "animal"
            else "False"
            if language == "python" and result == "b"
            else "nullptr"
            if language == "cpp" and result == "animal"
            else "null"
            if result == "animal"
            else "false"
            if result == "b"
            else "0"
        )
        content = (
            "pass"
            if language == "python" and result == "void"
            else "// Write your solution here."
            if result == "void"
            else "return " + value + ("" if language == "python" else ";")
        )
        signature = method_header(name, arguments, result, language)
        bodies.append(
            signature + "\n    " + content
            if language == "python"
            else signature + " { " + content + "\n}"
        )
    if language == "python":
        constructor = (
            "def __init__(self"
            + (", " + ", ".join(n for n, _ in params) if params else "")
            + "):\n    pass"
        )
        return (
            "class "
            + cls
            + ":\n"
            + "\n".join(
                "    " + line
                for line in (constructor + "\n" + "\n".join(bodies)).splitlines()
            )
            + "\n"
        )
    if language == "javascript":
        constructor = "constructor(" + ", ".join(n for n, _ in params) + ") {}"
        return (
            "class " + cls + " {\n" + constructor + "\n" + "\n".join(bodies) + "\n}\n"
        )
    constructor = (
        ("public " if language in ("csharp", "java") else "")
        + cls
        + "("
        + ", ".join(type_name(t, language) + " " + n for n, t in params)
        + ") {}"
    )
    return (
        ("public class " if language == "csharp" else "class ")
        + cls
        + " {\n"
        + ("public:\n" if language == "cpp" else "")
        + constructor
        + "\n"
        + "\n".join(bodies)
        + ("\n};\n" if language == "cpp" else "\n}\n")
    )
