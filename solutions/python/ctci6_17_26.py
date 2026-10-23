def SparseSimilarities(documentIds: list[int], documents: list[list[int]]) -> list[list[int]]:
    n = len(documentIds)
    postings = {}
    for index, document in enumerate(documents):
        for word in document:
            postings.setdefault(word, []).append(index)
    intersections = {}
    for posting in postings.values():
        for left in range(len(posting)):
            for right in range(left + 1, len(posting)):
                key = posting[left] * n + posting[right]
                intersections[key] = intersections.get(key, 0) + 1
    result = []
    for key, count in intersections.items():
        left, right = divmod(key, n)
        a, b = sorted((documentIds[left], documentIds[right]))
        result.append([a, b, count, len(documents[left]) + len(documents[right]) - count])
    result.sort()
    return result
