import random
import unittest

from engine_core import roll_dice


class FixedRng:
    def __init__(self, values):
        self._values = list(values)
        self._idx = 0

    def randint(self, _start, _end):
        value = self._values[self._idx]
        self._idx += 1
        return value


class RollDiceTests(unittest.TestCase):
    def test_injected_rng_is_deterministic(self):
        rng = FixedRng([2, 5])
        result = roll_dice(rng)
        self.assertEqual(result.die1, 5)
        self.assertEqual(result.die2, 2)
        self.assertEqual(result.total, 7)
        self.assertFalse(result.is_hard)

    def test_seeded_random_is_repeatable(self):
        seeded_a = random.Random(42)
        seeded_b = random.Random(42)
        first = roll_dice(seeded_a)
        second = roll_dice(seeded_b)
        self.assertEqual(first, second)

    def test_hard_roll_flag(self):
        rng = FixedRng([4, 4])
        result = roll_dice(rng)
        self.assertTrue(result.is_hard)
        self.assertEqual(result.total, 8)


if __name__ == "__main__":
    unittest.main()
