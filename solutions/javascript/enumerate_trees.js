function generateAllBinaryTrees(num_nodes) {
  const memo = new Map();
  function generate(count) {
    if (memo.has(count)) return memo.get(count);
    const shapes = [];
    if (!count) shapes.push(null);
    else
      for (let left = 0; left < count; left++)
        for (const first of generate(left))
          for (const second of generate(count - 1 - left))
            shapes.push({ left: first, right: second });
    memo.set(count, shapes);
    return shapes;
  }
  const result = [];
  for (const shape of generate(num_nodes)) {
    const encoding = [],
      queue = [shape];
    for (let head = 0; head < queue.length; head++) {
      const node = queue[head];
      encoding.push(node ? 1 : 0);
      if (node) queue.push(node.left, node.right);
    }
    result.push(encoding);
  }
  return result;
}

module.exports = { generateAllBinaryTrees };
