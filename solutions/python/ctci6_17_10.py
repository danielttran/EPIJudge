def MajorityElement(values: list[int]) -> list[int]:
    candidate = 0
    balance = 0
    for value in values:
        if balance == 0:
            candidate = value
        balance += 1 if value == candidate else -1
    count = sum(value == candidate for value in values)
    return [candidate] if count > len(values) // 2 else []
