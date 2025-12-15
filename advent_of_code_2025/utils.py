import string
from collections.abc import Iterable, Callable
from typing import Any

import numpy as np
from scipy import signal


class Item[T]:
    def __init__(self, value: T, trace=()):
        self._value = value
        self._trace = trace

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


class Stream[T](Iterable[T]):
    @classmethod
    def digits(cls):
        return Stream(string.digits)

    @classmethod
    def from_input_lines(cls):
        with open("input") as f:
            lines = f.readlines()
        return Stream([line[:-1] for line in lines])

    def __init__(self, iterable: Iterable[T]):
        self._value = list(iterable)

    def __iter__(self):
        return iter(self._value)

    def map[R](self, function: Callable[[T], R]):
        return Stream(map(function, self._value))

    def sum(self):
        return Item(sum(self._value))

    def reverse(self):
        stream: Stream[T] = Stream(reversed(self._value))
        return stream

    def collect(self):
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


def iterate_input_lines():
    with open("input") as f:
        lines = f.readlines()
    return Stream(lines)


class Matrix:
    @classmethod
    def from_input(cls):
        with open("input") as f:
            lines = f.readlines()
        return Matrix(list(map(lambda line: list(line[:-1]), lines)))

    def __init__(self, matrix, trace=()):
        self.matrix = np.array(matrix)
        self._trace = (*trace, self.matrix)

    def translate(self, dictionary: dict):
        return self.map(dictionary.get)

    def convolve(self, mask, mode="same"):
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
