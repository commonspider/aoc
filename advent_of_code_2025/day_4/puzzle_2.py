from advent_of_code_2025.utils import Matrix

matrix = Matrix.from_input().translate({
    "@": 1,
    ".": 0
})

starting_rolls = matrix.sum()


def remove(y, x, value):
    if value == 0:
        return 0
    neigh = matrix[max(0, y - 1):y + 2, max(0, x - 1):x + 2]
    return 1 - int(neigh.sum() <= 4)


old_rolls = starting_rolls
while True:
    matrix = matrix.enumerated_map(remove)
    new_rolls = matrix.sum()
    if new_rolls == old_rolls:
        (starting_rolls - new_rolls).print()
        break
    old_rolls = new_rolls
