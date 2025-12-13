from advent_of_code_2025.utils import Matrix

matrix_input = Matrix.from_input().translate({
    "@": 1,
    ".": 0
})


def solve(y, x, value):
    if value == 0:
        return 0
    neigh = matrix_input[max(0, y - 1):y + 2, max(0, x - 1):x + 2]
    return int(neigh.sum() <= 4)


matrix_input.enumerated_map(solve).sum().print()
