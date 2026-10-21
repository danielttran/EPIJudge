from collections import deque

def transform_string(dictionary, source, target):
    if source == target:
        return 0
    remaining = set(dictionary)
    remaining.discard(source)
    queue = deque([(source, 0)])
    while queue:
        word, distance = queue.popleft()
        for i in range(len(word)):
            for character in 'abcdefghijklmnopqrstuvwxyz':
                if character == word[i]:
                    continue
                candidate = word[:i] + character + word[i + 1:]
                if candidate not in remaining:
                    continue
                remaining.remove(candidate)
                if candidate == target:
                    return distance + 1
                queue.append((candidate, distance + 1))
    return -1
