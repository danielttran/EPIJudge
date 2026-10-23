def CountDigitTwos(n: int) -> int:
    total = 0
    place = 1
    while place <= n:
        high = n // (place * 10)
        digit = (n // place) % 10
        low = n % place
        total += high * place
        if digit == 2:
            total += low + 1
        elif digit > 2:
            total += place
        place *= 10
    return total
