def LastKLines(filePath: str, k: int) -> list[str]:
    from collections import deque

    suffix = deque(maxlen=k)
    with open(filePath, "r", encoding="ascii", newline="") as source:
        for line in source:
            suffix.append(line[:-1])
    return list(suffix)
