import random

def compute_random_permutation(n):
    values = list(range(n))
    for i in range(n):
        selected = random.randrange(i, n)
        values[i], values[selected] = values[selected], values[i]
    return values
