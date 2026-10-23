def BuildOrder(projectCount: int, dependencies: list[list[int]]) -> list[int]:
    adjacent = [[] for _ in range(projectCount)]
    indegree = [0] * projectCount
    for before, after in dependencies:
        adjacent[before].append(after)
        indegree[after] += 1
    order = [i for i in range(projectCount) if indegree[i] == 0]
    head = 0
    while head < len(order):
        project = order[head]
        head += 1
        for dependent in adjacent[project]:
            indegree[dependent] -= 1
            if indegree[dependent] == 0:
                order.append(dependent)
    return order if len(order) == projectCount else []
