function hasCycle(head) {
  let slow = head,
    fast = head;
  while (fast && fast.next) {
    slow = slow.next;
    fast = fast.next.next;
    if (slow !== fast) continue;
    let entry = head;
    while (entry !== slow) {
      entry = entry.next;
      slow = slow.next;
    }
    return entry;
  }
  return null;
}

module.exports = { hasCycle };
