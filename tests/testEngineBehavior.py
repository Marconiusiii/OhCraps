import unittest

from engineCore import GameState, RollOutcome, evaluateRoll


class EvaluateRollTests(unittest.TestCase):
    def testComeOutNatural(self):
        state = GameState(
            bank=1000,
            chipsOnTable=0,
            throws=0,
            pointIsOn=False,
            comeOut=0,
            p2=0,
        )
        self.assertEqual(evaluateRoll(state, 7), RollOutcome.natural)
        self.assertEqual(evaluateRoll(state, 11), RollOutcome.natural)

    def testComeOutCraps(self):
        state = GameState(
            bank=1000,
            chipsOnTable=0,
            throws=0,
            pointIsOn=False,
            comeOut=0,
            p2=0,
        )
        self.assertEqual(evaluateRoll(state, 2), RollOutcome.craps)
        self.assertEqual(evaluateRoll(state, 3), RollOutcome.craps)
        self.assertEqual(evaluateRoll(state, 12), RollOutcome.craps)

    def testPointPhaseOutcomes(self):
        state = GameState(
            bank=1000,
            chipsOnTable=0,
            throws=0,
            pointIsOn=True,
            comeOut=6,
            p2=0,
        )
        self.assertEqual(evaluateRoll(state, 7), RollOutcome.sevenOut)
        self.assertEqual(evaluateRoll(state, 6), RollOutcome.pointHit)
        self.assertEqual(evaluateRoll(state, 8), RollOutcome.neutral)


if __name__ == "__main__":
    unittest.main()
