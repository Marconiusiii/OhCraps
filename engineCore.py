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
