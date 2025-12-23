import math

import numpy as np

from advent_of_code_2025.utils import Stream, get_input_lines


lines = get_input_lines()
beam = list(lines[0])
count = 1

def solve(line: str):
    global beam, count
    new_beam = ["."] * len(line)
    for i, (l, b) in enumerate(zip(line, beam)):
        if l == "." and b == "S":
            new_beam[i] = "S"
        elif l == "^" and b == "S":
            count += 1
            new_beam[i] = "^"
            new_beam[i - 1] = "S"
            new_beam[i + 1] = "S"
    print("".join(new_beam))
    beam = new_beam
    return beam

Stream(lines[1:]).map(solve)
print(count)
