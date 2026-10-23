def ScoreMasterMind(guess: str, secret: str) -> list[int]:
    remaining = [0] * 4
    hits = 0
    for index in range(4):
        if guess[index] == secret[index]:
            hits += 1
        else:
            remaining["RGBY".index(secret[index])] += 1
    pseudo_hits = 0
    for index in range(4):
        if guess[index] == secret[index]:
            continue
        color = "RGBY".index(guess[index])
        if remaining[color]:
            remaining[color] -= 1
            pseudo_hits += 1
    return [hits, pseudo_hits]
