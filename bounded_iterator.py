from __future__ import annotations

from collections.abc import Iterable, Iterator
from operator import length_hint
from threading import BoundedSemaphore
from typing import TypeVar

from typing_extensions import Self

__all__ = ["BoundedIterator"]

T = TypeVar("T")


class BoundedIterator(Iterator[T]):
    """Limits the number of values to yield until yielded values are
    acknowledged.
    """

    def __init__(self, bound: int, it: Iterable[T]) -> None:
        assert bound > 0, f"bound must be positive, got {bound}."

        self._it = iter(it)

        self._sem = BoundedSemaphore(bound)

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> T:
        return self.next()

    def __length_hint__(self) -> int:
        return length_hint(self._it)

    def next(self, timeout: float | None = None) -> T:
        """Returns the next value from the iterable.

        This method is not thread-safe.

        :raises TimeoutError: if timeout is given and no value is acknowledged in the mean time.
        """
        if not self._sem.acquire(timeout=timeout):
            raise TimeoutError("Too many values un-acknowledged.")

        try:
            return next(self._it)
        except BaseException:
            self._sem.release()
            raise

    def processed(self) -> None:
        """Acknowledges one value allowing another one to be yielded.

        This method is thread-safe.
        """
        self._sem.release()
