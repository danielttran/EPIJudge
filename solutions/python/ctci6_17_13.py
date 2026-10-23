def ReSpace(text: str, dictionary: list[str]) -> list[str]:
    words = set(dictionary)
    maximum = max(map(len, words), default=0)
    cost = [0] * (len(text) + 1)
    previous = [0] * (len(text) + 1)
    for end in range(1, len(text) + 1):
        cost[end] = cost[end - 1] + 1
        previous[end] = end - 1
        for length in range(1, min(maximum, end) + 1):
            start = end - length
            if text[start:end] in words and cost[start] < cost[end]:
                cost[end] = cost[start]
                previous[end] = start
    result = []
    end = len(text)
    while end:
        result.append(text[previous[end] : end])
        end = previous[end]
    result.reverse()
    return result
