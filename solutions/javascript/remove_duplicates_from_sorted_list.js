function removeDuplicates(L) {
  for (let node = L; node; node = node.next)
    while (node.next && node.next.data === node.data)
      node.next = node.next.next;
  return L;
}

module.exports = { removeDuplicates };
