function lca(tree, node0, node1) {
  if (!tree) throw new RangeError("Targets must exist");
  const parents = new Map([[tree, null]]),
    pending = [tree];
  let first = null,
    second = null;
  while (pending.length && (!first || !second)) {
    const node = pending.pop();
    if (node.data === node0) first = node;
    if (node.data === node1) second = node;
    for (const child of [node.left, node.right])
      if (child) {
        parents.set(child, node);
        pending.push(child);
      }
  }
  if (!first || !second) throw new RangeError("Targets must exist");
  const ancestors = new Set();
  for (let node = first; node; node = parents.get(node)) ancestors.add(node);
  for (let node = second; node; node = parents.get(node))
    if (ancestors.has(node)) return node.data;
  throw new Error("Missing common ancestor");
}

module.exports = { lca };
