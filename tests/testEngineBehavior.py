import unittest

from engineCore import GameState, RollOutcome, evaluateRoll, settleLineBets, settleOddsBets, settlePlaceBets, settleLayBets, settleFieldBet, settleHardWays, settleComeTableBets, settleComeBarBet, settleDComeBarBet, maxPassOdds, maxComeOdds, maxLayOdds, settlePropSubsetBets, settleBuffaloBet, settleHopBets


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

	def testSettleFieldBetStandardWin(self):
		settlement = settleFieldBet(fieldBet=10, roll=9)
		self.assertEqual(settlement.didWin, True)
		self.assertEqual(settlement.winAmount, 10)
		self.assertEqual(settlement.bankDelta, 10)
		self.assertEqual(settlement.fieldBet, 10)
		self.assertEqual(settlement.chipsOnTableDelta, 0)

	def testSettleFieldBetDoubleOnTwo(self):
		settlement = settleFieldBet(fieldBet=10, roll=2)
		self.assertEqual(settlement.didWin, True)
		self.assertEqual(settlement.winAmount, 20)
		self.assertEqual(settlement.bankDelta, 20)
		self.assertIn("Double in the bubble!", settlement.messages)

	def testSettleFieldBetTripleOnTwelve(self):
		settlement = settleFieldBet(fieldBet=10, roll=12)
		self.assertEqual(settlement.didWin, True)
		self.assertEqual(settlement.winAmount, 30)
		self.assertEqual(settlement.bankDelta, 30)
		self.assertIn("Triple in the Field!", settlement.messages)

	def testSettleFieldBetLosesOnNonFieldRoll(self):
		settlement = settleFieldBet(fieldBet=10, roll=6)
		self.assertEqual(settlement.didWin, False)
		self.assertEqual(settlement.lossAmount, 10)
		self.assertEqual(settlement.fieldBet, 0)
		self.assertEqual(settlement.chipsOnTableDelta, -10)
		self.assertEqual(settlement.bankDelta, 0)

	def testSettleHardWaysWinOnHardFour(self):
		hardWays = {4: 5, 6: 0, 8: 0, 10: 0}
		settlement = settleHardWays(hardWays=hardWays, roll=4, rollHard=True)
		self.assertEqual(settlement.hitNumber, 4)
		self.assertEqual(settlement.winAmount, 35)
		self.assertEqual(settlement.bankDelta, 35)
		self.assertEqual(settlement.chipsOnTableDelta, 0)

	def testSettleHardWaysWinOnHardSix(self):
		hardWays = {4: 0, 6: 5, 8: 0, 10: 0}
		settlement = settleHardWays(hardWays=hardWays, roll=6, rollHard=True)
		self.assertEqual(settlement.hitNumber, 6)
		self.assertEqual(settlement.winAmount, 45)
		self.assertEqual(settlement.bankDelta, 45)

	def testSettleHardWaysLoseOnEasyRoll(self):
		hardWays = {4: 0, 6: 5, 8: 0, 10: 0}
		settlement = settleHardWays(hardWays=hardWays, roll=6, rollHard=False)
		self.assertEqual(settlement.lostNumber, 6)
		self.assertEqual(settlement.lossAmount, 5)
		self.assertEqual(settlement.chipsOnTableDelta, -5)
		self.assertEqual(settlement.hardWays[6], 0)

	def testSettleHardWaysSevenOutClearsAll(self):
		hardWays = {4: 5, 6: 10, 8: 15, 10: 20}
		settlement = settleHardWays(hardWays=hardWays, roll=7, rollHard=False)
		self.assertEqual(settlement.lossAmount, 50)
		self.assertEqual(settlement.chipsOnTableDelta, -50)
		self.assertEqual(settlement.hardWays, {4: 0, 6: 0, 8: 0, 10: 0})

	def testSettleComeTableBetsSevenOut(self):
		comeBets = {4: 10, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, "Come": 0}
		dComeBets = {4: 0, 5: 15, 6: 0, 8: 0, 9: 0, 10: 0}
		comeOdds = {4: 20, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0}
		dComeOdds = {4: 0, 5: 30, 6: 0, 8: 0, 9: 0, 10: 0}
		settlement = settleComeTableBets(
			comeBets=comeBets,
			dComeBets=dComeBets,
			comeOdds=comeOdds,
			dComeOdds=dComeOdds,
			roll=7,
			pointIsOn=True,
			working=False
		)
		self.assertEqual(settlement.bankDelta, 80)
		self.assertEqual(settlement.chipsOnTableDelta, -75)
		self.assertEqual(settlement.comeBets[4], 0)
		self.assertEqual(settlement.dComeBets[5], 0)

	def testSettleComeTableBetsComeNumberHit(self):
		comeBets = {4: 10, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, "Come": 0}
		dComeBets = {4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0}
		comeOdds = {4: 15, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0}
		dComeOdds = {4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0}
		settlement = settleComeTableBets(
			comeBets=comeBets,
			dComeBets=dComeBets,
			comeOdds=comeOdds,
			dComeOdds=dComeOdds,
			roll=4,
			pointIsOn=True,
			working=False
		)
		self.assertEqual(settlement.bankDelta, 65)
		self.assertEqual(settlement.chipsOnTableDelta, -25)
		self.assertEqual(settlement.comeBets[4], 0)
		self.assertEqual(settlement.comeOdds[4], 0)

	def testSettleComeTableBetsDontComeLosesOnNumber(self):
		comeBets = {4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, "Come": 0}
		dComeBets = {4: 12, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0}
		comeOdds = {4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0}
		dComeOdds = {4: 24, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0}
		settlement = settleComeTableBets(
			comeBets=comeBets,
			dComeBets=dComeBets,
			comeOdds=comeOdds,
			dComeOdds=dComeOdds,
			roll=4,
			pointIsOn=True,
			working=False
		)
		self.assertEqual(settlement.bankDelta, 0)
		self.assertEqual(settlement.chipsOnTableDelta, -36)
		self.assertEqual(settlement.dComeBets[4], 0)
		self.assertEqual(settlement.dComeOdds[4], 0)

	def testSettleComeBarBetWinsOnNatural(self):
		settlement = settleComeBarBet(comeBet=20, roll=11)
		self.assertEqual(settlement.comeBet, 0)
		self.assertEqual(settlement.bankDelta, 40)
		self.assertEqual(settlement.chipsOnTableDelta, -20)
		self.assertEqual(settlement.movedNumber, None)

	def testSettleComeBarBetLosesOnCraps(self):
		settlement = settleComeBarBet(comeBet=20, roll=2)
		self.assertEqual(settlement.comeBet, 0)
		self.assertEqual(settlement.bankDelta, 0)
		self.assertEqual(settlement.chipsOnTableDelta, -20)
		self.assertEqual(settlement.movedNumber, None)

	def testSettleComeBarBetMovesToNumber(self):
		settlement = settleComeBarBet(comeBet=25, roll=5)
		self.assertEqual(settlement.comeBet, 0)
		self.assertEqual(settlement.movedNumber, 5)
		self.assertEqual(settlement.movedAmount, 25)
		self.assertEqual(settlement.bankDelta, 0)
		self.assertEqual(settlement.chipsOnTableDelta, 0)

	def testSettleDComeBarBetLosesOnNatural(self):
		settlement = settleDComeBarBet(dComeBet=20, roll=7)
		self.assertEqual(settlement.dComeBet, 0)
		self.assertEqual(settlement.bankDelta, 0)
		self.assertEqual(settlement.chipsOnTableDelta, -20)
		self.assertEqual(settlement.movedNumber, None)

	def testSettleDComeBarBetWinsOnTwoOrThree(self):
		settlement = settleDComeBarBet(dComeBet=20, roll=3)
		self.assertEqual(settlement.dComeBet, 0)
		self.assertEqual(settlement.bankDelta, 40)
		self.assertEqual(settlement.chipsOnTableDelta, -20)
		self.assertEqual(settlement.movedNumber, None)

	def testSettleDComeBarBetPushOnTwelve(self):
		settlement = settleDComeBarBet(dComeBet=20, roll=12)
		self.assertEqual(settlement.dComeBet, 0)
		self.assertEqual(settlement.bankDelta, 20)
		self.assertEqual(settlement.chipsOnTableDelta, -20)
		self.assertEqual(settlement.movedNumber, None)

	def testSettleDComeBarBetMovesToNumber(self):
		settlement = settleDComeBarBet(dComeBet=30, roll=9)
		self.assertEqual(settlement.dComeBet, 0)
		self.assertEqual(settlement.movedNumber, 9)
		self.assertEqual(settlement.movedAmount, 30)
		self.assertEqual(settlement.bankDelta, 0)
		self.assertEqual(settlement.chipsOnTableDelta, 0)

	def testMaxPassOddsByPoint(self):
		self.assertEqual(maxPassOdds(4, 10), 30)
		self.assertEqual(maxPassOdds(5, 10), 40)
		self.assertEqual(maxPassOdds(6, 10), 50)
		self.assertEqual(maxPassOdds(12, 10), 0)

	def testMaxComeOddsUsesSameRule(self):
		self.assertEqual(maxComeOdds(10, 15), 45)
		self.assertEqual(maxComeOdds(9, 15), 60)
		self.assertEqual(maxComeOdds(8, 15), 75)

	def testMaxLayOdds(self):
		self.assertEqual(maxLayOdds(0), 0)
		self.assertEqual(maxLayOdds(12), 120)

	def testSettlePropSubsetAnySevenWin(self):
		propBets = {"Any Seven": 10, "Any Craps": 0, "Eleven": 0, "C and E": 0}
		settlement = settlePropSubsetBets(propBets=propBets, roll=7)
		self.assertEqual(settlement.bankDelta, 50)
		self.assertEqual(settlement.chipsOnTableDelta, -10)
		self.assertEqual(settlement.propBets["Any Seven"], 0)

	def testSettlePropSubsetAnyCrapsWin(self):
		propBets = {"Any Seven": 0, "Any Craps": 10, "Eleven": 0, "C and E": 0}
		settlement = settlePropSubsetBets(propBets=propBets, roll=3)
		self.assertEqual(settlement.bankDelta, 80)
		self.assertEqual(settlement.chipsOnTableDelta, -10)
		self.assertEqual(settlement.propBets["Any Craps"], 0)

	def testSettlePropSubsetElevenWin(self):
		propBets = {"Any Seven": 0, "Any Craps": 0, "Eleven": 5, "C and E": 0}
		settlement = settlePropSubsetBets(propBets=propBets, roll=11)
		self.assertEqual(settlement.bankDelta, 80)
		self.assertEqual(settlement.chipsOnTableDelta, -5)
		self.assertEqual(settlement.propBets["Eleven"], 0)

	def testSettlePropSubsetCandEWinsOnEleven(self):
		propBets = {"Any Seven": 0, "Any Craps": 0, "Eleven": 0, "C and E": 10}
		settlement = settlePropSubsetBets(propBets=propBets, roll=11)
		self.assertEqual(settlement.bankDelta, 80)
		self.assertEqual(settlement.chipsOnTableDelta, -10)
		self.assertEqual(settlement.propBets["C and E"], 0)

	def testSettlePropSubsetCandELoses(self):
		propBets = {"Any Seven": 0, "Any Craps": 0, "Eleven": 0, "C and E": 10}
		settlement = settlePropSubsetBets(propBets=propBets, roll=4)
		self.assertEqual(settlement.bankDelta, 0)
		self.assertEqual(settlement.chipsOnTableDelta, -10)
		self.assertEqual(settlement.propBets["C and E"], 0)

	def testSettlePropSubsetSnakeEyesWin(self):
		propBets = {"Snake Eyes": 5}
		settlement = settlePropSubsetBets(propBets=propBets, roll=2)
		self.assertEqual(settlement.bankDelta, 155)
		self.assertEqual(settlement.chipsOnTableDelta, -5)
		self.assertEqual(settlement.propBets["Snake Eyes"], 0)

	def testSettlePropSubsetHornWinStaysUp(self):
		propBets = {"Horn": 40}
		settlement = settlePropSubsetBets(propBets=propBets, roll=2)
		self.assertEqual(settlement.bankDelta, 260)
		self.assertEqual(settlement.chipsOnTableDelta, 0)
		self.assertEqual(settlement.propBets["Horn"], 40)
		self.assertIn("If it pays it stays! Horn bets are still up.", settlement.messages)

	def testSettlePropSubsetHornLosesAndClears(self):
		propBets = {"Horn": 40}
		settlement = settlePropSubsetBets(propBets=propBets, roll=7)
		self.assertEqual(settlement.bankDelta, 0)
		self.assertEqual(settlement.chipsOnTableDelta, -40)
		self.assertEqual(settlement.propBets["Horn"], 0)

	def testSettleBuffaloBetWinsOnHardNumber(self):
		propBets = {"Buffalo": 40}
		settlement = settleBuffaloBet(propBets=propBets, roll=8, die1=4, die2=4)
		self.assertEqual(settlement.bankDelta, 280)
		self.assertEqual(settlement.chipsOnTableDelta, -40)
		self.assertEqual(settlement.propBets["Buffalo"], 0)
		self.assertIn("You won $270 on the Buffalo bet!", settlement.messages)

	def testSettleBuffaloBetLosesOnNonHardRoll(self):
		propBets = {"Buffalo": 40}
		settlement = settleBuffaloBet(propBets=propBets, roll=8, die1=5, die2=3)
		self.assertEqual(settlement.bankDelta, 0)
		self.assertEqual(settlement.chipsOnTableDelta, -40)
		self.assertEqual(settlement.propBets["Buffalo"], 0)
		self.assertIn("You lost $40 from the Buffalo.", settlement.messages)

	def testSettleHopBetsHop4EasyWin(self):
		propBets = {"Hop 4": 20}
		settlement = settleHopBets(propBets=propBets, roll=4, die1=3, die2=1)
		self.assertEqual(settlement.bankDelta, 150)
		self.assertEqual(settlement.chipsOnTableDelta, -20)
		self.assertEqual(settlement.propBets["Hop 4"], 0)
		self.assertIn("You won $140 on the Hop 4 bet!", settlement.messages)

	def testSettleHopBetsHop4HardWin(self):
		propBets = {"Hop 4": 20}
		settlement = settleHopBets(propBets=propBets, roll=4, die1=2, die2=2)
		self.assertEqual(settlement.bankDelta, 300)
		self.assertEqual(settlement.chipsOnTableDelta, -20)
		self.assertEqual(settlement.propBets["Hop 4"], 0)
		self.assertIn("You won $290 on the Hop 4 bet!", settlement.messages)

	def testSettleHopBetsHop6EasyLosesOnHardSix(self):
		propBets = {"Hop 6 Easy": 20}
		settlement = settleHopBets(propBets=propBets, roll=6, die1=3, die2=3)
		self.assertEqual(settlement.bankDelta, 0)
		self.assertEqual(settlement.chipsOnTableDelta, -20)
		self.assertEqual(settlement.propBets["Hop 6 Easy"], 0)
		self.assertIn("You lost $20 from the Hop 6 Easy.", settlement.messages)

	def testSettleHopBetsHopHardWinsOnDouble(self):
		propBets = {"Hop Hard": 60}
		settlement = settleHopBets(propBets=propBets, roll=10, die1=5, die2=5)
		self.assertEqual(settlement.bankDelta, 260)
		self.assertEqual(settlement.chipsOnTableDelta, -60)
		self.assertEqual(settlement.propBets["Hop Hard"], 0)
		self.assertIn("You won $250 on the Hop Hard bet!", settlement.messages)

	def testSettleHopBetsHopHardSpecificLosesOnDifferentHardNumber(self):
		propBets = {"Hop Hard 8": 10}
		settlement = settleHopBets(propBets=propBets, roll=6, die1=3, die2=3)
		self.assertEqual(settlement.bankDelta, 0)
		self.assertEqual(settlement.chipsOnTableDelta, -10)
		self.assertEqual(settlement.propBets["Hop Hard 8"], 0)
		self.assertIn("You lost $10 from the Hop Hard 8.", settlement.messages)


if __name__ == "__main__":
	unittest.main()
