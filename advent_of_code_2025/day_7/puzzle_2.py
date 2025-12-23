import math

from advent_of_code_2025.utils import Stream, Matrix


def solve(i, problem: Matrix):
    lines = problem.to_list()
    sign = lines[0].pop()
    if sign not in ("+", "*"):
        raise ValueError
    numbers = Stream(lines).map(lambda l: "".join(l).strip()).map(lambda l: int(l) if len(l) > 0 else 0).to_list()
    if sign == "+":
        return sum(numbers)
    elif sign == "*":
        return math.prod(numbers)

(
    Matrix.from_input()
        .split_vertical()
        .map(lambda x: x.transpose())
        .enumerated_map(solve)
        .sum()
        .print()
)
