def decompose_into_dictionary_words(domain, dictionary):
    previous = [-1] * (len(domain) + 1)
    previous[0] = 0
    for end in range(1, len(domain) + 1):
        for start in range(end):
            if previous[start] >= 0 and domain[start:end] in dictionary:
                previous[end] = start
                break
    if previous[-1] < 0:
        return []
    result = []
    end = len(domain)
    while end:
        result.append(domain[previous[end]:end])
        end = previous[end]
    result.reverse()
    return result
