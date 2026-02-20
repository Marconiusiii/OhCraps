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
    is_hard: bool


@dataclass
class GameState:
    bank: int
    chips_on_table: int
    throws: int
    point_is_on: bool
    come_out: int
    p2: int

    def get_point(self):
        if self.point_is_on:
            return self.come_out
        return None


class RollOutcome(Enum):
    NATURAL = auto()
    CRAPS = auto()
    POINT_ESTABLISHED = auto()
    POINT_HIT = auto()
    SEVEN_OUT = auto()
    NEUTRAL = auto()


def evaluate_roll(game_state: GameState, roll_value: int) -> RollOutcome:
    if not game_state.point_is_on:
        if roll_value in (7, 11):
            return RollOutcome.NATURAL
        if roll_value in (2, 3, 12):
            return RollOutcome.CRAPS
        return RollOutcome.POINT_ESTABLISHED

    if roll_value == 7:
        return RollOutcome.SEVEN_OUT
    if roll_value == game_state.come_out:
        return RollOutcome.POINT_HIT
    return RollOutcome.NEUTRAL


def roll_dice(rng: Optional[random.Random] = None) -> DiceRoll:
    source = rng if rng is not None else random
    d1 = source.randint(1, 6)
    d2 = source.randint(1, 6)

    if d1 >= d2:
        die1, die2 = d1, d2
    else:
        die1, die2 = d2, d1

    total = die1 + die2
    is_hard = die1 == die2
    return DiceRoll(die1=die1, die2=die2, total=total, is_hard=is_hard)
