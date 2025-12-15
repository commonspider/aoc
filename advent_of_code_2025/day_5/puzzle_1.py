from advent_of_code_2025.utils import Stream

stream_ranges, stream_ids = Stream.from_input_lines().split("")

stream_ranges = stream_ranges.map(lambda x: x.split("-")).map(lambda x: (int(x[0]), int(x[1])))

def is_fresh(ingredient_id):
    for s, e in stream_ranges:
        if s <= ingredient_id <= e:
            return True
    return False

stream_ids.map(int).filter(is_fresh).count().print()
