import unittest

from engine_core import GameState, RollOutcome, evaluate_roll


class EvaluateRollTests(unittest.TestCase):
    def test_come_out_natural(self):
        state = GameState(
            bank=1000,
            chips_on_table=0,
            throws=0,
            point_is_on=False,
            come_out=0,
            p2=0,
        )
        self.assertEqual(evaluate_roll(state, 7), RollOutcome.NATURAL)
        self.assertEqual(evaluate_roll(state, 11), RollOutcome.NATURAL)

    def test_come_out_craps(self):
        state = GameState(
            bank=1000,
            chips_on_table=0,
            throws=0,
            point_is_on=False,
            come_out=0,
            p2=0,
        )
        self.assertEqual(evaluate_roll(state, 2), RollOutcome.CRAPS)
        self.assertEqual(evaluate_roll(state, 3), RollOutcome.CRAPS)
        self.assertEqual(evaluate_roll(state, 12), RollOutcome.CRAPS)

    def test_point_phase_outcomes(self):
        state = GameState(
            bank=1000,
            chips_on_table=0,
            throws=0,
            point_is_on=True,
            come_out=6,
            p2=0,
        )
        self.assertEqual(evaluate_roll(state, 7), RollOutcome.SEVEN_OUT)
        self.assertEqual(evaluate_roll(state, 6), RollOutcome.POINT_HIT)
        self.assertEqual(evaluate_roll(state, 8), RollOutcome.NEUTRAL)


if __name__ == "__main__":
    unittest.main()
