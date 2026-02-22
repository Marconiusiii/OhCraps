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

	def testSettleLayBetsForModeCraplessReturnsAnyLay(self):
		layBets = {4: 20, 5: 0, 6: 30, 8: 0, 9: 0, 10: 0}
		settlement = settleLayBetsForMode(layBets=layBets, roll=7, gameMode=GameMode.craplessCraps)
		self.assertEqual(settlement.bankDelta, 50)
		self.assertEqual(settlement.chipsOnTableDelta, -50)
		self.assertEqual(settlement.layBets[4], 0)
		self.assertEqual(settlement.layBets[6], 0)
		self.assertIn("Lay bets are not available in Crapless Craps. Returning $50.", settlement.messages)

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
		with patch("builtins.input", side_effect=["1"]):
			terminal["selectGameMode"]()
		self.assertEqual(terminal["gameMode"], terminal["GameMode"].craps)

	def testSelectGameModeAcceptsCrapless(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craps
		with patch("builtins.input", side_effect=["2"]):
			terminal["selectGameMode"]()
		self.assertEqual(terminal["gameMode"], terminal["GameMode"].craplessCraps)

	def testSelectGameModeRejectsInvalidThenAccepts(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craps
		with patch("builtins.input", side_effect=["x", "2"]):
			terminal["selectGameMode"]()
		self.assertEqual(terminal["gameMode"], terminal["GameMode"].craplessCraps)

	def testLineBettingRejectsDontPassInCrapless(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craplessCraps
		terminal["lineBets"] = {"Pass": 0, "Pass Odds": 0, "Don't Pass": 0, "Don't Pass Odds": 0}
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 0
		with patch("builtins.input", side_effect=["d", "x"]), patch("builtins.print"):
			terminal["lineBetting"]()
		self.assertEqual(terminal["lineBets"]["Don't Pass"], 0)

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

	def testHandleLayMenuCommandCraplessGuardExits(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craplessCraps
		with patch("builtins.print"):
			result = terminal["handleLayMenuCommand"]("y", pointPhase=True)
		self.assertEqual(result["success"], False)
		self.assertEqual(result["stateChanged"], False)
		self.assertEqual(result["shouldExitMenu"], True)

	def testHandleLayMenuCommandInvalidNoMutation(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craps
		terminal["layOff"] = False
		terminal["bank"] = 200
		terminal["chipsOnTable"] = 0
		terminal["layBets"] = {4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0}
		with patch("builtins.print"):
			result = terminal["handleLayMenuCommand"]("zz", pointPhase=True)
		self.assertEqual(result["success"], False)
		self.assertEqual(result["stateChanged"], False)
		self.assertEqual(result["shouldExitMenu"], False)
		self.assertEqual(terminal["layOff"], False)
		self.assertEqual(terminal["bank"], 200)
		self.assertEqual(terminal["chipsOnTable"], 0)
		self.assertEqual(terminal["layBets"], {4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0})

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
		self.assertEqual(result["shouldRoll"], False)
		self.assertEqual(calls, [False])

	def testHandleBettingCommandRoutesPlaceMenuInPointPhase(self):
		terminal = loadTerminalNamespace()
		calls = []
		def fakeRunPlaceMenu(pointPhase=False):
			calls.append(pointPhase)
		terminal["runPlaceMenu"] = fakeRunPlaceMenu
		with patch("builtins.print"):
			result = terminal["handleBettingCommand"]("p", pointPhase=True)
		self.assertEqual(result["shouldRoll"], False)
		self.assertEqual(calls, [True])

	def testHandleBettingCommandPointRollReturnsTrue(self):
		terminal = loadTerminalNamespace()
		with patch("builtins.print"):
			result = terminal["handleBettingCommand"]("x", pointPhase=True)
		self.assertEqual(result["shouldRoll"], True)

	def testHandleBettingCommandPointOddsWithoutLineBet(self):
		terminal = loadTerminalNamespace()
		terminal["lineBets"] = {"Pass": 0, "Pass Odds": 0, "Don't Pass": 0, "Don't Pass Odds": 0}
		with patch("builtins.print") as mockPrint:
			result = terminal["handleBettingCommand"]("o", pointPhase=True)
		self.assertEqual(result["shouldRoll"], False)
		printed = "\n".join(str(args[0]) for args, _ in mockPrint.call_args_list if args)
		self.assertIn("You don't have a Line bet, silly!", printed)

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
		self.assertEqual(result["enteredPointPhase"], False)
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
		self.assertEqual(result["enteredPointPhase"], True)
		self.assertEqual(terminal["pointIsOn"], True)
		self.assertEqual(terminal["working"], False)
		self.assertEqual(terminal["comeOut"], 6)

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
		self.assertEqual(result["pointRoundEnded"], True)
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
		self.assertEqual(result["pointRoundEnded"], False)
		self.assertEqual(terminal["pointIsOn"], True)
		self.assertEqual(terminal["throws"], 4)
		self.assertEqual(terminal["placeOff"], False)
		self.assertEqual(terminal["layOff"], False)
		self.assertEqual(terminal["hardOff"], False)

	def testRunPointPhaseBettingMenuLoopsUntilRollCommand(self):
		terminal = loadTerminalNamespace()
		calls = []
		def fakeHandleBettingCommand(command, pointPhase=False):
			calls.append((command, pointPhase))
			return {"shouldRoll": command == "x"}
		terminal["handleBettingCommand"] = fakeHandleBettingCommand
		with patch("builtins.input", side_effect=["h", "x"]), patch("builtins.print"):
			result = terminal["runPointPhaseBettingMenu"]()
		self.assertEqual(result["shouldRoll"], True)
		self.assertEqual(calls, [("h", True), ("x", True)])

	def testRunPointPhaseBettingMenuUsesPointPhaseTrue(self):
		terminal = loadTerminalNamespace()
		pointPhaseFlags = []
		def fakeHandleBettingCommand(command, pointPhase=False):
			pointPhaseFlags.append(pointPhase)
			return {"shouldRoll": True}
		terminal["handleBettingCommand"] = fakeHandleBettingCommand
		with patch("builtins.input", side_effect=["x"]), patch("builtins.print"):
			result = terminal["runPointPhaseBettingMenu"]()
		self.assertEqual(result["shouldRoll"], True)
		self.assertEqual(pointPhaseFlags, [True])

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

	def testCreateActionResultShape(self):
		terminal = loadTerminalNamespace()
		result = terminal["createActionResult"](success=False, messages=["m1"], stateChanged=True)
		self.assertEqual(result["success"], False)
		self.assertEqual(result["messages"], ["m1"])
		self.assertEqual(result["stateChanged"], True)

	def testComeCheckReturnsActionResultForMovedComeBet(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craps
		terminal["comeBet"] = 10
		terminal["comeBets"] = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, "Come": 0}
		terminal["comeOdds"] = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 10
		with patch("builtins.input", side_effect=["n"]), patch("builtins.print"):
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

		def fakePrint(*args, **kwargs):
			text = " ".join(str(part) for part in args)
			if "Moving your Come Bet to the 5." in text:
				seenMoveReminder["value"] = True

		def fakeInput(prompt=""):
			self.assertEqual(prompt, "Come Odds for the 5? > ")
			self.assertEqual(seenMoveReminder["value"], True)
			return "n"

		with patch("builtins.print", side_effect=fakePrint), patch("builtins.input", side_effect=fakeInput):
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

		def fakePrint(*args, **kwargs):
			printedTexts.append(" ".join(str(part) for part in args))

		with patch("builtins.print", side_effect=fakePrint), patch("builtins.input", side_effect=["y", "100", "20"]):
			result = terminal["comeCheck"](5)

		self.assertEqual(result["messages"].count("Way too high on your Odds, there. Try again."), 0)
		self.assertEqual(result["messages"].count("Ok, $20 on your Come 5 odds."), 1)
		self.assertEqual(sum(1 for text in printedTexts if "How much for your Come 5 Odds? Max is $40, multiples of 2" in text), 2)
		self.assertEqual(sum(1 for text in printedTexts if "Way too high on your Odds, there. Try again." in text), 1)
		self.assertEqual(terminal["comeOdds"][5], 20)

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

		def fakePrint(*args, **kwargs):
			text = " ".join(str(part) for part in args)
			printedTexts.append(text)
			if "Moving your Don't Come bet to the 5." in text:
				seenMoveReminder["value"] = True

		def fakeInput(prompt=""):
			inputCalls["count"] += 1
			if prompt == "Lay Odds on the 5? > ":
				self.assertEqual(seenMoveReminder["value"], True)
				return "y"
			if prompt == "\t$> ":
				if inputCalls["count"] == 2:
					return "120"
				if inputCalls["count"] == 3:
					return "90"
			raise AssertionError(f"Unexpected prompt: {prompt}")

		with patch("builtins.print", side_effect=fakePrint), patch("builtins.input", side_effect=fakeInput):
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

		def fakePrint(*args, **kwargs):
			printedTexts.append(" ".join(str(part) for part in args))

		with patch("builtins.print", side_effect=fakePrint), patch("builtins.input", side_effect=["y", "100", "99"]):
			result = terminal["comeCheck"](5)

		self.assertEqual(result["messages"].count("Way too much for your Lay Odds! Try again."), 0)
		self.assertEqual(result["messages"].count("Ok, $99 laid on the Don't Come 5."), 1)
		self.assertEqual(sum(1 for text in printedTexts if "How much for your Lay 5 Odds? Max is $99, multiples of 3" in text), 2)
		self.assertEqual(sum(1 for text in printedTexts if "Way too much for your Lay Odds! Try again." in text), 1)
		self.assertEqual(terminal["dComeOdds"][5], 99)

	def testComeCheckReturnsNoChangeActionResultWhenNoBarBets(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craps
		terminal["comeBet"] = 0
		terminal["dComeBet"] = 0
		with patch("builtins.print"):
			result = terminal["comeCheck"](9)
		self.assertEqual(result["success"], True)
		self.assertEqual(result["stateChanged"], False)

	def testCdcOddsChangeRejectsInvalidComeOddsUnitInCraps(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craps
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 0
		terminal["comeBets"] = {2: 0, 3: 0, 4: 0, 5: 10, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, "Come": 0}
		terminal["comeOdds"] = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		with patch("builtins.input", side_effect=["3", "4"]), patch("builtins.print"):
			terminal["cdcOddsChange"](terminal["comeBets"], terminal["comeOdds"])
		self.assertEqual(terminal["comeOdds"][5], 4)
		self.assertEqual(terminal["bank"], 96)
		self.assertEqual(terminal["chipsOnTable"], 4)

	def testCdcOddsChangeRejectsInvalidDontComeOddsUnitInCrapless(self):
		terminal = loadTerminalNamespace()
		terminal["gameMode"] = terminal["GameMode"].craplessCraps
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 0
		terminal["dComeBets"] = {2: 12, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		terminal["dComeOdds"] = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
		with patch("builtins.input", side_effect=["5", "6"]), patch("builtins.print"):
			terminal["cdcOddsChange"](terminal["dComeBets"], terminal["dComeOdds"])
		self.assertEqual(terminal["dComeOdds"][2], 6)
		self.assertEqual(terminal["bank"], 94)
		self.assertEqual(terminal["chipsOnTable"], 6)

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
		with patch("builtins.input", side_effect=["5", "", "", ""]):
			terminal["hardWaysBetting"]()
		self.assertEqual(terminal["hardWays"][4], 5)
		self.assertEqual(terminal["hardWays"][6], 0)
		self.assertEqual(terminal["hardWays"][8], 0)
		self.assertEqual(terminal["hardWays"][10], 0)
		self.assertEqual(terminal["bank"], 95)
		self.assertEqual(terminal["chipsOnTable"], 5)

	def testHardWaysBettingTakeDownReturnsFunds(self):
		terminal = loadTerminalNamespace()
		terminal["bank"] = 90
		terminal["chipsOnTable"] = 10
		terminal["hardWays"] = {4: 0, 6: 10, 8: 0, 10: 0}
		with patch("builtins.input", side_effect=["", "0", "", ""]):
			terminal["hardWaysBetting"]()
		self.assertEqual(terminal["hardWays"][6], 0)
		self.assertEqual(terminal["bank"], 100)
		self.assertEqual(terminal["chipsOnTable"], 0)

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
		with patch("builtins.input", side_effect=["3", "4"]), patch("builtins.print") as mockPrint:
			terminal["odds"]()
		printed = " ".join(" ".join(str(a) for a in call.args) for call in mockPrint.call_args_list)
		self.assertIn("How much for your Pass 5 Odds? Max is $40, multiples of 2", printed)
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
		with patch("builtins.input", side_effect=["100", "99"]), patch("builtins.print") as mockPrint:
			terminal["odds"]()
		printed = " ".join(" ".join(str(a) for a in call.args) for call in mockPrint.call_args_list)
		self.assertIn("How much for your Don't Pass 5 Lay Odds? Max is $99, multiples of 3", printed)
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
		terminal["bank"] = 100
		terminal["chipsOnTable"] = 0
		terminal["layBets"] = {4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0}
		with patch("builtins.input", side_effect=["2"]):
			terminal["layAll"]()
		self.assertEqual(terminal["layBets"], {4: 10, 5: 10, 6: 10, 8: 10, 9: 10, 10: 10})
		self.assertEqual(terminal["bank"], 40)
		self.assertEqual(terminal["chipsOnTable"], 60)

	def testLayBettingTakeDownReturnsFunds(self):
		terminal = loadTerminalNamespace()
		terminal["bank"] = 90
		terminal["chipsOnTable"] = 10
		terminal["layBets"] = {4: 10, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0}
		with patch("builtins.input", side_effect=["0", "", "", "", "", ""]):
			terminal["layBetting"]()
		self.assertEqual(terminal["layBets"], {4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0})
		self.assertEqual(terminal["bank"], 100)
		self.assertEqual(terminal["chipsOnTable"], 0)


if __name__ == "__main__":
	unittest.main()
