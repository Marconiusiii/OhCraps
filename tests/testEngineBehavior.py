import unittest
from pathlib import Path
import py_compile
from unittest.mock import patch

from engineCore import GameState, RollOutcome, evaluateRoll, settleLineBets, settleLineBetsForMode, settleOddsBets, settlePlaceBets, settlePlaceBetsForMode, settleLayBets, settleLayBetsForMode, settleFieldBet, settleHardWays, settleComeTableBets, settleComeBarBet, settleDComeBarBet, maxPassOdds, maxComeOdds, maxComeOddsForMode, comeOddsUnitForMode, dComeOddsUnitForMode, isOddsBetUnitValid, comeOddsWinForMode, dComeOddsWinForMode, maxLayOdds, oddsBetLimits, settlePropSubsetBets, settleBuffaloBet, settleHopBets, createDefaultPropBets, getPropKeyMatrix, resolvePropAliases, PROP_BET_KEYS, calculateHalfPressIncrement, createGameState, syncGameState, GameMode, parseGameModeChoice, getRulesProfile


def loadTerminalNamespace():
	scriptPath = Path(__file__).resolve().parents[1] / "OhCraps_Py3.command"
	sourceText = scriptPath.read_text()
	cutMarker = "# Game Start"
	markerIndex = sourceText.find(cutMarker)
	if markerIndex == -1:
		raise AssertionError("Could not locate game start marker in terminal script.")
	prefixSource = sourceText[:markerIndex]
	terminalNamespace = {}
	exec(prefixSource, terminalNamespace)
	return terminalNamespace


