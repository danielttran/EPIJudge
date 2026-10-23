def EnglishInteger(value: int) -> str:
    if value == 0:
        return "Zero"
    small = [
        "Zero",
        "One",
        "Two",
        "Three",
        "Four",
        "Five",
        "Six",
        "Seven",
        "Eight",
        "Nine",
        "Ten",
        "Eleven",
        "Twelve",
        "Thirteen",
        "Fourteen",
        "Fifteen",
        "Sixteen",
        "Seventeen",
        "Eighteen",
        "Nineteen",
    ]
    tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
    scales = ["", "Thousand", "Million", "Billion"]
    magnitude = abs(value)
    groups = []
    scale = 0
    while magnitude:
        chunk = magnitude % 1000
        if chunk:
            words = []
            if chunk >= 100:
                words.extend([small[chunk // 100], "Hundred"])
                chunk %= 100
            if chunk >= 20:
                words.append(tens[chunk // 10])
                chunk %= 10
            if chunk:
                words.append(small[chunk])
            if scale:
                words.append(scales[scale])
            groups.append(" ".join(words))
        magnitude //= 1000
        scale += 1
    return ("Negative " if value < 0 else "") + " ".join(reversed(groups))
