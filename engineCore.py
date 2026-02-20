#!/usr/bin/env python3

import random
import math
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


@dataclass(frozen=True)
class DiceRoll:
	die1: int
	die2: int
	total: int
	isHard: bool


@dataclass
class GameState:
	bank: int
	chipsOnTable: int
	throws: int
	pointIsOn: bool
	comeOut: int
	p2: int

	def getPoint(self):
		if self.pointIsOn:
			return self.comeOut
		return None


@dataclass(frozen=True)
class LineSettlement:
	lineBets: dict
	bankDelta: int
	chipsOnTableDelta: int
	messages: list[str]


@dataclass(frozen=True)
class PlaceSettlement:
	placeBets: dict
	bankDelta: int
	chipsOnTableDelta: int
	hitNumber: int | None
	winAmount: int
	commissionPaid: int
	lossAmount: int
	messages: list[str]


@dataclass(frozen=True)
class LaySettlement:
	layBets: dict
	bankDelta: int
	chipsOnTableDelta: int
	lostNumber: int | None
	lostAmount: int
	totalWinAmount: int
	totalVigAmount: int
	messages: list[str]


@dataclass(frozen=True)
class FieldSettlement:
	fieldBet: int
	bankDelta: int
	chipsOnTableDelta: int
	winAmount: int
	lossAmount: int
	didWin: bool
	messages: list[str]


@dataclass(frozen=True)
class HardWaysSettlement:
	hardWays: dict
	bankDelta: int
	chipsOnTableDelta: int
	hitNumber: int | None
	lostNumber: int | None
	winAmount: int
	lossAmount: int
	messages: list[str]


@dataclass(frozen=True)
class ComeTableSettlement:
	comeBets: dict
	dComeBets: dict
	comeOdds: dict
	dComeOdds: dict
	bankDelta: int
	chipsOnTableDelta: int
	messages: list[str]


@dataclass(frozen=True)
class ComeBarSettlement:
	comeBet: int
	bankDelta: int
	chipsOnTableDelta: int
	movedNumber: int | None
	movedAmount: int
	messages: list[str]


@dataclass(frozen=True)
class DComeBarSettlement:
	dComeBet: int
	bankDelta: int
	chipsOnTableDelta: int
	movedNumber: int | None
	movedAmount: int
	messages: list[str]


@dataclass(frozen=True)
class PropSubsetSettlement:
	propBets: dict
	bankDelta: int
	chipsOnTableDelta: int
	messages: list[str]


class RollOutcome(Enum):
	natural = auto()
	craps = auto()
	pointEstablished = auto()
	pointHit = auto()
	sevenOut = auto()
	neutral = auto()


def evaluateRoll(gameState: GameState, rollValue: int) -> RollOutcome:
	if not gameState.pointIsOn:
		if rollValue in (7, 11):
			return RollOutcome.natural
		if rollValue in (2, 3, 12):
			return RollOutcome.craps
		return RollOutcome.pointEstablished

	if rollValue == 7:
		return RollOutcome.sevenOut
	if rollValue == gameState.comeOut:
		return RollOutcome.pointHit
	return RollOutcome.neutral


def rollDice(rng: Optional[random.Random] = None) -> DiceRoll:
	source = rng if rng is not None else random
	d1 = source.randint(1, 6)
	d2 = source.randint(1, 6)

	if d1 >= d2:
		die1, die2 = d1, d2
	else:
		die1, die2 = d2, d1

	total = die1 + die2
	isHard = die1 == die2
	return DiceRoll(die1=die1, die2=die2, total=total, isHard=isHard)


def maxPassOdds(pointNumber: int, baseBet: int) -> int:
	bet = int(baseBet)
	if pointNumber in [4, 10]:
		return bet * 3
	if pointNumber in [5, 9]:
		return bet * 4
	if pointNumber in [6, 8]:
		return bet * 5
	return 0


def maxComeOdds(number: int, baseBet: int) -> int:
	return maxPassOdds(number, baseBet)


def maxLayOdds(baseBet: int) -> int:
	return int(baseBet) * 10


def normalizeLineBets(lineBets: dict) -> dict:
	normalized = {
		"Pass": 0,
		"Pass Odds": 0,
		"Don't Pass": 0,
		"Don't Pass Odds": 0
	}
	for key in normalized:
		if key in lineBets:
			normalized[key] = int(lineBets[key])
	return normalized


