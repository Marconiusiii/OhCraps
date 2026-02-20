#!/usr/bin/env python3

import random
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
