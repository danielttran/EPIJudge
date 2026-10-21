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
    FindDuplicateFiles(startingDirectory) {
        const directories = [path.resolve(startingDirectory)], groups = new Map(), result = [];
        while (directories.length !== 0) {
            const directory = directories.pop();
            for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
                const fullPath = path.join(directory, entry.name);
                if (entry.isDirectory()) { directories.push(fullPath); continue; }
                const info = fs.statSync(fullPath), parts = [String(info.size)];
                const offsets = [0, Math.floor(Math.max(0, info.size - 64) / 2), Math.max(0, info.size - 64)];
                const handle = fs.openSync(fullPath, 'r');
                try {
                    for (const offset of offsets) {
                        const buffer = Buffer.alloc(Math.min(64, info.size - offset));
                        if (buffer.length !== 0) fs.readSync(handle, buffer, 0, buffer.length, offset);
                        parts.push(buffer.toString('hex'));
                    }
                } finally { fs.closeSync(handle); }
                const fingerprint = String(info.size);
                const previous = groups.get(fingerprint);
                if (previous === undefined) groups.set(fingerprint, { fullPath, modified: info.mtimeMs });
                else if (previous.modified <= info.mtimeMs) result.push(new FilePaths(previous.fullPath, fullPath));
                else result.push(new FilePaths(fullPath, previous.fullPath));
            }
        }
        return result;
    }
}

module.exports = {LinkedListNode, BinaryTreeNode, GraphNode, Meeting, Rectangle, CakeType, FilePaths, InfinityException, RandomSource, Solution};
