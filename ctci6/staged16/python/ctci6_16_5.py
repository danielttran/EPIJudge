def CountFactorialZeros(n: int) -> int:
    count = 0
    while n:
        n //= 5
        count += n
    return count
