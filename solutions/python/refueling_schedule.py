def find_ample_city(gallons, distances):
    start = 0
    remaining_miles = 0
    for city in range(len(gallons)):
        remaining_miles += 20 * gallons[city] - distances[city]
        if remaining_miles < 0:
            start = city + 1
            remaining_miles = 0
    return start % len(gallons)
