from collections import deque
def LastKLines(filePath: str, k: int) -> list[str]:
    suffix = deque(maxlen=k)
    with open(filePath, "r", encoding="ascii", newline="") as source:
        for line in source:
            suffix.append(line[:-1])
    return list(suffix)
