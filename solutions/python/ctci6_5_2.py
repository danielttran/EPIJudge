def BinaryFraction(number: float) -> str:
    if not 0 < number < 1:
        return "ERROR"
    digits = []
    for _ in range(31):
        number *= 2
        bit = number >= 1
        digits.append("1" if bit else "0")
        if bit:
            number -= 1
        if number == 0:
            return "." + "".join(digits)
    return "ERROR"
