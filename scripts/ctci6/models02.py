"""Bank-owned list model bindings, shared with existing collection conventions."""

from core import HEADERS, TYPES, declaration, starter_body

NODE_TYPES = {
    "csharp": "LinkedListNode?",
    "java": "LinkedListNode",
    "cpp": "LinkedListNode*",
    "python": "LinkedListNode | None",
}
MODELS = {
    "csharp": "public class LinkedListNode { public int Value; public LinkedListNode? Next; public LinkedListNode(int value, LinkedListNode? next = null) { Value = value; Next = next; } }\n",
    "java": "class LinkedListNode { public int Value; public LinkedListNode Next; public LinkedListNode(int value) { this(value, null); } public LinkedListNode(int value, LinkedListNode next) { Value=value; Next=next; } }\n",
    "cpp": "#include <unordered_set>\nstruct LinkedListNode { int Value; LinkedListNode* Next; explicit LinkedListNode(int value, LinkedListNode* next=nullptr):Value(value),Next(next){} };\n",
    "python": "class LinkedListNode:\n    def __init__(self, value: int, next: 'LinkedListNode | None' = None):\n        self.Value, self.Next = value, next\n",
    "javascript": "class LinkedListNode { constructor(value, next = null) { this.Value=value; this.Next=next; } }\n",
}


def declare(spec, language, body, class_name="Solution"):
    if language in TYPES:
        TYPES[language]["node"] = NODE_TYPES[language]
    return declaration(spec, language, body, class_name)


def header(language):
    return HEADERS[language] + MODELS[language]


def neutral(spec, language):
    if spec["result"] == "node":
        return (
            "return None"
            if language == "python"
            else "return nullptr;"
            if language == "cpp"
            else "return null;"
        )
    return starter_body(spec, language)
