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
    ReverseWords(message) {
        function reverse(left, right) {
            while (left < right) { [message[left], message[right]] = [message[right], message[left]]; left++; right--; }
        }
        reverse(0, message.length - 1); let start = 0;
        for (let end = 0; end <= message.length; end++) if (end === message.length || message[end] === ' ') {
            reverse(start, end - 1); start = end + 1;
        }
    }
}

module.exports = {LinkedListNode, BinaryTreeNode, GraphNode, Meeting, Rectangle, CakeType, FilePaths, InfinityException, RandomSource, Solution};
