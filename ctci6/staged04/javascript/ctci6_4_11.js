'use strict';
class RandomNode {constructor(data){this.Data=data;this.Left=null;this.Right=null;}}
class RandomSource {static Draw=(lower,upper)=>{throw new Error("Provided by the judge");};static GetRandom(lower,upper){return RandomSource.Draw(lower,upper);}}
class RandomBst {
  static SizedNode = class extends RandomNode {
    constructor(value) {
      super(value);
      this.Size = 1;
    }
  };
  constructor() {
    this.Root = null;
  }
  Insert(value) {
    const added = new RandomBst.SizedNode(value);
    if (this.Root === null) {
      this.Root = added;
      return;
    }
    const path = [];
    let node = this.Root;
    while (true) {
      path.push(node);
      if (value <= node.Data) {
        if (node.Left === null) {
          node.Left = added;
          break;
        }
        node = node.Left;
      } else {
        if (node.Right === null) {
          node.Right = added;
          break;
        }
        node = node.Right;
      }
    }
    for (const ancestor of path) ++ancestor.Size;
  }
  Find(value) {
    let node = this.Root;
    while (node !== null) {
      if (value === node.Data) return node;
      node = value < node.Data ? node.Left : node.Right;
    }
    return null;
  }
  Delete(value) {
    const path = [];
    let node = this.Root;
    while (node !== null && node.Data !== value) {
      path.push(node);
      node = value < node.Data ? node.Left : node.Right;
    }
    if (node === null) return false;
    if (node.Left !== null && node.Right !== null) {
      path.push(node);
      let successor = node.Right;
      while (successor.Left !== null) {
        path.push(successor);
        successor = successor.Left;
      }
      node.Data = successor.Data;
      node = successor;
    }
    const replacement = node.Left !== null ? node.Left : node.Right;
    if (path.length === 0) this.Root = replacement;
    else {
      const parent = path[path.length - 1];
      if (parent.Left === node) parent.Left = replacement;
      else parent.Right = replacement;
    }
    for (const ancestor of path) --ancestor.Size;
    return true;
  }
  GetRandomNode() {
    if (this.Root === null) return null;
    let rank = RandomSource.GetRandom(0, this.Root.Size - 1),
      node = this.Root;
    while (node !== null) {
      const leftSize = node.Left === null ? 0 : node.Left.Size;
      if (rank < leftSize) node = node.Left;
      else if (rank === leftSize) return node;
      else {
        rank -= leftSize + 1;
        node = node.Right;
      }
    }
    return null;
  }
}
