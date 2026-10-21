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
