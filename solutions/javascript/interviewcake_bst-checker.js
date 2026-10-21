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
    IsBinarySearchTree(root) {
        const pending = root === null ? [] : [[root, -Infinity, Infinity]];
        while (pending.length !== 0) {
            const [node, lower, upper] = pending.pop();
            if (node.Value <= lower || node.Value >= upper) return false;
            if (node.Left !== null) pending.push([node.Left, lower, node.Value]);
            if (node.Right !== null) pending.push([node.Right, node.Value, upper]);
        }
        return true;
    }
}

module.exports = {LinkedListNode, BinaryTreeNode, GraphNode, Meeting, Rectangle, CakeType, FilePaths, InfinityException, RandomSource, Solution};
