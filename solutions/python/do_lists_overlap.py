def overlapping_lists(first, second):
    reachable = set()
    while first is not None and id(first) not in reachable:
        reachable.add(id(first))
        first = first.next
    visited = set()
    while second is not None and id(second) not in visited:
        if id(second) in reachable:
            return second
        visited.add(id(second))
        second = second.next
    return None


from test_framework.test_failure import TestFailure as _OverlapFailure
from test_framework.test_utils import enable_executor_hook as _overlap_executor_hook


@_overlap_executor_hook
def overlapping_lists_wrapper(executor, first, second, common, cycle0, cycle1):
    """Construct both cycles from acyclic snapshots, then validate node identity."""
    def nodes(head):
        result = []
        seen = set()
        while head is not None and id(head) not in seen:
            seen.add(id(head))
            result.append(head)
            head = head.next
        return result

    first_prefix, second_prefix = nodes(first), nodes(second)
    if first_prefix:
        first_prefix[-1].next = common
    else:
        first = common
    if second_prefix:
        second_prefix[-1].next = common
    else:
        second = common

    # Shared tails may become cyclic after either assignment. Never traverse
    # that modified topology while finding the other original tail.
    first_nodes, second_nodes = nodes(first), nodes(second)
    for chain, position in ((first_nodes, cycle0), (second_nodes, cycle1)):
        if position != -1:
            if not 0 <= position < len(chain):
                raise ValueError('Cycle position is outside the original chain.')
            chain[-1].next = chain[position]

    shared_ids = {id(node) for node in nodes(first)} & {id(node) for node in nodes(second)}
    result = executor.run(lambda: overlapping_lists(first, second))
    if (result is None and not shared_ids) or id(result) in shared_ids:
        return
    raise _OverlapFailure('Return an original node reachable from both heads, or None when disjoint.')
