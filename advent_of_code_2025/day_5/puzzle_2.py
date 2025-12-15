from advent_of_code_2025.utils import Stream

stream_ranges, _ = Stream.from_input_lines().split("")
stream_ranges: Stream = stream_ranges.map(lambda x: x.split("-")).map(lambda x: (int(x[0]), int(x[1])))


class Range:
    @classmethod
    def merge(cls, ranges):
        return Range(min(r._start for r in ranges), max(r._end for r in ranges))

    def __init__(self, start, end):
        self._start = start
        self._end = end

    def overlaps(self, start, end):
        return end >= self._start and self._end >= start

    def __len__(self):
        return self._end - self._start + 1


parsed_ranges = []


def insert_range(_range):
    overlaps = [r for r in parsed_ranges if r.overlaps(*_range)]
    if len(overlaps) > 0:
        for r in overlaps:
            parsed_ranges.remove(r)
        overlaps.append(Range(*_range))
        merged = Range.merge(overlaps)
        parsed_ranges.append(merged)
    else:
        parsed_ranges.append(Range(*_range))


stream_ranges.foreach(insert_range)

n_fresh = sum(map(len, parsed_ranges))
print(n_fresh)
