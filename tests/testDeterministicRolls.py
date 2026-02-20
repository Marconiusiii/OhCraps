import random
import unittest

from engineCore import rollDice


class FixedRng:
	def __init__(self, values):
		self.values = list(values)
		self.index = 0

	def randint(self, startValue, endValue):
		value = self.values[self.index]
		self.index += 1
		return value


class RollDiceTests(unittest.TestCase):
	def testInjectedRngIsDeterministic(self):
		rng = FixedRng([2, 5])
		result = rollDice(rng)
		self.assertEqual(result.die1, 5)
		self.assertEqual(result.die2, 2)
		self.assertEqual(result.total, 7)
		self.assertFalse(result.isHard)

	def testSeededRandomIsRepeatable(self):
		seededA = random.Random(42)
		seededB = random.Random(42)
		first = rollDice(seededA)
		second = rollDice(seededB)
		self.assertEqual(first, second)

	def testHardRollFlag(self):
		rng = FixedRng([4, 4])
		result = rollDice(rng)
		self.assertTrue(result.isHard)
		self.assertEqual(result.total, 8)


if __name__ == "__main__":
	unittest.main()
