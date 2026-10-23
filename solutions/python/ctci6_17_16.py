def MaximumMassageMinutes(appointments: list[int]) -> int:
    one_back = two_back = 0
    for duration in appointments:
        current = max(one_back, duration + two_back)
        two_back = one_back
        one_back = current
    return one_back
