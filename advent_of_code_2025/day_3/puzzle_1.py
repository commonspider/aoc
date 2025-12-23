from contextlib import suppress

from advent_of_code_2025.utils import stream_input_lines, Stream

digits = Stream.digits().reverse().to_list()

def get_largest_joltage(line: str) -> int:
    a = -1
    b = -1
    for a in digits:
        with suppress(ValueError):
            i_a = line[:-2].index(a)
            break
    for b in digits:
        with suppress(ValueError):
            line[i_a + 1:].index(b)
            break
    return int(a + b)

stream_input_lines().map(get_largest_joltage).sum().print()
