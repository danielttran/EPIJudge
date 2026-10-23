def MultiSearch(text: str, patterns: list[str]) -> list[list[int]]:
    result = []
    for pattern in patterns:
        positions = []
        for start in range(len(text) - len(pattern) + 1):
            if text.startswith(pattern, start):
                positions.append(start)
        result.append(positions)
    return result
