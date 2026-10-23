def Calculate(expression: str) -> float:
    total = 0.0
    term = 0.0
    operator = "+"
    index = 0
    while index < len(expression):
        number = 0
        while index < len(expression) and "0" <= expression[index] <= "9":
            number = number * 10 + ord(expression[index]) - ord("0")
            index += 1
        if operator == "+":
            total += term
            term = float(number)
        elif operator == "-":
            total += term
            term = -float(number)
        elif operator == "*":
            term *= number
        else:
            term /= number
        if index < len(expression):
            operator = expression[index]
            index += 1
    return total + term
