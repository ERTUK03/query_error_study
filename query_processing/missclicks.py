from math import hypot, exp
import random

QWERTY = [
    "1234567890",
    "qwertyuiop",
    "asdfghjkl",
    "zxcvbnm",
]

OFFSETS = [0.0, 0.0, 0.5, 1.0]

KEY_POS = {}
for row_idx, row in enumerate(QWERTY):
    for col_idx, key in enumerate(row):
        KEY_POS[key] = (col_idx + OFFSETS[row_idx], row_idx)


def random_nearby_key(char, sigma=1.0, max_distance=2.5):
    char = char.lower()

    if char not in KEY_POS:
        return char

    x0, y0 = KEY_POS[char]

    keys = []
    weights = []

    for key, (x, y) in KEY_POS.items():
        if key == char:
            continue

        d = hypot(x - x0, y - y0)

        if d <= max_distance:
            keys.append(key)
            weights.append(exp(-(d ** 2) / (2 * sigma ** 2)))

    return random.choices(keys, weights=weights, k=1)[0]

def missclicks(example, ratio):
    to_change = round(len(example["query"])*ratio)

    query = example["query"]
    for i in range(to_change):
        index = random.randint(0, len(query)-1)
        query = query[:index] + random_nearby_key(query[index]) + query[index + 1:]
    example["query"]=query
    return example