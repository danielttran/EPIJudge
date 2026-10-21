"""Bank-owned typed submission support. Every generated source is self-contained."""

TYPE = {
    "csharp": {
        "i": "int",
        "l": "long",
        "b": "bool",
        "s": "string",
        "ai": "int[]",
        "as": "string[]?",
        "tree": "BinaryTreeNode?",
        "list": "LinkedListNode?",
        "node": "LinkedListNode",
        "void": "void",
        "chars": "char[]",
        "graph": "GraphNode[]",
        "map": "Dictionary<string, string[]>",
        "meetings": "List<Meeting>",
        "rect": "Rectangle",
        "cakes": "CakeType[]",
        "files": "string",
        "pairs": "IList<FilePaths>",
        "set": "ISet<string>",
    },
    "cpp": {
        "i": "int",
        "l": "long long",
        "b": "bool",
        "s": "string",
        "ai": "vector<int>",
        "as": "vector<string>",
        "tree": "BinaryTreeNode*",
        "list": "LinkedListNode*",
        "node": "LinkedListNode*",
        "void": "void",
        "chars": "vector<char>",
        "graph": "vector<GraphNode*>",
        "map": "unordered_map<string, vector<string>>",
        "meetings": "vector<Meeting*>",
        "rect": "Rectangle*",
        "cakes": "vector<CakeType*>",
        "files": "string",
        "pairs": "vector<FilePaths>",
        "set": "set<string>",
    },
    "java": {
        "i": "int",
        "l": "long",
        "b": "boolean",
        "s": "String",
        "ai": "int[]",
        "as": "String[]",
        "tree": "BinaryTreeNode",
        "list": "LinkedListNode",
        "node": "LinkedListNode",
        "void": "void",
        "chars": "char[]",
        "graph": "GraphNode[]",
        "map": "Map<String, String[]>",
        "meetings": "List<Meeting>",
        "rect": "Rectangle",
        "cakes": "CakeType[]",
        "files": "String",
        "pairs": "List<FilePaths>",
        "set": "Set<String>",
    },
    "python": {
        "i": "int",
        "l": "int",
        "b": "bool",
        "s": "str",
        "ai": "list[int]",
        "as": "list[str] | None",
        "tree": "BinaryTreeNode | None",
        "list": "LinkedListNode | None",
        "node": "LinkedListNode",
        "void": "None",
        "chars": "list[str]",
        "graph": "list[GraphNode]",
        "map": "dict[str, list[str]]",
        "meetings": "list[Meeting]",
        "rect": "Rectangle",
        "cakes": "list[CakeType]",
        "files": "str",
        "pairs": "list[FilePaths]",
        "set": "set[str]",
    },
    "javascript": {
        "i": "number",
        "l": "number",
        "b": "boolean",
        "s": "string",
        "ai": "number[]",
        "as": "string[] | null",
        "tree": "BinaryTreeNode | null",
        "list": "LinkedListNode | null",
        "node": "LinkedListNode",
        "void": "void",
        "chars": "string[]",
        "graph": "GraphNode[]",
        "map": "Object<string, string[]>",
        "meetings": "Meeting[]",
        "rect": "Rectangle",
        "cakes": "CakeType[]",
        "files": "string",
        "pairs": "FilePaths[]",
        "set": "Set<string>",
    },
}
HEADER = {
    "csharp": """using System;
using System.Collections.Generic;
using System.Linq;
using System.IO;
using System.Text;
// Bank-supplied data types and injected randomness. No problem logic is hidden here.
public class LinkedListNode { public int Value; public LinkedListNode? Next; public LinkedListNode(int value, LinkedListNode? next=null) { Value=value; Next=next; } }
public class BinaryTreeNode { public int Value; public BinaryTreeNode? Left, Right; public BinaryTreeNode(int value) { Value=value; } }
public class GraphNode { public string Label; public HashSet<GraphNode> Neighbors=new(); public string? Color; public GraphNode(string label) { Label=label; } }
public class Meeting { public int StartTime, EndTime; public Meeting(int start,int end) { StartTime=start; EndTime=end; } }
public class Rectangle { public int LeftX, BottomY, Width, Height; public Rectangle(int x=0,int y=0,int width=0,int height=0) { LeftX=x; BottomY=y; Width=width; Height=height; } }
public class CakeType { public int Weight; public long Value; public CakeType(int weight,long value) { Weight=weight; Value=value; } }
public record FilePaths(string OriginalPath,string DuplicatePath);
public class InfinityException : Exception { public InfinityException():base("Unbounded optimum") {} }
public static class RandomSource {
    public static Func<int,int,int> Draw = (lower,upper) => throw new InvalidOperationException("Random source must be injected by the judge.");
    public static int GetRandom(int lower,int upper) => Draw(lower,upper);
    public static int Rand5() => GetRandom(1,5);
    public static int Rand7() => GetRandom(1,7);
}
""",
    "cpp": """#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <deque>
#include <filesystem>
#include <fstream>
#include <functional>
#include <limits>
#include <map>
#include <optional>
#include <queue>
#include <set>
#include <sstream>
#include <stack>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>
using namespace std;
// Bank-supplied data types and injected randomness; no hidden algorithm helpers.
struct LinkedListNode { int Value; LinkedListNode* Next; LinkedListNode(int value,LinkedListNode* next=nullptr):Value(value),Next(next){} };
struct BinaryTreeNode { int Value; BinaryTreeNode *Left=nullptr,*Right=nullptr; explicit BinaryTreeNode(int value):Value(value){} };
struct GraphNode { string Label; unordered_set<GraphNode*> Neighbors; string Color; explicit GraphNode(string label):Label(move(label)){} };
struct Meeting { int StartTime,EndTime; Meeting(int start,int end):StartTime(start),EndTime(end){} };
struct Rectangle { int LeftX,BottomY,Width,Height; Rectangle(int x=0,int y=0,int width=0,int height=0):LeftX(x),BottomY(y),Width(width),Height(height){} };
struct CakeType { int Weight; long long Value; CakeType(int weight,long long value):Weight(weight),Value(value){} };
struct FilePaths { string OriginalPath,DuplicatePath; };
struct InfinityException:runtime_error { InfinityException():runtime_error("Unbounded optimum"){} };
struct RandomSource {
    inline static function<int(int,int)> Draw=[](int,int)->int{throw runtime_error("Random source must be injected by judge");};
    static int GetRandom(int lower,int upper){return Draw(lower,upper);}
    static int Rand5(){return GetRandom(1,5);} static int Rand7(){return GetRandom(1,7);}
};
""",
    "java": """import java.util.*;
import java.io.*;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.util.function.IntBinaryOperator;
// Bank-supplied data types and injected randomness; no hidden algorithm helpers.
class LinkedListNode { public int Value; public LinkedListNode Next; LinkedListNode(int value){Value=value;} LinkedListNode(int value,LinkedListNode next){Value=value;Next=next;} }
class BinaryTreeNode { public int Value; public BinaryTreeNode Left,Right; BinaryTreeNode(int value){Value=value;} }
class GraphNode { public String Label,Color; public Set<GraphNode> Neighbors=new HashSet<>(); GraphNode(String label){Label=label;} }
class Meeting { public int StartTime,EndTime; Meeting(int start,int end){StartTime=start;EndTime=end;} }
class Rectangle { public int LeftX,BottomY,Width,Height; Rectangle(){this(0,0,0,0);} Rectangle(int x,int y,int width,int height){LeftX=x;BottomY=y;Width=width;Height=height;} }
class CakeType { public int Weight; public long Value; CakeType(int weight,long value){Weight=weight;Value=value;} }
class FilePaths { public String OriginalPath,DuplicatePath; FilePaths(String original,String duplicate){OriginalPath=original;DuplicatePath=duplicate;} }
class InfinityException extends RuntimeException { InfinityException(){super("Unbounded optimum");} }
class RandomSource { public static IntBinaryOperator Draw=(lower,upper)->{throw new IllegalStateException("Random source must be injected by judge");}; public static int GetRandom(int lower,int upper){return Draw.applyAsInt(lower,upper);} public static int Rand5(){return GetRandom(1,5);} public static int Rand7(){return GetRandom(1,7);} }
""",
    "python": """from __future__ import annotations
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

# Bank-supplied data types and injected randomness; no hidden algorithm helpers.
class LinkedListNode:
    def __init__(self, value: int, next: LinkedListNode | None = None):
        self.Value, self.Next = value, next
class BinaryTreeNode:
    def __init__(self, value: int):
        self.Value, self.Left, self.Right = value, None, None
class GraphNode:
    def __init__(self, label: str):
        self.Label, self.Color, self.Neighbors = label, None, set()
@dataclass
class Meeting:
    StartTime: int
    EndTime: int
@dataclass
class Rectangle:
    LeftX: int = 0
    BottomY: int = 0
    Width: int = 0
    Height: int = 0
@dataclass
class CakeType:
    Weight: int
    Value: int
@dataclass
class FilePaths:
    OriginalPath: str
    DuplicatePath: str
class InfinityException(Exception):
    pass
class RandomSource:
    @staticmethod
    def Draw(lower: int, upper: int) -> int:
        raise RuntimeError("Random source must be injected by judge")
    @staticmethod
    def GetRandom(lower: int, upper: int) -> int:
        return RandomSource.Draw(lower, upper)
    @staticmethod
    def Rand5() -> int:
        return RandomSource.GetRandom(1, 5)
    @staticmethod
    def Rand7() -> int:
        return RandomSource.GetRandom(1, 7)

""",
    "javascript": """"use strict";
const fs = require("node:fs");
const path = require("node:path");
// Bank-supplied data types and injected randomness; no hidden algorithm helpers.
class LinkedListNode { constructor(value, next = null) { this.Value = value; this.Next = next; } }
class BinaryTreeNode { constructor(value) { this.Value=value; this.Left=null; this.Right=null; } }
class GraphNode { constructor(label) { this.Label=label; this.Color=null; this.Neighbors=new Set(); } }
class Meeting { constructor(start,end) { this.StartTime=start; this.EndTime=end; } }
class Rectangle { constructor(x=0,y=0,width=0,height=0) { this.LeftX=x; this.BottomY=y; this.Width=width; this.Height=height; } }
class CakeType { constructor(weight,value) { this.Weight=weight; this.Value=value; } }
class FilePaths { constructor(original,duplicate) { this.OriginalPath=original; this.DuplicatePath=duplicate; } }
class InfinityException extends Error {}
class RandomSource {
    static Draw(lower,upper) { throw new Error("Random source must be injected by judge"); }
    static GetRandom(lower,upper) { return this.Draw(lower,upper); }
    static Rand5() { return this.GetRandom(1,5); }
    static Rand7() { return this.GetRandom(1,7); }
}
""",
}
STATE = {
    "queue": [("Enqueue", [("item", "i")], "void"), ("Dequeue", [], "i")],
    "stack": [("Push", [("item", "i")], "void"), ("Pop", [], "i"), ("GetMax", [], "i")],
    "temperature": [
        ("Insert", [("temperature", "i")], "void"),
        ("GetMin", [], "nullable_i"),
        ("GetMax", [], "nullable_i"),
        ("GetMean", [], "nullable_d"),
        ("GetMode", [], "nullable_i"),
    ],
    "wordcloud": [],
}
for lang, t in TYPE.items():
    t["nullable_i"] = {
        "csharp": "int?",
        "cpp": "optional<int>",
        "java": "Integer",
        "python": "int | None",
        "javascript": "number | null",
    }[lang]
    t["nullable_d"] = {
        "csharp": "double?",
        "cpp": "optional<double>",
        "java": "Double",
        "python": "float | None",
        "javascript": "number | null",
    }[lang]
