import itertools
import string
from collections.abc import Iterable, Callable
from typing import Any, Literal

import numpy as np
from scipy import signal


class Item[T]:
    def __init__(self, value: T, trace=()):
        self._value = value
        self._trace = trace

    def count(self, value):
        return Item(self._value.count(value))

    def print(self):
        value = self._value
        trace = self._trace
        print(self._value)

    def __add__(self, other):
        if isinstance(other, Item):
            return Item(self._value + other._value)
        else:
            raise TypeError

    def __sub__(self, other):
        if isinstance(other, Item):
            return Item(self._value - other._value)
        else:
            raise TypeError

    def __eq__(self, other):
        if isinstance(other, Item):
            return self._value == other._value
        else:
            raise TypeError

    def sum(self):
        return Item(sum(self._value))


class Stream[T](Iterable[T]):
    @classmethod
    def digits(cls):
        return Stream(string.digits)

    @classmethod
    def from_input_lines(cls):
        with open("input") as f:
            lines = f.readlines()
        return Stream(lines)

    def __init__(self, iterable: Iterable[T]):
        self._value = list(iterable)

    def __iter__(self):
        return iter(self._value)

    def map[R](self, function: Callable[[T], R]):
        return Stream(map(function, self._value))

    def enumerated_map[R](self, function: Callable[[int, T], R]):
        return Stream(map(lambda arg: function(arg[0], arg[1]), enumerate(self._value)))

    def sum(self):
        return Item(sum(self._value))

    def reverse(self):
        stream: Stream[T] = Stream(reversed(self._value))
        return stream

    def to_list(self):
        return list(self._value)

    def split(self, delimiter: T, limit=-1):
        streams = []
        current = self._value
        while len(current) > 0:
            if 0 <= limit <= len(streams):
                streams.append(Stream(current))
                break
            else:
                try:
                    index = current.index(delimiter)
                except ValueError:
                    streams.append(Stream(current))
                    break
                else:
                    streams.append(Stream(current[:index]))
                    current = current[index+1:]
        return streams

    def filter(self, function: Callable[[T], bool]):
        return Stream(item for item in self._value if function(item))

    def count(self):
        return Item(len(self._value))

    def foreach(self, function: Callable[[T], Any]):
        for item in self._value:
            function(item)

    def to_matrix(self):
        return Matrix(self._value)

    def __getitem__(self, item):
        if isinstance(item, int):
            return Item(self._value[item])
        else:
            raise TypeError


def get_input_lines():
    with open("input") as f:
        return [line[:-1] for line in f.readlines()]


def stream_input_lines():
    return Stream(get_input_lines())


class Matrix:
    @classmethod
    def from_input(cls, fill: str = " "):
        with open("input") as f:
            lines = f.readlines()
        lines = list(map(list, lines))
        length = max(*map(len, lines))
        for line in lines:
            line.extend([fill] * (length - len(line)))
        return Matrix(lines)

    def __init__(self, matrix, trace=()):
        self.matrix = np.array(matrix)
        self._trace = (*trace, self.matrix)

    def translate(self, dictionary: dict):
        return self.map(dictionary.get)

    def convolve(self, mask, mode: Literal["full", "same", "valid"] = "same"):
        matrix = signal.convolve2d(self.matrix, mask, mode=mode)
        return Matrix(matrix, self._trace)

    def sum(self):
        return Item(self.matrix.sum(), self._trace)

    def breakpoint(self):
        history = self._trace
        return self

    def map(self, func):
        matrix = np.vectorize(func)(self.matrix)
        return Matrix(matrix, self._trace)

    def enumerated_map(self, func):
        flattened = [
            func(*index, value)
            for index, value in np.ndenumerate(self.matrix)
        ]
        matrix = np.reshape(flattened, self.matrix.shape)
        return Matrix(matrix, self._trace)

    def __getitem__(self, item):
        return self.matrix[item]

    def __mul__(self, other):
        if isinstance(other, Matrix):
            return Matrix(self.matrix * other.matrix)
        else:
            raise TypeError

    def transpose(self):
        return Matrix(np.transpose(self.matrix), self._trace)

    def to_stream(self):
        return Stream(self.matrix.tolist())

    def split_horizontal(self, value: Any = " "):
        is_value: np.ndarray = self.matrix == value
        row_sum = is_value.sum(axis=1)
        delimiters = np.argwhere(row_sum == self.matrix.shape[1]).flatten().tolist()
        parts = [self.matrix[:delimiters[0]]] + [
            self.matrix[a+1:b]
            for a, b in itertools.pairwise(delimiters)
        ] + [self.matrix[delimiters[-1]+1:]]
        return Stream(parts).map(Matrix)

    def split_vertical(self, value: Any = " "):
        return self.transpose().split_horizontal(value).map(lambda x: x.transpose())

    def to_list(self) -> list[list]:
        return self.matrix.tolist()