class EvaluateRollTests(unittest.TestCase):
	def testTerminalScriptCompiles(self):
		scriptPath = Path(__file__).resolve().parents[1] / "OhCraps_Py3.command"
		py_compile.compile(str(scriptPath), doraise=True)

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

	def testComeOutCraplessUsesOnlySevenAsNatural(self):
		state = GameState(
			bank=1000,
			chipsOnTable=0,
			throws=0,
			pointIsOn=False,
			comeOut=0,
			p2=0,
			gameMode=GameMode.craplessCraps
		)
		self.assertEqual(evaluateRoll(state, 7), RollOutcome.natural)
		self.assertEqual(evaluateRoll(state, 11), RollOutcome.pointEstablished)
		self.assertEqual(evaluateRoll(state, 2), RollOutcome.pointEstablished)
		self.assertEqual(evaluateRoll(state, 3), RollOutcome.pointEstablished)
		self.assertEqual(evaluateRoll(state, 12), RollOutcome.pointEstablished)

	def testPointPhaseOutcomesCrapless(self):
		state = GameState(
			bank=1000,
			chipsOnTable=0,
			throws=0,
			pointIsOn=True,
			comeOut=11,
			p2=0,
			gameMode=GameMode.craplessCraps
		)
		self.assertEqual(evaluateRoll(state, 7), RollOutcome.sevenOut)
		self.assertEqual(evaluateRoll(state, 11), RollOutcome.pointHit)
		self.assertEqual(evaluateRoll(state, 6), RollOutcome.neutral)

	def testCreateGameState(self):
		state = createGameState(bank=1500, chipsOnTable=120, throws=9, pointIsOn=True, comeOut=8, p2=6)
		self.assertEqual(state.bank, 1500)
		self.assertEqual(state.chipsOnTable, 120)
		self.assertEqual(state.throws, 9)
		self.assertEqual(state.pointIsOn, True)
		self.assertEqual(state.comeOut, 8)
		self.assertEqual(state.p2, 6)
		self.assertEqual(state.gameMode, GameMode.craps)

	def testCreateGameStateWithCraplessMode(self):
		state = createGameState(bank=1500, chipsOnTable=120, throws=9, pointIsOn=True, comeOut=8, p2=6, gameMode=GameMode.craplessCraps)
		self.assertEqual(state.gameMode, GameMode.craplessCraps)

	def testSyncGameState(self):
		state = createGameState(bank=100, chipsOnTable=10, throws=1, pointIsOn=False, comeOut=0, p2=0)
		syncGameState(gameState=state, bank=200, chipsOnTable=50, throws=7, pointIsOn=True, comeOut=5, p2=9)
		self.assertEqual(state.bank, 200)
		self.assertEqual(state.chipsOnTable, 50)
		self.assertEqual(state.throws, 7)
		self.assertEqual(state.pointIsOn, True)
		self.assertEqual(state.comeOut, 5)
		self.assertEqual(state.p2, 9)
		self.assertEqual(state.gameMode, GameMode.craps)

	def testSyncGameStateCanUpdateGameMode(self):
		state = createGameState(bank=100, chipsOnTable=10, throws=1, pointIsOn=False, comeOut=0, p2=0, gameMode=GameMode.craps)
		syncGameState(gameState=state, bank=100, chipsOnTable=10, throws=1, pointIsOn=False, comeOut=0, p2=0, gameMode=GameMode.craplessCraps)
		self.assertEqual(state.gameMode, GameMode.craplessCraps)

	def testParseGameModeChoice(self):
		self.assertEqual(parseGameModeChoice("1"), GameMode.craps)
		self.assertEqual(parseGameModeChoice("2"), GameMode.craplessCraps)
		self.assertEqual(parseGameModeChoice(" 2 "), GameMode.craplessCraps)
		self.assertEqual(parseGameModeChoice("x"), None)

	def testGetRulesProfile(self):
		self.assertEqual(getRulesProfile(GameMode.craps).displayName, "Craps")
		self.assertEqual(getRulesProfile(GameMode.craplessCraps).displayName, "Crapless Craps")

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

	def testSettleLineBetsForModeCrapsMatchesCanonical(self):
		lineBets = {"Pass": 10, "Pass Odds": 0, "Don't Pass": 15, "Don't Pass Odds": 0}
		baseSettlement = settleLineBets(lineBets=lineBets, pointIsOn=False, roll=7, p2roll=0)
		modeSettlement = settleLineBetsForMode(lineBets=lineBets, pointIsOn=False, roll=7, p2roll=0, gameMode=GameMode.craps)
		self.assertEqual(modeSettlement.lineBets, baseSettlement.lineBets)
		self.assertEqual(modeSettlement.bankDelta, baseSettlement.bankDelta)
		self.assertEqual(modeSettlement.chipsOnTableDelta, baseSettlement.chipsOnTableDelta)

	def testSettleLineBetsForModeCraplessReturnsDontPass(self):
		lineBets = {"Pass": 0, "Pass Odds": 0, "Don't Pass": 20, "Don't Pass Odds": 30}
		settlement = settleLineBetsForMode(lineBets=lineBets, pointIsOn=False, roll=11, p2roll=0, gameMode=GameMode.craplessCraps)
		self.assertEqual(settlement.lineBets["Don't Pass"], 0)
		self.assertEqual(settlement.lineBets["Don't Pass Odds"], 0)
		self.assertEqual(settlement.bankDelta, 50)
		self.assertEqual(settlement.chipsOnTableDelta, -50)
		self.assertIn("Don't bets are not available in Crapless Craps. Returning $50.", settlement.messages)

	def testSettleLineBetsForModeCraplessComeOutElevenLeavesPassUp(self):
		lineBets = {"Pass": 10, "Pass Odds": 0, "Don't Pass": 0, "Don't Pass Odds": 0}
		settlement = settleLineBetsForMode(lineBets=lineBets, pointIsOn=False, roll=11, p2roll=0, gameMode=GameMode.craplessCraps)
		self.assertEqual(settlement.lineBets["Pass"], 10)
		self.assertEqual(settlement.bankDelta, 0)
		self.assertEqual(settlement.chipsOnTableDelta, 0)

	def testSettleLineBetsForModeCraplessPointElevenHitWins(self):
		lineBets = {"Pass": 10, "Pass Odds": 0, "Don't Pass": 0, "Don't Pass Odds": 0}
		settlement = settleLineBetsForMode(lineBets=lineBets, pointIsOn=True, roll=11, p2roll=11, gameMode=GameMode.craplessCraps)
		self.assertEqual(settlement.lineBets["Pass"], 0)
		self.assertEqual(settlement.bankDelta, 20)
		self.assertEqual(settlement.chipsOnTableDelta, -10)
		self.assertIn("You won $10 on the Pass Line!", settlement.messages)

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

	def testSettleOddsBetsCraplessPassOddsWinOnTwo(self):
		lineBets = {"Pass": 0, "Pass Odds": 10, "Don't Pass": 0, "Don't Pass Odds": 0}
		settlement = settleOddsBets(lineBets=lineBets, roll=2, comeOut=2, gameMode=GameMode.craplessCraps)
		self.assertEqual(settlement.bankDelta, 70)
		self.assertEqual(settlement.chipsOnTableDelta, -10)
		self.assertEqual(settlement.lineBets["Pass Odds"], 0)

	def testSettleOddsBetsCraplessPassOddsWinOnThreeElevenTwelve(self):
		cases = [
			{"roll": 3, "odds": 12, "expectedDelta": 48},
			{"roll": 11, "odds": 12, "expectedDelta": 48},
			{"roll": 12, "odds": 10, "expectedDelta": 70},
		]
		for case in cases:
			with self.subTest(roll=case["roll"]):
				lineBets = {"Pass": 0, "Pass Odds": case["odds"], "Don't Pass": 0, "Don't Pass Odds": 0}
				settlement = settleOddsBets(lineBets=lineBets, roll=case["roll"], comeOut=case["roll"], gameMode=GameMode.craplessCraps)
				self.assertEqual(settlement.bankDelta, case["expectedDelta"])
				self.assertEqual(settlement.chipsOnTableDelta, -case["odds"])
				self.assertEqual(settlement.lineBets["Pass Odds"], 0)

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

	def testSettlePlaceBetsForModeCrapsMatchesCanonical(self):
		placeBets = {4: 10, 5: 15, 6: 18, 8: 12, 9: 10, 10: 25}
		baseSettlement = settlePlaceBets(placeBets=placeBets, roll=5)
		modeSettlement = settlePlaceBetsForMode(placeBets=placeBets, roll=5, gameMode=GameMode.craps)
		self.assertEqual(modeSettlement.winAmount, baseSettlement.winAmount)
		self.assertEqual(modeSettlement.bankDelta, baseSettlement.bankDelta)
		self.assertEqual(modeSettlement.chipsOnTableDelta, baseSettlement.chipsOnTableDelta)

	def testSettlePlaceBetsForModeCraplessPlaceTwoUnderBuyThreshold(self):
		placeBets = {2: 10, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		settlement = settlePlaceBetsForMode(placeBets=placeBets, roll=2, gameMode=GameMode.craplessCraps)
		self.assertEqual(settlement.winAmount, 55)
		self.assertEqual(settlement.bankDelta, 55)

	def testSettlePlaceBetsForModeCraplessPlaceThreeBuyIncludesVig(self):
		placeBets = {2: 0, 3: 20, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		settlement = settlePlaceBetsForMode(placeBets=placeBets, roll=3, gameMode=GameMode.craplessCraps)
		self.assertEqual(settlement.commissionPaid, 1)
		self.assertEqual(settlement.winAmount, 59)
		self.assertEqual(settlement.bankDelta, 59)

	def testSettlePlaceBetsForModeCraplessEdgeNumbersUnderBuyThresholdMatrix(self):
		cases = [
			{"number": 2, "bet": 18, "expectedWin": 99},
			{"number": 12, "bet": 18, "expectedWin": 99},
			{"number": 3, "bet": 16, "expectedWin": 44},
			{"number": 11, "bet": 16, "expectedWin": 44}
		]
		for case in cases:
			with self.subTest(number=case["number"], bet=case["bet"]):
				placeBets = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
				placeBets[case["number"]] = case["bet"]
				settlement = settlePlaceBetsForMode(placeBets=placeBets, roll=case["number"], gameMode=GameMode.craplessCraps)
				self.assertEqual(settlement.commissionPaid, 0)
				self.assertEqual(settlement.winAmount, case["expectedWin"])
				self.assertEqual(settlement.bankDelta, case["expectedWin"])
				self.assertEqual(settlement.chipsOnTableDelta, 0)
				self.assertEqual(settlement.placeBets[case["number"]], case["bet"])

	def testSettlePlaceBetsForModeCraplessEdgeNumbersBuyThresholdMatrix(self):
		cases = [
			{"number": 2, "bet": 20, "expectedCommission": 1, "expectedWin": 119},
			{"number": 12, "bet": 20, "expectedCommission": 1, "expectedWin": 119},
			{"number": 3, "bet": 20, "expectedCommission": 1, "expectedWin": 59},
			{"number": 11, "bet": 20, "expectedCommission": 1, "expectedWin": 59}
		]
		for case in cases:
			with self.subTest(number=case["number"], bet=case["bet"]):
				placeBets = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
				placeBets[case["number"]] = case["bet"]
				settlement = settlePlaceBetsForMode(placeBets=placeBets, roll=case["number"], gameMode=GameMode.craplessCraps)
				self.assertEqual(settlement.commissionPaid, case["expectedCommission"])
				self.assertEqual(settlement.winAmount, case["expectedWin"])
				self.assertEqual(settlement.bankDelta, case["expectedWin"])
				self.assertIn(f"${case['expectedCommission']:,} paid to the House for the vig.", settlement.messages)

	def testSettlePlaceBetsForModeCraplessEdgeNumbersBuyVigRoundingMatrix(self):
		cases = [
			{"number": 2, "bet": 38, "expectedCommission": 1, "expectedWin": 227},
			{"number": 2, "bet": 40, "expectedCommission": 2, "expectedWin": 238},
			{"number": 12, "bet": 38, "expectedCommission": 1, "expectedWin": 227},
			{"number": 12, "bet": 40, "expectedCommission": 2, "expectedWin": 238},
			{"number": 3, "bet": 36, "expectedCommission": 1, "expectedWin": 107},
			{"number": 3, "bet": 44, "expectedCommission": 2, "expectedWin": 130},
			{"number": 11, "bet": 36, "expectedCommission": 1, "expectedWin": 107},
			{"number": 11, "bet": 44, "expectedCommission": 2, "expectedWin": 130}
		]
		for case in cases:
			with self.subTest(number=case["number"], bet=case["bet"]):
				placeBets = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
				placeBets[case["number"]] = case["bet"]
				settlement = settlePlaceBetsForMode(placeBets=placeBets, roll=case["number"], gameMode=GameMode.craplessCraps)
				self.assertEqual(settlement.commissionPaid, case["expectedCommission"])
				self.assertEqual(settlement.winAmount, case["expectedWin"])
				self.assertEqual(settlement.bankDelta, case["expectedWin"])

	def testSettlePlaceBetsForModeCraplessSevenOutClearsAll(self):
		placeBets = {2: 10, 3: 12, 4: 10, 5: 10, 6: 12, 8: 12, 9: 10, 10: 10, 11: 12, 12: 10}
		settlement = settlePlaceBetsForMode(placeBets=placeBets, roll=7, gameMode=GameMode.craplessCraps)
		self.assertEqual(settlement.lossAmount, 108)
		self.assertEqual(settlement.chipsOnTableDelta, -108)
		self.assertEqual(settlement.placeBets[2], 0)
		self.assertEqual(settlement.placeBets[12], 0)

	def testSettlePlaceBetsForModeCraplessSevenOutMixedLargeEdgeBets(self):
		placeBets = {2: 25, 3: 30, 4: 15, 5: 10, 6: 18, 8: 24, 9: 10, 10: 20, 11: 35, 12: 40}
		expectedLoss = sum(placeBets.values())
		settlement = settlePlaceBetsForMode(placeBets=placeBets, roll=7, gameMode=GameMode.craplessCraps)
		self.assertEqual(settlement.lossAmount, expectedLoss)
		self.assertEqual(settlement.chipsOnTableDelta, -expectedLoss)
		self.assertTrue(all(value == 0 for value in settlement.placeBets.values()))

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

	def testSettleLayBetsForModeCraplessIncludesEdgeLayPayouts(self):
		layBets = {2: 60, 3: 30, 4: 20, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 30, 12: 60}
		settlement = settleLayBetsForMode(layBets=layBets, roll=7, gameMode=GameMode.craplessCraps)
		self.assertEqual(settlement.totalWinAmount, 50)
		self.assertEqual(settlement.totalVigAmount, 5)
		self.assertEqual(settlement.bankDelta, 45)
		self.assertEqual(settlement.chipsOnTableDelta, 0)
		self.assertIn("You won $10 on the Lay 2!", settlement.messages)
		self.assertIn("You won $10 on the Lay 12!", settlement.messages)

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

	def testSettleComeBarBetCraplessMovesEleven(self):
		settlement = settleComeBarBet(comeBet=25, roll=11, gameMode=GameMode.craplessCraps)
		self.assertEqual(settlement.comeBet, 0)
		self.assertEqual(settlement.movedNumber, 11)
		self.assertEqual(settlement.movedAmount, 25)
		self.assertEqual(settlement.bankDelta, 0)
		self.assertEqual(settlement.chipsOnTableDelta, 0)

	def testSettleComeBarBetCraplessMovesTwo(self):
		settlement = settleComeBarBet(comeBet=25, roll=2, gameMode=GameMode.craplessCraps)
		self.assertEqual(settlement.comeBet, 0)
		self.assertEqual(settlement.movedNumber, 2)
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

	def testMaxComeOddsForModeCraplessEdgeNumbers(self):
		self.assertEqual(maxComeOddsForMode(number=2, baseBet=10, gameMode=GameMode.craplessCraps), 60)
		self.assertEqual(maxComeOddsForMode(number=12, baseBet=10, gameMode=GameMode.craplessCraps), 60)
		self.assertEqual(maxComeOddsForMode(number=3, baseBet=10, gameMode=GameMode.craplessCraps), 30)
		self.assertEqual(maxComeOddsForMode(number=11, baseBet=10, gameMode=GameMode.craplessCraps), 30)

	def testComeOddsWinForModeStandardAndCrapless(self):
		self.assertEqual(comeOddsWinForMode(number=6, oddsBet=10, gameMode=GameMode.craps), 12)
		self.assertEqual(comeOddsWinForMode(number=11, oddsBet=15, gameMode=GameMode.craplessCraps), 45)
		self.assertEqual(comeOddsWinForMode(number=2, oddsBet=12, gameMode=GameMode.craplessCraps), 72)

	def testDComeOddsWinForModeStandardAndCrapless(self):
		self.assertEqual(dComeOddsWinForMode(number=9, oddsBet=30, gameMode=GameMode.craps), 20)
		self.assertEqual(dComeOddsWinForMode(number=11, oddsBet=30, gameMode=GameMode.craplessCraps), 10)
		self.assertEqual(dComeOddsWinForMode(number=2, oddsBet=30, gameMode=GameMode.craplessCraps), 5)

	def testComeOddsUnitsByMode(self):
		self.assertEqual(comeOddsUnitForMode(number=5, gameMode=GameMode.craps), 2)
		self.assertEqual(comeOddsUnitForMode(number=6, gameMode=GameMode.craps), 5)
		self.assertEqual(comeOddsUnitForMode(number=2, gameMode=GameMode.craplessCraps), 1)
		self.assertEqual(comeOddsUnitForMode(number=11, gameMode=GameMode.craplessCraps), 1)

	def testDComeOddsUnitsByMode(self):
		self.assertEqual(dComeOddsUnitForMode(number=4, gameMode=GameMode.craps), 2)
		self.assertEqual(dComeOddsUnitForMode(number=6, gameMode=GameMode.craps), 6)
		self.assertEqual(dComeOddsUnitForMode(number=2, gameMode=GameMode.craplessCraps), 6)
		self.assertEqual(dComeOddsUnitForMode(number=11, gameMode=GameMode.craplessCraps), 3)

	def testIsOddsBetUnitValidByMode(self):
		self.assertEqual(isOddsBetUnitValid(number=5, oddsBet=3, gameMode=GameMode.craps), False)
		self.assertEqual(isOddsBetUnitValid(number=5, oddsBet=4, gameMode=GameMode.craps), True)
		self.assertEqual(isOddsBetUnitValid(number=2, oddsBet=5, gameMode=GameMode.craplessCraps), True)
		self.assertEqual(isOddsBetUnitValid(number=2, oddsBet=5, gameMode=GameMode.craplessCraps, isDont=True), False)
		self.assertEqual(isOddsBetUnitValid(number=2, oddsBet=6, gameMode=GameMode.craplessCraps, isDont=True), True)

	def testSettleComeTableBetsCraplessComeElevenHitWithOdds(self):
		comeBets = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 10, 12: 0, "Come": 0}
		dComeBets = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		comeOdds = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 15, 12: 0}
		dComeOdds = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		settlement = settleComeTableBets(
			comeBets=comeBets,
			dComeBets=dComeBets,
			comeOdds=comeOdds,
			dComeOdds=dComeOdds,
			roll=11,
			pointIsOn=True,
			working=False,
			gameMode=GameMode.craplessCraps
		)
		self.assertEqual(settlement.bankDelta, 80)
		self.assertEqual(settlement.chipsOnTableDelta, -25)
		self.assertEqual(settlement.comeBets[11], 0)
		self.assertEqual(settlement.comeOdds[11], 0)

	def testSettleComeTableBetsCraplessComeTwoHitWithOdds(self):
		comeBets = {2: 10, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, "Come": 0}
		dComeBets = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		comeOdds = {2: 12, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		dComeOdds = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		settlement = settleComeTableBets(
			comeBets=comeBets,
			dComeBets=dComeBets,
			comeOdds=comeOdds,
			dComeOdds=dComeOdds,
			roll=2,
			pointIsOn=True,
			working=False,
			gameMode=GameMode.craplessCraps
		)
		self.assertEqual(settlement.bankDelta, 104)
		self.assertEqual(settlement.chipsOnTableDelta, -22)
		self.assertEqual(settlement.comeBets[2], 0)
		self.assertEqual(settlement.comeOdds[2], 0)

	def testMaxLayOdds(self):
		self.assertEqual(maxLayOdds(0), 0)
		self.assertEqual(maxLayOdds(12), 120)

	def testOddsBetLimitsAlignsEffectiveMaxToUnit(self):
		limits = oddsBetLimits(number=5, baseBet=10, gameMode=GameMode.craps, isDont=True)
		self.assertEqual(limits["rawMax"], 100)
		self.assertEqual(limits["effectiveMax"], 99)
		self.assertEqual(limits["unit"], 3)

	def testOddsBetLimitsForComeInCraplessEdgeNumber(self):
		limits = oddsBetLimits(number=2, baseBet=10, gameMode=GameMode.craplessCraps, isDont=False)
		self.assertEqual(limits["rawMax"], 60)
		self.assertEqual(limits["effectiveMax"], 60)
		self.assertEqual(limits["unit"], 1)

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
		self.assertEqual(settlement.bankDelta, 270)
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
		self.assertEqual(settlement.bankDelta, 310)
		self.assertEqual(settlement.chipsOnTableDelta, -40)
		self.assertEqual(settlement.propBets["Buffalo"], 0)
		self.assertIn("You won $270 on the Buffalo bet!", settlement.messages)
		self.assertEqual(settlement.bankDelta + settlement.chipsOnTableDelta, 270)

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
		self.assertEqual(settlement.bankDelta, 160)
		self.assertEqual(settlement.chipsOnTableDelta, -20)
		self.assertEqual(settlement.propBets["Hop 4"], 0)
		self.assertIn("You won $140 on the Hop 4 bet!", settlement.messages)
		self.assertEqual(settlement.bankDelta + settlement.chipsOnTableDelta, 140)

	def testSettleHopBetsHop4HardWin(self):
		propBets = {"Hop 4": 20}
		settlement = settleHopBets(propBets=propBets, roll=4, die1=2, die2=2)
		self.assertEqual(settlement.bankDelta, 310)
		self.assertEqual(settlement.chipsOnTableDelta, -20)
		self.assertEqual(settlement.propBets["Hop 4"], 0)
		self.assertIn("You won $290 on the Hop 4 bet!", settlement.messages)
		self.assertEqual(settlement.bankDelta + settlement.chipsOnTableDelta, 290)

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
		self.assertEqual(settlement.bankDelta, 310)
		self.assertEqual(settlement.chipsOnTableDelta, -60)
		self.assertEqual(settlement.propBets["Hop Hard"], 0)
		self.assertIn("You won $250 on the Hop Hard bet!", settlement.messages)
		self.assertEqual(settlement.bankDelta + settlement.chipsOnTableDelta, 250)

	def testSettleHopBetsHopHardSpecificLosesOnDifferentHardNumber(self):
		propBets = {"Hop Hard 8": 10}
		settlement = settleHopBets(propBets=propBets, roll=6, die1=3, die2=3)
		self.assertEqual(settlement.bankDelta, 0)
		self.assertEqual(settlement.chipsOnTableDelta, -10)
		self.assertEqual(settlement.propBets["Hop Hard 8"], 0)
		self.assertIn("You lost $10 from the Hop Hard 8.", settlement.messages)

	def testSettleHopBetsHopEZLosesOnHardRoll(self):
		propBets = {"Hop EZ": 15}
		settlement = settleHopBets(propBets=propBets, roll=6, die1=3, die2=3)
		self.assertEqual(settlement.bankDelta, 0)
		self.assertEqual(settlement.chipsOnTableDelta, -15)
		self.assertEqual(settlement.propBets["Hop EZ"], 0)
		self.assertIn("You lost $15 from the Hop EZ.", settlement.messages)

	def testSettleHopBetsHopEZWinsOnEasyRoll(self):
		propBets = {"Hop EZ": 15}
		settlement = settleHopBets(propBets=propBets, roll=6, die1=4, die2=2)
		self.assertEqual(settlement.bankDelta, 16)
		self.assertEqual(settlement.chipsOnTableDelta, -15)
		self.assertEqual(settlement.bankDelta + settlement.chipsOnTableDelta, 1)
		self.assertEqual(settlement.propBets["Hop EZ"], 0)
		self.assertIn("You won $1 on the Hop EZ bet!", settlement.messages)

	def testPropKeyMatrixAccountsForEveryConfiguredPropKey(self):
		propKeyMatrix = getPropKeyMatrix()
		self.assertEqual(set(propKeyMatrix.keys()), set(PROP_BET_KEYS))
		for key in propKeyMatrix:
			self.assertIn(propKeyMatrix[key], ["engineSettled", "entryAlias"])
		entryAliasKeys = [key for key, owner in propKeyMatrix.items() if owner == "entryAlias"]
		self.assertEqual(set(entryAliasKeys), set(["World", "Hi Low"]))

	def testCreateDefaultPropBetsUsesCanonicalKeys(self):
		propBets = createDefaultPropBets()
		self.assertEqual(set(propBets.keys()), set(PROP_BET_KEYS))
		for key in propBets:
			self.assertEqual(propBets[key], 0)

	def testResolvePropAliasesConvertsWorldAndHiLow(self):
		propBets = createDefaultPropBets()
		propBets["World"] = 25
		propBets["Hi Low"] = 20
		resolution = resolvePropAliases(propBets=propBets)
		self.assertEqual(resolution.propBets["World"], 0)
		self.assertEqual(resolution.propBets["Hi Low"], 0)
		self.assertEqual(resolution.propBets["Any Seven"], 5)
		self.assertEqual(resolution.propBets["Horn"], 20)
		self.assertEqual(resolution.propBets["Snake Eyes"], 10)
		self.assertEqual(resolution.propBets["Boxcars"], 10)

	def testCalculateHalfPressIncrementSixFromEighteen(self):
		self.assertEqual(calculateHalfPressIncrement(number=6, currentWager=18), 6)

	def testCalculateHalfPressIncrementEightFromTwentyFour(self):
		self.assertEqual(calculateHalfPressIncrement(number=8, currentWager=24), 12)

	def testCalculateHalfPressIncrementSixMinimumIsSix(self):
		self.assertEqual(calculateHalfPressIncrement(number=6, currentWager=6), 6)

	def testCalculateHalfPressIncrementFiveUsesHalf(self):
		self.assertEqual(calculateHalfPressIncrement(number=5, currentWager=25), 12)


class TerminalFlowRegressionTests(unittest.TestCase):
	def testCraplessComeOutElevenIsPointEstablished(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craplessCraps
		state = terminal["createGameState"](
			bank=1000,
			chipsOnTable=0,
			throws=0,
			pointIsOn=False,
			comeOut=0,
			p2=0,
			gameMode=terminal["gameMode"]
		)
		outcome = terminal["evaluateRoll"](state, 11)
		self.assertEqual(outcome, terminal["RollOutcome"].pointEstablished)

	def testSelectGameModeAcceptsCraps(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craplessCraps
		inputs = iter(["1"])
		writes = []
		terminal["readInput"] = lambda promptText: next(inputs)
		terminal["writeOutput"] = lambda message: writes.append(str(message))
		terminal["selectGameMode"]()
		self.assertEqual(terminal["gameMode"], terminal["GameMode"].craps)
		self.assertIn("Craps selected.", " ".join(writes))

	def testSelectGameModeAcceptsCrapless(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craps
		inputs = iter(["2"])
		writes = []
		terminal["readInput"] = lambda promptText: next(inputs)
		terminal["writeOutput"] = lambda message: writes.append(str(message))
		terminal["selectGameMode"]()
		self.assertEqual(terminal["gameMode"], terminal["GameMode"].craplessCraps)
		self.assertIn("Crapless Craps selected.", " ".join(writes))

	def testSelectGameModeRejectsInvalidThenAccepts(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craps
		inputs = iter(["x", "2"])
		writes = []
		terminal["readInput"] = lambda promptText: next(inputs)
		terminal["writeOutput"] = lambda message: writes.append(str(message))
		terminal["selectGameMode"]()
		self.assertEqual(terminal["gameMode"], terminal["GameMode"].craplessCraps)
		writtenText = " ".join(writes)
		self.assertIn("Invalid choice. Enter 1 or 2.", writtenText)
		self.assertIn("Crapless Craps selected.", writtenText)

	def testSetGameModeAcceptsTextAndSyncsRuntime(self):
		terminal = loadTerminalNamespace()
		terminal["setGameMode"]("2")
		self.assertEqual(terminal["gameMode"], terminal["GameMode"].craplessCraps)
		self.assertEqual(terminal["gameRuntime"].gameMode, terminal["GameMode"].craplessCraps)

	def testInitializeGameSetsBankAndMode(self):
		terminal = loadTerminalNamespace()
		state = terminal["initializeGame"](startBank=500, selectedMode="crapless craps")
		self.assertEqual(terminal["bank"], 500)
		self.assertEqual(terminal["initBank"], 500)
		self.assertEqual(terminal["chipsOnTable"], 0)
		self.assertEqual(terminal["gameMode"], terminal["GameMode"].craplessCraps)
		self.assertEqual(terminal["gameRuntime"].bank, 500)
		self.assertEqual(state["bank"], 500)
		self.assertEqual(state["gameMode"], terminal["GameMode"].craplessCraps)
		self.assertEqual(state["engineApiVersion"], terminal["engineApiVersion"])

	def testInitializeGameRejectsZeroBank(self):
		terminal = loadTerminalNamespace()
		with self.assertRaises(ValueError):
			terminal["initializeGame"](startBank=0, selectedMode=terminal["GameMode"].craps)

	def testCreateHostStartupBundleReturnsFullPackageWithoutInit(self):
		terminal = loadTerminalNamespace()
		terminal["bank"] = 125
		bundle = terminal["createHostStartupBundle"](
			requiredApiVersion=terminal["engineApiVersion"],
			requiredFeatures=["autoCapture", "sessionBundle"]
		)
		self.assertEqual(bundle["success"], True)
		self.assertEqual(bundle["error"], None)
		self.assertEqual(bundle["initialized"], False)
		self.assertEqual(bundle["runtimeState"]["bank"], 125)
		self.assertIn("payloadKeys", bundle["schemaDescriptor"])
		self.assertEqual(bundle["compatibility"]["compatible"], True)
		self.assertEqual(bundle["features"]["autoCapture"], True)

	def testCreateHostStartupBundleCanInitializeGame(self):
		terminal = loadTerminalNamespace()
		bundle = terminal["createHostStartupBundle"](
			requiredApiVersion=terminal["engineApiVersion"],
			requiredFeatures=["structuredErrors"],
			startBank=600,
			selectedMode="2"
		)
		self.assertEqual(bundle["success"], True)
		self.assertEqual(bundle["initialized"], True)
		self.assertEqual(terminal["bank"], 600)
		self.assertEqual(terminal["gameMode"], terminal["GameMode"].craplessCraps)
		self.assertEqual(bundle["runtimeState"]["bank"], 600)

	def testCreateHostStartupBundleRejectsPartialInitArgs(self):
		terminal = loadTerminalNamespace()
		bundle = terminal["createHostStartupBundle"](startBank=300)
		self.assertEqual(bundle["success"], False)
		self.assertEqual(bundle["error"]["code"], terminal["hostErrorCodes"]["startupValidationFailed"])
		self.assertEqual(bundle["initialized"], False)

	def testCreateHostStartupBundleReturnsValidationErrorForBadInitValues(self):
		terminal = loadTerminalNamespace()
		bundle = terminal["createHostStartupBundle"](startBank=0, selectedMode="1")
		self.assertEqual(bundle["success"], False)
		self.assertEqual(bundle["error"]["code"], terminal["hostErrorCodes"]["startupValidationFailed"])
		self.assertEqual(bundle["error"]["details"]["exceptionType"], "ValueError")

	def testCreateHostStartupBundleIncludesCompatibilityFailureDetails(self):
		terminal = loadTerminalNamespace()
		bundle = terminal["createHostStartupBundle"](requiredApiVersion="9.9.9")
		self.assertEqual(bundle["success"], True)
		self.assertEqual(bundle["compatibility"]["compatible"], False)
		self.assertIn("Unsupported engineApiVersion requirement: 9.9.9", bundle["compatibility"]["reasons"])

	def testRunHardWaysMenuUsesReadInput(self):
		terminal = loadTerminalNamespace()
		prompts = []
		terminal["hardShow"] = lambda: None
		terminal["readInput"] = lambda promptText: prompts.append(promptText) or "x"
		with patch("builtins.print"):
			terminal["runHardWaysMenu"](pointPhase=False)
		self.assertIn("Hard Ways Bets? > ", prompts)

	def testLineBettingRejectsDontPassInCrapless(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craplessCraps
		terminal["lineBets"] = {"Pass": 0, "Pass Odds": 0, "Don't Pass": 0, "Don't Pass Odds": 0}
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 0
		inputs = iter(["d", "x"])
		writes = []
		terminal["readInput"] = lambda promptText: next(inputs)
		terminal["writeOutput"] = lambda message: writes.append(str(message))
		terminal["lineBetting"]()
		self.assertEqual(terminal["lineBets"]["Don't Pass"], 0)
		self.assertIn("Don't Pass is not available in Crapless Craps.", " ".join(writes))

	def testLineBettingUsesIoAdaptersForPassEntry(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craps
		terminal["lineBets"] = {"Pass": 0, "Pass Odds": 0, "Don't Pass": 0, "Don't Pass Odds": 0}
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 0
		inputs = iter(["p", "10", "x"])
		writes = []
		terminal["readInput"] = lambda promptText: next(inputs)
		terminal["writeOutput"] = lambda message: writes.append(str(message))
		terminal["lineBetting"]()
		self.assertEqual(terminal["lineBets"]["Pass"], 10)
		printed = " ".join(writes)
		self.assertIn("How much on the Pass Line?", printed)
		self.assertIn("Ok, $10 on the Pass Line.", printed)

	def testComeBettingInCraplessSkipsDontComeChoice(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craplessCraps
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 0
		terminal["comeBet"] = 0
		writes = []
		inputs = iter(["10"])
		terminal["writeOutput"] = lambda message: writes.append(str(message))
		terminal["readInput"] = lambda promptText: next(inputs)
		terminal["come"]()
		self.assertEqual(terminal["comeBet"], 10)
		self.assertEqual(terminal["bank"], 90)
		self.assertEqual(terminal["chipsOnTable"], 10)
		self.assertIn("How much on the Come?", " ".join(writes))
		self.assertNotIn("Come or Don't Come?", " ".join(writes))

	def testDpPhase2UsesIoAdaptersAndTakesDownBets(self):
		terminal = loadTerminalNamespace()
		terminal["lineBets"] = {"Pass": 0, "Pass Odds": 0, "Don't Pass": 15, "Don't Pass Odds": 30}
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 45
		writes = []
		terminal["writeOutput"] = lambda message: writes.append(str(message))
		terminal["readInput"] = lambda promptText: "y"
		terminal["dpPhase2"]()
		self.assertEqual(terminal["lineBets"]["Don't Pass"], 0)
		self.assertEqual(terminal["lineBets"]["Don't Pass Odds"], 0)
		self.assertEqual(terminal["bank"], 145)
		self.assertEqual(terminal["chipsOnTable"], 0)
		self.assertIn("Take down Don't Pass Bet and Odds?", " ".join(writes))
		self.assertIn("Ok, taking down your Don't Pass.", " ".join(writes))

	def testOddsCheckUsesWriteOutputAdapter(self):
		terminal = loadTerminalNamespace()
		terminal["lineBets"] = {"Pass": 0, "Pass Odds": 10, "Don't Pass": 0, "Don't Pass Odds": 0}
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 10
		terminal["comeOut"] = 5
		writes = []
		terminal["writeOutput"] = lambda message: writes.append(str(message))
		terminal["oddsCheck"](5)
		self.assertIn("You won $15 from your Pass Line Odds!", " ".join(writes))

	def testCashInUsesIoAdaptersAndRetriesInvalid(self):
		terminal = loadTerminalNamespace()
		terminal["bank"] = 0
		terminal["initBank"] = 0
		inputs = iter(["nope", "0", "250"])
		writes = []
		terminal["readInput"] = lambda promptText: next(inputs)
		terminal["writeOutput"] = lambda message: writes.append(str(message))
		terminal["cashIn"]()
		self.assertEqual(terminal["bank"], 250)
		self.assertEqual(terminal["initBank"], 250)
		printed = " ".join(writes)
		self.assertIn("How much are you cashing in for your bankroll?", printed)
		self.assertIn("That wasn't a number, doofus!", printed)
		self.assertIn("You won't get very far trying to play without any money, come on now...", printed)
		self.assertIn("Great, starting you off with $250.", printed)

	def testOutOfMoneyUsesIoAdaptersAndRejectsNegative(self):
		terminal = loadTerminalNamespace()
		terminal["bank"] = 100
		inputs = iter(["abc", "-5", "50"])
		writes = []
		terminal["readInput"] = lambda promptText: next(inputs)
		terminal["writeOutput"] = lambda message: writes.append(str(message))
		terminal["outOfMoney"]()
		self.assertEqual(terminal["bank"], 150)
		printed = " ".join(writes)
		self.assertIn("Your chips are getting really low.", printed)
		self.assertIn("You forgot what numbers were and the ATM beeps at you in annoyance.", printed)
		self.assertIn("This is for withdrawals only! Try again.", printed)
		self.assertIn("Alright, starting you off again with $150.", printed)

	def testBetPromptUsesIoAdaptersAndRetriesInvalid(self):
		terminal = loadTerminalNamespace()
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 0
		inputs = iter(["abc", "25"])
		writes = []
		terminal["readInput"] = lambda promptText: next(inputs)
		terminal["writeOutput"] = lambda message: writes.append(str(message))
		result = terminal["betPrompt"]()
		self.assertEqual(result, 25)
		self.assertEqual(terminal["bank"], 75)
		self.assertEqual(terminal["chipsOnTable"], 25)
		self.assertIn("That wasn't a number!", " ".join(writes))

	def testBetPromptInsufficientBankTriggersOutOfMoneyBranch(self):
		terminal = loadTerminalNamespace()
		terminal["bank"] = 50
		terminal["chipsOnTable"] = 0
		inputs = iter(["60", "y", "20"])
		terminal["readInput"] = lambda promptText: next(inputs)
		outCalls = []
		terminal["outOfMoney"] = lambda: outCalls.append(True)
		terminal["writeOutput"] = lambda message: None
		result = terminal["betPrompt"]()
		self.assertEqual(result, 20)
		self.assertEqual(outCalls, [True])

	def testValidPlaceNumbersInCraplessIncludesEdgeNumbers(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craplessCraps
		self.assertEqual(terminal["validPlaceNumbers"](), [2, 3, 4, 5, 6, 8, 9, 10, 11, 12])

	def testValidPlacePresetCodesForModeCraps(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craps
		self.assertEqual(terminal["validPlacePresetCodesForMode"](), ['a', 'i', 'c'])

	def testValidPlacePresetCodesForModeCrapless(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craplessCraps
		self.assertEqual(terminal["validPlacePresetCodesForMode"](), ['a', 'i', 'c', 'ea', 'e'])

	def testPlacePresetEdgeRejectedInCrapsNoMutation(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craps
		terminal["bank"] = 200
		terminal["chipsOnTable"] = 0
		terminal["place"] = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		with patch("builtins.print"):
			terminal["placePreset"]("e")
		self.assertEqual(terminal["place"], {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0})
		self.assertEqual(terminal["bank"], 200)
		self.assertEqual(terminal["chipsOnTable"], 0)

	def testPlacePresetExtremeAcrossRejectedInCrapsNoMutation(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craps
		terminal["bank"] = 200
		terminal["chipsOnTable"] = 0
		terminal["place"] = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		with patch("builtins.print"):
			terminal["placePreset"]("ea")
		self.assertEqual(terminal["place"], {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0})
		self.assertEqual(terminal["bank"], 200)
		self.assertEqual(terminal["chipsOnTable"], 0)

	def testPlaceHelpTextIsModeAware(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craps
		crapsHelp = terminal["placeHelpText"](pointPhase=False)
		self.assertNotIn("Extreme Across", crapsHelp)
		self.assertNotIn("edge numbers", crapsHelp)
		terminal["gameMode"] = terminal["GameMode"].craplessCraps
		craplessHelp = terminal["placeHelpText"](pointPhase=False)
		self.assertIn("Extreme Across", craplessHelp)
		self.assertIn("edge numbers", craplessHelp)

	def testHandlePlaceMenuCommandExit(self):
		terminal = loadTerminalNamespace()
		with patch("builtins.print"):
			result = terminal["handlePlaceMenuCommand"]("x", pointPhase=False)
		self.assertEqual(result["success"], True)
		self.assertEqual(result["stateChanged"], False)
		self.assertEqual(result["shouldExitMenu"], True)

	def testHandlePlaceMenuCommandPointTogglePlaceOff(self):
		terminal = loadTerminalNamespace()
		terminal["placeOff"] = False
		with patch("builtins.print"):
			result = terminal["handlePlaceMenuCommand"]("o", pointPhase=True)
		self.assertEqual(result["success"], True)
		self.assertEqual(result["stateChanged"], True)
		self.assertEqual(result["shouldExitMenu"], False)
		self.assertEqual(terminal["placeOff"], True)

	def testHandlePlaceMenuCommandPointOnlyIgnoredOnComeOut(self):
		terminal = loadTerminalNamespace()
		terminal["placeOff"] = False
		with patch("builtins.print"):
			result = terminal["handlePlaceMenuCommand"]("o", pointPhase=False)
		self.assertEqual(result["success"], False)
		self.assertEqual(result["stateChanged"], False)
		self.assertEqual(result["shouldExitMenu"], False)
		self.assertEqual(terminal["placeOff"], False)

	def testHandlePlaceMenuCommandInvalidNoMutation(self):
		terminal = loadTerminalNamespace()
		terminal["bank"] = 200
		terminal["chipsOnTable"] = 0
		terminal["place"] = {2: 0, 3: 0, 4: 5, 5: 5, 6: 6, 8: 6, 9: 5, 10: 5, 11: 0, 12: 0}
		with patch("builtins.print"):
			result = terminal["handlePlaceMenuCommand"]("zz", pointPhase=True)
		self.assertEqual(result["success"], False)
		self.assertEqual(result["stateChanged"], False)
		self.assertEqual(result["shouldExitMenu"], False)
		self.assertEqual(terminal["bank"], 200)
		self.assertEqual(terminal["chipsOnTable"], 0)
		self.assertEqual(terminal["place"], {2: 0, 3: 0, 4: 5, 5: 5, 6: 6, 8: 6, 9: 5, 10: 5, 11: 0, 12: 0})
		self.assertTrue(any("valid option" in msg for msg in result["messages"]))

	def testHandleLayMenuCommandExit(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craps
		with patch("builtins.print"):
			result = terminal["handleLayMenuCommand"]("x", pointPhase=False)
		self.assertEqual(result["success"], True)
		self.assertEqual(result["stateChanged"], False)
		self.assertEqual(result["shouldExitMenu"], True)

	def testHandleLayMenuCommandPointToggle(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craps
		terminal["layOff"] = False
		with patch("builtins.print"):
			result = terminal["handleLayMenuCommand"]("o", pointPhase=True)
		self.assertEqual(result["success"], True)
		self.assertEqual(result["stateChanged"], True)
		self.assertEqual(result["shouldExitMenu"], False)
		self.assertEqual(terminal["layOff"], True)

	def testHandleLayMenuCommandCraplessAllowsEntry(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craplessCraps
		calls = []
		terminal["layBetting"] = lambda: calls.append(True)
		with patch("builtins.print"):
			result = terminal["handleLayMenuCommand"]("y", pointPhase=True)
		self.assertEqual(result["success"], True)
		self.assertEqual(result["stateChanged"], True)
		self.assertEqual(result["shouldExitMenu"], False)
		self.assertEqual(calls, [True])

	def testHandleLayMenuCommandInvalidNoMutation(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craps
		terminal["layOff"] = False
		terminal["bank"] = 200
		terminal["chipsOnTable"] = 0
		terminal["layBets"] = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		with patch("builtins.print"):
			result = terminal["handleLayMenuCommand"]("zz", pointPhase=True)
		self.assertEqual(result["success"], False)
		self.assertEqual(result["stateChanged"], False)
		self.assertEqual(result["shouldExitMenu"], False)
		self.assertEqual(terminal["layOff"], False)
		self.assertEqual(terminal["bank"], 200)
		self.assertEqual(terminal["chipsOnTable"], 0)
		self.assertEqual(terminal["layBets"], {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0})

	def testHandleLayMenuCommandCraplessEdgeHelpers(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craplessCraps
		terminal["bank"] = 200
		terminal["chipsOnTable"] = 0
		terminal["layBets"] = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		terminal["readInput"] = lambda promptText: "1"
		terminal["writeOutput"] = lambda message: None
		with patch("builtins.print"):
			edgeResult = terminal["handleLayMenuCommand"]("e", pointPhase=True)
		self.assertEqual(edgeResult["success"], True)
		self.assertEqual(terminal["layBets"][2], 5)
		self.assertEqual(terminal["layBets"][3], 5)
		self.assertEqual(terminal["layBets"][11], 5)
		self.assertEqual(terminal["layBets"][12], 5)
		with patch("builtins.print"):
			extremeResult = terminal["handleLayMenuCommand"]("ea", pointPhase=True)
		self.assertEqual(extremeResult["success"], True)
		self.assertTrue(all(terminal["layBets"][number] == 5 for number in [2, 3, 4, 5, 6, 8, 9, 10, 11, 12]))

	def testHandleHardWaysMenuCommandExit(self):
		terminal = loadTerminalNamespace()
		with patch("builtins.print"):
			result = terminal["handleHardWaysMenuCommand"]("x", pointPhase=False)
		self.assertEqual(result["success"], True)
		self.assertEqual(result["stateChanged"], False)
		self.assertEqual(result["shouldExitMenu"], True)

	def testHandleHardWaysMenuCommandPointToggle(self):
		terminal = loadTerminalNamespace()
		terminal["hardOff"] = False
		with patch("builtins.print"):
			result = terminal["handleHardWaysMenuCommand"]("o", pointPhase=True)
		self.assertEqual(result["success"], True)
		self.assertEqual(result["stateChanged"], True)
		self.assertEqual(result["shouldExitMenu"], False)
		self.assertEqual(terminal["hardOff"], True)

	def testHandleHardWaysMenuCommandInvalidNoMutation(self):
		terminal = loadTerminalNamespace()
		terminal["hardOff"] = False
		terminal["bank"] = 200
		terminal["chipsOnTable"] = 0
		terminal["hardWays"] = {4: 5, 6: 0, 8: 0, 10: 0}
		with patch("builtins.print"):
			result = terminal["handleHardWaysMenuCommand"]("zz", pointPhase=True)
		self.assertEqual(result["success"], False)
		self.assertEqual(result["stateChanged"], False)
		self.assertEqual(result["shouldExitMenu"], False)
		self.assertEqual(terminal["hardOff"], False)
		self.assertEqual(terminal["bank"], 200)
		self.assertEqual(terminal["chipsOnTable"], 0)
		self.assertEqual(terminal["hardWays"], {4: 5, 6: 0, 8: 0, 10: 0})

	def testHandleBettingCommandRoutesPlaceMenuInComeOut(self):
		terminal = loadTerminalNamespace()
		calls = []
		def fakeRunPlaceMenu(pointPhase=False):
			calls.append(pointPhase)
		terminal["runPlaceMenu"] = fakeRunPlaceMenu
		with patch("builtins.print"):
			result = terminal["handleBettingCommand"]("p", pointPhase=False)
		self.assertEqual(result.shouldRoll, False)
		self.assertEqual(calls, [False])

	def testHandleBettingCommandRoutesPlaceMenuInPointPhase(self):
		terminal = loadTerminalNamespace()
		calls = []
		def fakeRunPlaceMenu(pointPhase=False):
			calls.append(pointPhase)
		terminal["runPlaceMenu"] = fakeRunPlaceMenu
		with patch("builtins.print"):
			result = terminal["handleBettingCommand"]("p", pointPhase=True)
		self.assertEqual(result.shouldRoll, False)
		self.assertEqual(calls, [True])

	def testRunPlaceMenuUsesReadInputAdapter(self):
		terminal = loadTerminalNamespace()
		seenCommands = []
		terminal["placeShow"] = lambda: None
		terminal["readInput"] = lambda promptText: "x"
		terminal["handlePlaceMenuCommand"] = lambda placeCommand, pointPhase=False: seenCommands.append((placeCommand, pointPhase)) or {"success": True, "messages": [], "stateChanged": False, "shouldExitMenu": True}
		terminal["emitActionResult"] = lambda actionResult: None
		terminal["runPlaceMenu"](pointPhase=True)
		self.assertEqual(seenCommands, [("x", True)])

	def testHandleBettingCommandPointRollReturnsTrue(self):
		terminal = loadTerminalNamespace()
		with patch("builtins.print"):
			result = terminal["handleBettingCommand"]("x", pointPhase=True)
		self.assertEqual(result.shouldRoll, True)

	def testHandleBettingCommandSyncsRuntimeOnNoStateChangePath(self):
		terminal = loadTerminalNamespace()
		terminal["throws"] = 5
		terminal["comeOut"] = 8
		terminal["gameRuntime"] = terminal["GameRuntime"](
			bank=terminal["bank"],
			chipsOnTable=terminal["chipsOnTable"],
			throws=1,
			comeOut=4,
			pointIsOn=terminal["pointIsOn"],
			p2=terminal["p2"],
			gameMode=terminal["gameMode"]
		)
		with patch("builtins.print"):
			result = terminal["handleBettingCommand"]("x", pointPhase=True)
		self.assertEqual(result.shouldRoll, True)
		self.assertEqual(terminal["gameRuntime"].throws, 5)
		self.assertEqual(terminal["gameRuntime"].comeOut, 8)

	def testHandleBettingCommandPointOddsWithoutLineBet(self):
		terminal = loadTerminalNamespace()
		terminal["lineBets"] = {"Pass": 0, "Pass Odds": 0, "Don't Pass": 0, "Don't Pass Odds": 0}
		with patch("builtins.print") as mockPrint:
			result = terminal["handleBettingCommand"]("o", pointPhase=True)
		self.assertEqual(result.shouldRoll, False)
		printed = "\n".join(str(args[0]) for args, _ in mockPrint.call_args_list if args)
		self.assertIn("You don't have a Line bet, silly!", printed)

	def testHandleBettingCommandBlocksDcdInCraplessAndRefundsLegacyDontCome(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craplessCraps
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 27
		terminal["dComeBet"] = 5
		terminal["dComeBets"] = {2: 0, 3: 0, 4: 0, 5: 10, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		terminal["dComeOdds"] = {2: 0, 3: 0, 4: 0, 5: 12, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		with patch("builtins.print") as mockPrint:
			result = terminal["handleBettingCommand"]("dcd", pointPhase=True)
		self.assertEqual(result.shouldRoll, False)
		self.assertEqual(terminal["dComeBet"], 0)
		self.assertEqual(sum(terminal["dComeBets"].values()), 0)
		self.assertEqual(sum(terminal["dComeOdds"].values()), 0)
		self.assertEqual(terminal["bank"], 127)
		self.assertEqual(terminal["chipsOnTable"], 0)
		printed = "\n".join(str(args[0]) for args, _ in mockPrint.call_args_list if args)
		self.assertIn("Don't Come is not available in Crapless Craps.", printed)

	def testHandleBettingCommandBbCallsOutOfMoneyComeOut(self):
		terminal = loadTerminalNamespace()
		calls = []
		terminal["outOfMoney"] = lambda: calls.append(True) or terminal.__setitem__("bank", 150)
		with patch("builtins.print"):
			result = terminal["handleBettingCommand"]("bb", pointPhase=False)
		self.assertEqual(result.shouldRoll, False)
		self.assertEqual(calls, [True])
		self.assertEqual(terminal["gameRuntime"].bank, 150)

	def testHandleBettingCommandBbCallsOutOfMoneyPointPhase(self):
		terminal = loadTerminalNamespace()
		calls = []
		terminal["outOfMoney"] = lambda: calls.append(True)
		with patch("builtins.print"):
			result = terminal["handleBettingCommand"]("bb", pointPhase=True)
		self.assertEqual(result.shouldRoll, False)
		self.assertEqual(calls, [True])

	def testSubmitCommandReturnsNormalizedPayload(self):
		terminal = loadTerminalNamespace()
		payload = terminal["submitCommand"]("x", pointPhase=True)
		self.assertEqual(payload["command"], "x")
		self.assertEqual(payload["pointPhase"], True)
		self.assertEqual(payload["shouldRoll"], True)
		self.assertEqual(payload["handled"], True)
		self.assertIn("runtimeState", payload)
		self.assertIn("capturedOutput", payload)
		self.assertIn("capturedPrompts", payload)
		self.assertEqual(payload["engineApiVersion"], terminal["engineApiVersion"])

	def testSubmitCommandReturnsUnhandledPayload(self):
		terminal = loadTerminalNamespace()
		payload = terminal["submitCommand"]("notACommand", pointPhase=False)
		self.assertEqual(payload["command"], "notacommand")
		self.assertEqual(payload["pointPhase"], False)
		self.assertEqual(payload["shouldRoll"], False)
		self.assertEqual(payload["handled"], False)
		self.assertIn("runtimeState", payload)
		self.assertIn("capturedOutput", payload)
		self.assertIn("capturedPrompts", payload)

	def testSubmitCommandEmitsCommandProcessedEvent(self):
		terminal = loadTerminalNamespace()
		events = []
		terminal["setEventHandler"](lambda eventName, payload: events.append((eventName, payload)))
		payload = terminal["submitCommand"]("x", pointPhase=False)
		self.assertEqual(len(events), 1)
		self.assertEqual(events[0][0], terminal["hostEventNames"]["commandProcessed"])
		self.assertEqual(events[0][1]["command"], "x")
		self.assertEqual(events[0][1]["shouldRoll"], True)
		self.assertEqual(events[0][1]["handled"], True)
		self.assertEqual(events[0][1], payload)
		self.assertEqual(events[0][1]["engineApiVersion"], terminal["engineApiVersion"])
		terminal["resetEventHandler"]()

	def testOutputCaptureBuffersWriteOutputWhenEnabled(self):
		terminal = loadTerminalNamespace()
		terminal["setIoHandlers"](outputFunc=lambda message: None)
		terminal["beginOutputCapture"]()
		terminal["writeOutput"]("alpha")
		terminal["writeOutput"]("beta")
		capturedOutput = terminal["getCapturedOutput"]()
		self.assertEqual(capturedOutput, ["alpha", "beta"])
		terminal["endOutputCapture"]()
		terminal["resetIoHandlers"]()

	def testPromptCaptureBuffersReadInputPromptWhenEnabled(self):
		terminal = loadTerminalNamespace()
		terminal["setIoHandlers"](inputFunc=lambda promptText: "ok")
		terminal["beginPromptCapture"]()
		response = terminal["readInput"]("Prompt > ")
		self.assertEqual(response, "ok")
		self.assertEqual(terminal["getCapturedPrompts"](), ["Prompt > "])
		terminal["endPromptCapture"]()
		terminal["resetIoHandlers"]()

	def testReadInputEmitsInputRequestedEvent(self):
		terminal = loadTerminalNamespace()
		events = []
		terminal["setIoHandlers"](inputFunc=lambda promptText: "y")
		terminal["setEventHandler"](lambda eventName, payload: events.append((eventName, payload)))
		response = terminal["readInput"]("Bankroll? > ")
		self.assertEqual(response, "y")
		self.assertEqual(events[0][0], terminal["hostEventNames"]["inputRequested"])
		self.assertEqual(events[0][1]["prompt"], "Bankroll? > ")
		terminal["resetEventHandler"]()
		terminal["resetIoHandlers"]()

	def testSubmitCommandIncludesCapturedOutputWhenCaptureEnabled(self):
		terminal = loadTerminalNamespace()
		terminal["beginOutputCapture"]()
		payload = terminal["submitCommand"]("x", pointPhase=False)
		self.assertTrue(len(payload["capturedOutput"]) >= 1)
		self.assertIn("Rolling the dice!", " ".join(payload["capturedOutput"]))
		terminal["endOutputCapture"]()

	def testSubmitCommandIncludesCapturedPromptsWhenCaptureEnabled(self):
		terminal = loadTerminalNamespace()
		terminal["bank"] = 100
		inputs = iter(["y", "10"])
		terminal["setIoHandlers"](inputFunc=lambda promptText: next(inputs))
		terminal["beginPromptCapture"]()
		payload = terminal["submitCommand"]("f", pointPhase=False)
		self.assertTrue(len(payload["capturedPrompts"]) >= 1)
		self.assertIn("Field Bet? > ", payload["capturedPrompts"])
		terminal["endPromptCapture"]()
		terminal["resetIoHandlers"]()

	def testRunWithCaptureCapturesAndRestoresState(self):
		terminal = loadTerminalNamespace()
		terminal["setIoHandlers"](outputFunc=lambda message: None, inputFunc=lambda promptText: "done")
		captureResult = terminal["runWithCapture"](lambda: (terminal["writeOutput"]("hello"), terminal["readInput"]("Prompt > ")))
		self.assertIn("hello", captureResult["capturedOutput"])
		self.assertIn("Prompt > ", captureResult["capturedPrompts"])
		self.assertEqual(terminal["outputCaptureOn"], False)
		self.assertEqual(terminal["promptCaptureOn"], False)
		self.assertEqual(terminal["getCapturedOutput"](), [])
		self.assertEqual(terminal["getCapturedPrompts"](), [])
		terminal["resetIoHandlers"]()

	def testRunWithCaptureRestoresStateAfterException(self):
		terminal = loadTerminalNamespace()
		with self.assertRaises(RuntimeError):
			terminal["runWithCapture"](lambda: (_ for _ in ()).throw(RuntimeError("boom")))
		self.assertEqual(terminal["outputCaptureOn"], False)
		self.assertEqual(terminal["promptCaptureOn"], False)

	def testSubmitCommandAutoCaptureIncludesOutputAndPrompts(self):
		terminal = loadTerminalNamespace()
		terminal["bank"] = 100
		inputs = iter(["y", "10"])
		terminal["setIoHandlers"](inputFunc=lambda promptText: next(inputs))
		payload = terminal["submitCommand"]("f", pointPhase=False, autoCapture=True)
		self.assertIn("How much on the Field?", " ".join(payload["capturedOutput"]))
		self.assertIn("Field Bet? > ", payload["capturedPrompts"])
		self.assertIn("$>", " ".join(payload["capturedPrompts"]))
		terminal["resetIoHandlers"]()

	def testStepCommandReturnsNormalizedPayload(self):
		terminal = loadTerminalNamespace()
		stepPayload = terminal["step"](commandText="x", pointPhase=True)
		self.assertEqual(stepPayload["stepType"], "command")
		self.assertEqual(stepPayload["success"], True)
		self.assertEqual(stepPayload["error"], None)
		self.assertEqual(stepPayload["commandResult"]["command"], "x")
		self.assertEqual(stepPayload["commandResult"]["pointPhase"], True)
		self.assertEqual(stepPayload["commandResult"]["shouldRoll"], True)
		self.assertEqual(stepPayload["cycleResult"], None)
		self.assertIn("runtimeState", stepPayload)
		self.assertIn("capturedOutput", stepPayload)
		self.assertIn("capturedPrompts", stepPayload)
		self.assertEqual(stepPayload["engineApiVersion"], terminal["engineApiVersion"])

	def testStepCycleReturnsNormalizedPayload(self):
		terminal = loadTerminalNamespace()
		terminal["runOneCycle"] = lambda: {
			"enteredPointPhase": False,
			"comeOutOutcome": terminal["RollOutcome"].natural,
			"pointPhaseOutcome": None,
			"pointRoundEnded": False,
			"point": 0,
			"throws": 1
		}
		stepPayload = terminal["step"]()
		self.assertEqual(stepPayload["stepType"], "cycle")
		self.assertEqual(stepPayload["success"], True)
		self.assertEqual(stepPayload["error"], None)
		self.assertEqual(stepPayload["commandResult"], None)
		self.assertEqual(stepPayload["cycleResult"]["enteredPointPhase"], False)
		self.assertIn("runtimeState", stepPayload)
		self.assertIn("capturedOutput", stepPayload)
		self.assertIn("capturedPrompts", stepPayload)
		self.assertEqual(stepPayload["engineApiVersion"], terminal["engineApiVersion"])

	def testStepAutoCaptureCycleIncludesCapturedOutput(self):
		terminal = loadTerminalNamespace()
		terminal["runOneCycle"] = lambda: (terminal["writeOutput"]("cycle message"), {
			"enteredPointPhase": False,
			"comeOutOutcome": terminal["RollOutcome"].natural,
			"pointPhaseOutcome": None,
			"pointRoundEnded": False,
			"point": 0,
			"throws": 1
		})[1]
		stepPayload = terminal["step"](autoCapture=True)
		self.assertIn("cycle message", " ".join(stepPayload["capturedOutput"]))

	def testStepEmitsStepCompletedEvent(self):
		terminal = loadTerminalNamespace()
		events = []
		terminal["setEventHandler"](lambda eventName, payload: events.append((eventName, payload)))
		stepPayload = terminal["step"](commandText="x", pointPhase=False)
		self.assertEqual(len(events), 2)
		self.assertEqual(events[0][0], terminal["hostEventNames"]["commandProcessed"])
		self.assertEqual(events[1][0], terminal["hostEventNames"]["stepCompleted"])
		self.assertEqual(events[1][1], stepPayload)
		terminal["resetEventHandler"]()

	def testStepRejectsPointPhaseWithoutCommand(self):
		terminal = loadTerminalNamespace()
		stepPayload = terminal["step"](pointPhase=True)
		self.assertEqual(stepPayload["success"], False)
		self.assertEqual(stepPayload["error"]["code"], terminal["hostErrorCodes"]["invalidStepArguments"])
		self.assertEqual(stepPayload["error"]["message"], "pointPhase can only be used with commandText.")
		self.assertEqual(stepPayload["cycleResult"], None)

	def testStepPointPhaseWithoutCommandRaisesWhenConfigured(self):
		terminal = loadTerminalNamespace()
		with self.assertRaises(ValueError):
			terminal["step"](pointPhase=True, raiseOnError=True)

	def testHostErrorCodesExposeExpectedContractValues(self):
		terminal = loadTerminalNamespace()
		self.assertEqual(terminal["hostErrorCodes"]["invalidStepArguments"], "invalidStepArguments")
		self.assertEqual(terminal["hostErrorCodes"]["commandExecutionFailed"], "commandExecutionFailed")
		self.assertEqual(terminal["hostErrorCodes"]["cycleExecutionFailed"], "cycleExecutionFailed")
		self.assertEqual(terminal["hostErrorCodes"]["startupValidationFailed"], "startupValidationFailed")

	def testHostEventNamesExposeExpectedContractValues(self):
		terminal = loadTerminalNamespace()
		self.assertEqual(terminal["hostEventNames"]["inputRequested"], "inputRequested")
		self.assertEqual(terminal["hostEventNames"]["commandProcessed"], "commandProcessed")
		self.assertEqual(terminal["hostEventNames"]["stepCompleted"], "stepCompleted")
		self.assertEqual(terminal["hostEventNames"]["cycleCompleted"], "cycleCompleted")

	def testBuildCycleCompletedEventPayloadIncludesCanonicalKeys(self):
		terminal = loadTerminalNamespace()
		payload = terminal["buildCycleCompletedEventPayload"](
			cycleResult={"enteredPointPhase": False},
			runtimeState={"bank": 10}
		)
		self.assertEqual(payload["cycleResult"]["enteredPointPhase"], False)
		self.assertEqual(payload["runtimeState"]["bank"], 10)
		self.assertEqual(payload["engineApiVersion"], terminal["engineApiVersion"])

	def testBuildHostCommandPayloadIncludesCanonicalKeys(self):
		terminal = loadTerminalNamespace()
		payload = terminal["buildHostCommandPayload"](
			command="x",
			pointPhase=False,
			shouldRoll=True,
			handled=True,
			runtimeState={"bank": 10},
			capturedOutput=["line1"],
			capturedPrompts=["prompt1"],
			success=True,
			error=None
		)
		self.assertEqual(payload["command"], "x")
		self.assertEqual(payload["success"], True)
		self.assertEqual(payload["error"], None)
		self.assertEqual(payload["capturedOutput"], ["line1"])
		self.assertEqual(payload["capturedPrompts"], ["prompt1"])
		self.assertEqual(payload["engineApiVersion"], terminal["engineApiVersion"])

	def testBuildHostStepPayloadIncludesCanonicalKeys(self):
		terminal = loadTerminalNamespace()
		payload = terminal["buildHostStepPayload"](
			stepType="cycle",
			commandResult=None,
			cycleResult={"enteredPointPhase": False},
			runtimeState={"bank": 10},
			capturedOutput=["line1"],
			capturedPrompts=["prompt1"],
			success=True,
			error=None
		)
		self.assertEqual(payload["stepType"], "cycle")
		self.assertEqual(payload["success"], True)
		self.assertEqual(payload["error"], None)
		self.assertEqual(payload["cycleResult"]["enteredPointPhase"], False)
		self.assertEqual(payload["engineApiVersion"], terminal["engineApiVersion"])

	def testHostSchemaDescriptorIncludesExpectedSections(self):
		terminal = loadTerminalNamespace()
		descriptor = terminal["hostSchemaDescriptor"]()
		self.assertEqual(descriptor["engineApiVersion"], terminal["engineApiVersion"])
		self.assertEqual(descriptor["schemaVersion"], "1")
		self.assertIn("errorCodes", descriptor)
		self.assertIn("eventNames", descriptor)
		self.assertIn("features", descriptor)
		self.assertIn("payloadKeys", descriptor)
		self.assertIn("command", descriptor["payloadKeys"])
		self.assertIn("step", descriptor["payloadKeys"])
		self.assertIn("sessionBundle", descriptor["payloadKeys"])
		self.assertIn("startupBundle", descriptor["payloadKeys"])
		self.assertIn("allowedCommands", descriptor["payloadKeys"])
		self.assertIn("events", descriptor["payloadKeys"])
		self.assertIn("cycleCompleted", descriptor["payloadKeys"]["events"])

	def testHostAllowedCommandsComeOutCrapsIncludesDontComeTakeDown(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craps
		payload = terminal["hostAllowedCommands"](pointPhase=False)
		commandsByCode = {item["code"]: item for item in payload["commands"]}
		self.assertEqual(payload["pointPhase"], False)
		self.assertIn("l", commandsByCode)
		self.assertIn("dcd", commandsByCode)
		self.assertEqual(commandsByCode["dcd"]["enabled"], True)

	def testHostAllowedCommandsComeOutCraplessDisablesDontComeTakeDown(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craplessCraps
		payload = terminal["hostAllowedCommands"](pointPhase=False)
		commandsByCode = {item["code"]: item for item in payload["commands"]}
		self.assertIn("dcd", commandsByCode)
		self.assertEqual(commandsByCode["dcd"]["enabled"], False)
		self.assertIn("Not available in Crapless Craps", commandsByCode["dcd"]["reason"])

	def testHostAllowedCommandsPointPhaseIncludesOddsAndCome(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craps
		payload = terminal["hostAllowedCommands"](pointPhase=True)
		commandsByCode = {item["code"]: item for item in payload["commands"]}
		self.assertEqual(payload["pointPhase"], True)
		self.assertIn("o", commandsByCode)
		self.assertIn("c", commandsByCode)
		self.assertIn("dp", commandsByCode)

	def testBuildGameInitializedEventPayloadIncludesCanonicalKeys(self):
		terminal = loadTerminalNamespace()
		payload = terminal["buildGameInitializedEventPayload"](
			startBank=500,
			mode=terminal["GameMode"].craps,
			runtimeState={"bank": 500}
		)
		self.assertEqual(payload["startBank"], 500)
		self.assertEqual(payload["runtimeState"]["bank"], 500)
		self.assertEqual(payload["engineApiVersion"], terminal["engineApiVersion"])

	def testCheckHostCompatibilityPassesForCurrentVersionAndFeatures(self):
		terminal = loadTerminalNamespace()
		result = terminal["checkHostCompatibility"](
			requiredApiVersion=terminal["engineApiVersion"],
			requiredFeatures=["autoCapture", "sessionBundle", "structuredErrors"]
		)
		self.assertEqual(result["compatible"], True)
		self.assertEqual(result["missingFeatures"], [])
		self.assertEqual(result["reasons"], [])
		self.assertEqual(result["engineApiVersion"], terminal["engineApiVersion"])

	def testCheckHostCompatibilityFailsForUnsupportedVersion(self):
		terminal = loadTerminalNamespace()
		result = terminal["checkHostCompatibility"](requiredApiVersion="9.9.9")
		self.assertEqual(result["compatible"], False)
		self.assertIn("Unsupported engineApiVersion requirement: 9.9.9", result["reasons"])

	def testCheckHostCompatibilityFailsForMissingFeature(self):
		terminal = loadTerminalNamespace()
		result = terminal["checkHostCompatibility"](requiredFeatures=["nonexistentFeature"])
		self.assertEqual(result["compatible"], False)
		self.assertEqual(result["missingFeatures"], ["nonexistentFeature"])
		self.assertIn("Missing required features: nonexistentFeature", result["reasons"])

	def testSubmitCommandReturnsStructuredErrorPayloadOnFailure(self):
		terminal = loadTerminalNamespace()
		terminal["handleBettingCommand"] = lambda commandText, pointPhase=False: (_ for _ in ()).throw(RuntimeError("forced command fail"))
		payload = terminal["submitCommand"]("x", pointPhase=False)
		self.assertEqual(payload["success"], False)
		self.assertEqual(payload["error"]["code"], terminal["hostErrorCodes"]["commandExecutionFailed"])
		self.assertEqual(payload["error"]["details"]["exceptionType"], "RuntimeError")
		self.assertEqual(payload["shouldRoll"], False)
		self.assertEqual(payload["handled"], False)

	def testStepReturnsStructuredCycleErrorPayloadOnFailure(self):
		terminal = loadTerminalNamespace()
		terminal["runOneCycle"] = lambda: (_ for _ in ()).throw(RuntimeError("forced cycle fail"))
		stepPayload = terminal["step"]()
		self.assertEqual(stepPayload["success"], False)
		self.assertEqual(stepPayload["error"]["code"], terminal["hostErrorCodes"]["cycleExecutionFailed"])
		self.assertEqual(stepPayload["cycleResult"], None)

	def testResolveComeOutRollNaturalResetsThrowCount(self):
		terminal = loadTerminalNamespace()
		terminal["atsOn"] = False
		terminal["working"] = True
		terminal["throws"] = 8
		terminal["pointIsOn"] = False
		terminal["comeOut"] = 0
		terminal["p2"] = 0
		terminal["roll"] = lambda: 7
		terminal["evaluateRoll"] = lambda gameState, rollValue: terminal["RollOutcome"].natural
		terminal["comeCheck"] = lambda rollValue: None
		terminal["layCheck"] = lambda rollValue: None
		terminal["fieldCheck"] = lambda rollValue: None
		terminal["placeCheck"] = lambda rollValue: None
		terminal["hardCheck"] = lambda rollValue: None
		terminal["propPay"] = lambda rollValue: None
		lineCalls = []
		terminal["lineCheck"] = lambda comeRoll, p2Roll: lineCalls.append((comeRoll, p2Roll))
		result = terminal["resolveComeOutRoll"]()
		self.assertEqual(result.enteredPointPhase, False)
		self.assertEqual(terminal["throws"], 0)
		self.assertEqual(terminal["working"], False)
		self.assertEqual(lineCalls, [(7, 0)])

	def testResolveComeOutRollPointEstablished(self):
		terminal = loadTerminalNamespace()
		terminal["atsOn"] = False
		terminal["working"] = True
		terminal["throws"] = 2
		terminal["pointIsOn"] = False
		terminal["comeOut"] = 0
		terminal["roll"] = lambda: 6
		terminal["evaluateRoll"] = lambda gameState, rollValue: terminal["RollOutcome"].pointEstablished
		terminal["comeCheck"] = lambda rollValue: None
		terminal["layCheck"] = lambda rollValue: None
		terminal["fieldCheck"] = lambda rollValue: None
		terminal["placeCheck"] = lambda rollValue: None
		terminal["hardCheck"] = lambda rollValue: None
		terminal["propPay"] = lambda rollValue: None
		terminal["lineCheck"] = lambda comeRoll, p2Roll: None
		result = terminal["resolveComeOutRoll"]()
		self.assertEqual(result.enteredPointPhase, True)
		self.assertEqual(terminal["pointIsOn"], True)
		self.assertEqual(terminal["working"], False)
		self.assertEqual(terminal["comeOut"], 6)

	def testResolveComeOutRollSyncsGameRuntimeOnReturn(self):
		terminal = loadTerminalNamespace()
		terminal["atsOn"] = False
		terminal["working"] = True
		terminal["throws"] = 8
		terminal["pointIsOn"] = False
		terminal["comeOut"] = 0
		terminal["p2"] = 0
		terminal["gameRuntime"] = terminal["GameRuntime"](
			bank=terminal["bank"],
			chipsOnTable=terminal["chipsOnTable"],
			throws=1,
			comeOut=0,
			pointIsOn=False,
			p2=0,
			gameMode=terminal["gameMode"]
		)
		terminal["roll"] = lambda: 6
		terminal["evaluateRoll"] = lambda gameState, rollValue: terminal["RollOutcome"].pointEstablished
		terminal["comeCheck"] = lambda rollValue: None
		terminal["layCheck"] = lambda rollValue: None
		terminal["fieldCheck"] = lambda rollValue: None
		terminal["placeCheck"] = lambda rollValue: None
		terminal["hardCheck"] = lambda rollValue: None
		terminal["propPay"] = lambda rollValue: None
		terminal["lineCheck"] = lambda comeRoll, p2Roll: None
		result = terminal["resolveComeOutRoll"]()
		self.assertEqual(result.enteredPointPhase, True)
		self.assertEqual(terminal["throws"], 9)
		self.assertEqual(terminal["gameRuntime"].throws, 9)
		self.assertEqual(terminal["comeOut"], 6)
		self.assertEqual(terminal["gameRuntime"].comeOut, 6)

	def testResolvePointRollSevenOutEndsPoint(self):
		terminal = loadTerminalNamespace()
		terminal["atsOn"] = False
		terminal["fireBet"] = 0
		terminal["throws"] = 3
		terminal["pointIsOn"] = True
		terminal["comeOut"] = 8
		terminal["p2"] = 0
		terminal["placeOff"] = False
		terminal["layOff"] = False
		terminal["hardOff"] = False
		terminal["roll"] = lambda: 7
		terminal["evaluateRoll"] = lambda gameState, rollValue: terminal["RollOutcome"].sevenOut
		terminal["comeCheck"] = lambda rollValue: None
		terminal["placeCheck"] = lambda rollValue: None
		terminal["layCheck"] = lambda rollValue: None
		terminal["fieldCheck"] = lambda rollValue: None
		terminal["hardCheck"] = lambda rollValue: None
		terminal["lineCheck"] = lambda pointNumber, rollValue: None
		terminal["propPay"] = lambda rollValue: None
		result = terminal["resolvePointRoll"]()
		self.assertEqual(result.pointRoundEnded, True)
		self.assertEqual(terminal["pointIsOn"], False)
		self.assertEqual(terminal["throws"], 0)

	def testResolvePointRollNeutralContinuesPoint(self):
		terminal = loadTerminalNamespace()
		terminal["atsOn"] = False
		terminal["fireBet"] = 0
		terminal["throws"] = 3
		terminal["pointIsOn"] = True
		terminal["comeOut"] = 8
		terminal["p2"] = 0
		terminal["placeOff"] = True
		terminal["layOff"] = True
		terminal["hardOff"] = True
		terminal["roll"] = lambda: 5
		terminal["evaluateRoll"] = lambda gameState, rollValue: terminal["RollOutcome"].neutral
		terminal["comeCheck"] = lambda rollValue: None
		terminal["placeCheck"] = lambda rollValue: None
		terminal["layCheck"] = lambda rollValue: None
		terminal["fieldCheck"] = lambda rollValue: None
		terminal["hardCheck"] = lambda rollValue: None
		terminal["lineCheck"] = lambda pointNumber, rollValue: None
		terminal["propPay"] = lambda rollValue: None
		result = terminal["resolvePointRoll"]()
		self.assertEqual(result.pointRoundEnded, False)
		self.assertEqual(terminal["pointIsOn"], True)
		self.assertEqual(terminal["throws"], 4)
		self.assertEqual(terminal["placeOff"], False)
		self.assertEqual(terminal["layOff"], False)
		self.assertEqual(terminal["hardOff"], False)

	def testResolvePointRollSyncsGameRuntimeOnReturn(self):
		terminal = loadTerminalNamespace()
		terminal["atsOn"] = False
		terminal["fireBet"] = 0
		terminal["throws"] = 10
		terminal["pointIsOn"] = True
		terminal["comeOut"] = 8
		terminal["p2"] = 0
		terminal["placeOff"] = True
		terminal["layOff"] = True
		terminal["hardOff"] = True
		terminal["gameRuntime"] = terminal["GameRuntime"](
			bank=terminal["bank"],
			chipsOnTable=terminal["chipsOnTable"],
			throws=1,
			comeOut=4,
			pointIsOn=False,
			p2=0,
			gameMode=terminal["gameMode"]
		)
		terminal["roll"] = lambda: 5
		terminal["evaluateRoll"] = lambda gameState, rollValue: terminal["RollOutcome"].neutral
		terminal["comeCheck"] = lambda rollValue: None
		terminal["placeCheck"] = lambda rollValue: None
		terminal["layCheck"] = lambda rollValue: None
		terminal["fieldCheck"] = lambda rollValue: None
		terminal["hardCheck"] = lambda rollValue: None
		lineCalls = []
		terminal["lineCheck"] = lambda pointNumber, rollValue: lineCalls.append((pointNumber, rollValue))
		terminal["propPay"] = lambda rollValue: None
		result = terminal["resolvePointRoll"]()
		self.assertEqual(result.pointRoundEnded, False)
		self.assertEqual(terminal["throws"], 11)
		self.assertEqual(terminal["gameRuntime"].throws, 11)
		self.assertEqual(terminal["comeOut"], 8)
		self.assertEqual(terminal["gameRuntime"].comeOut, 8)
		self.assertEqual(lineCalls, [(8, 5)])

	def testResolvePointRollPointHitUsesWriteOutput(self):
		terminal = loadTerminalNamespace()
		terminal["atsOn"] = False
		terminal["fireBet"] = 0
		terminal["throws"] = 3
		terminal["pointIsOn"] = True
		terminal["comeOut"] = 8
		terminal["p2"] = 0
		terminal["placeOff"] = False
		terminal["layOff"] = False
		terminal["hardOff"] = False
		terminal["roll"] = lambda: 8
		terminal["evaluateRoll"] = lambda gameState, rollValue: terminal["RollOutcome"].pointHit
		terminal["comeCheck"] = lambda rollValue: None
		terminal["placeCheck"] = lambda rollValue: None
		terminal["layCheck"] = lambda rollValue: None
		terminal["fieldCheck"] = lambda rollValue: None
		terminal["hardCheck"] = lambda rollValue: None
		terminal["lineCheck"] = lambda pointNumber, rollValue: None
		terminal["propPay"] = lambda rollValue: None
		writes = []
		terminal["writeOutput"] = lambda message: writes.append(str(message))
		with patch("builtins.print") as mockPrint:
			result = terminal["resolvePointRoll"]()
		self.assertEqual(result.pointRoundEnded, True)
		self.assertEqual(mockPrint.call_count, 0)
		self.assertIn("Point Hit! Front line winner!", " ".join(writes))

	def testRollUsesWriteOutputForHardWayCall(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craps
		terminal["pointIsOn"] = False
		terminal["rollDice"] = lambda: type("diceResult", (), {"die1": 3, "die2": 3, "total": 6})()
		terminal["stickman"] = lambda rollValue: "hard call"
		writes = []
		terminal["writeOutput"] = lambda message: writes.append(str(message))
		with patch("builtins.print") as mockPrint:
			rollTotal = terminal["roll"]()
		self.assertEqual(rollTotal, 6)
		self.assertEqual(mockPrint.call_count, 0)
		self.assertIn("6 the Hard Way!", " ".join(writes))
		self.assertIn("hard call", " ".join(writes))

	def testQuitGameUsesWriteOutput(self):
		terminal = loadTerminalNamespace()
		terminal["bank"] = 120
		terminal["chipsOnTable"] = 0
		terminal["initBank"] = 100
		writes = []
		terminal["writeOutput"] = lambda message: writes.append(str(message))
		with patch("builtins.print") as mockPrint:
			with self.assertRaises(SystemExit):
				terminal["quitGame"]()
		self.assertEqual(mockPrint.call_count, 0)
		self.assertIn("Nice work coloring up! Come back soon!", " ".join(writes))

	def testRunPointPhaseBettingMenuLoopsUntilRollCommand(self):
		terminal = loadTerminalNamespace()
		calls = []
		def fakeStep(commandText=None, pointPhase=False):
			calls.append((commandText, pointPhase))
			return {
				"stepType": "command",
				"commandResult": {
					"command": commandText,
					"pointPhase": pointPhase,
					"shouldRoll": (commandText == "x"),
					"handled": True,
					"runtimeState": {}
				},
				"cycleResult": None,
				"runtimeState": {}
			}
		terminal["step"] = fakeStep
		inputs = iter(["h", "x"])
		terminal["readInput"] = lambda promptText: next(inputs)
		terminal["writeOutput"] = lambda message: None
		result = terminal["runPointPhaseBettingMenu"]()
		self.assertEqual(result["shouldRoll"], True)
		self.assertEqual(calls, [("h", True), ("x", True)])

	def testRunPointPhaseBettingMenuUsesPointPhaseTrue(self):
		terminal = loadTerminalNamespace()
		pointPhaseFlags = []
		def fakeStep(commandText=None, pointPhase=False):
			pointPhaseFlags.append(pointPhase)
			return {
				"stepType": "command",
				"commandResult": {
					"command": commandText,
					"pointPhase": pointPhase,
					"shouldRoll": True,
					"handled": True,
					"runtimeState": {}
				},
				"cycleResult": None,
				"runtimeState": {}
			}
		terminal["step"] = fakeStep
		terminal["readInput"] = lambda promptText: "x"
		terminal["writeOutput"] = lambda message: None
		result = terminal["runPointPhaseBettingMenu"]()
		self.assertEqual(result["shouldRoll"], True)
		self.assertEqual(pointPhaseFlags, [True])

	def testRunComeOutBettingMenuLoopsUntilRollCommand(self):
		terminal = loadTerminalNamespace()
		calls = []
		def fakeStep(commandText=None, pointPhase=False):
			calls.append((commandText, pointPhase))
			return {
				"stepType": "command",
				"commandResult": {
					"command": commandText,
					"pointPhase": pointPhase,
					"shouldRoll": (commandText == "r"),
					"handled": True,
					"runtimeState": {}
				},
				"cycleResult": None,
				"runtimeState": {}
			}
		terminal["step"] = fakeStep
		inputs = iter(["h", "r"])
		terminal["readInput"] = lambda promptText: next(inputs)
		terminal["writeOutput"] = lambda message: None
		result = terminal["runComeOutBettingMenu"]()
		self.assertEqual(result["shouldRoll"], True)
		self.assertEqual(calls, [("h", False), ("r", False)])

	def testRunComeOutBettingMenuUsesPointPhaseFalse(self):
		terminal = loadTerminalNamespace()
		pointPhaseFlags = []
		def fakeStep(commandText=None, pointPhase=False):
			pointPhaseFlags.append(pointPhase)
			return {
				"stepType": "command",
				"commandResult": {
					"command": commandText,
					"pointPhase": pointPhase,
					"shouldRoll": True,
					"handled": True,
					"runtimeState": {}
				},
				"cycleResult": None,
				"runtimeState": {}
			}
		terminal["step"] = fakeStep
		terminal["readInput"] = lambda promptText: "x"
		terminal["writeOutput"] = lambda message: None
		result = terminal["runComeOutBettingMenu"]()
		self.assertEqual(result["shouldRoll"], True)
		self.assertEqual(pointPhaseFlags, [False])

	def testShowPointPhaseStatusUsesWriteOutputAdapter(self):
		terminal = loadTerminalNamespace()
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 25
		terminal["comeOut"] = 6
		terminal["throws"] = 9
		writes = []
		terminal["writeOutput"] = lambda message: writes.append(message)
		terminal["outOfMoney"] = lambda: None
		terminal["showPointPhaseStatus"]()
		self.assertEqual(writes[0], "You have $100 in the bank with $25 out on the table.")
		self.assertEqual(writes[1], "\n6 is the Point!\n")
		self.assertEqual(writes[2], "Throws: 9")

	def testRunComeOutRoundReturnsContinuePath(self):
		terminal = loadTerminalNamespace()
		menuCalls = []
		resolveCalls = []
		terminal["runComeOutBettingMenu"] = lambda: menuCalls.append(True)
		terminal["resolveComeOutRoll"] = lambda: (resolveCalls.append(True) or terminal["comeOutRollResult"](enteredPointPhase=False, outcome=terminal["RollOutcome"].natural))
		result = terminal["runComeOutRound"]()
		self.assertEqual(result.enteredPointPhase, False)
		self.assertEqual(result.outcome, terminal["RollOutcome"].natural)
		self.assertEqual(len(menuCalls), 1)
		self.assertEqual(len(resolveCalls), 1)

	def testRunComeOutRoundReturnsEnterPointPath(self):
		terminal = loadTerminalNamespace()
		menuCalls = []
		resolveCalls = []
		terminal["runComeOutBettingMenu"] = lambda: menuCalls.append(True)
		terminal["resolveComeOutRoll"] = lambda: (resolveCalls.append(True) or terminal["comeOutRollResult"](enteredPointPhase=True, outcome=terminal["RollOutcome"].pointEstablished))
		result = terminal["runComeOutRound"]()
		self.assertEqual(result.enteredPointPhase, True)
		self.assertEqual(result.outcome, terminal["RollOutcome"].pointEstablished)
		self.assertEqual(len(menuCalls), 1)
		self.assertEqual(len(resolveCalls), 1)

	def testRunOneCycleReturnsComeOutOnlyPath(self):
		terminal = loadTerminalNamespace()
		terminal["comeOut"] = 0
		terminal["throws"] = 3
		terminal["runComeOutRound"] = lambda: terminal["comeOutRoundResult"](enteredPointPhase=False, outcome=terminal["RollOutcome"].natural)
		pointPhaseCalls = []
		terminal["runPointPhaseRound"] = lambda: pointPhaseCalls.append(True)
		result = terminal["runOneCycle"]()
		self.assertEqual(result["enteredPointPhase"], False)
		self.assertEqual(result["comeOutOutcome"], terminal["RollOutcome"].natural)
		self.assertEqual(result["pointPhaseOutcome"], None)
		self.assertEqual(result["pointRoundEnded"], False)
		self.assertEqual(pointPhaseCalls, [])

	def testRunOneCycleReturnsPointPhasePath(self):
		terminal = loadTerminalNamespace()
		terminal["comeOut"] = 8
		terminal["throws"] = 5
		terminal["runComeOutRound"] = lambda: terminal["comeOutRoundResult"](enteredPointPhase=True, outcome=terminal["RollOutcome"].pointEstablished)
		terminal["runPointPhaseRound"] = lambda: terminal["pointPhaseRoundResult"](roundEnded=True, outcome=terminal["RollOutcome"].pointHit)
		result = terminal["runOneCycle"]()
		self.assertEqual(result["enteredPointPhase"], True)
		self.assertEqual(result["comeOutOutcome"], terminal["RollOutcome"].pointEstablished)
		self.assertEqual(result["pointPhaseOutcome"], terminal["RollOutcome"].pointHit)
		self.assertEqual(result["pointRoundEnded"], True)
		self.assertEqual(result["point"], 8)
		self.assertEqual(result["throws"], 5)

	def testRunOneCycleEmitsEventsForComeOutOnlyPath(self):
		terminal = loadTerminalNamespace()
		terminal["comeOut"] = 0
		terminal["throws"] = 2
		terminal["runComeOutRound"] = lambda: terminal["comeOutRoundResult"](enteredPointPhase=False, outcome=terminal["RollOutcome"].natural)
		terminal["runPointPhaseRound"] = lambda: terminal["pointPhaseRoundResult"](roundEnded=False, outcome=terminal["RollOutcome"].neutral)
		events = []
		terminal["setEventHandler"](lambda eventName, payload: events.append((eventName, payload)))
		result = terminal["runOneCycle"]()
		self.assertEqual(result["enteredPointPhase"], False)
		self.assertEqual(
			[event[0] for event in events],
			[
				terminal["hostEventNames"]["cycleStarted"],
				terminal["hostEventNames"]["comeOutResolved"],
				terminal["hostEventNames"]["cycleCompleted"]
			]
		)
		self.assertEqual(events[1][1]["enteredPointPhase"], False)
		self.assertIn("runtimeState", events[2][1])
		self.assertEqual(events[0][1]["engineApiVersion"], terminal["engineApiVersion"])
		terminal["resetEventHandler"]()

	def testRunOneCycleEmitsEventsForPointPhasePath(self):
		terminal = loadTerminalNamespace()
		terminal["comeOut"] = 6
		terminal["throws"] = 4
		terminal["runComeOutRound"] = lambda: terminal["comeOutRoundResult"](enteredPointPhase=True, outcome=terminal["RollOutcome"].pointEstablished)
		terminal["runPointPhaseRound"] = lambda: terminal["pointPhaseRoundResult"](roundEnded=True, outcome=terminal["RollOutcome"].pointHit)
		events = []
		terminal["setEventHandler"](lambda eventName, payload: events.append((eventName, payload)))
		result = terminal["runOneCycle"]()
		self.assertEqual(result["enteredPointPhase"], True)
		self.assertEqual(
			[event[0] for event in events],
			[
				terminal["hostEventNames"]["cycleStarted"],
				terminal["hostEventNames"]["comeOutResolved"],
				terminal["hostEventNames"]["pointPhaseResolved"],
				terminal["hostEventNames"]["cycleCompleted"]
			]
		)
		self.assertEqual(events[2][1]["roundEnded"], True)
		self.assertIn("runtimeState", events[3][1])
		terminal["resetEventHandler"]()

	def testResetEventHandlerClearsHandler(self):
		terminal = loadTerminalNamespace()
		terminal["setEventHandler"](lambda eventName, payload: None)
		terminal["resetEventHandler"]()
		self.assertEqual(terminal["eventHandler"], None)

	def testRunGameBootstrapsAndLoopsThroughComeOutStatus(self):
		terminal = loadTerminalNamespace()
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 0
		terminal["throws"] = 0
		terminal["gameMode"] = terminal["GameMode"].craps
		selectCalls = []
		cashInCalls = []
		syncCalls = []
		initCalls = []
		writes = []
		terminal["selectGameMode"] = lambda: selectCalls.append(True)
		terminal["cashIn"] = lambda: (cashInCalls.append(True), terminal.__setitem__("initBank", 100), terminal.__setitem__("bank", 100)) and None
		terminal["syncGameState"] = lambda **kwargs: syncCalls.append(kwargs)
		terminal["initializeGame"] = lambda startBank, selectedMode: initCalls.append((startBank, selectedMode))
		terminal["runOneCycle"] = lambda: (_ for _ in ()).throw(SystemExit())
		terminal["writeOutput"] = lambda message: writes.append(str(message))
		with self.assertRaises(SystemExit):
			terminal["runGame"]()
		self.assertEqual(len(selectCalls), 1)
		self.assertEqual(len(cashInCalls), 1)
		self.assertEqual(len(syncCalls), 0)
		self.assertEqual(initCalls, [(100, terminal["gameMode"])])
		writtenText = " ".join(writes)
		self.assertIn("Oh Craps! v.", writtenText)
		self.assertIn("You have $100 in the bank.", writtenText)
		self.assertIn("Throws: 0", writtenText)

	def testRunGameTransitionsIntoPointPhaseRound(self):
		terminal = loadTerminalNamespace()
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 0
		terminal["throws"] = 0
		terminal["gameMode"] = terminal["GameMode"].craps
		terminal["selectGameMode"] = lambda: None
		terminal["cashIn"] = lambda: (terminal.__setitem__("initBank", 100), terminal.__setitem__("bank", 100)) and None
		terminal["initializeGame"] = lambda startBank, selectedMode: None
		pointPhaseCalls = []
		def fakeRunPointPhaseRound():
			pointPhaseCalls.append(True)
			raise SystemExit()
		terminal["runOneCycle"] = fakeRunPointPhaseRound
		terminal["writeOutput"] = lambda message: None
		with self.assertRaises(SystemExit):
			terminal["runGame"]()
		self.assertEqual(pointPhaseCalls, [True])

	def testSetIoHandlersOverridesReadAndWrite(self):
		terminal = loadTerminalNamespace()
		writes = []
		prompts = []
		terminal["setIoHandlers"](
			outputFunc=lambda message: writes.append(str(message)),
			inputFunc=lambda promptText: prompts.append(promptText) or "abc"
		)
		terminal["writeOutput"]("hello")
		response = terminal["readInput"]("prompt> ")
		self.assertEqual(writes, ["hello"])
		self.assertEqual(prompts, ["prompt> "])
		self.assertEqual(response, "abc")

	def testResetIoHandlersRestoresDefaults(self):
		terminal = loadTerminalNamespace()
		terminal["setIoHandlers"](outputFunc=lambda message: None, inputFunc=lambda promptText: "x")
		terminal["resetIoHandlers"]()
		self.assertEqual(terminal["outputHandler"], None)
		self.assertEqual(terminal["inputHandler"], None)

	def testSetRandomProviderControlsStickmanChoice(self):
		terminal = loadTerminalNamespace()
		class fakeRandomProvider:
			def __init__(self, values):
				self.values = iter(values)
			def randrange(self, start, stop=None):
				return next(self.values)
		terminal["dealerCalls"] = {5: ["first", "second"]}
		terminal["rollHard"] = False
		terminal["setRandomProvider"](fakeRandomProvider([1]))
		self.assertEqual(terminal["stickman"](5), "second")
		terminal["resetRandomProvider"]()
		self.assertIs(terminal["randomProvider"], terminal["random"])

	def testRollUsesInjectedRandomProviderForNarrationBranch(self):
		terminal = loadTerminalNamespace()
		class fakeRandomProvider:
			def __init__(self, values):
				self.values = iter(values)
			def randrange(self, start, stop=None):
				return next(self.values)
		terminal["gameMode"] = terminal["GameMode"].craps
		terminal["pointIsOn"] = False
		terminal["rollDice"] = lambda: type("diceResult", (), {"die1": 4, "die2": 5, "total": 9})()
		terminal["setRandomProvider"](fakeRandomProvider([20]))
		writes = []
		terminal["writeOutput"] = lambda message: writes.append(str(message))
		with patch("builtins.print") as mockPrint:
			total = terminal["roll"]()
		self.assertEqual(total, 9)
		self.assertEqual(mockPrint.call_count, 0)
		self.assertIn("a 4 5 9", " ".join(writes))
		terminal["resetRandomProvider"]()

	def testShowPointPhaseStatusWithChipsShowsTableAmount(self):
		terminal = loadTerminalNamespace()
		terminal["bank"] = 250
		terminal["chipsOnTable"] = 75
		terminal["comeOut"] = 9
		terminal["throws"] = 14
		outCalls = []
		terminal["outOfMoney"] = lambda: outCalls.append(True)
		with patch("builtins.print") as mockPrint:
			terminal["showPointPhaseStatus"]()
		printed = "\n".join(str(args[0]) for args, _ in mockPrint.call_args_list if args)
		self.assertIn("You have $250 in the bank with $75 out on the table.", printed)
		self.assertIn("9 is the Point!", printed)
		self.assertIn("Throws: 14", printed)
		self.assertEqual(outCalls, [])

	def testShowPointPhaseStatusNoChipsCallsOutOfMoney(self):
		terminal = loadTerminalNamespace()
		terminal["bank"] = 0
		terminal["chipsOnTable"] = 0
		terminal["comeOut"] = 4
		terminal["throws"] = 3
		outCalls = []
		terminal["outOfMoney"] = lambda: outCalls.append(True)
		with patch("builtins.print") as mockPrint:
			terminal["showPointPhaseStatus"]()
		printed = "\n".join(str(args[0]) for args, _ in mockPrint.call_args_list if args)
		self.assertIn("You have $0 in the bank.", printed)
		self.assertIn("4 is the Point!", printed)
		self.assertIn("Throws: 3", printed)
		self.assertEqual(outCalls, [True])

	def testRunPointPhaseRoundEndsWhenPointRoundEnds(self):
		terminal = loadTerminalNamespace()
		statusCalls = []
		menuCalls = []
		resolveCalls = []
		terminal["showPointPhaseStatus"] = lambda: statusCalls.append(True)
		terminal["runPointPhaseBettingMenu"] = lambda: menuCalls.append(True)
		terminal["resolvePointRoll"] = lambda: (resolveCalls.append(True) or terminal["pointRollResult"](pointRoundEnded=True, outcome=terminal["RollOutcome"].pointHit))
		result = terminal["runPointPhaseRound"]()
		self.assertEqual(result.roundEnded, True)
		self.assertEqual(result.outcome, terminal["RollOutcome"].pointHit)
		self.assertEqual(len(statusCalls), 1)
		self.assertEqual(len(menuCalls), 1)
		self.assertEqual(len(resolveCalls), 1)

	def testRunPointPhaseRoundContinuesUntilPointRoundEnds(self):
		terminal = loadTerminalNamespace()
		statusCalls = []
		menuCalls = []
		resolveCalls = []
		outcomes = [
			terminal["pointRollResult"](pointRoundEnded=False, outcome=terminal["RollOutcome"].neutral),
			terminal["pointRollResult"](pointRoundEnded=True, outcome=terminal["RollOutcome"].sevenOut)
		]
		terminal["showPointPhaseStatus"] = lambda: statusCalls.append(True)
		terminal["runPointPhaseBettingMenu"] = lambda: menuCalls.append(True)
		def fakeResolvePointRoll():
				resolveCalls.append(True)
				return outcomes[len(resolveCalls) - 1]
		terminal["resolvePointRoll"] = fakeResolvePointRoll
		result = terminal["runPointPhaseRound"]()
		self.assertEqual(result.roundEnded, True)
		self.assertEqual(result.outcome, terminal["RollOutcome"].sevenOut)
		self.assertEqual(len(statusCalls), 2)
		self.assertEqual(len(menuCalls), 2)
		self.assertEqual(len(resolveCalls), 2)

	def testBetSnapshotCaptureApplyRoundTrip(self):
		terminal = loadTerminalNamespace()
		terminal["bank"] = 321
		terminal["chipsOnTable"] = 45
		terminal["comeBet"] = 10
		terminal["dComeBet"] = 15
		terminal["comeBets"] = {2: 0, 3: 0, 4: 5, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, "Come": 0}
		terminal["dComeBets"] = {2: 0, 3: 0, 4: 0, 5: 5, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		terminal["comeOdds"] = {2: 0, 3: 0, 4: 10, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		terminal["dComeOdds"] = {2: 0, 3: 0, 4: 0, 5: 12, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		terminal["place"] = {2: 2, 3: 4, 4: 5, 5: 5, 6: 6, 8: 6, 9: 5, 10: 5, 11: 4, 12: 2}
		terminal["layBets"] = {4: 0, 5: 5, 6: 0, 8: 0, 9: 0, 10: 0}
		terminal["hardWays"] = {4: 5, 6: 0, 8: 0, 10: 0}
		terminal["fieldBet"] = 20
		snapshot = terminal["captureBetSnapshot"]()
		terminal["bank"] = 0
		terminal["chipsOnTable"] = 0
		terminal["comeBet"] = 0
		terminal["dComeBet"] = 0
		terminal["comeBets"] = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, "Come": 0}
		terminal["dComeBets"] = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		terminal["comeOdds"] = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		terminal["dComeOdds"] = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		terminal["place"] = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		terminal["layBets"] = {4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0}
		terminal["hardWays"] = {4: 0, 6: 0, 8: 0, 10: 0}
		terminal["fieldBet"] = 0
		terminal["applyBetSnapshot"](snapshot)
		self.assertEqual(terminal["bank"], 321)
		self.assertEqual(terminal["chipsOnTable"], 45)
		self.assertEqual(terminal["comeBet"], 10)
		self.assertEqual(terminal["dComeBet"], 15)
		self.assertEqual(terminal["comeBets"][4], 5)
		self.assertEqual(terminal["dComeBets"][5], 5)
		self.assertEqual(terminal["comeOdds"][4], 10)
		self.assertEqual(terminal["dComeOdds"][5], 12)
		self.assertEqual(terminal["place"][11], 4)
		self.assertEqual(terminal["layBets"][5], 5)
		self.assertEqual(terminal["hardWays"][4], 5)
		self.assertEqual(terminal["fieldBet"], 20)

	def testSnapshotApplyWithPlaceSettlementPreservesOtherBets(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craplessCraps
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 0
		terminal["place"] = {2: 10, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		terminal["layBets"] = {4: 0, 5: 5, 6: 0, 8: 0, 9: 0, 10: 0}
		terminal["hardWays"] = {4: 5, 6: 0, 8: 0, 10: 0}
		with patch("builtins.input", side_effect=[""]):
			terminal["placeCheck"](2)
		self.assertEqual(terminal["place"][2], 10)
		self.assertEqual(terminal["layBets"][5], 5)
		self.assertEqual(terminal["hardWays"][4], 5)

	def testGetRuntimeStateIncludesCoreAndSnapshot(self):
		terminal = loadTerminalNamespace()
		terminal["bank"] = 250
		terminal["chipsOnTable"] = 40
		terminal["throws"] = 7
		runtimeState = terminal["getRuntimeState"]()
		self.assertEqual(runtimeState["bank"], 250)
		self.assertEqual(runtimeState["chipsOnTable"], 40)
		self.assertEqual(runtimeState["throws"], 7)
		self.assertIn("betSnapshot", runtimeState)
		self.assertEqual(runtimeState["betSnapshot"]["bank"], 250)

	def testSetRuntimeStateAppliesCoreValuesAndMode(self):
		terminal = loadTerminalNamespace()
		terminal["setRuntimeState"]({
			"bank": 500,
			"chipsOnTable": 35,
			"throws": 4,
			"pointIsOn": True,
			"comeOut": 9,
			"gameMode": "crapless craps"
		})
		self.assertEqual(terminal["bank"], 500)
		self.assertEqual(terminal["chipsOnTable"], 35)
		self.assertEqual(terminal["throws"], 4)
		self.assertEqual(terminal["pointIsOn"], True)
		self.assertEqual(terminal["comeOut"], 9)
		self.assertEqual(terminal["gameMode"], terminal["GameMode"].craplessCraps)

	def testSetRuntimeStateRejectsUnknownKeys(self):
		terminal = loadTerminalNamespace()
		with self.assertRaises(ValueError):
			terminal["setRuntimeState"]({"unknownKey": 1})

	def testNormalizeRuntimeStatePayloadCastsTypes(self):
		terminal = loadTerminalNamespace()
		normalizedState = terminal["normalizeRuntimeStatePayload"]({
			"bank": "120",
			"pointIsOn": 1,
			"gameMode": "2",
			"allNums": (2, 3, 4)
		})
		self.assertEqual(normalizedState["bank"], 120)
		self.assertEqual(normalizedState["pointIsOn"], True)
		self.assertEqual(normalizedState["gameMode"], terminal["GameMode"].craplessCraps)
		self.assertEqual(normalizedState["allNums"], [2, 3, 4])

	def testBuildDefaultRuntimeStateMatchesResetDefaults(self):
		terminal = loadTerminalNamespace()
		defaultState = terminal["buildDefaultRuntimeState"]()
		resetState = terminal["resetRuntimeState"]()
		self.assertEqual(resetState["bank"], defaultState["bank"])
		self.assertEqual(resetState["chipsOnTable"], defaultState["chipsOnTable"])
		self.assertEqual(resetState["gameMode"], defaultState["gameMode"])
		self.assertEqual(resetState["lineBets"], defaultState["lineBets"])
		self.assertEqual(resetState["betSnapshot"]["fieldBet"], defaultState["betSnapshot"]["fieldBet"])

	def testExportSessionBundleIncludesVersionAndCaptureState(self):
		terminal = loadTerminalNamespace()
		terminal["setRuntimeState"]({"bank": 123, "gameMode": terminal["GameMode"].craplessCraps})
		terminal["outputCaptureOn"] = True
		terminal["outputCaptureBuffer"] = ["out1"]
		terminal["promptCaptureOn"] = True
		terminal["promptCaptureBuffer"] = ["p1"]
		bundle = terminal["exportSessionBundle"]()
		self.assertEqual(bundle["engineApiVersion"], terminal["engineApiVersion"])
		self.assertEqual(bundle["bundleType"], "ohcrapsSession")
		self.assertEqual(bundle["runtimeState"]["bank"], 123)
		self.assertEqual(bundle["captureState"]["outputCaptureOn"], True)
		self.assertEqual(bundle["captureState"]["promptCaptureBuffer"], ["p1"])

	def testImportSessionBundleRoundTripRestoresState(self):
		terminal = loadTerminalNamespace()
		terminal["setRuntimeState"]({"bank": 222, "throws": 4, "gameMode": terminal["GameMode"].craplessCraps})
		terminal["outputCaptureOn"] = True
		terminal["outputCaptureBuffer"] = ["a", "b"]
		terminal["promptCaptureOn"] = False
		terminal["promptCaptureBuffer"] = ["q1"]
		bundle = terminal["exportSessionBundle"]()
		terminal["setRuntimeState"]({"bank": 1, "throws": 0, "gameMode": terminal["GameMode"].craps})
		terminal["outputCaptureOn"] = False
		terminal["outputCaptureBuffer"] = []
		terminal["promptCaptureOn"] = True
		terminal["promptCaptureBuffer"] = []
		importedBundle = terminal["importSessionBundle"](bundle)
		self.assertEqual(terminal["bank"], 222)
		self.assertEqual(terminal["throws"], 4)
		self.assertEqual(terminal["gameMode"], terminal["GameMode"].craplessCraps)
		self.assertEqual(terminal["outputCaptureOn"], True)
		self.assertEqual(terminal["outputCaptureBuffer"], ["a", "b"])
		self.assertEqual(importedBundle["runtimeState"]["bank"], 222)

	def testImportSessionBundleRejectsInvalidVersion(self):
		terminal = loadTerminalNamespace()
		bundle = terminal["exportSessionBundle"]()
		bundle["engineApiVersion"] = "0.0.1"
		with self.assertRaises(ValueError):
			terminal["importSessionBundle"](bundle)

	def testImportSessionBundleEmitsSessionImportedEvent(self):
		terminal = loadTerminalNamespace()
		bundle = terminal["exportSessionBundle"]()
		events = []
		terminal["setEventHandler"](lambda eventName, payload: events.append((eventName, payload)))
		terminal["importSessionBundle"](bundle)
		self.assertEqual(events[-1][0], terminal["hostEventNames"]["sessionImported"])
		self.assertEqual(events[-1][1]["engineApiVersion"], terminal["engineApiVersion"])
		self.assertEqual(events[-1][1]["bundleType"], "ohcrapsSession")
		terminal["resetEventHandler"]()

	def testSyncRuntimeFromGlobalsCapturesCoreLoopValues(self):
		terminal = loadTerminalNamespace()
		terminal["bank"] = 345
		terminal["chipsOnTable"] = 55
		terminal["throws"] = 8
		terminal["comeOut"] = 10
		terminal["pointIsOn"] = True
		terminal["p2"] = 6
		terminal["gameMode"] = terminal["GameMode"].craplessCraps
		runtime = terminal["syncRuntimeFromGlobals"]()
		self.assertEqual(runtime.bank, 345)
		self.assertEqual(runtime.chipsOnTable, 55)
		self.assertEqual(runtime.throws, 8)
		self.assertEqual(runtime.comeOut, 10)
		self.assertEqual(runtime.pointIsOn, True)
		self.assertEqual(runtime.p2, 6)
		self.assertEqual(runtime.gameMode, terminal["GameMode"].craplessCraps)

	def testSyncGlobalsFromRuntimeAppliesCoreLoopValues(self):
		terminal = loadTerminalNamespace()
		runtime = terminal["GameRuntime"](
			bank=777,
			chipsOnTable=23,
			throws=11,
			comeOut=9,
			pointIsOn=True,
			p2=5,
			gameMode=terminal["GameMode"].craplessCraps
		)
		terminal["syncGlobalsFromRuntime"](runtime)
		self.assertEqual(terminal["bank"], 777)
		self.assertEqual(terminal["chipsOnTable"], 23)
		self.assertEqual(terminal["throws"], 11)
		self.assertEqual(terminal["comeOut"], 9)
		self.assertEqual(terminal["pointIsOn"], True)
		self.assertEqual(terminal["p2"], 5)
		self.assertEqual(terminal["gameMode"], terminal["GameMode"].craplessCraps)
		self.assertEqual(terminal["gameRuntime"].bank, 777)

	def testResetRuntimeStateRestoresDefaults(self):
		terminal = loadTerminalNamespace()
		terminal["bank"] = 500
		terminal["chipsOnTable"] = 100
		terminal["throws"] = 12
		terminal["pointIsOn"] = True
		terminal["comeOut"] = 10
		terminal["placeOff"] = True
		terminal["working"] = True
		terminal["gameMode"] = terminal["GameMode"].craplessCraps
		terminal["lineBets"]["Pass"] = 25
		terminal["fieldBet"] = 15
		resetState = terminal["resetRuntimeState"]()
		self.assertEqual(terminal["bank"], 0)
		self.assertEqual(terminal["chipsOnTable"], 0)
		self.assertEqual(terminal["throws"], 0)
		self.assertEqual(terminal["pointIsOn"], False)
		self.assertEqual(terminal["comeOut"], 0)
		self.assertEqual(terminal["placeOff"], False)
		self.assertEqual(terminal["working"], False)
		self.assertEqual(terminal["gameMode"], terminal["GameMode"].craps)
		self.assertEqual(terminal["lineBets"]["Pass"], 0)
		self.assertEqual(terminal["fieldBet"], 0)
		self.assertEqual(resetState["bank"], 0)

	def testCreateActionResultShape(self):
		terminal = loadTerminalNamespace()
		result = terminal["createActionResult"](success=False, messages=["m1"], stateChanged=True)
		self.assertEqual(result["success"], False)
		self.assertEqual(result["messages"], ["m1"])
		self.assertEqual(result["stateChanged"], True)

	def testEmitActionResultUsesWriteOutput(self):
		terminal = loadTerminalNamespace()
		writes = []
		terminal["writeOutput"] = lambda message: writes.append(str(message))
		with patch("builtins.print") as mockPrint:
			terminal["emitActionResult"]({"messages": ["m1", "m2"]})
		self.assertEqual(mockPrint.call_count, 0)
		self.assertEqual(writes, ["m1", "m2"])

	def testLineCheckUsesWriteOutputForSettlementMessages(self):
		terminal = loadTerminalNamespace()
		terminal["pointIsOn"] = False
		terminal["lineBets"] = {"Pass": 10, "Pass Odds": 0, "Don't Pass": 0, "Don't Pass Odds": 0}
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 10
		terminal["settleLineBetsForMode"] = lambda **kwargs: type("settlement", (), {
			"lineBets": kwargs["lineBets"],
			"bankDelta": 5,
			"chipsOnTableDelta": -5,
			"messages": ["line message"]
		})()
		writes = []
		terminal["writeOutput"] = lambda message: writes.append(str(message))
		with patch("builtins.print") as mockPrint:
			terminal["lineCheck"](6, 0)
		self.assertEqual(mockPrint.call_count, 0)
		self.assertIn("line message", writes)
		self.assertEqual(terminal["bank"], 105)
		self.assertEqual(terminal["chipsOnTable"], 5)

	def testComeShowUsesWriteOutput(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craps
		terminal["comeBets"] = {2: 0, 3: 0, 4: 10, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, "Come": 0}
		terminal["comeOdds"] = {2: 0, 3: 0, 4: 20, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		terminal["dComeBets"] = {2: 0, 3: 0, 4: 0, 5: 5, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		terminal["dComeOdds"] = {2: 0, 3: 0, 4: 0, 5: 12, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		writes = []
		terminal["writeOutput"] = lambda message: writes.append(str(message))
		with patch("builtins.print") as mockPrint:
			terminal["comeShow"]()
		self.assertEqual(mockPrint.call_count, 0)
		writtenText = " ".join(writes)
		self.assertIn("You have $10 on the Come 4 with $20 in Odds.", writtenText)
		self.assertIn("You have $5 on the Don't Come 5 with $12 in odds.", writtenText)

	def testComePayUsesWriteOutputForSettlementMessages(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craps
		terminal["pointIsOn"] = True
		terminal["working"] = True
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 20
		terminal["comeBets"] = {2: 0, 3: 0, 4: 10, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, "Come": 0}
		terminal["dComeBets"] = {2: 0, 3: 0, 4: 0, 5: 5, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		terminal["comeOdds"] = {2: 0, 3: 0, 4: 20, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		terminal["dComeOdds"] = {2: 0, 3: 0, 4: 0, 5: 12, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		terminal["settleComeTableBets"] = lambda **kwargs: type("settlement", (), {
			"comeBets": kwargs["comeBets"],
			"dComeBets": kwargs["dComeBets"],
			"comeOdds": kwargs["comeOdds"],
			"dComeOdds": kwargs["dComeOdds"],
			"bankDelta": 7,
			"chipsOnTableDelta": -7,
			"messages": ["come settlement message"]
		})()
		writes = []
		terminal["writeOutput"] = lambda message: writes.append(str(message))
		with patch("builtins.print") as mockPrint:
			terminal["comePay"](4)
		self.assertEqual(mockPrint.call_count, 0)
		self.assertIn("come settlement message", writes)
		self.assertEqual(terminal["bank"], 107)
		self.assertEqual(terminal["chipsOnTable"], 13)

	def testComeCheckReturnsActionResultForMovedComeBet(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craps
		terminal["comeBet"] = 10
		terminal["comeBets"] = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, "Come": 0}
		terminal["comeOdds"] = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 10
		terminal["readInput"] = lambda promptText: "n"
		terminal["writeOutput"] = lambda message: None
		with patch("builtins.print"):
			result = terminal["comeCheck"](5)
		self.assertEqual(result["stateChanged"], True)
		self.assertEqual(any("Moving your Come Bet to the 5." in msg for msg in result["messages"]), False)
		self.assertEqual(terminal["comeBets"][5], 10)

	def testComeCheckPrintsMoveReminderBeforeOddsPromptWithNumber(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craps
		terminal["comeBet"] = 10
		terminal["comeBets"] = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, "Come": 0}
		terminal["comeOdds"] = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 10
		seenMoveReminder = {"value": False}

		def fakeWriteOutput(text):
			if "Moving your Come Bet to the 5." in text:
				seenMoveReminder["value"] = True

		def fakeReadInput(promptText):
			self.assertEqual(promptText, "Come Odds for the 5? > ")
			self.assertEqual(seenMoveReminder["value"], True)
			return "n"

		terminal["writeOutput"] = fakeWriteOutput
		terminal["readInput"] = fakeReadInput
		with patch("builtins.print"):
			terminal["comeCheck"](5)

	def testComeCheckRetriesWithContextPromptAndImmediateError(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craps
		terminal["comeBet"] = 10
		terminal["comeBets"] = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, "Come": 0}
		terminal["comeOdds"] = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		terminal["bank"] = 200
		terminal["chipsOnTable"] = 10
		printedTexts = []

		terminal["writeOutput"] = lambda message: printedTexts.append(str(message))
		inputs = iter(["y", "100", "20"])
		promptLog = []

		def fakeReadInput(promptText):
			promptLog.append(promptText)
			return next(inputs)

		terminal["readInput"] = fakeReadInput
		result = terminal["comeCheck"](5)

		self.assertEqual(result["messages"].count("Way too high on your Odds, there. Try again."), 0)
		self.assertEqual(result["messages"].count("Ok, $20 on your Come 5 odds."), 1)
		self.assertEqual(sum(1 for text in printedTexts if "How much for your Come 5 Odds? Max is $40, multiples of 2" in text), 2)
		self.assertEqual(sum(1 for text in printedTexts if "Way too high on your Odds, there. Try again." in text), 1)
		self.assertEqual(terminal["comeOdds"][5], 20)
		self.assertEqual(promptLog[0], "Come Odds for the 5? > ")
		self.assertEqual(sum(1 for promptText in promptLog if "$>" in promptText), 2)

	def testDontComeCheckUsesLayOddsPromptTextAndRetriesWithContext(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craps
		terminal["dComeBet"] = 10
		terminal["dComeBets"] = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		terminal["dComeOdds"] = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		terminal["bank"] = 200
		terminal["chipsOnTable"] = 10
		printedTexts = []
		seenMoveReminder = {"value": False}
		inputCalls = {"count": 0}

		def fakeWriteOutput(text):
			printedTexts.append(text)
			if "Moving your Don't Come bet to the 5." in text:
				seenMoveReminder["value"] = True

		inputs = iter(["y", "120", "90"])

		def fakeReadInput(promptText):
			inputCalls["count"] += 1
			if promptText == "Lay Odds on the 5? > ":
				self.assertEqual(seenMoveReminder["value"], True)
			elif "$>" not in promptText:
				raise AssertionError(f"Unexpected prompt: {promptText}")
			return next(inputs)

		terminal["writeOutput"] = fakeWriteOutput
		terminal["readInput"] = fakeReadInput
		result = terminal["comeCheck"](5)

		self.assertEqual(result["messages"].count("Way too much for your Lay Odds! Try again."), 0)
		self.assertEqual(result["messages"].count("Ok, $90 laid on the Don't Come 5."), 1)
		self.assertEqual(sum(1 for text in printedTexts if "How much for your Lay 5 Odds? Max is $99, multiples of 3" in text), 2)
		self.assertEqual(sum(1 for text in printedTexts if "Way too much for your Lay Odds! Try again." in text), 1)
		self.assertEqual(terminal["dComeOdds"][5], 90)

	def testDontComeCheckUsesEffectiveMaxForUnitRestrictedLayOdds(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craps
		terminal["dComeBet"] = 10
		terminal["dComeBets"] = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		terminal["dComeOdds"] = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		terminal["bank"] = 200
		terminal["chipsOnTable"] = 10
		printedTexts = []

		terminal["writeOutput"] = lambda message: printedTexts.append(str(message))
		inputs = iter(["y", "100", "99"])
		promptLog = []
		terminal["readInput"] = lambda promptText: promptLog.append(promptText) or next(inputs)
		result = terminal["comeCheck"](5)

		self.assertEqual(result["messages"].count("Way too much for your Lay Odds! Try again."), 0)
		self.assertEqual(result["messages"].count("Ok, $99 laid on the Don't Come 5."), 1)
		self.assertEqual(sum(1 for text in printedTexts if "How much for your Lay 5 Odds? Max is $99, multiples of 3" in text), 2)
		self.assertEqual(sum(1 for text in printedTexts if "Way too much for your Lay Odds! Try again." in text), 1)
		self.assertEqual(terminal["dComeOdds"][5], 99)
		self.assertEqual(promptLog[0], "Lay Odds on the 5? > ")
		self.assertEqual(sum(1 for promptText in promptLog if "$>" in promptText), 2)

	def testComeCheckCraplessUnitOnePromptOmitsMultiplesText(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craplessCraps
		terminal["comeBet"] = 10
		terminal["comeBets"] = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, "Come": 0}
		terminal["comeOdds"] = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		terminal["bank"] = 200
		terminal["chipsOnTable"] = 10
		writes = []
		terminal["writeOutput"] = lambda message: writes.append(str(message))
		inputs = iter(["y", "10"])
		terminal["readInput"] = lambda promptText: next(inputs)

		with patch("builtins.print"):
			terminal["comeCheck"](2)

		printed = " ".join(writes)
		self.assertIn("How much for your Come 2 Odds? Max is $60", printed)
		self.assertNotIn("multiples of 1", printed.lower())

	def testComeCheckReturnsNoChangeActionResultWhenNoBarBets(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craps
		terminal["comeBet"] = 0
		terminal["dComeBet"] = 0
		with patch("builtins.print"):
			result = terminal["comeCheck"](9)
		self.assertEqual(result["success"], True)
		self.assertEqual(result["stateChanged"], False)

	def testComeCheckCrapsComeBarLossOnTwoIncludesMessageAndStateChange(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craps
		terminal["comeBet"] = 10
		terminal["dComeBet"] = 0
		terminal["comeBets"] = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, "Come": 0}
		terminal["comeOdds"] = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 10
		terminal["writeOutput"] = lambda message: None
		terminal["readInput"] = lambda promptText: "n"
		with patch("builtins.print"):
			result = terminal["comeCheck"](2)
		self.assertEqual(terminal["comeBet"], 0)
		self.assertEqual(terminal["bank"], 100)
		self.assertEqual(terminal["chipsOnTable"], 0)
		self.assertIn("You lost $10 from the Come Bet.", result["messages"])
		self.assertEqual(result["stateChanged"], True)

	def testComeCheckCrapsComeBarWinOnSevenIncludesMessageAndStateChange(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craps
		terminal["comeBet"] = 10
		terminal["dComeBet"] = 0
		terminal["comeBets"] = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, "Come": 0}
		terminal["comeOdds"] = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 10
		terminal["writeOutput"] = lambda message: None
		terminal["readInput"] = lambda promptText: "n"
		with patch("builtins.print"):
			result = terminal["comeCheck"](7)
		self.assertEqual(terminal["comeBet"], 0)
		self.assertEqual(terminal["bank"], 120)
		self.assertEqual(terminal["chipsOnTable"], 0)
		self.assertIn("You won $10 on the Come!", result["messages"])
		self.assertEqual(result["stateChanged"], True)

	def testCdcOddsChangeRejectsInvalidComeOddsUnitInCraps(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craps
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 0
		terminal["comeBets"] = {2: 0, 3: 0, 4: 0, 5: 10, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, "Come": 0}
		terminal["comeOdds"] = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		writes = []
		terminal["writeOutput"] = lambda message: writes.append(str(message))
		inputs = iter(["3", "4"])
		terminal["readInput"] = lambda promptText: next(inputs)
		terminal["cdcOddsChange"](terminal["comeBets"], terminal["comeOdds"])
		self.assertEqual(terminal["comeOdds"][5], 4)
		self.assertEqual(terminal["bank"], 96)
		self.assertEqual(terminal["chipsOnTable"], 4)
		self.assertIn("Invalid odds amount. Must be in increments of $2.", " ".join(writes))

	def testCdcOddsChangeRejectsInvalidDontComeOddsUnitInCrapless(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craplessCraps
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 0
		terminal["dComeBets"] = {2: 12, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		terminal["dComeOdds"] = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		writes = []
		terminal["writeOutput"] = lambda message: writes.append(str(message))
		inputs = iter(["5", "6"])
		terminal["readInput"] = lambda promptText: next(inputs)
		terminal["cdcOddsChange"](terminal["dComeBets"], terminal["dComeOdds"])
		self.assertEqual(terminal["dComeOdds"][2], 6)
		self.assertEqual(terminal["bank"], 94)
		self.assertEqual(terminal["chipsOnTable"], 6)
		self.assertIn("Invalid odds amount. Must be in increments of $6.", " ".join(writes))

	def testCdcOddsChangeComeUnitOnePromptOmitsMultiplesText(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craplessCraps
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 0
		terminal["comeBets"] = {2: 10, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, "Come": 0}
		terminal["comeOdds"] = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		writes = []
		terminal["writeOutput"] = lambda message: writes.append(str(message))
		terminal["readInput"] = lambda promptText: "10"
		terminal["cdcOddsChange"](terminal["comeBets"], terminal["comeOdds"])
		printedText = " ".join(writes)
		self.assertIn("How much for your Come 2 Odds? Max is $60; you have $0 in Odds.", printedText)
		self.assertNotIn("multiples of 1", printedText.lower())

	def testPlacePresetAcrossWorksInCrapless(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craplessCraps
		terminal["bank"] = 200
		terminal["chipsOnTable"] = 0
		terminal["place"] = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		with patch("builtins.input", side_effect=["1"]):
			terminal["placePreset"]("a")
		self.assertEqual(terminal["place"], {2: 0, 3: 0, 4: 5, 5: 5, 6: 6, 8: 6, 9: 5, 10: 5, 11: 0, 12: 0})
		self.assertEqual(terminal["bank"], 168)
		self.assertEqual(terminal["chipsOnTable"], 32)

	def testPlacePresetInsideWorksInCrapless(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craplessCraps
		terminal["bank"] = 200
		terminal["chipsOnTable"] = 0
		terminal["place"] = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		with patch("builtins.input", side_effect=["1"]):
			terminal["placePreset"]("i")
		self.assertEqual(terminal["place"], {2: 0, 3: 0, 4: 0, 5: 5, 6: 6, 8: 6, 9: 5, 10: 0, 11: 0, 12: 0})
		self.assertEqual(terminal["bank"], 178)
		self.assertEqual(terminal["chipsOnTable"], 22)

	def testPlacePresetCenterWorksInCrapless(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craplessCraps
		terminal["bank"] = 200
		terminal["chipsOnTable"] = 0
		terminal["place"] = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		with patch("builtins.input", side_effect=["1"]):
			terminal["placePreset"]("c")
		self.assertEqual(terminal["place"], {2: 0, 3: 0, 4: 0, 5: 0, 6: 6, 8: 6, 9: 0, 10: 0, 11: 0, 12: 0})
		self.assertEqual(terminal["bank"], 188)
		self.assertEqual(terminal["chipsOnTable"], 12)

	def testPlacePresetExtremeAcrossInCrapless(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craplessCraps
		terminal["bank"] = 200
		terminal["chipsOnTable"] = 0
		terminal["place"] = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		with patch("builtins.input", side_effect=["1"]):
			terminal["placePreset"]("ea")
		self.assertEqual(terminal["place"], {2: 2, 3: 4, 4: 5, 5: 5, 6: 6, 8: 6, 9: 5, 10: 5, 11: 4, 12: 2})
		self.assertEqual(terminal["chipsOnTable"], 44)
		self.assertEqual(terminal["bank"], 156)

	def testPlacePresetEdgeOnlyInCrapless(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craplessCraps
		terminal["bank"] = 168
		terminal["chipsOnTable"] = 32
		terminal["place"] = {2: 0, 3: 0, 4: 5, 5: 5, 6: 6, 8: 6, 9: 5, 10: 5, 11: 0, 12: 0}
		with patch("builtins.input", side_effect=["1"]):
			terminal["placePreset"]("e")
		self.assertEqual(terminal["place"], {2: 2, 3: 4, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 4, 12: 2})
		self.assertEqual(terminal["chipsOnTable"], 12)
		self.assertEqual(terminal["bank"], 188)

	def testPlacePresetAcrossExcludePointInCrapless(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craplessCraps
		terminal["bank"] = 200
		terminal["chipsOnTable"] = 0
		terminal["pointIsOn"] = True
		terminal["comeOut"] = 6
		terminal["place"] = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		with patch("builtins.input", side_effect=["1", "n"]):
			terminal["placePreset"]("a")
		self.assertEqual(terminal["place"], {2: 0, 3: 0, 4: 5, 5: 5, 6: 0, 8: 6, 9: 5, 10: 5, 11: 0, 12: 0})
		self.assertEqual(terminal["chipsOnTable"], 26)
		self.assertEqual(terminal["bank"], 174)

	def testPlacePresetInsideExcludePointInCrapless(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craplessCraps
		terminal["bank"] = 200
		terminal["chipsOnTable"] = 0
		terminal["pointIsOn"] = True
		terminal["comeOut"] = 9
		terminal["place"] = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		with patch("builtins.input", side_effect=["1", "n"]):
			terminal["placePreset"]("i")
		self.assertEqual(terminal["place"], {2: 0, 3: 0, 4: 0, 5: 5, 6: 6, 8: 6, 9: 0, 10: 0, 11: 0, 12: 0})
		self.assertEqual(terminal["chipsOnTable"], 17)
		self.assertEqual(terminal["bank"], 183)

	def testPlacePresetSequenceAcrossEdgeExtremeInCrapless(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craplessCraps
		terminal["bank"] = 200
		terminal["chipsOnTable"] = 0
		terminal["pointIsOn"] = False
		terminal["place"] = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		with patch("builtins.input", side_effect=["1"]):
			terminal["placePreset"]("a")
		with patch("builtins.input", side_effect=["1"]):
			terminal["placePreset"]("e")
		with patch("builtins.input", side_effect=["1"]):
			terminal["placePreset"]("ea")
		self.assertEqual(terminal["place"], {2: 2, 3: 4, 4: 5, 5: 5, 6: 6, 8: 6, 9: 5, 10: 5, 11: 4, 12: 2})
		self.assertEqual(terminal["chipsOnTable"], 44)
		self.assertEqual(terminal["bank"], 156)

	def testPlaceMoverStaysDisabledInCrapless(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craplessCraps
		terminal["bank"] = 168
		terminal["chipsOnTable"] = 32
		terminal["comeOut"] = 6
		terminal["place"] = {2: 0, 3: 0, 4: 5, 5: 5, 6: 6, 8: 6, 9: 5, 10: 5, 11: 0, 12: 0}
		with patch("builtins.print"):
			terminal["placeMover"]()
		self.assertEqual(terminal["place"], {2: 0, 3: 0, 4: 5, 5: 5, 6: 6, 8: 6, 9: 5, 10: 5, 11: 0, 12: 0})
		self.assertEqual(terminal["chipsOnTable"], 32)
		self.assertEqual(terminal["bank"], 168)

	def testHardWaysBettingSavesWager(self):
		terminal = loadTerminalNamespace()
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 0
		terminal["hardWays"] = {4: 0, 6: 0, 8: 0, 10: 0}
		writes = []
		terminal["writeOutput"] = lambda message: writes.append(str(message))
		inputs = iter(["5", "", "", ""])
		terminal["readInput"] = lambda promptText: next(inputs)
		terminal["hardWaysBetting"]()
		self.assertEqual(terminal["hardWays"][4], 5)
		self.assertEqual(terminal["hardWays"][6], 0)
		self.assertEqual(terminal["hardWays"][8], 0)
		self.assertEqual(terminal["hardWays"][10], 0)
		self.assertEqual(terminal["bank"], 95)
		self.assertEqual(terminal["chipsOnTable"], 5)
		self.assertEqual(sum(1 for text in writes if "How much on the Hard" in text), 4)

	def testHardWaysBettingTakeDownReturnsFunds(self):
		terminal = loadTerminalNamespace()
		terminal["bank"] = 90
		terminal["chipsOnTable"] = 10
		terminal["hardWays"] = {4: 0, 6: 10, 8: 0, 10: 0}
		writes = []
		terminal["writeOutput"] = lambda message: writes.append(str(message))
		inputs = iter(["", "0", "", ""])
		terminal["readInput"] = lambda promptText: next(inputs)
		terminal["hardWaysBetting"]()
		self.assertEqual(terminal["hardWays"][6], 0)
		self.assertEqual(terminal["bank"], 100)
		self.assertEqual(terminal["chipsOnTable"], 0)
		self.assertIn("Ok, taking down your Hard 6 bet.", " ".join(writes))

	def testHardCheckHitPressUsesIoAdapters(self):
		terminal = loadTerminalNamespace()
		terminal["hardWays"] = {4: 5, 6: 0, 8: 0, 10: 0}
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 5
		terminal["rollHard"] = True
		writes = []
		prompts = []
		terminal["writeOutput"] = lambda message: writes.append(str(message))
		terminal["readInput"] = lambda promptText: prompts.append(promptText) or "y"
		terminal["betPrompt"] = lambda: 10
		terminal["hardCheck"](4)
		self.assertEqual(terminal["hardWays"][4], 10)
		self.assertIn("Press your bet? > ", prompts)
		self.assertIn("Ok, bumping up your Hard 4 bet to $10.", " ".join(writes))

	def testHardCheckLostNumberReUpUsesIoAdapters(self):
		terminal = loadTerminalNamespace()
		terminal["hardWays"] = {4: 5, 6: 0, 8: 0, 10: 0}
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 5
		terminal["rollHard"] = False
		writes = []
		prompts = []
		terminal["writeOutput"] = lambda message: writes.append(str(message))
		terminal["readInput"] = lambda promptText: prompts.append(promptText) or "y"
		terminal["betPrompt"] = lambda: 5
		terminal["hardCheck"](4)
		self.assertEqual(terminal["hardWays"][4], 5)
		self.assertIn("Go back up on your Hard 4 bet? > ", prompts)
		self.assertIn("Ok, going back up on the Hard 4 for $5.", " ".join(writes))

	def testFieldUsesIoAdaptersForEntry(self):
		terminal = loadTerminalNamespace()
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 0
		terminal["fieldBet"] = 0
		writes = []
		terminal["writeOutput"] = lambda message: writes.append(str(message))
		terminal["readInput"] = lambda promptText: "15"
		terminal["field"]()
		self.assertEqual(terminal["fieldBet"], 15)
		self.assertEqual(terminal["bank"], 85)
		self.assertEqual(terminal["chipsOnTable"], 15)
		self.assertIn("How much on the Field?", " ".join(writes))
		self.assertIn("Ok, $15 on the Field.", " ".join(writes))

	def testFieldCheckWinChangePathUsesIoAdapters(self):
		terminal = loadTerminalNamespace()
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 10
		terminal["fieldBet"] = 10
		writes = []
		prompts = []
		inputs = iter(["y", "12"])
		terminal["writeOutput"] = lambda message: writes.append(str(message))
		terminal["readInput"] = lambda promptText: prompts.append(promptText) or next(inputs)
		terminal["fieldCheck"](9)
		self.assertEqual(terminal["fieldBet"], 12)
		self.assertEqual(terminal["bank"], 108)
		self.assertEqual(terminal["chipsOnTable"], 12)
		self.assertIn("Change your Field bet? > ", prompts)

	def testFieldCheckLossReUpPathUsesIoAdapters(self):
		terminal = loadTerminalNamespace()
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 10
		terminal["fieldBet"] = 10
		writes = []
		prompts = []
		inputs = iter(["y", "8"])
		terminal["writeOutput"] = lambda message: writes.append(str(message))
		terminal["readInput"] = lambda promptText: prompts.append(promptText) or next(inputs)
		terminal["fieldCheck"](6)
		self.assertEqual(terminal["fieldBet"], 8)
		self.assertEqual(terminal["bank"], 92)
		self.assertEqual(terminal["chipsOnTable"], 8)
		self.assertIn("Go back up on the Field? > ", prompts)

	def testAtsBettingUsesIoAdapters(self):
		terminal = loadTerminalNamespace()
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 0
		terminal["atsAll"] = 0
		terminal["atsTall"] = 0
		terminal["atsSmall"] = 0
		writes = []
		inputs = iter(["5", "4", "3"])
		terminal["writeOutput"] = lambda message: writes.append(str(message))
		terminal["readInput"] = lambda promptText: next(inputs)
		terminal["atsBetting"]()
		self.assertEqual(terminal["atsAll"], 5)
		self.assertEqual(terminal["atsTall"], 4)
		self.assertEqual(terminal["atsSmall"], 3)
		self.assertIn("How much on the All?", " ".join(writes))
		self.assertIn("How much on the Tall?", " ".join(writes))
		self.assertIn("How much on the Small?", " ".join(writes))

	def testAtsWritesLossOnSevenOut(self):
		terminal = loadTerminalNamespace()
		terminal["atsAll"] = 5
		terminal["atsTall"] = 4
		terminal["atsSmall"] = 3
		terminal["chipsOnTable"] = 12
		terminal["bank"] = 100
		writes = []
		terminal["writeOutput"] = lambda message: writes.append(str(message))
		terminal["ats"](7)
		self.assertEqual(terminal["atsAll"], 0)
		self.assertEqual(terminal["atsTall"], 0)
		self.assertEqual(terminal["atsSmall"], 0)
		self.assertEqual(terminal["chipsOnTable"], 0)
		self.assertIn("You lost $12 from the All Tall Small.", " ".join(writes))

	def testFireBettingUsesIoAdapters(self):
		terminal = loadTerminalNamespace()
		terminal["fireBet"] = 0
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 0
		writes = []
		terminal["writeOutput"] = lambda message: writes.append(str(message))
		terminal["readInput"] = lambda promptText: "5"
		terminal["fireBetting"]()
		self.assertEqual(terminal["fireBet"], 5)
		self.assertIn("How much on the Fire Bet?", " ".join(writes))

	def testHandleBettingCommandFieldPromptUsesReadInput(self):
		terminal = loadTerminalNamespace()
		terminal["fieldBet"] = 0
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 0
		inputs = iter(["y", "10"])
		terminal["readInput"] = lambda promptText: next(inputs)
		terminal["writeOutput"] = lambda message: None
		with patch("builtins.print"):
			result = terminal["handleBettingCommand"]("f", pointPhase=False)
		self.assertEqual(result.shouldRoll, False)
		self.assertEqual(terminal["fieldBet"], 10)

	def testShowAllBetsUsesWriteOutputForSummaryRows(self):
		terminal = loadTerminalNamespace()
		terminal["lineBets"] = {"Pass": 10, "Pass Odds": 0, "Don't Pass": 0, "Don't Pass Odds": 0}
		terminal["comeBet"] = 5
		terminal["dComeBet"] = 0
		terminal["propBets"] = terminal["createDefaultPropBets"]()
		terminal["propBets"]["Any Craps"] = 4
		terminal["atsAll"] = 2
		terminal["atsTall"] = 3
		terminal["atsSmall"] = 1
		terminal["fireBet"] = 6
		terminal["comeShow"] = lambda: None
		terminal["placeShow"] = lambda: None
		terminal["layShow"] = lambda: None
		terminal["fieldShow"] = lambda: None
		terminal["hardShow"] = lambda: None
		writes = []
		terminal["writeOutput"] = lambda message: writes.append(str(message))
		with patch("builtins.print") as mockPrint:
			terminal["showAllBets"]()
		self.assertEqual(mockPrint.call_count, 0)
		writtenText = " ".join(writes)
		self.assertIn("You have $10 on the Pass.", writtenText)
		self.assertIn("You have $5 on the Come.", writtenText)
		self.assertIn("$4 on Any Craps.", writtenText)
		self.assertIn("You have $2 on the All, $3 on the Tall, and $1 on the Small.", writtenText)
		self.assertIn("You have $6 on the Fire Bet.", writtenText)

	def testHandleBettingCommandBankUsesWriteOutput(self):
		terminal = loadTerminalNamespace()
		terminal["bank"] = 120
		terminal["chipsOnTable"] = 30
		terminal["comeOut"] = 8
		writes = []
		terminal["writeOutput"] = lambda message: writes.append(str(message))
		with patch("builtins.print") as mockPrint:
			result = terminal["handleBettingCommand"]("b", pointPhase=True)
		self.assertEqual(result.shouldRoll, False)
		self.assertEqual(mockPrint.call_count, 0)
		self.assertIn("You have $120 in your rack with $30 on the table. The Point is 8.", " ".join(writes))

	def testHandleBettingCommandHelpUsesWriteOutput(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craps
		writes = []
		terminal["writeOutput"] = lambda message: writes.append(str(message))
		with patch("builtins.print") as mockPrint:
			result = terminal["handleBettingCommand"]("h", pointPhase=False)
		self.assertEqual(result.shouldRoll, False)
		self.assertEqual(mockPrint.call_count, 0)
		self.assertIn("Betting Codes:", " ".join(writes))

	def testOddsPassRejectOverMaxRefundsBeforeRetry(self):
		terminal = loadTerminalNamespace()
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 10
		terminal["comeOut"] = 6
		terminal["lineBets"] = {
			"Pass": 10,
			"Pass Odds": 0,
			"Don't Pass": 0,
			"Don't Pass Odds": 0
		}
		with patch("builtins.input", side_effect=["60", "30"]):
			terminal["odds"]()
		self.assertEqual(terminal["lineBets"]["Pass Odds"], 30)
		self.assertEqual(terminal["bank"], 70)
		self.assertEqual(terminal["chipsOnTable"], 40)

	def testOddsPassUsesCraplessMaxOnEdgePoints(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craplessCraps
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 10
		terminal["comeOut"] = 2
		terminal["lineBets"] = {
			"Pass": 10,
			"Pass Odds": 0,
			"Don't Pass": 0,
			"Don't Pass Odds": 0
		}
		with patch("builtins.input", side_effect=["70", "60"]):
			terminal["odds"]()
		self.assertEqual(terminal["lineBets"]["Pass Odds"], 60)
		self.assertEqual(terminal["bank"], 40)
		self.assertEqual(terminal["chipsOnTable"], 70)

	def testOddsCheckPaysCraplessPassOddsOnPointTwo(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craplessCraps
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 10
		terminal["comeOut"] = 2
		terminal["lineBets"] = {
			"Pass": 0,
			"Pass Odds": 10,
			"Don't Pass": 0,
			"Don't Pass Odds": 0
		}
		with patch("builtins.print"):
			terminal["oddsCheck"](2)
		self.assertEqual(terminal["lineBets"]["Pass Odds"], 0)
		self.assertEqual(terminal["bank"], 170)
		self.assertEqual(terminal["chipsOnTable"], 0)

	def testOddsPassRejectsInvalidUnitThenAccepts(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craps
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 10
		terminal["comeOut"] = 5
		terminal["lineBets"] = {
			"Pass": 10,
			"Pass Odds": 0,
			"Don't Pass": 0,
			"Don't Pass Odds": 0
		}
		writes = []
		terminal["writeOutput"] = lambda message: writes.append(str(message))
		with patch("builtins.input", side_effect=["3", "4"]):
			terminal["odds"]()
		printed = " ".join(writes)
		self.assertIn("Odds on the 5?", printed)
		self.assertIn("Max odds is $40.", printed)
		self.assertIn("Multiples of 2.", printed)
		self.assertIn("Invalid odds amount. Must be in increments of $2.", printed)
		self.assertEqual(terminal["lineBets"]["Pass Odds"], 4)
		self.assertEqual(terminal["bank"], 96)
		self.assertEqual(terminal["chipsOnTable"], 14)

	def testOddsDontPassUsesEffectiveMaxAndUnit(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craps
		terminal["bank"] = 200
		terminal["chipsOnTable"] = 10
		terminal["comeOut"] = 5
		terminal["lineBets"] = {
			"Pass": 0,
			"Pass Odds": 0,
			"Don't Pass": 10,
			"Don't Pass Odds": 0
		}
		writes = []
		terminal["writeOutput"] = lambda message: writes.append(str(message))
		with patch("builtins.input", side_effect=["100", "99"]):
			terminal["odds"]()
		printed = " ".join(writes)
		self.assertIn("Lay Odds against the 5?", printed)
		self.assertIn("Max odds is $99.", printed)
		self.assertIn("Multiples of 3.", printed)
		self.assertIn("Nope, you laid too much! Try again.", printed)
		self.assertEqual(terminal["lineBets"]["Don't Pass Odds"], 99)
		self.assertEqual(terminal["bank"], 101)
		self.assertEqual(terminal["chipsOnTable"], 109)

	def testOddsDontPassRejectOverMaxRefundsBeforeRetry(self):
		terminal = loadTerminalNamespace()
		terminal["bank"] = 400
		terminal["chipsOnTable"] = 10
		terminal["comeOut"] = 6
		terminal["lineBets"] = {
			"Pass": 0,
			"Pass Odds": 0,
			"Don't Pass": 10,
			"Don't Pass Odds": 0
		}
		with patch("builtins.input", side_effect=["150", "90"]):
			terminal["odds"]()
		self.assertEqual(terminal["lineBets"]["Don't Pass Odds"], 90)
		self.assertEqual(terminal["bank"], 310)
		self.assertEqual(terminal["chipsOnTable"], 100)

	def testOddsPassExistingWordingAndNoMultiplesWhenUnitOne(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craplessCraps
		terminal["bank"] = 200
		terminal["chipsOnTable"] = 20
		terminal["comeOut"] = 2
		terminal["lineBets"] = {
			"Pass": 10,
			"Pass Odds": 12,
			"Don't Pass": 0,
			"Don't Pass Odds": 0
		}
		writes = []
		terminal["writeOutput"] = lambda message: writes.append(str(message))
		with patch("builtins.input", side_effect=["12"]):
			terminal["odds"]()
		printed = " ".join(writes)
		self.assertIn("You have $12 in Odds for the 2. How much for your Odds?", printed)
		self.assertIn("Max odds is $60.", printed)
		self.assertNotIn("Multiples of 1.", printed)

	def testOddsDontPassExistingWordingAndTakeDownMessage(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craps
		terminal["bank"] = 200
		terminal["chipsOnTable"] = 50
		terminal["comeOut"] = 5
		terminal["lineBets"] = {
			"Pass": 0,
			"Pass Odds": 0,
			"Don't Pass": 10,
			"Don't Pass Odds": 30
		}
		writes = []
		terminal["writeOutput"] = lambda message: writes.append(str(message))
		with patch("builtins.input", side_effect=["0"]):
			terminal["odds"]()
		printed = " ".join(writes)
		self.assertIn("You have $30 laid against the 5. How much do you want to Lay?", printed)
		self.assertIn("Max odds is $99.", printed)
		self.assertIn("Multiples of 3.", printed)
		self.assertIn("Taking down your Lay Odds.", printed)

	def testPropBettingHiLowRetryPreservesAccounting(self):
		terminal = loadTerminalNamespace()
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 0
		terminal["propBets"] = terminal["createDefaultPropBets"]()
		with patch("builtins.input", side_effect=["hl", "3", "4", "x"]):
			terminal["propBetting"]()
		self.assertEqual(terminal["propBets"]["Snake Eyes"], 2)
		self.assertEqual(terminal["propBets"]["Boxcars"], 2)
		self.assertEqual(terminal["propBets"]["Hi Low"], 0)
		self.assertEqual(terminal["bank"], 96)
		self.assertEqual(terminal["chipsOnTable"], 4)

	def testPropBettingUsesIoAdaptersForHiLowFlow(self):
		terminal = loadTerminalNamespace()
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 0
		terminal["propBets"] = terminal["createDefaultPropBets"]()
		writes = []
		inputs = iter(["hl", "3", "4", "x"])
		terminal["writeOutput"] = lambda message: writes.append(str(message))
		terminal["readInput"] = lambda promptText: next(inputs)
		terminal["propBetting"]()
		self.assertEqual(terminal["propBets"]["Snake Eyes"], 2)
		self.assertEqual(terminal["propBets"]["Boxcars"], 2)
		self.assertEqual(terminal["bank"], 96)
		self.assertEqual(terminal["chipsOnTable"], 4)
		printed = " ".join(writes)
		self.assertIn("Type in your Prop Bet:", printed)
		self.assertIn("How much on the Hi-Low? Must be a multiple of 2.", printed)
		self.assertIn("That wasn't a multiple of 2! Try again, genius.", printed)
		self.assertIn("Done Prop Betting.", printed)

	def testPropPayUsesWriteOutputAdapter(self):
		terminal = loadTerminalNamespace()
		terminal["bank"] = 0
		terminal["chipsOnTable"] = 40
		terminal["propBets"] = terminal["createDefaultPropBets"]()
		terminal["propBets"]["Horn"] = 40
		terminal["die1"] = 5
		terminal["die2"] = 4
		writes = []
		terminal["writeOutput"] = lambda message: writes.append(str(message))
		terminal["propPay"](9)
		self.assertTrue(len(writes) > 0)

	def testPlacePresetAcrossExcludePoint(self):
		terminal = loadTerminalNamespace()
		terminal["bank"] = 200
		terminal["chipsOnTable"] = 0
		terminal["pointIsOn"] = True
		terminal["comeOut"] = 6
		terminal["place"] = {4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0}
		with patch("builtins.input", side_effect=["2", "n"]):
			terminal["placePreset"]("a")
		self.assertEqual(terminal["place"], {4: 10, 5: 10, 6: 0, 8: 12, 9: 10, 10: 10})
		self.assertEqual(terminal["bank"], 148)
		self.assertEqual(terminal["chipsOnTable"], 52)

	def testPlacePresetInsideExcludePoint(self):
		terminal = loadTerminalNamespace()
		terminal["bank"] = 200
		terminal["chipsOnTable"] = 0
		terminal["pointIsOn"] = True
		terminal["comeOut"] = 5
		terminal["place"] = {4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0}
		with patch("builtins.input", side_effect=["2", "n"]):
			terminal["placePreset"]("i")
		self.assertEqual(terminal["place"], {4: 0, 5: 0, 6: 12, 8: 12, 9: 10, 10: 0})
		self.assertEqual(terminal["bank"], 166)
		self.assertEqual(terminal["chipsOnTable"], 34)

	def testPlacePresetCenterSetsOnlySixAndEight(self):
		terminal = loadTerminalNamespace()
		terminal["bank"] = 168
		terminal["chipsOnTable"] = 32
		terminal["place"] = {4: 5, 5: 5, 6: 6, 8: 6, 9: 5, 10: 5}
		terminal["pointIsOn"] = False
		with patch("builtins.input", side_effect=["2"]):
			terminal["placePreset"]("c")
		self.assertEqual(terminal["place"], {4: 0, 5: 0, 6: 12, 8: 12, 9: 0, 10: 0})
		self.assertEqual(terminal["bank"], 176)
		self.assertEqual(terminal["chipsOnTable"], 24)

	def testPlaceMoverConvertsSixToFiveUnitNumber(self):
		terminal = loadTerminalNamespace()
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 24
		terminal["comeOut"] = 6
		terminal["place"] = {4: 0, 5: 0, 6: 24, 8: 0, 9: 0, 10: 0}
		terminal["placeMover"]()
		self.assertEqual(terminal["place"], {4: 20, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0})
		self.assertEqual(terminal["bank"], 104)
		self.assertEqual(terminal["chipsOnTable"], 20)

	def testPlaceMoverConvertsFiveUnitNumberToSix(self):
		terminal = loadTerminalNamespace()
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 30
		terminal["comeOut"] = 5
		terminal["place"] = {4: 10, 5: 25, 6: 0, 8: 0, 9: 0, 10: 0}
		terminal["placeMover"]()
		self.assertEqual(terminal["place"], {4: 10, 5: 0, 6: 30, 8: 0, 9: 0, 10: 0})
		self.assertEqual(terminal["bank"], 95)
		self.assertEqual(terminal["chipsOnTable"], 35)

	def testPlaceCheckFullPressMaintainsAccounting(self):
		terminal = loadTerminalNamespace()
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 18
		terminal["place"] = {4: 0, 5: 0, 6: 18, 8: 0, 9: 0, 10: 0}
		with patch("builtins.input", side_effect=["p"]):
			terminal["placeCheck"](6)
		self.assertEqual(terminal["place"][6], 36)
		self.assertEqual(terminal["bank"], 103)
		self.assertEqual(terminal["chipsOnTable"], 36)

	def testPlaceCheckHalfPressUsesNormalizedSixIncrement(self):
		terminal = loadTerminalNamespace()
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 18
		terminal["place"] = {4: 0, 5: 0, 6: 18, 8: 0, 9: 0, 10: 0}
		with patch("builtins.input", side_effect=["hp"]):
			terminal["placeCheck"](6)
		self.assertEqual(terminal["place"][6], 24)
		self.assertEqual(terminal["bank"], 115)
		self.assertEqual(terminal["chipsOnTable"], 24)

	def testPlaceCheckUsesReadInputForPressPrompt(self):
		terminal = loadTerminalNamespace()
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 18
		terminal["place"] = {4: 0, 5: 0, 6: 18, 8: 0, 9: 0, 10: 0}
		prompts = []
		terminal["readInput"] = lambda promptText: prompts.append(promptText) or ""
		terminal["writeOutput"] = lambda message: None
		terminal["placeCheck"](6)
		self.assertEqual(len(prompts), 1)
		self.assertIn("Change your bet?", prompts[0])

	def testPlaceCheckHalfPressNormalizedAfterCraplessHelperFlow(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craplessCraps
		terminal["bank"] = 200
		terminal["chipsOnTable"] = 0
		terminal["place"] = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		with patch("builtins.input", side_effect=["3"]):
			terminal["placePreset"]("c")
		with patch("builtins.input", side_effect=["hp"]):
			terminal["placeCheck"](8)
		self.assertEqual(terminal["place"][8], 24)
		self.assertEqual(terminal["bank"], 179)
		self.assertEqual(terminal["chipsOnTable"], 42)

	def testPlaceBetsCraplessEdgeUnderTwentyRejectsInvalidMultiple(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craplessCraps
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 0
		terminal["place"] = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		with patch("builtins.input", side_effect=["19", "18", "", "", "", "", "", "", "", "", ""]), patch("builtins.print") as mockPrint:
			terminal["placeBets"]()
		printed = " ".join(" ".join(str(a) for a in call.args) for call in mockPrint.call_args_list)
		self.assertIn("Invalid amount for that Place bet. Try again.", printed)
		self.assertEqual(terminal["place"][2], 18)
		self.assertEqual(terminal["bank"], 82)
		self.assertEqual(terminal["chipsOnTable"], 18)

	def testPlaceBetsCraplessEdgeOverTwentyAllowsNonMultipleAndShowsBuy(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craplessCraps
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 0
		terminal["place"] = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		with patch("builtins.input", side_effect=["21", "22", "", "", "", "", "", "", "", "", ""]), patch("builtins.print") as mockPrint:
			terminal["placeBets"]()
		printed = " ".join(" ".join(str(a) for a in call.args) for call in mockPrint.call_args_list)
		self.assertIn("Buying the 2 for $21.", printed)
		self.assertIn("Buying the 3 for $22.", printed)
		self.assertEqual(terminal["place"][2], 21)
		self.assertEqual(terminal["place"][3], 22)
		self.assertEqual(terminal["bank"], 57)
		self.assertEqual(terminal["chipsOnTable"], 43)

	def testPlaceBetsCraplessEdgeOverTwentyShowsBuyForElevenAndTwelve(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craplessCraps
		terminal["bank"] = 120
		terminal["chipsOnTable"] = 0
		terminal["place"] = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		with patch("builtins.input", side_effect=["", "", "", "", "", "", "", "", "21", "22"]), patch("builtins.print") as mockPrint:
			terminal["placeBets"]()
		printed = " ".join(" ".join(str(a) for a in call.args) for call in mockPrint.call_args_list)
		self.assertIn("Buying the 11 for $21.", printed)
		self.assertIn("Buying the 12 for $22.", printed)
		self.assertEqual(terminal["place"][11], 21)
		self.assertEqual(terminal["place"][12], 22)
		self.assertEqual(terminal["bank"], 77)
		self.assertEqual(terminal["chipsOnTable"], 43)

	def testPlaceBetsStandardFourAndTenShowBuyAtThreshold(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craps
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 0
		terminal["place"] = {4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0}
		with patch("builtins.input", side_effect=["10", "", "", "", "", "10"]), patch("builtins.print") as mockPrint:
			terminal["placeBets"]()
		printed = " ".join(" ".join(str(a) for a in call.args) for call in mockPrint.call_args_list)
		self.assertIn("Buying the 4 for $10.", printed)
		self.assertIn("Buying the 10 for $10.", printed)
		self.assertEqual(terminal["place"][4], 10)
		self.assertEqual(terminal["place"][10], 10)
		self.assertEqual(terminal["bank"], 80)
		self.assertEqual(terminal["chipsOnTable"], 20)

	def testPlaceBetsStandardFourUnderThresholdShowsNonBuyMessage(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craps
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 0
		terminal["place"] = {4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0}
		with patch("builtins.input", side_effect=["5", "", "", "", "", ""]), patch("builtins.print") as mockPrint:
			terminal["placeBets"]()
		printed = " ".join(" ".join(str(a) for a in call.args) for call in mockPrint.call_args_list)
		self.assertIn("$5 on the Place 4.", printed)
		self.assertNotIn("Buying the 4 for $5.", printed)
		self.assertEqual(terminal["place"][4], 5)
		self.assertEqual(terminal["bank"], 95)
		self.assertEqual(terminal["chipsOnTable"], 5)

	def testPlaceCheckCraplessEdgeTwoHalfPressNormalizesAndAccounts(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craplessCraps
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 18
		terminal["place"] = {2: 18, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		with patch("builtins.input", side_effect=["hp"]):
			terminal["placeCheck"](2)
		self.assertEqual(terminal["place"][2], 26)
		self.assertEqual(terminal["bank"], 191)
		self.assertEqual(terminal["chipsOnTable"], 26)

	def testPlaceCheckCraplessEdgeThreeHalfPressNormalizesAndAccounts(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craplessCraps
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 16
		terminal["place"] = {2: 0, 3: 16, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		with patch("builtins.input", side_effect=["hp"]):
			terminal["placeCheck"](3)
		self.assertEqual(terminal["place"][3], 24)
		self.assertEqual(terminal["bank"], 136)
		self.assertEqual(terminal["chipsOnTable"], 24)

	def testPlaceCheckCraplessEdgeTwoFullPressAccountsFromBuyHit(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craplessCraps
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 21
		terminal["place"] = {2: 21, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		with patch("builtins.input", side_effect=["p"]):
			terminal["placeCheck"](2)
		self.assertEqual(terminal["place"][2], 42)
		self.assertEqual(terminal["bank"], 203)
		self.assertEqual(terminal["chipsOnTable"], 42)

	def testPlaceCheckManualChangeCraplessEdgeUnderTwentyRejectsInvalidThenAccepts(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craplessCraps
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 18
		terminal["place"] = {2: 18, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		with patch("builtins.input", side_effect=["y", "19", "18"]), patch("builtins.print") as mockPrint:
			terminal["placeCheck"](2)
		printed = " ".join(" ".join(str(a) for a in call.args) for call in mockPrint.call_args_list)
		self.assertIn("Invalid amount for that Place bet. Try again.", printed)
		self.assertEqual(terminal["place"][2], 18)
		self.assertEqual(terminal["bank"], 199)
		self.assertEqual(terminal["chipsOnTable"], 18)

	def testPlaceCheckManualChangeCraplessEdgeOverTwentyAcceptsNonMultiple(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craplessCraps
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 18
		terminal["place"] = {2: 18, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		with patch("builtins.input", side_effect=["y", "21"]), patch("builtins.print"):
			terminal["placeCheck"](2)
		self.assertEqual(terminal["place"][2], 21)
		self.assertEqual(terminal["bank"], 196)
		self.assertEqual(terminal["chipsOnTable"], 21)

	def testLayAllAcrossSetsEachNumber(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craps
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 0
		terminal["layBets"] = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		terminal["readInput"] = lambda promptText: "2"
		terminal["writeOutput"] = lambda message: None
		terminal["layAll"]()
		self.assertEqual(terminal["layBets"], {2: 0, 3: 0, 4: 10, 5: 10, 6: 10, 8: 10, 9: 10, 10: 10, 11: 0, 12: 0})
		self.assertEqual(terminal["bank"], 40)
		self.assertEqual(terminal["chipsOnTable"], 60)

	def testLayEdgesCraplessSetsOnlyEdgeNumbers(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craplessCraps
		terminal["bank"] = 120
		terminal["chipsOnTable"] = 0
		terminal["layBets"] = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		terminal["readInput"] = lambda promptText: "2"
		terminal["writeOutput"] = lambda message: None
		terminal["layEdges"]()
		self.assertEqual(terminal["layBets"], {2: 10, 3: 10, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 10, 12: 10})
		self.assertEqual(terminal["bank"], 80)
		self.assertEqual(terminal["chipsOnTable"], 40)

	def testLayExtremeAcrossCraplessSetsAllLayNumbers(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craplessCraps
		terminal["bank"] = 200
		terminal["chipsOnTable"] = 0
		terminal["layBets"] = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		terminal["readInput"] = lambda promptText: "1"
		terminal["writeOutput"] = lambda message: None
		terminal["layExtremeAcross"]()
		self.assertEqual(terminal["layBets"], {2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 8: 5, 9: 5, 10: 5, 11: 5, 12: 5})
		self.assertEqual(terminal["bank"], 150)
		self.assertEqual(terminal["chipsOnTable"], 50)

	def testLayBettingTakeDownReturnsFunds(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craps
		terminal["bank"] = 90
		terminal["chipsOnTable"] = 10
		terminal["layBets"] = {2: 0, 3: 0, 4: 10, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		inputs = iter(["0", "", "", "", "", ""])
		terminal["readInput"] = lambda promptText: next(inputs)
		terminal["writeOutput"] = lambda message: None
		terminal["layBetting"]()
		self.assertEqual(terminal["layBets"], {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0})
		self.assertEqual(terminal["bank"], 100)
		self.assertEqual(terminal["chipsOnTable"], 0)


if __name__ == "__main__":
	unittest.main()
