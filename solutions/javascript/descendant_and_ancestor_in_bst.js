function pairIncludesAncestorAndDescendantOfM(
  tree,
  possible_anc_or_desc_0,
  possible_anc_or_desc_1,
  middle_idx,
) {
  function find(node, value) {
    while (node && node.data !== value)
      node = value < node.data ? node.left : node.right;
    return node;
  }
  if (
    possible_anc_or_desc_0 === middle_idx ||
    possible_anc_or_desc_1 === middle_idx ||
    possible_anc_or_desc_0 === possible_anc_or_desc_1
  )
    return false;
  const first = find(tree, possible_anc_or_desc_0),
    second = find(tree, possible_anc_or_desc_1),
    middle = find(tree, middle_idx);
  if (!first || !second || !middle) return false;
  return Boolean(
    (find(first, middle_idx) && find(middle, possible_anc_or_desc_1)) ||
      (find(second, middle_idx) && find(middle, possible_anc_or_desc_0)),
  );
}

module.exports = { pairIncludesAncestorAndDescendantOfM };
