def CountCoinCombinations(amount: int) -> int:
    ways = [0] * (amount + 1)
    ways[0] = 1
    for coin in (1, 5, 10, 25):
        for value in range(coin, amount + 1):
            ways[value] += ways[value - coin]
    return ways[amount]
