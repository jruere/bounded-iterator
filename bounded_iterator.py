from threading import BoundedSemaphore
from typing import Iterable, Iterator, TypeVar

T = TypeVar("T")


class BoundedIterator(Iterator):
    """Limits the number of values to yield until yielded values are
    acknowledged.
    """

    def __init__(self, bound, it: Iterable[T]):
        self._it = iter(it)

        self._sem = BoundedSemaphore(bound)

    def __iter__(self) -> Iterator[T]:
        return self

    def __next__(self) -> T:
        return self.next()

    def next(self, timeout=None) -> T:
        """Returns the next value from the iterable.

        This method is not thread-safe.

        :raises TimeoutError: if timeout is given and no value is acknowledged in the mean time.
        """
        if not self._sem.acquire(timeout=timeout):
            raise TimeoutError("Too many values un-acknowledged.")

        return next(self._it)

    def processed(self):
        """Acknowledges one value allowing another one to be yielded.

        This method is thread-safe.
        """
        self._sem.release()
