def CountBooleanParenthesizations(expression: str, desired: bool) -> int:
    if not expression:
        return 0
    count = (len(expression) + 1) // 2
    truth = [[0] * count for _ in range(count)]
    falsity = [[0] * count for _ in range(count)]
    for index in range(count):
        truth[index][index] = 1 if expression[2 * index] == "1" else 0
        falsity[index][index] = 1 - truth[index][index]
    for length in range(2, count + 1):
        for low in range(count - length + 1):
            high = low + length - 1
            for split in range(low, high):
                lt, lf = truth[low][split], falsity[low][split]
                rt, rf = truth[split + 1][high], falsity[split + 1][high]
                total = (lt + lf) * (rt + rf)
                operation = expression[2 * split + 1]
                true_count = (
                    lt * rt
                    if operation == "&"
                    else total - lf * rf
                    if operation == "|"
                    else lt * rf + lf * rt
                )
                truth[low][high] += true_count
                falsity[low][high] += total - true_count
    return truth[0][count - 1] if desired else falsity[0][count - 1]