def settleLineBets(lineBets: dict, pointIsOn: bool, roll: int, p2roll: int) -> LineSettlement:
	updatedLineBets = normalizeLineBets(lineBets)
	bankDelta = 0
	chipsOnTableDelta = 0
	messages = []

	if not pointIsOn:
		if roll in [7, 11]:
			if updatedLineBets["Pass"] > 0:
				messages.append(f"You won ${updatedLineBets['Pass']:,} on the Pass Line!")
				bankDelta += updatedLineBets["Pass"]
			if updatedLineBets["Don't Pass"] > 0:
				dontPassValue = updatedLineBets["Don't Pass"]
				messages.append(f"You lost ${dontPassValue:,} from the Don't Pass Line.")
				chipsOnTableDelta -= updatedLineBets["Don't Pass"]
				updatedLineBets["Don't Pass"] = 0
		elif roll in [2, 3, 12]:
			if updatedLineBets["Pass"] > 0:
				messages.append(f"You lost ${updatedLineBets['Pass']:,} from the Pass Line.")
				chipsOnTableDelta -= updatedLineBets["Pass"]
				updatedLineBets["Pass"] = 0
			if updatedLineBets["Don't Pass"] > 0:
				if roll in [2, 3]:
					dontPassValue = updatedLineBets["Don't Pass"]
					messages.append(f"You won ${dontPassValue:,} on the Don't Pass Line!")
					bankDelta += updatedLineBets["Don't Pass"]
				elif roll == 12:
					messages.append("12 is a Push!")
	elif pointIsOn:
		if p2roll == roll:
			if updatedLineBets["Pass"] > 0:
				messages.append(f"You won ${updatedLineBets['Pass']:,} on the Pass Line!")
				bankDelta += updatedLineBets["Pass"] * 2
				chipsOnTableDelta -= updatedLineBets["Pass"]
				updatedLineBets["Pass"] = 0
			if updatedLineBets["Don't Pass"] > 0:
				dontPassValue = updatedLineBets["Don't Pass"]
				messages.append(f"You lost ${dontPassValue:,} from the Don't Pass Line.")
				chipsOnTableDelta -= updatedLineBets["Don't Pass"]
				updatedLineBets["Don't Pass"] = 0
		elif p2roll == 7:
			if updatedLineBets["Pass"] > 0:
				messages.append(f"You lost ${updatedLineBets['Pass']:,} from the Pass Line.")
				chipsOnTableDelta -= updatedLineBets["Pass"]
				updatedLineBets["Pass"] = 0
			if updatedLineBets["Don't Pass"] > 0:
				dontPassValue = updatedLineBets["Don't Pass"]
				messages.append(f"You won ${dontPassValue:,} on the Don't Pass Line!")
				bankDelta += updatedLineBets["Don't Pass"] * 2
				chipsOnTableDelta -= updatedLineBets["Don't Pass"]
				updatedLineBets["Don't Pass"] = 0

	return LineSettlement(
		lineBets=updatedLineBets,
		bankDelta=bankDelta,
		chipsOnTableDelta=chipsOnTableDelta,
		messages=messages
	)


def normalizePlaceBets(placeBets: dict) -> dict:
	normalized = {
		4: 0,
		5: 0,
		6: 0,
		8: 0,
		9: 0,
		10: 0
	}
	for key in normalized:
		if key in placeBets:
			normalized[key] = int(placeBets[key])
	return normalized


def calculateVig(bet: int) -> int:
	total = bet * 0.05
	if bet < 25:
		return math.ceil(total)
	return math.floor(total)


