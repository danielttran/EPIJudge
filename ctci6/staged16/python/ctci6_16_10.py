def MostPopulatedYear(people: list[list[int]]) -> int:
    changes = [0] * 102
    for birth, death in people:
        changes[birth - 1900] += 1
        changes[death - 1900 + 1] -= 1
    alive = 0
    best = 0
    answer = 1900
    for offset in range(101):
        alive += changes[offset]
        if alive > best:
            best = alive
            answer = 1900 + offset
    return answer
