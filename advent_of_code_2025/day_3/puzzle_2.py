from contextlib import suppress

from advent_of_code_2025.utils import iterate_input_lines, Stream

digits = Stream.digits().reverse().collect()

def get_largest_joltage(line: str, n: int = 12) -> str:
    if n == 0:
        return ""
    for value in digits:
        with suppress(ValueError):
            index = line[:-n].index(value)
            break
    else:
        raise ValueError
    return value + get_largest_joltage(line[index + 1:], n - 1)

iterate_input_lines().map(get_largest_joltage).map(int).sum().print()
