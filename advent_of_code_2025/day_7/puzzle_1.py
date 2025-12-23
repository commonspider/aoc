import math

import numpy as np

from advent_of_code_2025.utils import Stream, get_input_lines


lines = get_input_lines()
beam = [0] * len(lines[0])
beam[lines[0].index("S")] = 1

def solve(line: str):
    global beam
    new_beam = [0] * len(line)
    for i, (l, b) in enumerate(zip(line, beam)):
        if l == "." and b > 0:
            new_beam[i] += b
        elif l == "^" and b > 0:
            new_beam[i - 1] += b
            new_beam[i + 1] += b
    beam = new_beam
    return beam

Stream(lines[1:]).map(solve)[-1].sum().print()
