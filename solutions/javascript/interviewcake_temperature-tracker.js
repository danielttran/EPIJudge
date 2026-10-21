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
class TempTracker {
    constructor() {
        this.count = 0; this.total = 0; this.minimum = null; this.maximum = null;
        this.counts = Array(111).fill(0); this.mode = null; this.modeCount = 0;
    }
    Insert(temperature) {
        this.count++; this.total += temperature;
        this.minimum = this.minimum === null ? temperature : Math.min(this.minimum, temperature);
        this.maximum = this.maximum === null ? temperature : Math.max(this.maximum, temperature);
        this.counts[temperature]++;
        if (this.counts[temperature] > this.modeCount) { this.mode = temperature; this.modeCount = this.counts[temperature]; }
    }
    GetMin() { return this.minimum; }
    GetMax() { return this.maximum; }
    GetMean() { return this.count === 0 ? null : this.total / this.count; }
    GetMode() { return this.mode; }
}

module.exports = {LinkedListNode, BinaryTreeNode, GraphNode, Meeting, Rectangle, CakeType, FilePaths, InfinityException, RandomSource, TempTracker};
