import unittest
from itertools import count

from bounded_iterator import BoundedIterator


class BoundedIteratorTest(unittest.TestCase):
    def test_when_the_iterable_is_empty_then_it_produces_no_results(self) -> None:
        subject: BoundedIterator[int] = BoundedIterator(10, it=())

        results = list(subject)

        self.assertEqual([], results)

    def test_when_the_max_number_of_items_were_yielded_then_it_will_not_yield_more(self) -> None:
        subject = BoundedIterator(2, count())

        chunk0 = next(subject), next(subject)

        self.assertEqual((0, 1), chunk0)

        with self.assertRaises(TimeoutError):
            subject.next(timeout=0.01)

    def test_when_a_value_is_acknowledged_then_it_will_yield_one_more(self) -> None:
        subject = BoundedIterator(2, count())

        chunk0 = next(subject), next(subject)
        self.assertEqual((0, 1), chunk0)
        with self.assertRaises(TimeoutError):
            subject.next(timeout=0.01)

        subject.processed()
        self.assertEqual(2, next(subject))
