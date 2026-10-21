"use strict";
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
class Solution {
    BfsGetPath(graph, start, end) {
        const previous = new Map([[start, null]]), queue = [start];
        for (let head = 0; head < queue.length; head++) {
            const node = queue[head]; if (node === end) break;
            for (const neighbor of graph[node]) if (!previous.has(neighbor)) { previous.set(neighbor, node); queue.push(neighbor); }
        }
        if (!previous.has(end)) return null;
        const route = []; for (let node = end; node !== null; node = previous.get(node)) route.push(node);
        route.reverse(); return route;
    }
}

module.exports = {LinkedListNode, BinaryTreeNode, GraphNode, Meeting, Rectangle, CakeType, FilePaths, InfinityException, RandomSource, Solution};
