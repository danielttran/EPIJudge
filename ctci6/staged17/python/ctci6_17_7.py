def TrueNameFrequencies(
    names: list[str], frequencies: list[int], synonyms: list[list[int]]
) -> list[list[int]]:
    adjacent = [[] for _ in names]
    for first, second in synonyms:
        adjacent[first].append(second)
        adjacent[second].append(first)
    visited = [False] * len(names)
    result = []
    for start in range(len(names)):
        if visited[start]:
            continue
        visited[start] = True
        queue = [start]
        total = 0
        for name in queue:
            total += frequencies[name]
            for other in adjacent[name]:
                if not visited[other]:
                    visited[other] = True
                    queue.append(other)
        result.append([start, total])
    return result
