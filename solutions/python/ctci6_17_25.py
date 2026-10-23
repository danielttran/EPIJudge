def LargestWordRectangle(words: list[str]) -> list[str]:
    groups = {}
    seen = set()
    maximum = 0
    for word in words:
        if word not in seen:
            seen.add(word)
            groups.setdefault(len(word), []).append(word)
            maximum = max(maximum, len(word))
    for area in range(maximum * maximum, 0, -1):
        for height in range(1, maximum + 1):
            if area % height:
                continue
            width = area // height
            if width not in groups or height not in groups:
                continue
            prefixes = {word[:length] for word in groups[height] for length in range(1, height + 1)}
            rows = []

            def search():
                if len(rows) == height:
                    return True
                for word in groups[width]:
                    rows.append(word)
                    if (
                        all(
                            "".join(row[column] for row in rows) in prefixes
                            for column in range(width)
                        )
                        and search()
                    ):
                        return True
                    rows.pop()
                return False

            if search():
                return rows
    return []
