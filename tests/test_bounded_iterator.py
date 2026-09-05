import threading
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

    def test_when_iter_called_then_it_returns_self(self) -> None:
        subject = BoundedIterator(2, count())

        result = iter(subject)

        self.assertIs(subject, result)

    def test_when_the_iterable_is_finite_then_it_yields_all_and_raises_stop_iteration(self) -> None:
        subject = BoundedIterator(10, [0, 1])

        results = [next(subject), next(subject)]

        self.assertEqual([0, 1], results)
        with self.assertRaises(StopIteration):
            next(subject)

    def test_when_bound_is_full_then_it_raises_timeout_before_exhaustion(self) -> None:
        subject = BoundedIterator(2, [0, 1])

        results = [next(subject), next(subject)]

        self.assertEqual([0, 1], results)
        with self.assertRaises(TimeoutError):
            subject.next(timeout=0.01)

    def test_when_processed_called_without_yield_then_it_raises_value_error(self) -> None:
        subject = BoundedIterator(1, count())

        with self.assertRaises(ValueError):
            subject.processed()

        self.assertEqual(0, next(subject))

    def test_when_values_are_acknowledged_repeatedly_then_it_yields_in_order(self) -> None:
        subject = BoundedIterator(2, count())

        results: list[int] = []
        for _ in range(5):
            results.append(next(subject))
            results.append(next(subject))

            subject.processed()
            subject.processed()

        self.assertEqual(list(range(10)), results)

    def test_when_bound_is_one_then_it_blocks_after_a_single_item(self) -> None:
        subject = BoundedIterator(1, count())

        first = next(subject)

        self.assertEqual(0, first)
        with self.assertRaises(TimeoutError):
            subject.next(timeout=0.01)

        subject.processed()

        self.assertEqual(1, next(subject))

    def test_when_next_called_with_timeout_and_slot_available_then_it_succeeds(self) -> None:
        subject = BoundedIterator(2, count())

        result = subject.next(timeout=10)

        self.assertEqual(0, result)

    def test_when_bound_is_zero_then_it_raises_assertion_error(self) -> None:
        with self.assertRaisesRegex(AssertionError, "0"):
            BoundedIterator(0, count())

    def test_when_bound_is_negative_then_it_raises_assertion_error(self) -> None:
        with self.assertRaisesRegex(AssertionError, "-1"):
            BoundedIterator(-1, count())

    def test_when_exhausted_repeatedly_then_it_always_raises_stop_iteration(self) -> None:
        subject = BoundedIterator(10, [99])

        first = next(subject)

        self.assertEqual(99, first)
        for _ in range(12):
            with self.assertRaises(StopIteration):
                subject.next(timeout=0.01)

    def test_when_consumer_blocks_then_processed_unblocks_it(self) -> None:
        subject = BoundedIterator(1, count())
        first = next(subject)
        self.assertEqual(0, first)

        results: list[int] = []
        consumer = threading.Thread(target=lambda: results.append(subject.next()))

        consumer.start()
        consumer.join(timeout=0.1)
        self.assertTrue(consumer.is_alive())

        subject.processed()
        consumer.join(timeout=5)

        self.assertFalse(consumer.is_alive())
        self.assertEqual([1], results)
