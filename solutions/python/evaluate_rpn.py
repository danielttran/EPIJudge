def evaluate(expression):
    stack = []
    for raw in expression.split(','):
        token = raw.strip()
        if token not in ('+', '-', '*', '/'):
            stack.append(int(token))
            continue
        right, left = stack.pop(), stack.pop()
        if token == '+':
            value = left + right
        elif token == '-':
            value = left - right
        elif token == '*':
            value = left * right
        else:
            value = abs(left) // abs(right)
            if (left < 0) != (right < 0):
                value = -value
        stack.append(value)
    return stack[-1]
