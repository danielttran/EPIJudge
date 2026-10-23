def KthMultiple357(k: int) -> int:
    values = [1]
    third = fifth = seventh = 0
    for _ in range(k):
        next_three = values[third] * 3
        next_five = values[fifth] * 5
        next_seven = values[seventh] * 7
        value = min(next_three, next_five, next_seven)
        values.append(value)
        if value == next_three:
            third += 1
        if value == next_five:
            fifth += 1
        if value == next_seven:
            seventh += 1
    return values[k]
