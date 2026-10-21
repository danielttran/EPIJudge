class AddingCredits {
  constructor() {
    this.credits = new Map();
    this.root = null;
    this.offset = 0n;
  }
  compare(credit, id, node) {
    if (credit !== node.credit) return credit < node.credit ? -1 : 1;
    return id === node.id ? 0 : id < node.id ? -1 : 1;
  }
  merge(left, right) {
    if (!left) return right;
    if (!right) return left;
    if (left.priority < right.priority) {
      left.right = this.merge(left.right, right);
      return left;
    }
    right.left = this.merge(left, right.left);
    return right;
  }
  add(root, node) {
    if (!root) return node;
    if (this.compare(node.credit, node.id, root) < 0) {
      root.left = this.add(root.left, node);
      if (root.left.priority < root.priority) {
        const top = root.left;
        root.left = top.right;
        top.right = root;
        return top;
      }
    } else {
      root.right = this.add(root.right, node);
      if (root.right.priority < root.priority) {
        const top = root.right;
        root.right = top.left;
        top.left = root;
        return top;
      }
    }
    return root;
  }
  delete(root, credit, id) {
    if (!root) return null;
    const order = this.compare(credit, id, root);
    if (order < 0) root.left = this.delete(root.left, credit, id);
    else if (order > 0) root.right = this.delete(root.right, credit, id);
    else return this.merge(root.left, root.right);
    return root;
  }
  insert(clientId, credit) {
    this.remove(clientId);
    const normalized = BigInt(credit) - this.offset;
    this.credits.set(clientId, normalized);
    this.root = this.add(this.root, {
      credit: normalized,
      id: clientId,
      priority: Math.random(),
      left: null,
      right: null,
    });
  }
  remove(clientId) {
    if (!this.credits.has(clientId)) return false;
    this.root = this.delete(this.root, this.credits.get(clientId), clientId);
    this.credits.delete(clientId);
    return true;
  }
  lookup(clientId) {
    return this.credits.has(clientId)
      ? Number(this.credits.get(clientId) + this.offset)
      : -1;
  }
  addAll(amount) {
    this.offset += BigInt(amount);
  }
  max() {
    let node = this.root;
    if (!node) return "";
    while (node.right) node = node.right;
    return node.id;
  }
}
module.exports = { AddingCredits };
