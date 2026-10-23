def HasDirectedRoute(nodeCount: int, edges: list[list[int]], start: int, target: int) -> bool:
    if start == target:
        return True
    adjacent = [[] for _ in range(nodeCount)]
    for source, destination in edges:
        adjacent[source].append(destination)
    visited = [False] * nodeCount
    visited[start] = True
    queue = [start]
    head = 0
    while head < len(queue):
        node = queue[head]
        head += 1
        for neighbor in adjacent[node]:
            if not visited[neighbor]:
                if neighbor == target:
                    return True
                visited[neighbor] = True
                queue.append(neighbor)
    return False