def settlePlaceBets(placeBets: dict, roll: int) -> PlaceSettlement:
	updatedPlaceBets = normalizePlaceBets(placeBets)
	bankDelta = 0
	chipsOnTableDelta = 0
	hitNumber = None
	winAmount = 0
	commissionPaid = 0
	lossAmount = 0
	messages = []

	if roll in [4, 5, 6, 8, 9, 10] and updatedPlaceBets[roll] > 0:
		hitNumber = roll
		if roll in [4, 10] and updatedPlaceBets[roll] >= 10:
			commissionPaid = calculateVig(updatedPlaceBets[roll])
			winAmount = updatedPlaceBets[roll] * 2 - commissionPaid
		elif roll in [4, 10]:
			winAmount = (updatedPlaceBets[roll]//5) * 9
		elif roll in [5, 9]:
			winAmount = (updatedPlaceBets[roll]//5) * 7
		elif roll in [6, 8]:
			winAmount = (updatedPlaceBets[roll]//6) * 7 + updatedPlaceBets[roll]%6
		bankDelta += winAmount
		if commissionPaid > 0:
			messages.append(f"${commissionPaid:,} paid to the House for the vig.")
		messages.append(f"You won ${winAmount:,} on the Place {roll}!")

	elif roll == 7:
		for key in updatedPlaceBets:
			lossAmount += updatedPlaceBets[key]
			updatedPlaceBets[key] = 0
		chipsOnTableDelta -= lossAmount
		if lossAmount > 0:
			messages.append(f"You lost ${lossAmount:,} from the Place bets.")

	return PlaceSettlement(
		placeBets=updatedPlaceBets,
		bankDelta=bankDelta,
		chipsOnTableDelta=chipsOnTableDelta,
		hitNumber=hitNumber,
		winAmount=winAmount,
		commissionPaid=commissionPaid,
		lossAmount=lossAmount,
		messages=messages
	)


def normalizeLayBets(layBets: dict) -> dict:
	normalized = {
		4: 0,
		5: 0,
		6: 0,
		8: 0,
		9: 0,
		10: 0
	}
	for key in normalized:
		if key in layBets:
			normalized[key] = int(layBets[key])
	return normalized


def calculateLayWin(number: int, bet: int) -> int:
	if number in [4, 10]:
		return bet//2
	if number in [5, 9]:
		return (bet//3) * 2
	if number in [6, 8]:
		return (bet//6) * 5
	return 0


def calculateLayVig(win: int) -> int:
	if win <= 0:
		return 0
	vig = win * 0.05
	if vig < 1:
		return 1
	return math.floor(vig)


def settleLayBets(layBets: dict, roll: int) -> LaySettlement:
	updatedLayBets = normalizeLayBets(layBets)
	bankDelta = 0
	chipsOnTableDelta = 0
	lostNumber = None
	lostAmount = 0
	totalWinAmount = 0
	totalVigAmount = 0
	messages = []

	if roll in [4, 5, 6, 8, 9, 10] and updatedLayBets[roll] > 0:
		lostNumber = roll
		lostAmount = updatedLayBets[roll]
		messages.append(f"You lost ${lostAmount:,} from the Lay {roll}.")
		chipsOnTableDelta -= lostAmount
		updatedLayBets[roll] = 0

	elif roll == 7:
		for key in updatedLayBets:
			if updatedLayBets[key] > 0:
				win = calculateLayWin(key, updatedLayBets[key])
				vigPay = calculateLayVig(win)
				totalWinAmount += win
				totalVigAmount += vigPay
				messages.append(f"You won ${win:,} on the Lay {key}!")
		if totalWinAmount > 0:
			bankDelta += totalWinAmount
		if totalVigAmount > 0:
			messages.append(f"Taking out ${totalVigAmount:,} for the vig.")
			bankDelta -= totalVigAmount

	return LaySettlement(
		layBets=updatedLayBets,
		bankDelta=bankDelta,
		chipsOnTableDelta=chipsOnTableDelta,
		lostNumber=lostNumber,
		lostAmount=lostAmount,
		totalWinAmount=totalWinAmount,
		totalVigAmount=totalVigAmount,
		messages=messages
	)


def settleFieldBet(fieldBet: int, roll: int) -> FieldSettlement:
	currentFieldBet = int(fieldBet)
	bankDelta = 0
	chipsOnTableDelta = 0
	winAmount = 0
	lossAmount = 0
	didWin = False
	messages = []

	if currentFieldBet > 0:
		payout = currentFieldBet
		if roll in [2, 3, 4, 9, 10, 11, 12]:
			didWin = True
			if roll == 2:
				payout *= 2
				messages.append("Double in the bubble!")
			elif roll == 12:
				payout *= 3
				messages.append("Triple in the Field!")
			winAmount = payout
			bankDelta += payout
			messages.append(f"You won ${payout:,} on the Field!")
		else:
			lossAmount = currentFieldBet
			chipsOnTableDelta -= currentFieldBet
			currentFieldBet = 0
			messages.append(f"You lost ${lossAmount:,} from the Field.")

	return FieldSettlement(
		fieldBet=currentFieldBet,
		bankDelta=bankDelta,
		chipsOnTableDelta=chipsOnTableDelta,
		winAmount=winAmount,
		lossAmount=lossAmount,
		didWin=didWin,
		messages=messages
	)


def normalizeHardWays(hardWays: dict) -> dict:
	normalized = {
		4: 0,
		6: 0,
		8: 0,
		10: 0
	}
	for key in normalized:
		if key in hardWays:
			normalized[key] = int(hardWays[key])
	return normalized


def settleHardWays(hardWays: dict, roll: int, rollHard: bool) -> HardWaysSettlement:
	updatedHardWays = normalizeHardWays(hardWays)
	bankDelta = 0
	chipsOnTableDelta = 0
	hitNumber = None
	lostNumber = None
	winAmount = 0
	lossAmount = 0
	messages = []

	if roll == 7:
		for key in updatedHardWays:
			if updatedHardWays[key] > 0:
				lossAmount += updatedHardWays[key]
				updatedHardWays[key] = 0
		if lossAmount > 0:
			messages.append(f"You lost ${lossAmount:,} from the Hard Ways.")
			chipsOnTableDelta -= lossAmount

	elif roll in [4, 6, 8, 10] and updatedHardWays[roll] > 0:
		if rollHard:
			hitNumber = roll
			if roll in [4, 10]:
				winAmount = updatedHardWays[roll] * 7
			elif roll in [6, 8]:
				winAmount = updatedHardWays[roll] * 9
			messages.append(f"You won ${winAmount:,} on the Hard {roll}!")
			bankDelta += winAmount
		else:
			lostNumber = roll
			lossAmount = updatedHardWays[roll]
			messages.append(f"You lost ${lossAmount:,} from the Hard {roll}.")
			chipsOnTableDelta -= lossAmount
			updatedHardWays[roll] = 0

	return HardWaysSettlement(
		hardWays=updatedHardWays,
		bankDelta=bankDelta,
		chipsOnTableDelta=chipsOnTableDelta,
		hitNumber=hitNumber,
		lostNumber=lostNumber,
		winAmount=winAmount,
		lossAmount=lossAmount,
		messages=messages
	)


def normalizeComeBets(comeBets: dict) -> dict:
	normalized = dict(comeBets)
	for key in [4, 5, 6, 8, 9, 10]:
		if key not in normalized:
			normalized[key] = 0
		else:
			normalized[key] = int(normalized[key])
	return normalized


def normalizeNumberBetDict(numberDict: dict) -> dict:
	normalized = {
		4: 0,
		5: 0,
		6: 0,
		8: 0,
		9: 0,
		10: 0
	}
	for key in normalized:
		if key in numberDict:
			normalized[key] = int(numberDict[key])
	return normalized


def settleComeTableBets(comeBets: dict, dComeBets: dict, comeOdds: dict, dComeOdds: dict, roll: int, pointIsOn: bool, working: bool) -> ComeTableSettlement:
	updatedComeBets = normalizeComeBets(comeBets)
	updatedDComeBets = normalizeNumberBetDict(dComeBets)
	updatedComeOdds = normalizeNumberBetDict(comeOdds)
	updatedDComeOdds = normalizeNumberBetDict(dComeOdds)
	bankDelta = 0
	chipsOnTableDelta = 0
	messages = []

	if roll == 7:
		loss = 0
		lossOdds = 0
		for key in [4, 5, 6, 8, 9, 10]:
			loss += updatedComeBets[key]
			lossOdds += updatedComeOdds[key]
		if loss > 0:
			messages.append(f"You lost ${loss:,} from your Come Bets.")
			if lossOdds > 0 and (pointIsOn or working):
				messages.append(f"You lost ${lossOdds:,} from your Come Bet Odds.")
			elif lossOdds > 0 and not pointIsOn:
				messages.append(f"${lossOdds:,} returned to you from Come Odds.")
				bankDelta += lossOdds
			chipsOnTableDelta -= loss + lossOdds
			for key in [4, 5, 6, 8, 9, 10]:
				updatedComeBets[key] = 0
				updatedComeOdds[key] = 0

		win = 0
		winOdds = 0
		for key in [4, 5, 6, 8, 9, 10]:
			win += updatedDComeBets[key] * 2
			chipsOnTableDelta -= updatedDComeBets[key]
		for key in [4, 5, 6, 8, 9, 10]:
			if updatedDComeOdds[key] > 0 and (pointIsOn or working):
				chipsOnTableDelta -= updatedDComeOdds[key]
				bankDelta += updatedDComeOdds[key]
				if key in [4, 10]:
					winOdds += updatedDComeOdds[key]//2
				elif key in [5, 9]:
					winOdds += (updatedDComeOdds[key]//3) * 2
				elif key in [6, 8]:
					winOdds += (updatedDComeOdds[key]//6) * 5
			else:
				chipsOnTableDelta -= updatedDComeOdds[key]
				winOdds += updatedDComeOdds[key]
				updatedDComeOdds[key] = 0
		if win > 0:
			messages.append(f"You won ${win//2:,} from your Don't Come Bets!")
			if winOdds > 0 and (pointIsOn or working):
				messages.append(f"You won ${winOdds:,} from your Don't Come Bet Odds!")
			elif winOdds > 0 and not pointIsOn:
				messages.append(f"Returning ${winOdds:,} to you from your Don't Come odds.")
			bankDelta += win + winOdds
		for key in [4, 5, 6, 8, 9, 10]:
			updatedDComeBets[key] = 0
			updatedDComeOdds[key] = 0

	if roll in [4, 5, 6, 8, 9, 10]:
		if updatedComeBets[roll] > 0:
			messages.append(f"You won ${updatedComeBets[roll]:,} on the Come {roll}!")
			bankDelta += updatedComeBets[roll] * 2
			chipsOnTableDelta -= updatedComeBets[roll]
			updatedComeBets[roll] = 0
			if updatedComeOdds[roll] > 0 and (pointIsOn or working):
				cOddsWin = 0
				if roll in [4, 10]:
					cOddsWin = updatedComeOdds[roll] * 2
				elif roll in [5, 9]:
					cOddsWin += (updatedComeOdds[roll]//2) * 3
				elif roll in [6, 8]:
					cOddsWin += (updatedComeOdds[roll]//5) * 6
				messages.append(f"You won ${cOddsWin:,} on the Come {roll} Odds!")
				bankDelta += cOddsWin + updatedComeOdds[roll]
				chipsOnTableDelta -= updatedComeOdds[roll]
				updatedComeOdds[roll] = 0
			elif updatedComeOdds[roll] > 0 and not pointIsOn:
				messages.append(f"Returning ${updatedComeOdds[roll]:,} to you from your Come {roll} odds.")
				chipsOnTableDelta -= updatedComeOdds[roll]
				bankDelta += updatedComeOdds[roll]
				updatedComeOdds[roll] = 0

		if updatedDComeBets[roll] > 0:
			messages.append(f"You lost ${updatedDComeBets[roll]:,} from the Don't Come {roll}.")
			chipsOnTableDelta -= updatedDComeBets[roll]
			updatedDComeBets[roll] = 0
			if updatedDComeOdds[roll] > 0:
				messages.append(f"You lost ${updatedDComeOdds[roll]:,} from the Don't Come {roll} Odds.")
				chipsOnTableDelta -= updatedDComeOdds[roll]
				updatedDComeOdds[roll] = 0

	return ComeTableSettlement(
		comeBets=updatedComeBets,
		dComeBets=updatedDComeBets,
		comeOdds=updatedComeOdds,
		dComeOdds=updatedDComeOdds,
		bankDelta=bankDelta,
		chipsOnTableDelta=chipsOnTableDelta,
		messages=messages
	)


def settleComeBarBet(comeBet: int, roll: int) -> ComeBarSettlement:
	currentComeBet = int(comeBet)
	bankDelta = 0
	chipsOnTableDelta = 0
	movedNumber = None
	movedAmount = 0
	messages = []

	if currentComeBet > 0:
		if roll in [7, 11]:
			messages.append(f"You won ${currentComeBet:,} on the Come!")
			bankDelta += currentComeBet * 2
			chipsOnTableDelta -= currentComeBet
			currentComeBet = 0
		elif roll in [2, 3, 12]:
			messages.append(f"You lost ${currentComeBet:,} from the Come Bet.")
			chipsOnTableDelta -= currentComeBet
			currentComeBet = 0
		else:
			movedNumber = roll
			movedAmount = currentComeBet
			messages.append(f"Moving your Come Bet to the {roll}.")
			currentComeBet = 0

	return ComeBarSettlement(
		comeBet=currentComeBet,
		bankDelta=bankDelta,
		chipsOnTableDelta=chipsOnTableDelta,
		movedNumber=movedNumber,
		movedAmount=movedAmount,
		messages=messages
	)


def settleDComeBarBet(dComeBet: int, roll: int) -> DComeBarSettlement:
	currentDComeBet = int(dComeBet)
	bankDelta = 0
	chipsOnTableDelta = 0
	movedNumber = None
	movedAmount = 0
	messages = []

	if currentDComeBet > 0:
		if roll in [7, 11]:
			messages.append(f"You lost ${currentDComeBet:,} from the Don't Come.")
			chipsOnTableDelta -= currentDComeBet
			currentDComeBet = 0
		elif roll in [2, 3, 12]:
			if roll in [2, 3]:
				messages.append(f"You won ${currentDComeBet:,} on the Don't Come!")
				bankDelta += currentDComeBet * 2
			elif roll == 12:
				messages.append("12 is a Push!")
				bankDelta += currentDComeBet
			chipsOnTableDelta -= currentDComeBet
			currentDComeBet = 0
		else:
			movedNumber = roll
			movedAmount = currentDComeBet
			messages.append(f"Moving your Don't Come bet to the {roll}.")
			currentDComeBet = 0

	return DComeBarSettlement(
		dComeBet=currentDComeBet,
		bankDelta=bankDelta,
		chipsOnTableDelta=chipsOnTableDelta,
		movedNumber=movedNumber,
		movedAmount=movedAmount,
		messages=messages
	)


def settleOddsBets(lineBets: dict, roll: int, comeOut: int) -> LineSettlement:
	updatedLineBets = normalizeLineBets(lineBets)
	bankDelta = 0
	chipsOnTableDelta = 0
	messages = []

	passOdds = updatedLineBets["Pass Odds"]
	if passOdds > 0 and roll != 7:
		payout = 0
		if roll in [4, 10]:
			payout = passOdds * 2
		elif roll in [5, 9]:
			payout += (passOdds//2) * 3
		elif roll in [6, 8]:
			payout += (passOdds//5) * 6
		messages.append(f"You won ${payout:,} from your Pass Line Odds!")
		bankDelta += payout + passOdds
		chipsOnTableDelta -= passOdds
		updatedLineBets["Pass Odds"] = 0
	elif passOdds > 0 and roll == 7:
		messages.append(f"You lost ${passOdds:,} from your Pass Line Odds.")
		chipsOnTableDelta -= passOdds
		updatedLineBets["Pass Odds"] = 0

	dontPassOdds = updatedLineBets["Don't Pass Odds"]
	if dontPassOdds > 0 and roll == 7:
		payout = 0
		if comeOut in [4, 10]:
			payout += dontPassOdds//2
		elif comeOut in [5, 9]:
			payout += (dontPassOdds//3) * 2
		elif comeOut in [6, 8]:
			payout += (dontPassOdds//6) * 5
		messages.append(f"You won ${payout:,} on your Don't Pass Odds!")
		bankDelta += payout + dontPassOdds
		chipsOnTableDelta -= dontPassOdds
		updatedLineBets["Don't Pass Odds"] = 0
	elif dontPassOdds > 0 and roll == comeOut:
		messages.append(f"You lost ${dontPassOdds:,} from your Don't Pass Odds.")
		chipsOnTableDelta -= dontPassOdds
		updatedLineBets["Don't Pass Odds"] = 0

	return LineSettlement(
		lineBets=updatedLineBets,
		bankDelta=bankDelta,
		chipsOnTableDelta=chipsOnTableDelta,
		messages=messages
	)


def settlePropSubsetBets(propBets: dict, roll: int) -> PropSubsetSettlement:
	updatedPropBets = dict(propBets)
	bankDelta = 0
	chipsOnTableDelta = 0
	messages = []

	subsetKeys = ["Any Seven", "Any Craps", "Eleven", "C and E"]
	for key in subsetKeys:
		if key not in updatedPropBets:
			continue
		bet = int(updatedPropBets[key])
		if bet <= 0:
			continue

		multiplier = 0
		if key == "Any Seven" and roll == 7:
			multiplier = 4
		elif key == "Any Craps" and roll in [2, 3, 12]:
			multiplier = 7
		elif key == "Eleven" and roll == 11:
			multiplier = 15
		elif key == "C and E" and roll in [2, 3, 12]:
			multiplier = 3
		elif key == "C and E" and roll == 11:
			multiplier = 7

		if multiplier > 0:
			winAmount = bet * multiplier
			messages.append(f"You won ${winAmount:,} on the {key} bet!")
			bankDelta += bet + winAmount
			chipsOnTableDelta -= bet
			updatedPropBets[key] = 0
		else:
			messages.append(f"You lost ${bet:,} from the {key}.")
			chipsOnTableDelta -= bet
			updatedPropBets[key] = 0

	return PropSubsetSettlement(
		propBets=updatedPropBets,
		bankDelta=bankDelta,
		chipsOnTableDelta=chipsOnTableDelta,
		messages=messages
	)
