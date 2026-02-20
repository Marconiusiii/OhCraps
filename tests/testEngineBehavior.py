import unittest

from engineCore import GameState, RollOutcome, evaluateRoll, settleLineBets, settleOddsBets, settlePlaceBets, settleLayBets


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

	def testSettleLineBetsComeOutNatural(self):
		lineBets = {"Pass": 10, "Pass Odds": 0, "Don't Pass": 15, "Don't Pass Odds": 0}
		settlement = settleLineBets(lineBets=lineBets, pointIsOn=False, roll=7, p2roll=0)
		self.assertEqual(settlement.bankDelta, 10)
		self.assertEqual(settlement.chipsOnTableDelta, -15)
		self.assertEqual(settlement.lineBets["Don't Pass"], 0)

	def testSettleLineBetsPointHit(self):
		lineBets = {"Pass": 20, "Pass Odds": 0, "Don't Pass": 25, "Don't Pass Odds": 0}
		settlement = settleLineBets(lineBets=lineBets, pointIsOn=True, roll=6, p2roll=6)
		self.assertEqual(settlement.bankDelta, 40)
		self.assertEqual(settlement.chipsOnTableDelta, -45)
		self.assertEqual(settlement.lineBets["Pass"], 0)
		self.assertEqual(settlement.lineBets["Don't Pass"], 0)

	def testSettleLineBetsSevenOut(self):
		lineBets = {"Pass": 20, "Pass Odds": 0, "Don't Pass": 25, "Don't Pass Odds": 0}
		settlement = settleLineBets(lineBets=lineBets, pointIsOn=True, roll=6, p2roll=7)
		self.assertEqual(settlement.bankDelta, 50)
		self.assertEqual(settlement.chipsOnTableDelta, -45)
		self.assertEqual(settlement.lineBets["Pass"], 0)
		self.assertEqual(settlement.lineBets["Don't Pass"], 0)

	def testSettleLineBetsSevenOutDontPassOnly(self):
		lineBets = {"Pass": 0, "Pass Odds": 0, "Don't Pass": 25, "Don't Pass Odds": 0}
		settlement = settleLineBets(lineBets=lineBets, pointIsOn=True, roll=6, p2roll=7)
		self.assertEqual(settlement.bankDelta, 50)
		self.assertEqual(settlement.chipsOnTableDelta, -25)
		self.assertEqual(settlement.lineBets["Don't Pass"], 0)

	def testSettleOddsBetsPassOddsWin(self):
		lineBets = {"Pass": 0, "Pass Odds": 10, "Don't Pass": 0, "Don't Pass Odds": 0}
		settlement = settleOddsBets(lineBets=lineBets, roll=5, comeOut=5)
		self.assertEqual(settlement.bankDelta, 25)
		self.assertEqual(settlement.chipsOnTableDelta, -10)
		self.assertEqual(settlement.lineBets["Pass Odds"], 0)

	def testSettleOddsBetsDontPassOddsWinOnSeven(self):
		lineBets = {"Pass": 0, "Pass Odds": 0, "Don't Pass": 0, "Don't Pass Odds": 30}
		settlement = settleOddsBets(lineBets=lineBets, roll=7, comeOut=5)
		self.assertEqual(settlement.bankDelta, 50)
		self.assertEqual(settlement.chipsOnTableDelta, -30)
		self.assertEqual(settlement.lineBets["Don't Pass Odds"], 0)

	def testSettleOddsBetsDontPassOddsLosesOnPointHit(self):
		lineBets = {"Pass": 0, "Pass Odds": 0, "Don't Pass": 0, "Don't Pass Odds": 40}
		settlement = settleOddsBets(lineBets=lineBets, roll=4, comeOut=4)
		self.assertEqual(settlement.bankDelta, 0)
		self.assertEqual(settlement.chipsOnTableDelta, -40)
		self.assertEqual(settlement.lineBets["Don't Pass Odds"], 0)

	def testSettlePlaceBetsBuy4IncludesVig(self):
		placeBets = {4: 25, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0}
		settlement = settlePlaceBets(placeBets=placeBets, roll=4)
		self.assertEqual(settlement.commissionPaid, 1)
		self.assertEqual(settlement.winAmount, 49)
		self.assertEqual(settlement.bankDelta, 49)
		self.assertEqual(settlement.hitNumber, 4)

	def testSettlePlaceBetsSixHandlesImproperBet(self):
		placeBets = {4: 0, 5: 0, 6: 5, 8: 0, 9: 0, 10: 0}
		settlement = settlePlaceBets(placeBets=placeBets, roll=6)
		self.assertEqual(settlement.winAmount, 5)
		self.assertEqual(settlement.bankDelta, 5)
		self.assertEqual(settlement.hitNumber, 6)

	def testSettlePlaceBetsSevenOutClearsAll(self):
		placeBets = {4: 10, 5: 15, 6: 18, 8: 12, 9: 10, 10: 25}
		settlement = settlePlaceBets(placeBets=placeBets, roll=7)
		self.assertEqual(settlement.lossAmount, 90)
		self.assertEqual(settlement.chipsOnTableDelta, -90)
		self.assertEqual(settlement.placeBets, {4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0})

	def testSettleLayBetsLosesOnLayNumber(self):
		layBets = {4: 30, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0}
		settlement = settleLayBets(layBets=layBets, roll=4)
		self.assertEqual(settlement.lostNumber, 4)
		self.assertEqual(settlement.lostAmount, 30)
		self.assertEqual(settlement.chipsOnTableDelta, -30)
		self.assertEqual(settlement.layBets[4], 0)

	def testSettleLayBetsSevenPayoutAndVig(self):
		layBets = {4: 40, 5: 30, 6: 36, 8: 0, 9: 0, 10: 0}
		settlement = settleLayBets(layBets=layBets, roll=7)
		self.assertEqual(settlement.totalWinAmount, 70)
		self.assertEqual(settlement.totalVigAmount, 3)
		self.assertEqual(settlement.bankDelta, 67)
		self.assertEqual(settlement.chipsOnTableDelta, 0)
		self.assertEqual(settlement.layBets, layBets)

	def testSettleLayBetsNeutralRollNoChange(self):
		layBets = {4: 25, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0}
		settlement = settleLayBets(layBets=layBets, roll=8)
		self.assertEqual(settlement.bankDelta, 0)
		self.assertEqual(settlement.chipsOnTableDelta, 0)
		self.assertEqual(settlement.lostNumber, None)
		self.assertEqual(settlement.layBets, layBets)


if __name__ == "__main__":
	unittest.main()
