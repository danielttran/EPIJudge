def WordFrequencies(book: list[str], queries: list[str]) -> list[int]:
    counts = {}
    for word in book:
        key = word.lower()
        counts[key] = counts.get(key, 0) + 1
    return [counts.get(word.lower(), 0) for word in queries]
