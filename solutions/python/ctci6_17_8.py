def CircusTower(people: list[list[int]]) -> list[int]:
    if not people:
        return []
    order = sorted(range(len(people)), key=lambda i: (people[i][0], people[i][1], i))
    length = [1] * len(order)
    previous = [-1] * len(order)
    best = 0
    for i in range(len(order)):
        for j in range(i):
            a, b = people[order[j]], people[order[i]]
            if a[0] < b[0] and a[1] < b[1] and length[j] + 1 > length[i]:
                length[i] = length[j] + 1
                previous[i] = j
        if length[i] > length[best]:
            best = i
    result = []
    while best != -1:
        result.append(order[best])
        best = previous[best]
    result.reverse()
    return result
