from collections import deque

def is_any_placement_feasible(graph):
    adjacency = {id(vertex): [] for vertex in graph}
    for vertex in graph:
        for other in vertex.edges:
            adjacency[id(vertex)].append(id(other))
            adjacency[id(other)].append(id(vertex))
    colors = {}
    for vertex in graph:
        start = id(vertex)
        if start in colors:
            continue
        colors[start] = 0
        queue = deque([start])
        while queue:
            current = queue.popleft()
            for other in adjacency[current]:
                if other in colors:
                    if colors[other] == colors[current]:
                        return False
                else:
                    colors[other] = 1 - colors[current]
                    queue.append(other)
    return True
