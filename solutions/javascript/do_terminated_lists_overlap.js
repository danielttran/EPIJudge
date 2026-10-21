function overlappingLists(first, second) {
  function length(node) {
    let count = 0;
    while (node) {
      count++;
      node = node.next;
    }
    return count;
  }
  let difference = length(first) - length(second);
  while (difference > 0) {
    first = first.next;
    difference--;
  }
  while (difference < 0) {
    second = second.next;
    difference++;
  }
  while (first !== second) {
    first = first.next;
    second = second.next;
  }
  return first;
}

module.exports = { overlappingLists };
