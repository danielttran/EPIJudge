def GroupAnagrams(words: list[str]) -> list[str]:
    words.sort(key=lambda word: "".join(sorted(word)))
    return words.copy()
