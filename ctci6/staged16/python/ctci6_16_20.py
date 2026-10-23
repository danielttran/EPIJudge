def T9Words(digits: str, dictionary: list[str]) -> list[str]:
    mapping = "22233344455566677778889999"
    result = []
    for word in dictionary:
        if len(word) == len(digits) and all(
            mapping[ord(letter) - ord("a")] == digit for letter, digit in zip(word, digits)
        ):
            result.append(word)
    return result
