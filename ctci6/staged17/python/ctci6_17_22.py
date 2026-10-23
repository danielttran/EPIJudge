def WordTransformation(start: str, stop: str, dictionary: list[str]) -> list[str]:
    words = set(dictionary)
    previous = {start: None}
    queue = [start]
    head = 0
    while head < len(queue):
        word = queue[head]
        head += 1
        if word == stop:
            path = []
            current = stop
            while current is not None:
                path.append(current)
                current = previous[current]
            path.reverse()
            return path
        for position in range(len(word)):
            for letter in "abcdefghijklmnopqrstuvwxyz":
                if letter == word[position]:
                    continue
                candidate = word[:position] + letter + word[position + 1 :]
                if candidate in words and candidate not in previous:
                    previous[candidate] = word
                    queue.append(candidate)
    return []
