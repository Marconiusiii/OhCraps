#!/usr/bin/env python3

import random
import math
import os
from engineCore import settleLineBetsForMode, settleOddsBets, settlePlaceBetsForMode, settleLayBetsForMode, settleFieldBet, settleHardWays, settleComeTableBets, settleComeBarBet, settleDComeBarBet, maxPassOdds, maxComeOdds, maxComeOddsForMode, comeOddsUnitForMode, dComeOddsUnitForMode, isOddsBetUnitValid, maxLayOdds, oddsBetLimits, settlePropSubsetBets, settleBuffaloBet, settleHopBets, createDefaultPropBets, getPropKeyMatrix, resolvePropAliases, calculateHalfPressIncrement, createGameState, syncGameState, GameState, RollOutcome, evaluateRoll, rollDice, GameMode, parseGameModeChoice, getRulesProfile

#Version Number
version = "7.0.0"
engineApiVersion = "1.0.0"

outputHandler = None
inputHandler = None
randomProvider = random
eventHandler = None
outputCaptureOn = False
outputCaptureBuffer = []
promptCaptureOn = False
promptCaptureBuffer = []

def setIoHandlers(outputFunc=None, inputFunc=None):
	global outputHandler, inputHandler
	if outputFunc is not None:
		outputHandler = outputFunc
	if inputFunc is not None:
		inputHandler = inputFunc

def resetIoHandlers():
	global outputHandler, inputHandler
	outputHandler = None
	inputHandler = None

def setRandomProvider(provider=None):
	global randomProvider
	if provider is None:
		randomProvider = random
	else:
		randomProvider = provider

def resetRandomProvider():
	global randomProvider
	randomProvider = random

def setEventHandler(handler=None):
	global eventHandler
	eventHandler = handler

def resetEventHandler():
	global eventHandler
	eventHandler = None

def emitEvent(eventName, payload=None):
	if eventHandler is not None:
		eventPayload = payload if payload is not None else {}
		if isinstance(eventPayload, dict):
			eventPayload = withApiVersion(eventPayload)
		eventHandler(str(eventName), eventPayload)

def withApiVersion(payload):
	payloadDict = dict(payload) if payload is not None else {}
	payloadDict["engineApiVersion"] = engineApiVersion
	return payloadDict

def beginOutputCapture():
	global outputCaptureOn, outputCaptureBuffer
	outputCaptureOn = True
	outputCaptureBuffer = []
	return list(outputCaptureBuffer)

def endOutputCapture():
	global outputCaptureOn
	outputCaptureOn = False
	return getCapturedOutput()

def getCapturedOutput():
	return list(outputCaptureBuffer)

def beginPromptCapture():
	global promptCaptureOn, promptCaptureBuffer
	promptCaptureOn = True
	promptCaptureBuffer = []
	return list(promptCaptureBuffer)

def endPromptCapture():
	global promptCaptureOn
	promptCaptureOn = False
	return getCapturedPrompts()

def getCapturedPrompts():
	return list(promptCaptureBuffer)

def runWithCapture(func):
	global outputCaptureOn, outputCaptureBuffer, promptCaptureOn, promptCaptureBuffer
	priorOutputCaptureOn = bool(outputCaptureOn)
	priorPromptCaptureOn = bool(promptCaptureOn)
	priorOutputBuffer = list(outputCaptureBuffer)
	priorPromptBuffer = list(promptCaptureBuffer)
	beginOutputCapture()
	beginPromptCapture()
	try:
		resultValue = func()
		return {
			"result": resultValue,
			"capturedOutput": getCapturedOutput(),
			"capturedPrompts": getCapturedPrompts()
		}
	finally:
		outputCaptureOn = priorOutputCaptureOn
		promptCaptureOn = priorPromptCaptureOn
		outputCaptureBuffer = priorOutputBuffer if priorOutputCaptureOn else []
		promptCaptureBuffer = priorPromptBuffer if priorPromptCaptureOn else []

def writeOutput(message):
	global outputCaptureBuffer
	if outputCaptureOn:
		outputCaptureBuffer.append(str(message))
	if outputHandler is None:
		print(message)
	else:
		outputHandler(message)

def readInput(promptText):
	global promptCaptureBuffer
	promptValue = str(promptText)
	if promptCaptureOn:
		promptCaptureBuffer.append(promptValue)
	emitEvent("inputRequested", {"prompt": promptValue})
	if inputHandler is None:
		return str(input(promptValue))
	return str(inputHandler(promptValue))

class comeOutRollResult:
	def __init__(self, enteredPointPhase, outcome):
		self.enteredPointPhase = bool(enteredPointPhase)
		self.outcome = outcome

class pointRollResult:
	def __init__(self, pointRoundEnded, outcome):
		self.pointRoundEnded = bool(pointRoundEnded)
		self.outcome = outcome

class comeOutRoundResult:
	def __init__(self, enteredPointPhase, outcome):
		self.enteredPointPhase = bool(enteredPointPhase)
		self.outcome = outcome

class pointPhaseRoundResult:
	def __init__(self, roundEnded, outcome):
		self.roundEnded = bool(roundEnded)
		self.outcome = outcome

class bettingCommandResult:
	def __init__(self, shouldRoll=False, handled=True):
		self.shouldRoll = bool(shouldRoll)
		self.handled = bool(handled)

class GameRuntime:
	def __init__(self, bank=0, chipsOnTable=0, throws=0, comeOut=0, pointIsOn=False, p2=0, gameMode=GameMode.craps):
		self.bank = int(bank)
		self.chipsOnTable = int(chipsOnTable)
		self.throws = int(throws)
		self.comeOut = int(comeOut)
		self.pointIsOn = bool(pointIsOn)
		self.p2 = int(p2)
		self.gameMode = gameMode

#Roll and Dice Setup
die1 = die2 = 0

def roll():
	global rollHard, pointIsOn, die1, die2

	rollHard = False

	dice = rollDice()
	die1 = dice.die1
	die2 = dice.die2
	total = dice.total

	if die1 == die2 and total in [4, 6, 8, 10]:
		rollHard = True
		writeOutput(f"\n{total} the Hard Way!\n")
		writeOutput("\n" + stickman(total))
	elif total == 7 and pointIsOn == False:
		writeOutput(f"\n{total} winner! Pay the line, take the don't!\n")
	elif total == 11 and pointIsOn == False and gameMode == GameMode.craps:
		writeOutput(f"\n{total} winner! Pay the line, take the don't!\n")
	else:
		call = randomProvider.randrange(1, 21)

		# Call picks a random number between 1 and 20. If the number is <= 10,
		# or if the total is in [2, 3, 11, 12], it uses stickman.
		# Otherwise it calls out the dice faces.
		if call <= 10 or total in [2, 3, 11, 12]:
			writeOutput(f"\n{total}, {stickman(total)}!\n")
		else:
			writeOutput(f"\n{total}, a {die1} {die2} {total}!\n")

	return total

dealerCalls = {
2: ["Craps", "eye balls", "two aces", "rats eyes", "snake eyes", "eleven in a shoe store", "twice in the rice", "two craps two, two bad boys from Illinois", "two crap aces", "aces in both places", "a spot and a dot", "dimples", "double the Field"],
3: ["Craps", "ace-deuce", "three craps, ace caught a deuce, no use", "divorce roll, come up single", "three craps three, the indicator", "crap and a half", "small ace deuce, can't produce", "2 , 1, son of a gun"],
4: ["Little Joe", "Little Joe from Kokomo", "Ace Tres", "Ace Tres the easy way", "Little Billy from Piccadilly", "Little Joe from Idaho"],
5: ["After 5 the Field's alive", "Fiver Fiver Race car Driver", "No Field 5", "Little Phoebe", "We got the fiver", "Five 5", "Take a dive"],
6: ["The national average", "Catch 'em in the corner", "Sixie from Dixie"],
7: ["Line Away, grab the money", "the bruiser", "Out", "Loser 7", "Nevada Breakfast, two rolls and no coffee", "Cinco Dos, Adios", "Adios", "3 4 on the floor", "Big Red"],
8: ["eighter from the theater", "the Great", "get yer mate"],
9: ["niner 9.", "center field 9", "Center of the garden", "ocean liner Niner", "Nina from Pasadena", "nina Niner, wine and dine her", "El Nine-O", "Niner, nothing finer", "Neener Neener from Pasadeener"],
10: ["The big one on the end", "64 out the door", "The Big One"],
11: ["Yo Eleven", "Yo", "6 5, no drive", "yo 'leven", "It's not my eleven, it's Yo Eleven", "Bow wow wow yippie Yo yippie yay"],
12: ["craps", "midnight", "a whole lotta crap", "craps to the max", "boxcars", "all the spots we gots", "triple field", "atomic craps", "Hobo's delight"]
}

hardCalls = {
4: ["Double deuce", "2 2 Ballerina Special", "Hit us in the tutu", "2 spots and 2 dots", "It's little but it came Hard"],
6: ["Sixie from Dixie", "tree tre", "Pair of trees", "Double 3s"],
8: ["Double 4s", "Ozzy and Harriet", "A square pair", "A square pair will take ya there", "Pair of windows", "Windows"],
10: ["Pair of sunflowers", "Two stars from Mars", "Double 5s", "A Hard 10 to please 'er", "Girl's best friend", "Puppy paws", "55 to stay alive", "Pair of roses", "Two starfish walkin'"]
}

def stickman(roll):
	global rollHard
	if rollHard:
		return hardCalls[roll][randomProvider.randrange(0, len(hardCalls[roll]))]
	else:
		return dealerCalls[roll][randomProvider.randrange(0, len(dealerCalls[roll]))]

# Fire Bet Setup

fire = []
fireBet = 0

def fireBetting():
	global fireBet
	writeOutput("\tHow much on the Fire Bet?")
	fireBet = betPrompt()
	writeOutput(f"\tOk, ${fireBet:,} on the Fire Bet. Good Luck!")

def fireCheck():
	global bank, fire, fireBet, comeOut, p2, chipsOnTable
	if p2 == 7:
		chipsOnTable -= fireBet
		if len(fire) < 4:
			writeOutput(f"You lost ${fireBet:,} from the Fire Bet.")
			fireBet = 0
			fire = []
		elif len(fire) == 4:
			writeOutput(f"You won ${fireBet * 25:,} on the Fire Bet! Great job!")
			bank += fireBet * 25
			fireBet = 0
			fire = []
		elif len(fire) == 5:
			writeOutput(f"You won ${fireBet * 250:,} on the Fire Bet! Holy Crap!")
			bank += fireBet * 250
			fireBet = 0
			fire = []
		elif len(fire) == 6:
			writeOutput(f"Wowsers! You nailed the Fire Bet Jackpot and won ${fireBet * 1000:,}!!")
			bank += fireBet * 1000
			fireBet = 0
			fire = []
	elif p2 in [4, 5, 6, 8, 9, 10] and p2 == comeOut:
		if p2 not in fire:
			fire.append(p2)
			fire.sort()
			writeOutput(f"Fire Bet Point Numbers: {fire}")

# Hard Ways Setup
rollHard = False
hardOff = False

hardWays = {
4: 0,
6: 0,
8: 0,
10: 0
}

def hardWaysBetting():
	global hardWays, bank, chipsOnTable
	for key in hardWays:
		if hardWays[key] > 0:
			writeOutput(f"You have ${hardWays[key]:,} on the hard {key}.")
		writeOutput(f"How much on the Hard {key}?")
		madeBet = True
		while True:
			bet = 0
			try:
				bet = int(readInput("$>"))
				if bet > bank + chipsOnTable:
					writeOutput("You don't have enough money to make that bet! Try again.")
					outOfMoney()
					writeOutput(f"How much on the Hard {key}?")
					continue
				madeBet = True
				break
			except ValueError:
				bet = hardWays[key]
				madeBet = False
				break

		if bet > 0:
			chipsOnTable -= hardWays[key]
			if madeBet and bet != hardWays[key]:
				bank -= bet - hardWays[key]
			hardWays[key] = bet
			chipsOnTable += bet
			writeOutput(f"${bet:,} on the Hard {key}.")
		elif hardWays[key] > 0 and bet == 0:
			writeOutput(f"Ok, taking down your Hard {key} bet.")
			chipsOnTable -= hardWays[key]
			bank += hardWays[key]
			hardWays[key] = 0

def hardTakeDown():
	global hardWays, bank, chipsOnTable
	writeOutput("Taking down your Hard Ways.")
	for key in hardWays:
		chipsOnTable -= hardWays[key]
		bank += hardWays[key]
		hardWays[key] = 0

def hardAuto():
	global chipsOnTable, bank, hardWays
	writeOutput("How many $1 units on each of the Hard Ways?")
	hardAcr = betPrompt()
	chipsOnTable -= hardAcr
	bank += hardAcr
	for key in hardWays:
		chipsOnTable -= hardWays[key]
		bank += hardWays[key]
		hardWays[key] = hardAcr
		chipsOnTable += hardAcr
		bank -= hardAcr
	writeOutput(f"Ok, ${hardAcr:,} on each of the Hard Ways.")

def hardHigh(num):
	global chipsOnTable, bank, hardWays
	number = int(num[1:])
	writeOutput(f"How much to spread across the Hard Ways, high on the {number}?")
	bet = betPrompt()
	lowBet = bet//5
	highBet = bet - (lowBet*3)
	for key in hardWays:
		chipsOnTable -= hardWays[key]
		bank += hardWays[key]
		if key == number:
			hardWays[key] = highBet
		else:
			hardWays[key] = lowBet
	writeOutput(f"Ok, ${highBet:,} on the Hard {number}, ${lowBet:,} each on the other Hard Ways for a total of ${bet:,}.")


"""
algorithm for spreading weird bets across with a high number:
bet - (bet//5 * 3) = high bet
bet//5 = low bets
"""

def hardCheck(roll):
	global bank, chipsOnTable, hardWays, rollHard
	snapshot = captureBetSnapshot()
	settlement = settleHardWays(hardWays=hardWays, roll=roll, rollHard=rollHard)
	snapshot["hardWays"] = settlement.hardWays
	snapshot["bank"] += settlement.bankDelta
	snapshot["chipsOnTable"] += settlement.chipsOnTableDelta
	applyBetSnapshot(snapshot)
	for message in settlement.messages:
		writeOutput(message)

	if settlement.hitNumber is not None:
		if str(readInput("Press your bet? > ")).lower() in ['y', 'yes']:
			writeOutput(f"How much on the Hard {settlement.hitNumber}?")
			chipsOnTable -= hardWays[settlement.hitNumber]
			bank += hardWays[settlement.hitNumber]
			hardWays[settlement.hitNumber] = betPrompt()
			if hardWays[settlement.hitNumber] == 0:
				writeOutput(f"Ok, taking down your Hard {settlement.hitNumber} bet.")
			else:
				writeOutput(f"Ok, bumping up your Hard {settlement.hitNumber} bet to ${hardWays[settlement.hitNumber]:,}.")
	elif settlement.lostNumber is not None:
		if str(readInput(f"Go back up on your Hard {settlement.lostNumber} bet? > ")).lower() in ['y', 'yes']:
			writeOutput(f"How much on the Hard {settlement.lostNumber}?")
			hardWays[settlement.lostNumber] = betPrompt()
			writeOutput(f"Ok, going back up on the Hard {settlement.lostNumber} for ${hardWays[settlement.lostNumber]:,}.")
		else:
			hardWays[settlement.lostNumber] = 0


def hardShow():
	global hardWays
	for key in hardWays:
		if hardWays[key] > 0:
			writeOutput(f"You have ${hardWays[key]:,} on the Hard {key}.")

#Line Bets

lineBets = {
"Pass": 0,
"Pass Odds": 0,
"Don't Pass": 0,
"Don't Pass Odds": 0
}


def lineBetting():
	global lineBets, bank, chipsOnTable
	for key in lineBets:
		if lineBets[key] > 0:
			writeOutput(f"You have ${lineBets[key]:,} on the {key} bet.")
	writeOutput("Enter the Line Bet you'd like to make, or type 'x' and hit Enter to finish Line Betting.")
	while True:
		if lineBets["Pass"] > 0:
			writeOutput(f'You have ${lineBets["Pass"]:,} on the Pass Line.')
		if lineBets["Don't Pass"] > 0:
			writeOutput(f"You have ${lineBets["Don't Pass"]:,} on the Don't Pass Line.")
		try:
			lBet = readInput(">")
		except ValueError:
			writeOutput("That won't work, try again.")
			continue
		if lBet.lower() in ['p', 'pass', 'passline', 'pass line']:
			chipsOnTable -= lineBets["Pass"]
			bank += lineBets["Pass"]
			writeOutput("How much on the Pass Line?")
			lineBets["Pass"] = betPrompt()
			writeOutput(f'Ok, ${lineBets["Pass"]:,} on the Pass Line.')
			continue
		elif lBet.lower() in ["d", "dp", "don't pass", "don't"]:
			if gameMode == GameMode.craplessCraps:
				writeOutput("Don't Pass is not available in Crapless Craps.")
				continue
			chipsOnTable -= lineBets["Don't Pass"]
			bank += lineBets["Don't Pass"]
			writeOutput("How much on the Don't Pass line?")
			lineBets["Don't Pass"] = betPrompt()
			writeOutput(f"Ok, ${lineBets["Don't Pass"]:,} on the Don't Pass Line.")
			continue
		elif lBet.lower() in ['x', 'close', 'esc', 'exit', 'done']:
			writeOutput("Ok, moving on!")
			break
		else:
			writeOutput("Invalid entry, try again or type 'x' and hit Enter!")
			continue

def lineCheck(roll, p2roll):
	global lineBets, bank, chipsOnTable, pointIsOn
	settlement = settleLineBetsForMode(
		lineBets=lineBets,
		pointIsOn=pointIsOn,
		roll=roll,
		p2roll=p2roll,
		gameMode=gameMode
	)
	lineBets = settlement.lineBets
	bank += settlement.bankDelta
	chipsOnTable += settlement.chipsOnTableDelta
	for message in settlement.messages:
		writeOutput(message)

	if pointIsOn and (p2roll == roll or p2roll == 7):
		oddsCheck(p2roll)

def dpPhase2():
	global lineBets, bank, chipsOnTable
	writeOutput("Take down Don't Pass Bet and Odds?")
	while True:
		try:
			takeDown = readInput(">")
			break
		except ValueError:
			writeOutput("Invalid entry, try again!")
			continue
	if takeDown.lower() in ['y', 'yes']:
		writeOutput("Ok, taking down your Don't Pass.")
		chipsOnTable -= lineBets["Don't Pass"] + lineBets["Don't Pass Odds"]
		bank += lineBets["Don't Pass"] + lineBets["Don't Pass Odds"]
		lineBets["Don't Pass"] = lineBets["Don't Pass Odds"] =  0
	elif takeDown.lower() in ['n', 'no']:
		writeOutput("Ok leaving your Don't Pass bets up.")
	else:
		pass

# Odds Betting

def odds():
	global lineBets, bank, chipsOnTable, comeOut
	pOddsChange = dpOddsChange = 0
	passLimits = oddsBetLimits(number=comeOut, baseBet=lineBets["Pass"], gameMode=gameMode, isDont=False)
	dontPassLimits = oddsBetLimits(number=comeOut, baseBet=lineBets["Don't Pass"], gameMode=gameMode, isDont=True)
	if lineBets["Pass"] > 0:
		while True:
			chipsOnTable -= lineBets["Pass Odds"]
			bank += lineBets["Pass Odds"]
			if lineBets["Pass Odds"] > 0:
				writeOutput(f"You have ${lineBets['Pass Odds']:,} in Odds for the {comeOut}. How much for your Odds?")
			else:
				writeOutput(f"Odds on the {comeOut}?")
			writeOutput(f"Max odds is ${passLimits['effectiveMax']:,}.")
			if passLimits["unit"] != 1:
				writeOutput(f"Multiples of {passLimits['unit']}.")
			pOddsChange = betPrompt()
			if pOddsChange > 0 and pOddsChange <= passLimits["effectiveMax"] and isOddsBetUnitValid(number=comeOut, oddsBet=pOddsChange, gameMode=gameMode):
				lineBets["Pass Odds"] = pOddsChange
				writeOutput(f"Ok, ${lineBets['Pass Odds']:,} on your Pass Line Odds.")
				break
			elif pOddsChange > passLimits["effectiveMax"]:
				writeOutput("Nope, that bet is over the Max Odds. Try again!")
				chipsOnTable -= pOddsChange
				bank += pOddsChange
				continue
			elif not isOddsBetUnitValid(number=comeOut, oddsBet=pOddsChange, gameMode=gameMode):
				writeOutput(f"Invalid odds amount. Must be in increments of ${passLimits['unit']:,}.")
				chipsOnTable -= pOddsChange
				bank += pOddsChange
				continue
			elif lineBets["Pass Odds"] > 0 and pOddsChange == 0:
				writeOutput("Ok, taking down your Pass Line Odds.")
				lineBets["Pass Odds"] = pOddsChange
				break
			else:
				writeOutput("No change to your Pass Line Odds.")
				break

	if lineBets["Don't Pass"] > 0:
		while True:
			chipsOnTable -= lineBets["Don't Pass Odds"]
			bank += lineBets["Don't Pass Odds"]
			if lineBets["Don't Pass Odds"] > 0:
				currentLayOdds = lineBets["Don't Pass Odds"]
				writeOutput(f"You have ${currentLayOdds:,} laid against the {comeOut}. How much do you want to Lay?")
			else:
				writeOutput(f"Lay Odds against the {comeOut}?")
			writeOutput(f"Max odds is ${dontPassLimits['effectiveMax']:,}.")
			if dontPassLimits["unit"] != 1:
				writeOutput(f"Multiples of {dontPassLimits['unit']}.")
			dpOddsChange = betPrompt()
			if dpOddsChange > 0 and dpOddsChange <= dontPassLimits["effectiveMax"] and isOddsBetUnitValid(number=comeOut, oddsBet=dpOddsChange, gameMode=gameMode, isDont=True):
				lineBets["Don't Pass Odds"] = dpOddsChange
				currentLayOdds = lineBets["Don't Pass Odds"]
				writeOutput(f"Ok, ${currentLayOdds:,} laid against the Point.")
				break
			elif dpOddsChange > dontPassLimits["effectiveMax"]:
				writeOutput("Nope, you laid too much! Try again.")
				chipsOnTable -= dpOddsChange
				bank += dpOddsChange
				continue
			elif not isOddsBetUnitValid(number=comeOut, oddsBet=dpOddsChange, gameMode=gameMode, isDont=True):
				writeOutput(f"Invalid odds amount. Must be in increments of ${dontPassLimits['unit']:,}.")
				chipsOnTable -= dpOddsChange
				bank += dpOddsChange
				continue
			elif lineBets["Don't Pass Odds"] > 0 and dpOddsChange == 0:
				writeOutput("Taking down your Lay Odds.")
				lineBets["Don't Pass Odds"] = dpOddsChange
				break
			else:
				writeOutput("Leaving your Don't Pass Odds as is.")
				chipsOnTable += lineBets["Don't Pass Odds"]
				bank -= lineBets["Don't Pass Odds"]
				break

def oddsCheck(roll):
	global bank, chipsOnTable, lineBets, comeOut
	settlement = settleOddsBets(
		lineBets=lineBets,
		roll=roll,
		comeOut=comeOut,
		gameMode=gameMode
	)
	lineBets = settlement.lineBets
	bank += settlement.bankDelta
	chipsOnTable += settlement.chipsOnTableDelta
	for message in settlement.messages:
		writeOutput(message)

# Come Betting

comeBets = {
2: 0,
3: 0,
4: 0,
5: 0,
6: 0,
8: 0,
9: 0,
10: 0,
11: 0,
12: 0,
	"Come": 0
}

comeOdds = {
2: 0,
3: 0,
4: 0,
5: 0,
6: 0,
8: 0,
9: 0,
10: 0,
11: 0,
12: 0
}

dComeBets = {
2: 0,
3: 0,
4: 0,
5: 0,
6: 0,
8: 0,
9: 0,
10: 0,
11: 0,
12: 0,
	}

dComeOdds = {
2: 0,
3: 0,
4: 0,
5: 0,
6: 0,
8: 0,
9: 0,
10: 0,
11: 0,
12: 0
}

comeBet = dComeBet = 0

def come():
	global comeBet, dComeBet, chipsOnTable, bank
	if gameMode == GameMode.craplessCraps:
		writeOutput("How much on the Come?")
		chipsOnTable -= comeBet
		bank += comeBet
		comeBet = betPrompt()
		writeOutput(f"Ok, ${comeBet:,} on the Come.")
		return
	while True:
		writeOutput("Come or Don't Come?")
		choice = readInput("> ").strip().lower()
		match choice:
			case "c":
				writeOutput("How much on the Come?")
				chipsOnTable -= comeBet
				bank += comeBet
				comeBet = betPrompt()
				writeOutput(f"Ok, ${comeBet:,} on the Come.")
				break
			case "dc" | "d":
				writeOutput("How much on the Don't Come?")
				chipsOnTable -= dComeBet
				bank += dComeBet
				dComeBet = betPrompt()
				writeOutput(f"Ok, ${dComeBet:,} on the Don't Come.")
				break
			case "x":
				writeOutput("Finished betting the Come.")
				break
			case _:
				writeOutput("Invalid choice, try again.")
				continue

def dComeDown():
	global dComeBets, dComeOdds, chipsOnTable, bank
	if gameMode == GameMode.craplessCraps:
		clearDontComeForCrapless()
		writeOutput("Don't Come is not available in Crapless Craps.")
		return
	checkVal = 0
	for bet in dComeBets:
		checkVal += dComeBets[bet]
		if dComeBets[bet] > 0:
			chipsOnTable -= dComeBets[bet] + dComeOdds[bet]
			bank += dComeBets[bet] + dComeOdds[bet]
			if dComeOdds[bet] > 0:
				writeOutput(f"Taking down your No {bet} and Odds. Returning ${dComeBets[bet] + dComeOdds[bet]:,} to your rack.")
			else:
				writeOutput(f"Taking down your No {bet} bet. Returning ${dComeBets[bet]:,} to your rack.")
			dComeBets[bet] = dComeOdds[bet] = 0
	if checkVal == 0:
		writeOutput("Nothing to take down, silly!")

def clearDontComeForCrapless():
	global dComeBet, dComeBets, dComeOdds, chipsOnTable, bank
	if gameMode != GameMode.craplessCraps:
		return
	totalDontCome = int(dComeBet)
	for number in dComeBets:
		totalDontCome += int(dComeBets[number]) + int(dComeOdds[number])
	if totalDontCome <= 0:
		dComeBet = 0
		for number in dComeBets:
			dComeBets[number] = 0
			dComeOdds[number] = 0
		return
	bank += totalDontCome
	chipsOnTable -= totalDontCome
	dComeBet = 0
	for number in dComeBets:
		dComeBets[number] = 0
		dComeOdds[number] = 0
	writeOutput(f"Don't Come bets are not available in Crapless Craps. Returning ${totalDontCome:,}.")

def comeShow():
	global comeBets, dComeBets, comeOdds, dComeOdds
	for key in comeBets:
		if comeBets[key] > 0:
			writeOutput(f"You have ${comeBets[key]:,} on the Come {key} with ${comeOdds[key]:,} in Odds.")
	if gameMode != GameMode.craplessCraps:
		for key in dComeBets:
			if dComeBets[key] > 0:
				writeOutput(f"You have ${dComeBets[key]:,} on the Don't Come {key} with ${dComeOdds[key]:,} in odds.")

def comeOddsChange():
	global comeBets, dComeBets, comeOdds, dComeOdds, chipsOnTable, bank
	cO = dCO = 0
	for value in comeBets:
		cO += comeBets[value]
	for value in dComeBets:
		dCO += dComeBets[value]
	if cO > 0:
		if readInput("Change your Come Odds? > ").strip().lower() in ['yes', 'y']:
			cdcOddsChange(comeBets, comeOdds)
		else:
			writeOutput("Ok, nothing doing.")
	if dCO > 0 and gameMode != GameMode.craplessCraps:
		if readInput("Change your Don't Come odds? > ").strip().lower() in ['y', 'yes']:
			cdcOddsChange(dComeBets, dComeOdds)
		else:
			writeOutput("Ok, nothing doing.")

def cdcOddsChange(dict, dict2):
	global chipsOnTable, bank
	for key in dict:
		if dict[key] > 0:
			if 'Come' in dict:
				limits = oddsBetLimits(number=key, baseBet=dict[key], gameMode=gameMode, isDont=False)
				multiplesText = f", multiples of {limits['unit']}" if limits["unit"] != 1 else ""
				writeOutput(f"How much for your Come {key} Odds? Max is ${limits['effectiveMax']:,}{multiplesText}; you have ${dict2[key]:,} in Odds.")
			else:
				limits = oddsBetLimits(number=key, baseBet=dict[key], gameMode=gameMode, isDont=True)
				multiplesText = f", multiples of {limits['unit']}" if limits["unit"] != 1 else ""
				writeOutput(f"How much for your Lay {key} Odds? Max is ${limits['effectiveMax']:,}{multiplesText}; you have ${dict2[key]:,} in Lay Odds.")
			while True:
				try:
					bet = int(readInput("	$> "))
					if bet > bank:
						writeOutput("You don't have enough money to make that bet! Try again.")
						outOfMoney()
						writeOutput("Change your Odds?")
						continue
					if bet > limits["effectiveMax"]:
						writeOutput("Nope, that is over the max odds. Try again.")
						continue
					if not isOddsBetUnitValid(number=key, oddsBet=bet, gameMode=gameMode, isDont=('Come' not in dict)):
						writeOutput(f"Invalid odds amount. Must be in increments of ${limits['unit']:,}.")
						continue
					break
				except ValueError:
					bet = dict2[key]
					break
			if bet > 0:
				chipsOnTable -= dict2[key]
				bank += dict2[key]
				writeOutput(f"Ok, you have ${bet:,} Odds for your {key}.")
				dict2[key] = bet
				chipsOnTable += bet
				bank -= bet
			elif dict2[key] > 0 and bet == 0:
				writeOutput("Ok, taking down your Odds.")
				chipsOnTable -= dict2[key]
				bank += dict2[key]
				dict2[key] = bet

def createActionResult(success=True, messages=None, stateChanged=False):
	return {
		"success": bool(success),
		"messages": list(messages) if messages is not None else [],
		"stateChanged": bool(stateChanged)
	}

def mergeActionResult(baseResult, newResult):
	baseResult["success"] = bool(baseResult["success"] and newResult["success"])
	baseResult["messages"].extend(newResult["messages"])
	baseResult["stateChanged"] = bool(baseResult["stateChanged"] or newResult["stateChanged"])
	return baseResult

def emitActionResult(actionResult):
	for message in actionResult["messages"]:
		writeOutput(message)

def processComePostRollAction(roll):
	global comeBet, comeBets, dComeBet, dComeBets, bank, chipsOnTable, comeOdds, dComeOdds, pointIsOn
	actionResult = createActionResult(success=True, messages=[], stateChanged=False)
	if comeBet > 0:
		settlement = settleComeBarBet(comeBet=comeBet, roll=roll, gameMode=gameMode)
		comeBet = settlement.comeBet
		bank += settlement.bankDelta
		chipsOnTable += settlement.chipsOnTableDelta
		settlementMessages = list(settlement.messages)
		if settlement.movedNumber is not None:
			moveMessage = f"Moving your Come Bet to the {settlement.movedNumber}."
			settlementMessages = [msg for msg in settlementMessages if msg != moveMessage]
		mergeActionResult(
			actionResult,
			createActionResult(
				success=True,
				messages=settlementMessages,
				stateChanged=(settlement.bankDelta != 0 or settlement.chipsOnTableDelta != 0 or settlement.movedNumber is not None)
			)
		)
		if settlement.movedNumber is not None:
			comeBets[settlement.movedNumber] = settlement.movedAmount
			actionResult["stateChanged"] = True
			limits = oddsBetLimits(number=settlement.movedNumber, baseBet=comeBets[settlement.movedNumber], gameMode=gameMode, isDont=False)
			writeOutput(f"Moving your Come Bet to the {settlement.movedNumber}.")
			if readInput(f"Come Odds for the {settlement.movedNumber}? > ").strip().lower() in ['y', 'yes']:
				while True:
					multiplesText = f", multiples of {limits['unit']}" if limits["unit"] != 1 else ""
					writeOutput(f"How much for your Come {settlement.movedNumber} Odds? Max is ${limits['effectiveMax']:,}{multiplesText}")
					comeOdds[settlement.movedNumber] = betPrompt()
					if comeOdds[settlement.movedNumber] > limits["effectiveMax"]:
						writeOutput("Way too high on your Odds, there. Try again.")
						chipsOnTable -= comeOdds[settlement.movedNumber]
						bank += comeOdds[settlement.movedNumber]
						comeOdds[settlement.movedNumber] = 0
						continue
					if not isOddsBetUnitValid(number=settlement.movedNumber, oddsBet=comeOdds[settlement.movedNumber], gameMode=gameMode):
						writeOutput(f"Invalid odds amount. Must be in increments of ${limits['unit']:,}.")
						chipsOnTable -= comeOdds[settlement.movedNumber]
						bank += comeOdds[settlement.movedNumber]
						comeOdds[settlement.movedNumber] = 0
						continue
					mergeActionResult(actionResult, createActionResult(success=True, messages=[f"Ok, ${comeOdds[settlement.movedNumber]:,} on your Come {settlement.movedNumber} odds."], stateChanged=True))
					break
	elif dComeBet > 0:
		settlement = settleDComeBarBet(dComeBet=dComeBet, roll=roll)
		dComeBet = settlement.dComeBet
		bank += settlement.bankDelta
		chipsOnTable += settlement.chipsOnTableDelta
		settlementMessages = list(settlement.messages)
		if settlement.movedNumber is not None:
			moveMessage = f"Moving your Don't Come bet to the {settlement.movedNumber}."
			settlementMessages = [msg for msg in settlementMessages if msg != moveMessage]
		mergeActionResult(
			actionResult,
			createActionResult(
				success=True,
				messages=settlementMessages,
				stateChanged=(settlement.bankDelta != 0 or settlement.chipsOnTableDelta != 0 or settlement.movedNumber is not None)
			)
		)
		if settlement.movedNumber is not None:
			dComeBets[settlement.movedNumber] = settlement.movedAmount
			actionResult["stateChanged"] = True
			writeOutput(f"Moving your Don't Come bet to the {settlement.movedNumber}.")
			if readInput(f"Lay Odds on the {settlement.movedNumber}? > ").strip().lower() in ['y', 'yes']:
				limits = oddsBetLimits(number=settlement.movedNumber, baseBet=dComeBets[settlement.movedNumber], gameMode=gameMode, isDont=True)
				while True:
					multiplesText = f", multiples of {limits['unit']}" if limits["unit"] != 1 else ""
					writeOutput(f"How much for your Lay {settlement.movedNumber} Odds? Max is ${limits['effectiveMax']:,}{multiplesText}")
					dComeOdds[settlement.movedNumber] = betPrompt()
					if dComeOdds[settlement.movedNumber] > limits["effectiveMax"]:
						writeOutput("Way too much for your Lay Odds! Try again.")
						chipsOnTable -= dComeOdds[settlement.movedNumber]
						bank += dComeOdds[settlement.movedNumber]
						dComeOdds[settlement.movedNumber] = 0
						continue
					if not isOddsBetUnitValid(number=settlement.movedNumber, oddsBet=dComeOdds[settlement.movedNumber], gameMode=gameMode, isDont=True):
						writeOutput(f"Invalid odds amount. Must be in increments of ${limits['unit']:,}.")
						chipsOnTable -= dComeOdds[settlement.movedNumber]
						bank += dComeOdds[settlement.movedNumber]
						dComeOdds[settlement.movedNumber] = 0
						continue
					mergeActionResult(actionResult, createActionResult(success=True, messages=[f"Ok, ${dComeOdds[settlement.movedNumber]:,} laid on the Don't Come {settlement.movedNumber}."], stateChanged=True))
					break
	return actionResult


def comeCheck(roll):
	clearDontComeForCrapless()
	comePay(roll)
	actionResult = processComePostRollAction(roll)
	emitActionResult(actionResult)
	return actionResult

def comePay(roll):
	global bank, chipsOnTable, comeBets, dComeBets, comeOdds, dComeOdds, pointIsOn, working
	snapshot = captureBetSnapshot()
	settlement = settleComeTableBets(
		comeBets=comeBets,
		dComeBets=dComeBets,
		comeOdds=comeOdds,
		dComeOdds=dComeOdds,
		roll=roll,
		pointIsOn=pointIsOn,
		working=working,
		gameMode=gameMode
	)
	snapshot["comeBets"] = settlement.comeBets
	snapshot["dComeBets"] = settlement.dComeBets
	snapshot["comeOdds"] = settlement.comeOdds
	snapshot["dComeOdds"] = settlement.dComeOdds
	snapshot["bank"] += settlement.bankDelta
	snapshot["chipsOnTable"] += settlement.chipsOnTableDelta
	applyBetSnapshot(snapshot)
	for message in settlement.messages:
		writeOutput(message)

#Field Betting

fieldBet = 0

def fieldShow():
	if fieldBet > 0:
		writeOutput(f"You have ${fieldBet:,} on the Field.")

def field():
	global fieldBet, chipsOnTable, bank
	writeOutput("How much on the Field?")
	bet = betPrompt()
	if bet > 0:
		chipsOnTable -= fieldBet
		fieldBet = bet
		writeOutput(f"Ok, ${fieldBet:,} on the Field.")
	elif fieldBet > 0 and bet == 0:
		bank += fieldBet
		chipsOnTable -= fieldBet
		writeOutput("Taking down your Field bet.")
		fieldBet = 0

def fieldTakeDown():
	global fieldBet, bank, chipsOnTable
	chipsOnTable -= fieldBet
	bank += fieldBet
	fieldBet = 0
	writeOutput("Taking down your Field Bet.")

def fieldCheck(roll):
	global fieldBet, bank, chipsOnTable
	snapshot = captureBetSnapshot()
	settlement = settleFieldBet(fieldBet=fieldBet, roll=roll)
	snapshot["fieldBet"] = settlement.fieldBet
	snapshot["bank"] += settlement.bankDelta
	snapshot["chipsOnTable"] += settlement.chipsOnTableDelta
	applyBetSnapshot(snapshot)
	for message in settlement.messages:
		writeOutput(message)

	if settlement.didWin and fieldBet > 0:
		if str(readInput("Change your Field bet? > ")).strip().lower() in ['y', 'yes']:
			chipsOnTable -= fieldBet
			bank += fieldBet
			fieldBet = 0
			field()
	elif settlement.lossAmount > 0:
		if str(readInput("Go back up on the Field? > ")).strip().lower() in ['y', 'yes']:
			field()

propBets = createDefaultPropBets()

def propHelp():
	writeOutput("Proposition Bet Codes:\n\t'a': Aces\n\t'ad': Acey-Deucey\n\t'ce': C and E\n\t'cr': Any Craps\n\t'seven': Any 7'\n\t'b': Boxcars\n\t'h4-h10': Hop bets\n\t'h6e, h8e': Hop 6 or 8 Easies\n\t'hez': Hop the Easies\n\t'hh': Hop the Hard Ways\n\t'hh4-hh10': Hop Hard 4, 6, 8, or 10\n\t'h': Horn Bet\n\t'hl': Hi-Low\n\t'wh': Whirl/World Bet\n\t'bf': Buffalo Bet\n\t'bf11': Buffalo Yo\n\t'all': Show all bets\n\t'help': Show this menu\n\t'x': Finish betting")

def propBetting():
	global propBets, chipsOnTable, bank
	while True:
		writeOutput("Type in your Prop Bet:")
		bet = readInput(">").strip().lower()
		if bet in ['2', 's']:
			writeOutput("How much on Snake Eyes?")
			bank += propBets["Snake Eyes"]
			chipsOnTable -= propBets["Snake Eyes"]
			propBets["Snake Eyes"] = betPrompt()
			writeOutput(f"Ok, ${propBets['Snake Eyes']:,} on Snake Eyes.")
			continue
		elif bet in ['hh4', 'hh6', 'hh8', 'hh10']:
			if len(bet) == 3:
				number = bet[-1]
			else:
				number = bet[2:]
			outKey = "Hop Hard " + str(number)
			writeOutput(f"How much to Hop the Hard {number}?")
			bank += propBets[outKey]
			chipsOnTable -= propBets[outKey]
			propBets[outKey] = betPrompt()
			writeOutput(f"Ok, ${propBets[outKey]:,} on the {outKey}.")
			continue
		elif bet in ['ad', '3']:
			writeOutput("How much on Acey Deucey?")
			bank += propBets["Acey Deucey"]
			chipsOnTable -= propBets["Acey Deucey"]
			propBets["Acey Deucey"] = betPrompt()
			writeOutput(f"Ok, ${propBets['Acey Deucey']:,} on Acey-Deucey.")
			continue
		elif bet in ['7', 'a7']:
			writeOutput("How much on Any 7?")
			bank += propBets["Any Seven"]
			chipsOnTable -= propBets["Any Seven"]
			propBets["Any Seven"] = betPrompt()
			writeOutput(f"Ok, ${propBets['Any Seven']:,} on Any Seven.")
			continue
		elif bet in ['ac', 'c', 'cr']:
			writeOutput("How much on Any Craps?")
			bank += propBets["Any Craps"]
			chipsOnTable -= propBets["Any Craps"]
			propBets["Any Craps"] = betPrompt()
			writeOutput(f"Ok, ${propBets['Any Craps']:,} on Any Craps.")
			continue
		elif bet == 'ce':
			writeOutput("How much on C and E?")
			bank += propBets["C and E"]
			chipsOnTable -= propBets["C and E"]
			propBets["C and E"] = betPrompt()
			writeOutput(f"Ok, ${propBets['C and E']:,} on C and E.")
			continue
		elif bet in ['h', 'horn']:
			writeOutput("How much on the Horn Bet? Must be a multiple of 4.")
			bank += propBets["Horn"]
			chipsOnTable -= propBets["Horn"]
			propBets["Horn"] = betPrompt()
			writeOutput(f"Ok, ${propBets['Horn']:,} on the Horn Bet.")
			continue
		elif bet == 'hh2':
			writeOutput("How much on the Horn High Deuce? Must be multiple of 5.")
			bank += propBets["Snake Eyes"] + propBets["Acey Deucey"] + propBets["Eleven"] + propBets["Boxcars"]
			chipsOnTable -= propBets["Snake Eyes"] + propBets["Acey Deucey"] + propBets["Eleven"] + propBets["Boxcars"]
			while True:
				hornHigh2 = betPrompt()
				if hornHigh2%5 == 0:
					break
				else:
					writeOutput("That wasn't a multiple of 5, try again!")
					bank += hornHigh2
					chipsOnTable -= hornHigh2
					continue
			propBets["Snake Eyes"] = hornHigh2//5*2
			propBets["Acey Deucey"] = propBets["Eleven"] = propBets["Boxcars"] = hornHigh2//5
			writeOutput(f"Ok, ${hornHigh2:,} on the Horn High Deuce.")
			continue
		elif bet == 'hh3':
			writeOutput("How much on the Horn High Ace-Deuce? Must be a multiple of 5.")
			bank += propBets["Snake Eyes"] + propBets["Acey Deucey"] + propBets["Eleven"] + propBets["Boxcars"]
			chipsOnTable -= propBets["Snake Eyes"] + propBets["Acey Deucey"] + propBets["Eleven"] + propBets["Boxcars"]
			while True:
				hornHigh3 = betPrompt()
				if hornHigh3%5 == 0:
					break
				else:
					writeOutput("That wasn't a multiple of 5, doofus. Try again!")
					bank += hornHigh3
					chipsOnTable -= hornHigh3
					continue
			propBets["Acey Deucey"] = hornHigh3//5*2
			propBets["Snake Eyes"] = propBets["Eleven"] = propBets["Boxcars"] = hornHigh3//5
			writeOutput(f"Ok, ${hornHigh3:,} on the Horn High Ace-Deuce.")
			continue
		elif bet in ['hhy', 'hh11']:
			writeOutput("How much on the Horn High Yo? Must be a multiple of 5.")
			bank += propBets["Snake Eyes"] + propBets["Acey Deucey"] + propBets["Eleven"] + propBets["Boxcars"]
			chipsOnTable -= propBets["Snake Eyes"] + propBets["Acey Deucey"] + propBets["Eleven"] + propBets["Boxcars"]
			while True:
				hornHigh11 = betPrompt()
				if hornHigh11%5 == 0:
					break
				else:
					writeOutput("Not a multiple of 5, try again!")
					bank += hornHigh11
					chipsOnTable -= hornHigh11
					continue
			propBets["Eleven"] = hornHigh11//5*2
			propBets["Snake Eyes"] = propBets["Acey Deucey"] = propBets["Boxcars"] = hornHigh11//5
			writeOutput(f"Ok, ${hornHigh11:,} on the Horn High Yo!")
			continue
		elif bet in ['hh12', 'hhm', 'hhb']:
			writeOutput("How much on the Horn High 12? Must be a multiple of 5.")
			bank += propBets["Snake Eyes"] + propBets["Acey Deucey"] + propBets["Eleven"] + propBets["Boxcars"]
			chipsOnTable -= propBets["Snake Eyes"] + propBets["Acey Deucey"] + propBets["Eleven"] + propBets["Boxcars"]
			while True:
				hornHigh12 = betPrompt()
				if hornHigh12%5 == 0:
					break
				else:
					writeOutput("That wasn't a multiple of 5, try again!")
					bank += hornHigh12
					chipsOnTable -= hornHigh12
					continue
			propBets["Boxcars"] = hornHigh12//5*2
			propBets["Snake Eyes"] = propBets["Acey Deucey"] = propBets["Eleven"] = hornHigh12//5
			writeOutput(f"Ok, ${hornHigh12:,} on the Horn High Midnight.")
			continue
		elif bet in ['b', '12']:
			writeOutput("How much on Boxcars?")
			bank += propBets["Boxcars"]
			chipsOnTable -= propBets["Boxcars"]
			propBets["Boxcars"] = betPrompt()
			writeOutput(f"Ok, ${propBets['Boxcars']:,} on Boxcars.")
			continue
		elif bet in ['11', 'e', 'yo']:
			writeOutput("How much on Yo Eleven?")
			bank += propBets["Eleven"]
			chipsOnTable -= propBets["Eleven"]
			propBets["Eleven"] = betPrompt()
			writeOutput(f"Ok, ${propBets['Eleven']:,} on Eleven.")
			continue
		elif bet == 'w':
			writeOutput("How much on the World bet? Must be a multiple of 5.")
			bank += propBets["Any Seven"] + propBets["Horn"]
			chipsOnTable -= propBets["Any Seven"] + propBets["Horn"]
			while True:
				chipsOnTable -= propBets["World"]
				propBets["World"] = betPrompt()
				if propBets["World"]%5 == 0:
					break
				else:
					writeOutput("That wasn't a multiple of 5! Try again, genius.")
					bank += propBets["World"]
					continue
			propBets["Any Seven"] = propBets["World"]//5
			propBets["World"] -= propBets["World"]//5
			propBets["Horn"] = propBets["World"]
			writeOutput(f"Ok, you have ${propBets['Any Seven']:,} bet on the Any Seven and ${propBets['Horn']:,} on the Horn.")
			propBets["World"] = 0
			if propBets["Buffalo"] > 0 and propBets["Eleven"] > 0:
				writeOutput("You've got yourself a Whirly Buffalo!")
		elif bet == 'bf':
			writeOutput("How much for the Buffalo bet? Must be a multiple of 5.")
			bank += propBets["Any Seven"] + propBets["Buffalo"]
			chipsOnTable -= propBets["Any Seven"]
			while True:
				chipsOnTable -= propBets["Buffalo"]
				propBets["Buffalo"] = betPrompt()
				if propBets["Buffalo"]%5 == 0:
					break
				else:
					writeOutput("That wasn't a multiple of 5! Try again, genius.")
					bank += propBets["Buffalo"]
					continue
			writeOutput(f"Ok, ${propBets['Buffalo']//5:,} each on the Any 7 and hard ways hopping.")
			propBets["Any Seven"] = propBets["Buffalo"]//5
			propBets["Buffalo"] -= propBets["Buffalo"]//5
			if propBets["Horn"] > 0 and propBets["Any Seven"] > 0:
				writeOutput("You've got yourself a Whirly Buffalo!")
		elif bet in ['bf11', 'by']:
			writeOutput("How much for the Buffalo bet with the Yo? Must be a multiple of 5.")
			bank += propBets["Eleven"] + propBets["Buffalo"]
			chipsOnTable -= propBets["Eleven"]
			while True:
				chipsOnTable -= propBets["Buffalo"]
				propBets["Buffalo"] = betPrompt()
				if propBets["Buffalo"]%5 == 0:
					break
				else:
					writeOutput("That wasn't a multiple of 5! Try again, genius.")
					bank += propBets["Buffalo"]
					continue
			writeOutput(f"Ok, ${propBets['Buffalo']//5:,} each on the Yo Eleven and hard ways hopping.")
			propBets["Eleven"] = propBets["Buffalo"]//5
			propBets["Buffalo"] -= propBets["Buffalo"]//5
			if propBets["Horn"] > 0 and propBets["Any Seven"] > 0:
				writeOutput("You've got yourself a Whirly Buffalo!")
		elif bet == 'hl':
			writeOutput("How much on the Hi-Low? Must be a multiple of 2.")
			bank += propBets["Snake Eyes"] + propBets["Boxcars"]
			chipsOnTable -= propBets["Snake Eyes"] + propBets["Boxcars"]
			while True:
				chipsOnTable -= propBets["Hi Low"]
				propBets["Hi Low"] = betPrompt()
				if propBets["Hi Low"]%2 == 0:
					break
				else:
					writeOutput("That wasn't a multiple of 2! Try again, genius.")
					bank += propBets["Hi Low"]
					continue
			writeOutput(f"Ok, ${propBets['Hi Low']//2:,} each on the 2 and 12.")
			propBets["Snake Eyes"] = propBets["Hi Low"]//2
			propBets["Boxcars"] = propBets["Hi Low"]//2
			propBets["Hi Low"] = 0
		elif bet == 'hh':
			hardBets = ['Snake Eyes', 'Boxcars', 'Hop Hard 4', 'Hop Hard 6', 'Hop Hard 8', 'Hop Hard 10']
			writeOutput("How much to Hop the Hard Ways? Must be a multiple of 6.")
			while True:
				for item in hardBets:
					bank += propBets[item]
					chipsOnTable -= propBets[item]
				hardAmount = betPrompt()
				if hardAmount%6 == 0:
					for item in hardBets:
						propBets[item] = hardAmount//6
					break
				else:
					writeOutput("That wasn't a multiple of 6! Math again!")
					continue
			writeOutput(f"Ok, ${hardAmount:,} hopping the Hard Ways.")
			continue
		elif bet == 'h4':
			writeOutput("How much to Hop the 4? Must be an even number.")
			while True:
				bank += propBets["Hop 4"]
				chipsOnTable -= propBets["Hop 4"]
				propBets["Hop 4"] = betPrompt()
				if propBets["Hop 4"]%2 == 0:
					break
				else:
					writeOutput("That wasn't an even number! You can't even!")
					continue
			writeOutput(f"Ok, ${propBets['Hop 4']:,} hopping the 4s.")
			continue
		elif bet == 'h10':
			writeOutput("How much to Hop the 10? Must be an even number.")
			while True:
				bank += propBets["Hop 10"]
				chipsOnTable -= propBets["Hop 10"]
				propBets["Hop 10"] = betPrompt()
				if propBets["Hop 10"]%2 == 0:
					break
				else:
					writeOutput("That wasn't an even number! You can't even!")
					continue
			writeOutput(f"Ok, ${propBets['Hop 10']:,} hopping the 10s.")
			continue
		elif bet == 'h5':
			writeOutput("How much to Hop the 5? Must be an even number.")
			while True:
				bank += propBets["Hop 5"]
				chipsOnTable -= propBets["Hop 5"]
				propBets["Hop 5"] = betPrompt()
				if propBets["Hop 5"]%2 == 0:
					break
				else:
					writeOutput("That wasn't an even number! You can't even!")
					continue
			writeOutput(f"Ok, ${propBets['Hop 5']:,} hopping the 5s.")
			continue
		elif bet == 'h9':
			writeOutput("How much to Hop the 9? Must be an even number.")
			while True:
				bank += propBets["Hop 9"]
				chipsOnTable -= propBets["Hop 9"]
				propBets["Hop 9"] = betPrompt()
				if propBets["Hop 9"]%2 == 0:
					break
				else:
					writeOutput("That wasn't an even number! You can't even!")
					continue
			writeOutput(f"Ok, ${propBets['Hop 9']:,} hopping the 9s.")
			continue
		elif bet == 'h6':
			writeOutput("How much to Hop the 6? Must be a multiple of 3.")
			while True:
				bank += propBets["Hop 6"]
				chipsOnTable -= propBets["Hop 6"]
				propBets["Hop 6"] = betPrompt()
				if propBets["Hop 6"]%3 == 0:
					break
				else:
					writeOutput("That's not a multiple of 3! Can't you math?")
					continue
			writeOutput(f"Ok, ${propBets['Hop 6']:,} hopping the 6s.")
			continue
		elif bet == 'h6e':
			writeOutput("How much to Hop the 6 Easies? Must be a multiple of 2.")
			while True:
				bank += propBets["Hop 6 Easy"]
				chipsOnTable -= propBets["Hop 6 Easy"]
				propBets["Hop 6 Easy"] = betPrompt()
				if propBets["Hop 6 Easy"]%2 == 0:
					break
				else:
					writeOutput("That's not a multiple of 2! Can't you math?")
					continue
			writeOutput(f"Ok, ${propBets['Hop 6 Easy']:,} hopping the 6 Easies.")
			continue
		elif bet == 'h7':
			writeOutput("How much to Hop Big Red? Must be a multiple of 3.")
			while True:
				bank += propBets["Hop 7"]
				chipsOnTable -= propBets["Hop 7"]
				propBets["Hop 7"] = betPrompt()
				if propBets["Hop 7"]%3 == 0:
					break
				else:
					writeOutput("That's not a multiple of 3! Can't you math?")
					continue
			writeOutput(f"Ok, ${propBets['Hop 7']:,} hopping the 7s.")
			continue
		elif bet == 'h8':
			writeOutput("How much to Hop the 8? Must be a multiple of 3.")
			while True:
				bank += propBets["Hop 8"]
				chipsOnTable -= propBets["Hop 8"]
				propBets["Hop 8"] = betPrompt()
				if propBets["Hop 8"]%3 == 0:
					break
				else:
					writeOutput("That's not a multiple of 3! Can't you math?")
					continue
			writeOutput(f"Ok, ${propBets['Hop 8']:,} hopping the 8s.")
			continue
		elif bet == 'h8e':
			writeOutput("How much to Hop the 8 Easies? Must be a multiple of 2.")
			while True:
				bank += propBets["Hop 8 Easy"]
				chipsOnTable -= propBets["Hop 8 Easy"]
				propBets["Hop 8 Easy"] = betPrompt()
				if propBets["Hop 8 Easy"]%2 == 0:
					break
				else:
					writeOutput("That's not a multiple of 2! Can't you math?")
					continue
			writeOutput(f"Ok, ${propBets['Hop 8 Easy']:,} hopping the 8 Easies.")
			continue
		elif bet == 'hez':
			writeOutput("How much to Hop the Easies? Must be a multiple of 15.")
			while True:
				bank += propBets["Hop EZ"]
				chipsOnTable -= propBets["Hop EZ"]
				propBets["Hop EZ"] = betPrompt()
				if propBets["Hop EZ"]%15 == 0:
					break
				else:
					writeOutput("That's not a multiple of 15! Can't you math?")
					continue
			writeOutput(f"Ok, ${propBets['Hop EZ']:,} hopping the Easies.")
			continue
		elif bet == 'a':
			writeOutput("Showing your Prop Bets:\n")
			for key in propBets:
				if propBets[key] > 0:
					writeOutput(f"\t${propBets[key]:,} on {key}.")
			continue
		elif bet == 'help':
			propHelp()
			continue 
		elif bet == 'x':
			writeOutput("Done Prop Betting.")
			break
		else:
			writeOutput("That's simply not an option! Try again...")
			continue

def propPay(roll):
	global propBets, bank, chipsOnTable, die1, die2
	aliasResolution = resolvePropAliases(propBets=propBets)
	propBets = aliasResolution.propBets
	for message in aliasResolution.messages:
		writeOutput(message)
	subsetSettlement = settlePropSubsetBets(propBets=propBets, roll=roll)
	propBets = subsetSettlement.propBets
	bank += subsetSettlement.bankDelta
	chipsOnTable += subsetSettlement.chipsOnTableDelta
	for message in subsetSettlement.messages:
		writeOutput(message)
	buffaloSettlement = settleBuffaloBet(propBets=propBets, roll=roll, die1=die1, die2=die2)
	propBets = buffaloSettlement.propBets
	bank += buffaloSettlement.bankDelta
	chipsOnTable += buffaloSettlement.chipsOnTableDelta
	for message in buffaloSettlement.messages:
		writeOutput(message)
	hopSettlement = settleHopBets(propBets=propBets, roll=roll, die1=die1, die2=die2)
	propBets = hopSettlement.propBets
	bank += hopSettlement.bankDelta
	chipsOnTable += hopSettlement.chipsOnTableDelta
	for message in hopSettlement.messages:
		writeOutput(message)
#	multiplier = 0
	propKeyMatrix = getPropKeyMatrix()
	extractedPropKeys = []
	for key in propKeyMatrix:
		if propKeyMatrix[key] == "engineSettled":
			extractedPropKeys.append(key)
	for key in propBets:
		if key in extractedPropKeys:
			continue
		if propBets[key] > 0:
			writeOutput(f"{key} remains up for manual player management.")


#All Tall Small setup
atsAll = atsSmall = atsTall = 0
allNums = []
smallNums = []
tallNums = []
atsOn = False

def atsBetting():
	global atsAll, atsSmall, atsTall, atsOn, bank
	atsOn = True
	writeOutput("How much on the All?")
	atsAll = betPrompt()
	writeOutput(f"Ok, ${atsAll:,} on the All.")
	writeOutput("How much on the Tall?")
	atsTall = betPrompt()
	writeOutput(f"Ok, ${atsTall:,} on the Tall.")
	writeOutput("How much on the Small?")
	atsSmall = betPrompt()
	writeOutput(f"Ok, ${atsSmall:,} on the Small.")

def ats(roll):
	global allNums, smallNums, tallNums, bank, chipsOnTable, atsAll, atsSmall, atsTall, atsOn
	smallSet = [2, 3, 4, 5, 6]
	tallSet = [8, 9, 10, 11, 12]
	allSet = [2, 3, 4, 5, 6, 8, 9, 10, 11, 12]

	if roll in smallSet and roll not in smallNums:
		smallNums.append(roll)
	if roll in tallSet and roll not in tallNums:
		tallNums.append(roll)
	if roll in allSet and roll not in allNums:
		allNums.append(roll)

	if roll == 7 and (atsAll + atsSmall + atsTall) > 0:
		atsOn = False
		writeOutput(f"You lost ${atsAll+atsTall+atsSmall:,} from the All Tall Small.")
		#bank -= atsAll + atsTall + atsSmall
		chipsOnTable -= atsAll + atsTall + atsSmall
		atsAll = atsSmall = atsTall = 0
		allNums = []
		smallNums = []
		tallNums = []
	elif (atsAll + atsSmall + atsTall) > 0:
		allNums.sort()
		writeOutput(f"All Tall Small: {allNums}")

	if set(smallNums) == set(smallSet):
		writeOutput(f"You won ${atsSmall * 34:,} on the Small!")
		bank += atsSmall * 34
		chipsOnTable -= atsSmall
		atsSmall = 0
		smallNums = []
	if set(tallNums) == set(tallSet):
		writeOutput(f"You won ${atsTall*34:,} from the Tall!")
		bank += atsTall * 34
		chipsOnTable -= atsTall
		atsTall = 0
		tallNums = []
	if set(allNums) == set(allSet):
		writeOutput(f"You won ${atsAll*175:,} on the All! Holy Crap!")
		bank += atsAll * 175
		chipsOnTable -= atsAll
		atsAll = 0
		allNums = []
		atsOn = False

# Lay Bet Setup

layOff = False

layBets = {
2: 0,
3: 0,
4: 0,
5: 0,
6: 0,
8: 0,
9: 0,
10: 0,
11: 0,
12: 0
}

def layNumbersForCurrentMode():
	if gameMode == GameMode.craplessCraps:
		return [2, 3, 4, 5, 6, 8, 9, 10, 11, 12]
	return [4, 5, 6, 8, 9, 10]

def collectLayUnit(numbers, promptText):
	outlay = 0
	for number in numbers:
		outlay += layBets[number]
	while True:
		writeOutput(promptText)
		try:
			unit = int(readInput("> "))
		except ValueError:
			writeOutput("That wasn't even a unit! Try again.")
			continue
		if (unit*5)*len(numbers) > bank + outlay:
			writeOutput("You don't have enough money for that! Egads!")
			outOfMoney()
			continue
		return unit

def applyLayUnits(numbers, unit, summaryText):
	global chipsOnTable, bank, layBets
	total = 0
	for key in numbers:
		chipsOnTable -= layBets[key]
		bank += layBets[key]
		layBets[key] = 5 * unit
		chipsOnTable += layBets[key]
		bank -= layBets[key]
		total += layBets[key]
	writeOutput(summaryText.format(total=total))

def layAll():
	unit = collectLayUnit(numbers=[4, 5, 6, 8, 9, 10], promptText="How many units across the Lay Numbers?")
	applyLayUnits(numbers=[4, 5, 6, 8, 9, 10], unit=unit, summaryText="Laying ${total:,} Across.")

def layEdges():
	unit = collectLayUnit(numbers=[2, 3, 11, 12], promptText="How many Edge units for Lay 2, 3, 11, and 12?")
	applyLayUnits(numbers=[2, 3, 11, 12], unit=unit, summaryText="Laying ${total:,} on the edge Lay numbers.")

def layExtremeAcross():
	numbers = layNumbersForCurrentMode()
	unit = collectLayUnit(numbers=numbers, promptText="How many Extreme Across units for Lay 2 through 12?")
	applyLayUnits(numbers=numbers, unit=unit, summaryText="Laying ${total:,} Extreme Across.")

def layBetting():
	global layBets, bank, chipsOnTable
	for key in layNumbersForCurrentMode():
		writeOutput(f"You have ${layBets[key]:,} on the Lay {key}.")
		writeOutput(f"How much on the Lay {key}?")
		while True:
			try:
				bet = int(readInput("$>"))
				if bet > bank + chipsOnTable - chipsOnTable:
					writeOutput("You don't have enough money to make that bet! Try again.")
					outOfMoney()
					writeOutput(f"How much on the Lay {key}?")
					continue
				break
			except ValueError:
				bet = layBets[key]
				break
		if bet > 0:
			chipsOnTable -= layBets[key]
			bank += layBets[key]
			layBets[key] = bet
			chipsOnTable += bet
			bank -= bet
			writeOutput(f"Ok, ${bet:,} on the Lay {key}.")
		elif layBets[key] > 0 and bet == 0:
			writeOutput(f"Ok, taking down your Lay {key} bet.")
			chipsOnTable -= layBets[key]
			bank += layBets[key]
			layBets[key] = 0

def layTakeDown():
	global layBets, bank, chipsOnTable
	for key in layNumbersForCurrentMode():
		chipsOnTable -= layBets[key]
		bank += layBets[key]
		layBets[key] = 0

def layShow():
	global layBets
	for key in layNumbersForCurrentMode():
		if layBets[key] > 0:
			writeOutput(f"You have ${layBets[key]:,} on the Lay {key}.")

def layCheck(roll):
	global layBets, bank, chipsOnTable
	snapshot = captureBetSnapshot()
	settlement = settleLayBetsForMode(layBets=layBets, roll=roll, gameMode=gameMode)
	snapshot["layBets"] = settlement.layBets
	snapshot["bank"] += settlement.bankDelta
	snapshot["chipsOnTable"] += settlement.chipsOnTableDelta
	applyBetSnapshot(snapshot)
	for message in settlement.messages:
		writeOutput(message)

	if settlement.lostNumber is not None:
		if str(readInput(f"Go back up on your Lay {settlement.lostNumber}? > ")).strip().lower() == 'y':
			writeOutput(f"How much on the Lay {settlement.lostNumber}?")
			layBets[settlement.lostNumber] = betPrompt()
			writeOutput(f"Ok, ${layBets[settlement.lostNumber]:,} on the Lay {settlement.lostNumber}.")
		else:
			writeOutput("Got it, you are done being Layed.")

# Bank and bet setup
bank = 0
initBank = 0
chipsOnTable = 0

def cashIn():
	global bank, initBank
	writeOutput("How much are you cashing in for your bankroll?")
	while True:
		try:
			cash = int(readInput("$>"))
		except ValueError:
			writeOutput("That wasn't a number, doofus!")
			continue
		if cash <= 0:
			writeOutput("You won't get very far trying to play without any money, come on now...")
			continue
		else:
			bank += cash
			initBank = cash
			break
	writeOutput(f"Great, starting you off with ${bank:,}.")

def quitGame():
	global bank, chipsOnTable, initBank
	if bank+chipsOnTable > initBank:
		writeOutput("\nNice work coloring up! Come back soon!\n")
	elif bank+chipsOnTable == initBank:
		writeOutput("\nWell, at least you didn't lose anything! Try again soon!\n")
	else:
		writeOutput("\nOops, tough loss today. Better luck next time!\n")
	raise SystemExit

def betPrompt():
	global bank, chipsOnTable
	while True:
		try:
			playerBet =  int(readInput("\t$> "))
		except ValueError:
			writeOutput("\tThat wasn't a number!")
			continue
		if playerBet > bank:
			if readInput("\tYou simply don't have enough money to do that! DO you want to add more to your bankroll? > ").strip().lower() == "y":
				outOfMoney()
			continue
		else:
			chipsOnTable += playerBet
			bank -= playerBet
			return playerBet

def outOfMoney():
	global bank
	if bank <= 0:
		writeOutput("\tYou are totally out of money.\n\tLet's hit the ATM again and get you more cash.\n\tHow much do you want?")
	else:
		writeOutput("\tYour chips are getting really low.\n\tHow much would you like to add to your bankroll?")
	while True:
		try:
			cash = int(readInput("\t$>"))
		except ValueError:
			writeOutput("\tYou forgot what numbers were and the ATM beeps at you in annoyance.\n\tTry again.")
			continue
		if cash < 0:
			writeOutput("\tWhat am I, a bank?\n\tThis is for withdrawals only! Try again.")
			continue
		else:
			bank += cash
			break
	writeOutput(f"\tAlright, starting you off again with ${bank:,}. Don't lose it all this time!")

#Place Betting

place = {
2: 0,
3: 0,
4: 0,
5: 0,
6: 0,
8: 0,
9: 0,
10: 0,
11: 0,
12: 0
}

def captureBetSnapshot():
	return {
		"bank": int(bank),
		"chipsOnTable": int(chipsOnTable),
		"comeBet": int(comeBet),
		"dComeBet": int(dComeBet),
		"comeBets": dict(comeBets),
		"dComeBets": dict(dComeBets),
		"comeOdds": dict(comeOdds),
		"dComeOdds": dict(dComeOdds),
		"place": dict(place),
		"layBets": dict(layBets),
		"hardWays": dict(hardWays),
		"fieldBet": int(fieldBet)
	}

def applyBetSnapshot(snapshot):
	global bank, chipsOnTable, comeBet, dComeBet, comeBets, dComeBets, comeOdds, dComeOdds, place, layBets, hardWays, fieldBet
	bank = int(snapshot["bank"])
	chipsOnTable = int(snapshot["chipsOnTable"])
	comeBet = int(snapshot["comeBet"])
	dComeBet = int(snapshot["dComeBet"])
	comeBets = dict(snapshot["comeBets"])
	dComeBets = dict(snapshot["dComeBets"])
	comeOdds = dict(snapshot["comeOdds"])
	dComeOdds = dict(snapshot["dComeOdds"])
	place = dict(snapshot["place"])
	layBets = dict(snapshot["layBets"])
	hardWays = dict(snapshot["hardWays"])
	fieldBet = int(snapshot["fieldBet"])

def normalizedGameMode(modeValue):
	if isinstance(modeValue, GameMode):
		return modeValue
	modeText = str(modeValue).strip().lower()
	if modeText in ["1", "craps"]:
		return GameMode.craps
	if modeText in ["2", "crapless craps", "craplesscraps"]:
		return GameMode.craplessCraps
	raise ValueError("Invalid game mode value.")

def syncRuntimeFromGlobals(runtime=None):
	global gameRuntime
	targetRuntime = runtime if runtime is not None else gameRuntime
	if targetRuntime is None:
		targetRuntime = GameRuntime()
		if runtime is None:
			gameRuntime = targetRuntime
	targetRuntime.bank = int(bank)
	targetRuntime.chipsOnTable = int(chipsOnTable)
	targetRuntime.throws = int(throws)
	targetRuntime.comeOut = int(comeOut)
	targetRuntime.pointIsOn = bool(pointIsOn)
	targetRuntime.p2 = int(p2)
	targetRuntime.gameMode = gameMode
	return targetRuntime

def syncGlobalsFromRuntime(runtime=None):
	global bank, chipsOnTable, throws, comeOut, pointIsOn, p2, gameMode, gameRuntime
	sourceRuntime = runtime if runtime is not None else gameRuntime
	if sourceRuntime is None:
		return syncRuntimeFromGlobals()
	bank = int(sourceRuntime.bank)
	chipsOnTable = int(sourceRuntime.chipsOnTable)
	throws = int(sourceRuntime.throws)
	comeOut = int(sourceRuntime.comeOut)
	pointIsOn = bool(sourceRuntime.pointIsOn)
	p2 = int(sourceRuntime.p2)
	gameMode = normalizedGameMode(sourceRuntime.gameMode)
	if runtime is not None:
		gameRuntime = sourceRuntime
	syncGameState(gameState=gameState, bank=bank, chipsOnTable=chipsOnTable, throws=throws, pointIsOn=pointIsOn, comeOut=comeOut, p2=p2, gameMode=gameMode)
	return syncRuntimeFromGlobals()

def runtimeStateKeys():
	return {
		"bank", "initBank", "chipsOnTable", "throws", "pointIsOn", "comeOut", "p2",
		"working", "placeOff", "layOff", "hardOff", "rollHard", "gameMode",
		"lineBets", "propBets", "atsAll", "atsTall", "atsSmall", "atsOn",
		"allNums", "fire", "fireBet", "betSnapshot"
	}

def buildDefaultBetSnapshot():
	return {
		"bank": 0,
		"chipsOnTable": 0,
		"comeBet": 0,
		"dComeBet": 0,
		"comeBets": {key: 0 for key in comeBets},
		"dComeBets": {key: 0 for key in dComeBets},
		"comeOdds": {key: 0 for key in comeOdds},
		"dComeOdds": {key: 0 for key in dComeOdds},
		"place": {key: 0 for key in place},
		"layBets": {key: 0 for key in layBets},
		"hardWays": {key: 0 for key in hardWays},
		"fieldBet": 0
	}

def buildDefaultRuntimeState():
	return {
		"bank": 0,
		"initBank": 0,
		"chipsOnTable": 0,
		"throws": 0,
		"pointIsOn": False,
		"comeOut": 0,
		"p2": 0,
		"working": False,
		"placeOff": False,
		"layOff": False,
		"hardOff": False,
		"rollHard": False,
		"gameMode": GameMode.craps,
		"lineBets": {"Pass": 0, "Pass Odds": 0, "Don't Pass": 0, "Don't Pass Odds": 0},
		"propBets": createDefaultPropBets(),
		"atsAll": 0,
		"atsTall": 0,
		"atsSmall": 0,
		"atsOn": False,
		"allNums": [],
		"fire": [],
		"fireBet": 0,
		"betSnapshot": buildDefaultBetSnapshot()
	}

def validateRuntimeStatePayload(runtimeState):
	if not isinstance(runtimeState, dict):
		raise ValueError("Runtime state must be a dictionary.")
	unknownKeys = [key for key in runtimeState if key not in runtimeStateKeys()]
	if unknownKeys:
		raise ValueError(f"Unsupported runtime state keys: {', '.join(str(key) for key in sorted(unknownKeys))}")

def normalizeRuntimeStatePayload(runtimeState):
	validateRuntimeStatePayload(runtimeState)
	normalizedState = {}
	if "betSnapshot" in runtimeState:
		normalizedState["betSnapshot"] = dict(runtimeState["betSnapshot"])
	if "bank" in runtimeState:
		normalizedState["bank"] = int(runtimeState["bank"])
	if "initBank" in runtimeState:
		normalizedState["initBank"] = int(runtimeState["initBank"])
	if "chipsOnTable" in runtimeState:
		normalizedState["chipsOnTable"] = int(runtimeState["chipsOnTable"])
	if "throws" in runtimeState:
		normalizedState["throws"] = int(runtimeState["throws"])
	if "pointIsOn" in runtimeState:
		normalizedState["pointIsOn"] = bool(runtimeState["pointIsOn"])
	if "comeOut" in runtimeState:
		normalizedState["comeOut"] = int(runtimeState["comeOut"])
	if "p2" in runtimeState:
		normalizedState["p2"] = int(runtimeState["p2"])
	if "working" in runtimeState:
		normalizedState["working"] = bool(runtimeState["working"])
	if "placeOff" in runtimeState:
		normalizedState["placeOff"] = bool(runtimeState["placeOff"])
	if "layOff" in runtimeState:
		normalizedState["layOff"] = bool(runtimeState["layOff"])
	if "hardOff" in runtimeState:
		normalizedState["hardOff"] = bool(runtimeState["hardOff"])
	if "rollHard" in runtimeState:
		normalizedState["rollHard"] = bool(runtimeState["rollHard"])
	if "gameMode" in runtimeState:
		normalizedState["gameMode"] = normalizedGameMode(runtimeState["gameMode"])
	if "lineBets" in runtimeState:
		normalizedState["lineBets"] = dict(runtimeState["lineBets"])
	if "propBets" in runtimeState:
		normalizedState["propBets"] = dict(runtimeState["propBets"])
	if "atsAll" in runtimeState:
		normalizedState["atsAll"] = int(runtimeState["atsAll"])
	if "atsTall" in runtimeState:
		normalizedState["atsTall"] = int(runtimeState["atsTall"])
	if "atsSmall" in runtimeState:
		normalizedState["atsSmall"] = int(runtimeState["atsSmall"])
	if "atsOn" in runtimeState:
		normalizedState["atsOn"] = bool(runtimeState["atsOn"])
	if "allNums" in runtimeState:
		normalizedState["allNums"] = list(runtimeState["allNums"])
	if "fire" in runtimeState:
		normalizedState["fire"] = list(runtimeState["fire"])
	if "fireBet" in runtimeState:
		normalizedState["fireBet"] = int(runtimeState["fireBet"])
	return normalizedState

def getRuntimeState():
	return normalizeRuntimeStatePayload({
		"bank": int(bank),
		"initBank": int(initBank),
		"chipsOnTable": int(chipsOnTable),
		"throws": int(throws),
		"pointIsOn": bool(pointIsOn),
		"comeOut": int(comeOut),
		"p2": int(p2),
		"working": bool(working),
		"placeOff": bool(placeOff),
		"layOff": bool(layOff),
		"hardOff": bool(hardOff),
		"rollHard": bool(rollHard),
		"gameMode": gameMode,
		"lineBets": dict(lineBets),
		"propBets": dict(propBets),
		"atsAll": int(atsAll),
		"atsTall": int(atsTall),
		"atsSmall": int(atsSmall),
		"atsOn": bool(atsOn),
		"allNums": list(allNums),
		"fire": list(fire),
		"fireBet": int(fireBet),
		"betSnapshot": captureBetSnapshot()
	})

def setRuntimeState(runtimeState):
	global bank, initBank, chipsOnTable, throws, pointIsOn, comeOut, p2, working, placeOff, layOff, hardOff, rollHard, gameMode, lineBets, propBets, atsAll, atsTall, atsSmall, atsOn, allNums, fire, fireBet
	normalizedState = normalizeRuntimeStatePayload(runtimeState)
	if "betSnapshot" in normalizedState:
		applyBetSnapshot(normalizedState["betSnapshot"])
	if "bank" in normalizedState:
		bank = normalizedState["bank"]
	if "initBank" in normalizedState:
		initBank = normalizedState["initBank"]
	if "chipsOnTable" in normalizedState:
		chipsOnTable = normalizedState["chipsOnTable"]
	if "throws" in normalizedState:
		throws = normalizedState["throws"]
	if "pointIsOn" in normalizedState:
		pointIsOn = normalizedState["pointIsOn"]
	if "comeOut" in normalizedState:
		comeOut = normalizedState["comeOut"]
	if "p2" in normalizedState:
		p2 = normalizedState["p2"]
	if "working" in normalizedState:
		working = normalizedState["working"]
	if "placeOff" in normalizedState:
		placeOff = normalizedState["placeOff"]
	if "layOff" in normalizedState:
		layOff = normalizedState["layOff"]
	if "hardOff" in normalizedState:
		hardOff = normalizedState["hardOff"]
	if "rollHard" in normalizedState:
		rollHard = normalizedState["rollHard"]
	if "gameMode" in normalizedState:
		gameMode = normalizedState["gameMode"]
	if "lineBets" in normalizedState:
		lineBets = normalizedState["lineBets"]
	if "propBets" in normalizedState:
		propBets = normalizedState["propBets"]
	if "atsAll" in normalizedState:
		atsAll = normalizedState["atsAll"]
	if "atsTall" in normalizedState:
		atsTall = normalizedState["atsTall"]
	if "atsSmall" in normalizedState:
		atsSmall = normalizedState["atsSmall"]
	if "atsOn" in normalizedState:
		atsOn = normalizedState["atsOn"]
	if "allNums" in normalizedState:
		allNums = normalizedState["allNums"]
	if "fire" in normalizedState:
		fire = normalizedState["fire"]
	if "fireBet" in normalizedState:
		fireBet = normalizedState["fireBet"]
	syncGameState(gameState=gameState, bank=bank, chipsOnTable=chipsOnTable, throws=throws, pointIsOn=pointIsOn, comeOut=comeOut, p2=p2, gameMode=gameMode)
	syncRuntimeFromGlobals()
	return getRuntimeState()

def resetRuntimeState():
	return setRuntimeState(buildDefaultRuntimeState())

def exportSessionBundle():
	return withApiVersion({
		"bundleType": "ohcrapsSession",
		"runtimeState": getRuntimeState(),
		"gameMode": gameMode,
		"captureState": {
			"outputCaptureOn": bool(outputCaptureOn),
			"outputCaptureBuffer": list(outputCaptureBuffer),
			"promptCaptureOn": bool(promptCaptureOn),
			"promptCaptureBuffer": list(promptCaptureBuffer)
		},
		"hostMetadata": {
			"appName": "Oh Craps",
			"bundleFormat": "sessionBundleV1"
		}
	})

def importSessionBundle(bundle):
	global outputCaptureOn, outputCaptureBuffer, promptCaptureOn, promptCaptureBuffer
	if not isinstance(bundle, dict):
		raise ValueError("Session bundle must be a dictionary.")
	if bundle.get("engineApiVersion") != engineApiVersion:
		raise ValueError("Unsupported session bundle version.")
	requiredKeys = ["bundleType", "runtimeState", "captureState"]
	for key in requiredKeys:
		if key not in bundle:
			raise ValueError(f"Missing required bundle key: {key}")
	if bundle["bundleType"] != "ohcrapsSession":
		raise ValueError("Unsupported session bundle type.")
	captureState = bundle["captureState"]
	if not isinstance(captureState, dict):
		raise ValueError("Invalid captureState in session bundle.")
	setRuntimeState(bundle["runtimeState"])
	outputCaptureOn = bool(captureState.get("outputCaptureOn", False))
	outputCaptureBuffer = list(captureState.get("outputCaptureBuffer", []))
	promptCaptureOn = bool(captureState.get("promptCaptureOn", False))
	promptCaptureBuffer = list(captureState.get("promptCaptureBuffer", []))
	importedBundle = exportSessionBundle()
	emitEvent("sessionImported", withApiVersion({"runtimeState": getRuntimeState(), "bundleType": importedBundle["bundleType"]}))
	return importedBundle

placeOff = False

def validPlaceNumbers():
	if gameMode == GameMode.craplessCraps:
		return [2, 3, 4, 5, 6, 8, 9, 10, 11, 12]
	return [4, 5, 6, 8, 9, 10]

def placeUnitSize(number):
	if number in [2, 12]:
		return 2
	if number in [3, 11]:
		return 4
	if number in [6, 8]:
		return 6
	return 5

def isPlaceAmountAllowed(number, bet):
	if bet <= 0:
		return True
	if gameMode == GameMode.craplessCraps and number in [2, 12] and bet < 20:
		return bet%2 == 0
	if gameMode == GameMode.craplessCraps and number in [3, 11] and bet < 20:
		return bet%4 == 0
	return True

def normalizedHalfPressIncrement(number, currentWager):
	if number in [6, 8]:
		return calculateHalfPressIncrement(number=number, currentWager=currentWager)
	unit = placeUnitSize(number)
	inc = currentWager//2
	if number in [2, 3, 11, 12]:
		inc = (inc//unit) * unit
		if inc < unit:
			inc = unit
	return inc

def validPlacePresetCodesForMode():
	if gameMode == GameMode.craplessCraps:
		return ['a', 'i', 'c', 'ea', 'e']
	return ['a', 'i', 'c']

def placeHelpText(pointPhase=False):
	helpLines = [
		"Place Betting Codes:",
		"\ty: Enter individual Place Betting mode.",
		"\ta: Auto-bet Across all the numbers.",
		"\ti: Auto-bet on the Inside numbers.",
		"\tc: Auto-bet on the 6 and 8."
	]
	if gameMode == GameMode.craplessCraps:
		helpLines.append("\te: Auto-bet edge numbers (2, 3, 11, 12).")
		helpLines.append("\tea: Auto-bet Extreme Across (2 through 12).")
	helpLines.append("\td: Take down all Place Bets.")
	if pointPhase:
		helpLines.append("\to: Turn Place Bets Off for next roll.")
		helpLines.append("\tm: Move Point number to empty Place Bet.")
		helpLines.append("\tp: Take down Point number place bet.")
	helpLines.append("\th: Show this Help Menu.")
	helpLines.append("\tx: Exit Place Betting.")
	return "\n".join(helpLines) + "\n"

def handlePlaceMenuCommand(command, pointPhase=False):
	global placeOff, chipsOnTable, bank, place, comeOut
	cmd = str(command).strip().lower()
	if cmd == "y":
		placeBets()
		return createActionResult(success=True, messages=[], stateChanged=True) | {"shouldExitMenu": False}
	if pointPhase and cmd == "o":
		if placeOff:
			placeOff = False
			messages = ["Ok, your Place Bets are back on."]
		else:
			placeOff = True
			messages = ["All your Place Bets are Off."]
		return createActionResult(success=True, messages=messages, stateChanged=True) | {"shouldExitMenu": False}
	if cmd == "d":
		if pointPhase:
			messages = ["Taking down all of your Place Bets."]
		else:
			messages = ["Taking down your Place Bets."]
		placeTakeDown()
		return createActionResult(success=True, messages=messages, stateChanged=True) | {"shouldExitMenu": False}
	if cmd in validPlacePresetCodesForMode():
		placePreset(cmd)
		return createActionResult(success=True, messages=[], stateChanged=True) | {"shouldExitMenu": False}
	if pointPhase and cmd == "m":
		placeMover()
		return createActionResult(success=True, messages=[], stateChanged=True) | {"shouldExitMenu": False}
	if pointPhase and cmd == "p":
		chipsOnTable -= place[comeOut]
		bank += place[comeOut]
		place[comeOut] = 0
		return createActionResult(success=True, messages=[f"Taking down the Place {comeOut} bet."], stateChanged=True) | {"shouldExitMenu": False}
	if cmd == "h":
		return createActionResult(success=True, messages=[placeHelpText(pointPhase=pointPhase)], stateChanged=False) | {"shouldExitMenu": False}
	if cmd == "x":
		return createActionResult(success=True, messages=["Done Place Betting!"], stateChanged=False) | {"shouldExitMenu": True}
	return createActionResult(success=False, messages=["That's not a valid option!"], stateChanged=False) | {"shouldExitMenu": False}

def layHelpText(pointPhase=False):
	helpLines = [
		"Lay Bet Codes:",
		"\ty: Enter Lay Betting mode.",
		"\ta: Lay Bets across all numbers.",
		"\td: Take down all Lay Bets."
	]
	if gameMode == GameMode.craplessCraps:
		helpLines.append("\te: Lay only 2, 3, 11, and 12.")
		helpLines.append("\tea: Lay all numbers from 2 through 12.")
	if pointPhase:
		helpLines.append("\to: Toggle Lay Bets Off or On for next roll.")
	helpLines.append("\th: Show this Help menu.")
	helpLines.append("\tx: Finish Lay Betting.")
	return "\n".join(helpLines) + "\n"

def hardWaysHelpText(pointPhase=False):
	helpLines = [
		"Hard Ways Codes:",
		"\ty: Enter Hard Ways betting mode.",
		"\td: Take down Hard Ways bets.",
		"\ta: Auto-bet Across all Hard Ways.",
		"\th4: Bet all Hard Ways High 4.",
		"\th6: Bet all Hard Ways High 6.",
		"\th8: Bet all Hard Ways High 8.",
		"\th10: Bet all Hard Ways High 10."
	]
	if pointPhase:
		helpLines.append("\to: Toggle Hard Ways Bets On or Off for next roll.")
	helpLines.append("\th: Show this Help menu.")
	helpLines.append("\tx: Finish Hard Ways Betting.")
	return "\n".join(helpLines) + "\n"

def handleLayMenuCommand(command, pointPhase=False):
	global layOff
	cmd = str(command).strip().lower()
	if cmd in ["y", "yes"]:
		layBetting()
		return createActionResult(success=True, messages=[], stateChanged=True) | {"shouldExitMenu": False}
	if pointPhase and cmd in ["o", "off"]:
		if layOff == False:
			layOff = True
			messages = ["Your Lay Bets are Off."]
		else:
			layOff = False
			messages = ["Your Lay Bets are On."]
		return createActionResult(success=True, messages=messages, stateChanged=True) | {"shouldExitMenu": False}
	if cmd in ["d", "td", "takedown"]:
		if pointPhase:
			messages = ["Taking down all of your Lay Bets."]
		else:
			messages = ["Taking down your Lay Bets."]
		layTakeDown()
		return createActionResult(success=True, messages=messages, stateChanged=True) | {"shouldExitMenu": False}
	if cmd in ["a", "across", "all"]:
		layAll()
		return createActionResult(success=True, messages=[], stateChanged=True) | {"shouldExitMenu": False}
	if cmd == "e":
		if gameMode != GameMode.craplessCraps:
			return createActionResult(success=False, messages=["Edge lay helper is only available in Crapless Craps."], stateChanged=False) | {"shouldExitMenu": False}
		layEdges()
		return createActionResult(success=True, messages=[], stateChanged=True) | {"shouldExitMenu": False}
	if cmd == "ea":
		if gameMode != GameMode.craplessCraps:
			return createActionResult(success=False, messages=["Extreme Across lay helper is only available in Crapless Craps."], stateChanged=False) | {"shouldExitMenu": False}
		layExtremeAcross()
		return createActionResult(success=True, messages=[], stateChanged=True) | {"shouldExitMenu": False}
	if cmd == "h":
		return createActionResult(success=True, messages=[layHelpText(pointPhase=pointPhase)], stateChanged=False) | {"shouldExitMenu": False}
	if cmd == "x":
		return createActionResult(success=True, messages=["Done Lay Betting!"], stateChanged=False) | {"shouldExitMenu": True}
	return createActionResult(success=False, messages=["That's not an option!"], stateChanged=False) | {"shouldExitMenu": False}

def handleHardWaysMenuCommand(command, pointPhase=False):
	global hardOff
	cmd = str(command).strip().lower()
	if cmd in ["y", "yes"]:
		hardWaysBetting()
		return createActionResult(success=True, messages=[], stateChanged=True) | {"shouldExitMenu": False}
	if pointPhase and cmd in ["o", "off"]:
		if hardOff == False:
			hardOff = True
			messages = ["Your Hard Ways are Off."]
		else:
			hardOff = False
			messages = ["Hard Ways are On."]
		return createActionResult(success=True, messages=messages, stateChanged=True) | {"shouldExitMenu": False}
	if cmd in ["d", "td", "takedown"]:
		hardTakeDown()
		return createActionResult(success=True, messages=[], stateChanged=True) | {"shouldExitMenu": False}
	if cmd in ["a", "all", "across"]:
		hardAuto()
		return createActionResult(success=True, messages=[], stateChanged=True) | {"shouldExitMenu": False}
	if cmd in ["h4", "h6", "h8", "h10"]:
		hardHigh(cmd)
		return createActionResult(success=True, messages=[], stateChanged=True) | {"shouldExitMenu": False}
	if cmd == "h":
		return createActionResult(success=True, messages=[hardWaysHelpText(pointPhase=pointPhase)], stateChanged=False) | {"shouldExitMenu": False}
	if cmd == "x":
		if pointPhase:
			messages = ["Finished betting on the Hard Ways!"]
		else:
			messages = ["Done betting the Hard Ways!"]
		return createActionResult(success=True, messages=messages, stateChanged=False) | {"shouldExitMenu": True}
	return createActionResult(success=False, messages=["That's not an option!"], stateChanged=False) | {"shouldExitMenu": False}

def placePreset(pre):
	global chipsOnTable, bank, pointIsOn, place, comeOut
	preset = pre.strip().lower()
	if preset not in validPlacePresetCodesForMode():
		writeOutput("That preset is not valid for this game mode.")
		return
	total = 0
	outlay = 0
	for number in place:
		outlay += place[number]
	if preset == 'a':
		while True:
			writeOutput("How many units across the Place Numbers?")
			try:
				unit = int(readInput("> "))
			except ValueError:
				writeOutput("That wasn't even a unit! Try again.")
				continue
			if ((unit*5)*4 + (unit*6)*2) > bank + outlay:
				writeOutput("You don't have enough money for that! Egads!")
				outOfMoney()
				continue
			else:
				break
		point = "y"
		if pointIsOn:
			writeOutput("Include the Point?")
			try:
				point = readInput("> ")
			except ValueError:
				point = "y"
		for key in place:
			chipsOnTable -= place[key]
			bank += place[key]
			if key in [4, 5, 9, 10]:
				place[key] = 5 * unit
			elif key in [6, 8]:
				place[key] = 6 * unit
			if pointIsOn and point not in ['y', 'yes'] and key == comeOut:
				place[key] = 0
			chipsOnTable += place[key]
			bank -= place[key]
			total += place[key]
		writeOutput(f"Placing ${total:,} Across.")
	elif preset == 'i':
		writeOutput("How many units Inside?")
		while True:
			try:
				unit = int(readInput("> "))
			except ValueError:
				writeOutput("Invalid entry, try again.")
				continue
			if ((unit*5)*2 + (unit*6)*2) > bank + outlay:
				writeOutput("You don't have enough money for that! Egads!")
				outOfMoney()
				continue
			else:
				break

		if pointIsOn:
			writeOutput("Include the Point?")
			try:
				insidePoint = readInput("> ")
			except ValueError:
				insidePoint = "n"
		else:
			insidePoint = 'y'
		for key in place:
			chipsOnTable -= place[key]
			bank += place[key]
			if key in [5, 9]:
				place[key] = 5 * unit
			elif key in [6, 8]:
				place[key] = 6 * unit
			else:
				place[key] = 0
			if insidePoint not in ['y', 'yes'] and key == comeOut:
				place[key] = 0
			chipsOnTable += place[key]
			bank -= place[key]
			total += place[key]
		writeOutput(f"Ok, placing ${total:,} inside.")

	elif preset == "c":
		writeOutput("How many units on the 6 and 8?")
		while True:
			try:
				unit = int(readInput("> "))
			except ValueError:
				writeOutput("Invalid entry, try again.")
				continue
			if (unit*6)*2 > bank + outlay:
				writeOutput("You don't have enough money for that! Egads!")
				outOfMoney()
				continue
			else:
				break

		for key in place:
			chipsOnTable -= place[key]
			bank += place[key]
			if key in [6, 8]:
				place[key] = 6 * unit
			else:
				place[key] = 0
			chipsOnTable += place[key]
			bank -= place[key]
			total += place[key]
		writeOutput(f"Ok, placing ${total:,} on the 6 and 8.")
	elif preset == "ea":
		while True:
			writeOutput("How many Extreme Across units from 2 through 12?")
			try:
				unit = int(readInput("> "))
			except ValueError:
				writeOutput("That wasn't even a unit! Try again.")
				continue
			targetNumbers = [2, 3, 4, 5, 6, 8, 9, 10, 11, 12]
			totalNeed = 0
			for number in targetNumbers:
				totalNeed += placeUnitSize(number) * unit
			if totalNeed > bank + outlay:
				writeOutput("You don't have enough money for that! Egads!")
				outOfMoney()
				continue
			break

		for key in place:
			chipsOnTable -= place[key]
			bank += place[key]
			if key in [2, 3, 4, 5, 6, 8, 9, 10, 11, 12]:
				place[key] = placeUnitSize(key) * unit
			else:
				place[key] = 0
			chipsOnTable += place[key]
			bank -= place[key]
			total += place[key]
		writeOutput(f"Ok, placing ${total:,} Extreme Across.")
	elif preset == "e":
		while True:
			writeOutput("How many Edge units on 2, 3, 11, and 12?")
			try:
				unit = int(readInput("> "))
			except ValueError:
				writeOutput("That wasn't even a unit! Try again.")
				continue
			targetNumbers = [2, 3, 11, 12]
			totalNeed = 0
			for number in targetNumbers:
				totalNeed += placeUnitSize(number) * unit
			if totalNeed > bank + outlay:
				writeOutput("You don't have enough money for that! Egads!")
				outOfMoney()
				continue
			break

		for key in place:
			chipsOnTable -= place[key]
			bank += place[key]
			if key in [2, 3, 11, 12]:
				place[key] = placeUnitSize(key) * unit
			else:
				place[key] = 0
			chipsOnTable += place[key]
			bank -= place[key]
			total += place[key]
		writeOutput(f"Ok, placing ${total:,} on the edges.")


def placeMover():
	global place, chipsOnTable, bank, comeOut
	if gameMode == GameMode.craplessCraps:
		writeOutput("Place mover is currently disabled in Crapless Craps.")
		return
	for key in place:
		if place[key] == 0 and place[comeOut] > 0:
			if key in [6, 8] and comeOut in [4, 5, 9, 10]:
				place[key] = place[comeOut] + place[comeOut]//5
			elif key in [6, 8] and comeOut in [6, 8]:
				place[key] = place[comeOut]
			elif key in [4, 5, 9, 10] and comeOut in [6, 8]:
				place[key] = place[comeOut] - place[comeOut]//6
			elif key in [4, 5, 9, 10] and comeOut in [4, 5, 9, 10]:
				place[key] = place[comeOut]
				writeOutput(f"Moving your ${place[comeOut]:,} Place {comeOut} bet. You now have ${place[key]:,} on the {key}.")
			chipsOnTable -= place[comeOut]
			bank += place[comeOut]
			chipsOnTable += place[key]
			bank -= place[key]
			place[comeOut] = 0

def placeBets():
	global place, chipsOnTable, bank
	madeBet = True
	for key in validPlaceNumbers():
		writeOutput(f"You have ${place[key]:,} on the Place {key}.")
		writeOutput(f"How much on the Place {key}?")
		while True:
			bet = 0
			try:
				bet = int(readInput("$>"))
				if bet > bank + chipsOnTable:
					writeOutput("You don't have enough money to make that bet! Try again.")
					outOfMoney()
					writeOutput(f"How much on the Place {key}?")
					continue
				if not isPlaceAmountAllowed(number=key, bet=bet):
					writeOutput("Invalid amount for that Place bet. Try again.")
					continue
				madeBet = True
				break
			except ValueError:
				bet = place[key]
				madeBet = False
				break

		if bet > 0:
			chipsOnTable -= place[key]
			if madeBet and bet != place[key]:
				bank -= bet - place[key] 
			place[key] = bet
			chipsOnTable += bet
			if (key in [4, 10] and bet >= 10) or (gameMode == GameMode.craplessCraps and key in [2, 3, 11, 12] and bet >= 20):
				writeOutput(f"Buying the {key} for ${bet:,}.")
			else:
				writeOutput(f"${bet:,} on the Place {key}.")
		elif place[key] > 0 and bet == 0:
			writeOutput(f"Ok, taking down your Place {key} bet.")
			chipsOnTable -= place[key]
			bank += place[key]
			place[key] = 0

def placeShow():
	global place
	for key in validPlaceNumbers():
		if place[key] > 0:
			writeOutput(f"You have ${place[key]:,} on the Place {key}.")

def placeTakeDown():
	global place, bank, chipsOnTable
	for key in place:
		chipsOnTable -= place[key]
		bank += place[key]
		place[key] = 0

def vig(bet):
	total = bet * 0.05
	if bet < 25:
		commission = math.ceil(total)
	else:
		commission = math.floor(total)
	writeOutput(f"${commission:,} paid to the House for the vig.")
	return commission

def placeCheck(roll):
	global place, bank, chipsOnTable
	snapshot = captureBetSnapshot()
	settlement = settlePlaceBetsForMode(placeBets=place, roll=roll, gameMode=gameMode)
	snapshot["place"] = settlement.placeBets
	for key in [2, 3, 4, 5, 6, 8, 9, 10, 11, 12]:
		if key not in snapshot["place"]:
			snapshot["place"][key] = 0
	snapshot["bank"] += settlement.bankDelta
	snapshot["chipsOnTable"] += settlement.chipsOnTableDelta
	applyBetSnapshot(snapshot)
	for message in settlement.messages:
		writeOutput(message)

	hitNumber = settlement.hitNumber
	if hitNumber is not None:
		press = str(readInput("Change your bet? 'y' to change, 'p' to full-press, 'hp' to half-press, or 'u' to press 1 unit, or Enter to do nothing.\n > ")).strip().lower()
		if press == 'y':
			writeOutput(f"How much on the Place {hitNumber}?")
			bank += place[hitNumber]
			while True:
				bet = betPrompt()
				if isPlaceAmountAllowed(number=hitNumber, bet=bet):
					break
				writeOutput("Invalid amount for that Place bet. Try again.")
				chipsOnTable -= bet
				bank += bet
			if bet == 0:
				chipsOnTable -= place[hitNumber]
				place[hitNumber] = bet
				writeOutput(f"Ok, taking down your Place {hitNumber} bet.")
			else:
				chipsOnTable -= place[hitNumber]
				place[hitNumber] = bet
				writeOutput(f"Ok, ${place[hitNumber]:,} on the Place {hitNumber}.")
		elif press == 'p':
			bank += place[hitNumber]
			chipsOnTable -= place[hitNumber]
			place[hitNumber] *= 2
			bank -= place[hitNumber]
			chipsOnTable += place[hitNumber]
			writeOutput(f"Full Press! You now have ${place[hitNumber]} on the Place {hitNumber}")
		elif press == 'hp':
			bank += place[hitNumber]
			chipsOnTable -= place[hitNumber]
			place[hitNumber] += normalizedHalfPressIncrement(number=hitNumber, currentWager=place[hitNumber])
			bank -= place[hitNumber]
			chipsOnTable += place[hitNumber]
			writeOutput(f"Half Press! You now have ${place[hitNumber]} on the Place {hitNumber}")
		elif press == 'u':
			bank += place[hitNumber]
			chipsOnTable -= place[hitNumber]
			place[hitNumber] += placeUnitSize(hitNumber)
			bank -= place[hitNumber]
			chipsOnTable += place[hitNumber]
			writeOutput(f"Pressing up one unit. You now have ${place[hitNumber]} on the Place {hitNumber}")

def showAllBets():
	global comeBet, dComeBet, fireBet, lineBets, propBets, atsAll, atsTall, atsSmall
	for value in lineBets:
		if lineBets[value] > 0:
			writeOutput(f"You have ${lineBets[value]:,} on the {value}.")
	if comeBet > 0:
		writeOutput(f"You have ${comeBet:,} on the Come.")
	if dComeBet > 0:
		writeOutput(f"You have ${dComeBet:,} on the Don't Come.")
	comeShow()
	placeShow()
	layShow() 
	fieldShow()
	hardShow()
	for value in propBets:
		if propBets[value] > 0:
			writeOutput(f"${propBets[value]:,} on {value}.")
	if atsAll + atsSmall + atsTall > 0:
		writeOutput(f"You have ${atsAll:,} on the All, ${atsTall:,} on the Tall, and ${atsSmall:,} on the Small.")
	if fireBet > 0:
		writeOutput(f"You have ${fireBet:,} on the Fire Bet.")

def runPlaceMenu(pointPhase=False):
	while True:
		placeShow()
		placeCommand = str(readInput("Place Bets? > ")).strip().lower()
		commandResult = handlePlaceMenuCommand(placeCommand, pointPhase=pointPhase)
		emitActionResult(commandResult)
		if commandResult["shouldExitMenu"]:
			break

def runLayMenu(pointPhase=False):
	while True:
		layShow()
		layCommand = str(readInput("Lay Bets? > ")).strip().lower()
		commandResult = handleLayMenuCommand(layCommand, pointPhase=pointPhase)
		emitActionResult(commandResult)
		if commandResult["shouldExitMenu"]:
			break

def runHardWaysMenu(pointPhase=False):
	while True:
		hardShow()
		hardCommand = str(readInput("Hard Ways Bets? > ")).strip().lower()
		commandResult = handleHardWaysMenuCommand(hardCommand, pointPhase=pointPhase)
		emitActionResult(commandResult)
		if commandResult["shouldExitMenu"]:
			break

def handleBettingCommand(command, pointPhase=False):
	global working
	syncRuntimeFromGlobals()
	def returnCommandResult(shouldRoll=False, handled=True):
		syncRuntimeFromGlobals()
		return bettingCommandResult(shouldRoll=shouldRoll, handled=handled)
	cmd = str(command).strip().lower()
	if cmd == "q":
		quitGame()
		return returnCommandResult(shouldRoll=False, handled=True)
	if cmd == "b":
		if pointPhase:
			writeOutput(f"You have ${bank:,} in your rack with ${chipsOnTable:,} on the table. The Point is {comeOut}.")
		else:
			writeOutput(f"You have ${bank:,} in the Bank and ${chipsOnTable:,} out on the table.")
		return returnCommandResult(shouldRoll=False, handled=True)
	if cmd == "bb":
		outOfMoney()
		return returnCommandResult(shouldRoll=False, handled=True)
	if cmd == "a":
		showAllBets()
		return returnCommandResult(shouldRoll=False, handled=True)
	if pointPhase:
		if cmd in ["o", "po", "dpo"]:
			if lineBets["Pass"] > 0 or lineBets["Don't Pass"] > 0:
				odds()
			else:
				writeOutput("You don't have a Line bet, silly!")
			return returnCommandResult(shouldRoll=False, handled=True)
		if cmd == "dp":
			if gameMode == GameMode.craplessCraps:
				writeOutput("Don't Pass is not available in Crapless Craps.")
				return returnCommandResult(shouldRoll=False, handled=True)
			if lineBets["Don't Pass"] > 0:
				dpPhase2()
			else:
				writeOutput("You don't have a Don't Pass bet!")
			return returnCommandResult(shouldRoll=False, handled=True)
		if cmd == "c":
			comeShow()
			writeOutput("Come Bet:\n")
			come()
			return returnCommandResult(shouldRoll=False, handled=True)
		if cmd == "co":
			comeOddsChange()
			return returnCommandResult(shouldRoll=False, handled=True)
		if cmd == "dcd":
			if gameMode == GameMode.craplessCraps:
				clearDontComeForCrapless()
				writeOutput("Don't Come is not available in Crapless Craps.")
				return returnCommandResult(shouldRoll=False, handled=True)
			dComeDown()
			return returnCommandResult(shouldRoll=False, handled=True)
		if cmd == "p":
			runPlaceMenu(pointPhase=True)
			return returnCommandResult(shouldRoll=False, handled=True)
		if cmd in ["ly", "lay"]:
			runLayMenu(pointPhase=True)
			return returnCommandResult(shouldRoll=False, handled=True)
		if cmd == "f":
			fieldShow()
			fb2 = str(readInput("Field Bet? > ")).strip().lower()
			if fb2 in ['y', 'yes']:
				field()
			elif fb2 in ['d', 'td', 'takedown']:
				fieldTakeDown()
			return returnCommandResult(shouldRoll=False, handled=True)
		if cmd == "hd":
			runHardWaysMenu(pointPhase=True)
			return returnCommandResult(shouldRoll=False, handled=True)
		if cmd in ["pr", "prop"]:
			propBetting()
			return returnCommandResult(shouldRoll=False, handled=True)
		if cmd == "h":
			if gameMode == GameMode.craplessCraps:
				writeOutput("Betting Codes:\n\n\to: Line and Lay Odds\n\tp: Place Bets\n\tly: Lay Bets\n\tc: Come Bets\n\tf: Field Bet\n\thd: Hard Ways Bets\n\tpr: Prop Bets\n\tbb: Add bankroll from the ATM\n\th: Show this Help Menu\n\tx: Finish betting and Roll the Dice")
			else:
				writeOutput("Betting Codes:\n\n\to: Line and Lay Odds\n\tdp: Take Down Don't Pass Bet\n\tp: Place Bets\n\tly: Lay Bets\n\tc: Come Bets\n\tdcd: Take down DC and Odds\n\tf: Field Bet\n\thd: Hard Ways Bets\n\tpr: Prop Bets\n\tbb: Add bankroll from the ATM\n\th: Show this Help Menu\n\tx: Finish betting and Roll the Dice")
			return returnCommandResult(shouldRoll=False, handled=True)
		if cmd in ["r", "x"]:
			writeOutput("Dice are rolling!")
			return returnCommandResult(shouldRoll=True, handled=True)
		writeOutput("That's not a betting option, silly!")
		return returnCommandResult(shouldRoll=False, handled=False)
	if cmd in ["l", "line", "line bets"]:
		writeOutput("Line Bets:\n")
		lineBetting()
		return returnCommandResult(shouldRoll=False, handled=True)
	if cmd == "p":
		runPlaceMenu(pointPhase=False)
		return returnCommandResult(shouldRoll=False, handled=True)
	if cmd in ["ly", "lay"]:
		runLayMenu(pointPhase=False)
		return returnCommandResult(shouldRoll=False, handled=True)
	if cmd in ["f", "field"]:
		fieldShow()
		fBet = str(readInput("Field Bet? > ")).strip().lower()
		if fBet in ['y', 'yes']:
			field()
		elif fBet in ['d', 'td', 'takedown']:
			fieldTakeDown()
		return returnCommandResult(shouldRoll=False, handled=True)
	if cmd in ["hd", "hard", "hw"]:
		runHardWaysMenu(pointPhase=False)
		return returnCommandResult(shouldRoll=False, handled=True)
	if cmd in ["w", "work", "working"]:
		plCheck = hCheck = lCheck = cCheck = 0
		for value in place.values():
			plCheck += value
		for value in hardWays.values():
			hCheck += value
		for value in layBets.values():
			lCheck += value
		for value in comeBets.values():
			cCheck += value
		for value in dComeBets.values():
			cCheck += value
		if plCheck > 0 or hCheck > 0 or lCheck > 0 or cCheck > 0:
			if working:
				working = False
				writeOutput("Ok, all bets are Off.")
			else:
				working = True
				writeOutput("Ok, all bets are Working!")
		else:
			writeOutput("Make some bets first so they can Work!")
		return returnCommandResult(shouldRoll=False, handled=True)
	if cmd in ["pr", "prop"]:
		propBetting()
		return returnCommandResult(shouldRoll=False, handled=True)
	if cmd == "dcd":
		if gameMode == GameMode.craplessCraps:
			clearDontComeForCrapless()
			writeOutput("Don't Come is not available in Crapless Craps.")
			return returnCommandResult(shouldRoll=False, handled=True)
		dComeDown()
		return returnCommandResult(shouldRoll=False, handled=True)
	if cmd == "ats":
		if atsOn == True:
			writeOutput(f"All Tall Small: {allNums}")
		elif throws == 0:
			writeOutput("All Tall Small:\n")
			atsBetting()
		else:
			writeOutput("All Tall Small will be available after the next 7 rolls.")
		return returnCommandResult(shouldRoll=False, handled=True)
	if cmd == "fire":
		if fireBet == 0:
			writeOutput("Fire Bet:\n")
			fireBetting()
		else:
			writeOutput(f"You have ${fireBet:,} on the Fire Bet; Numbers Hit: {fire}.")
		return returnCommandResult(shouldRoll=False, handled=True)
	if cmd == "h":
		if gameMode == GameMode.craplessCraps:
			writeOutput("Betting Codes:\n\tl: Line Bets\n\tp: Place Bets\n\tly: Lay Bets\n\tf: Field Bet\n\thd: Hard Ways Bets\n\tpr: Prop Bets\n\tw: Toggle if Bets are Working\n\tats: All Tall Small\n\tfire: Fire Bet\n\tbb: Add bankroll from the ATM\n\th: Show this Help Menu\n\tx or r: Roll the Dice!")
		else:
			writeOutput("Betting Codes:\n\tl: Line Bets\n\tp: Place Bets\n\tly: Lay Bets\n\tf: Field Bet\n\thd: Hard Ways Bets\n\tpr: Prop Bets\n\tw: Toggle if Bets are Working\n\tdcd: Take down Don't Come bet\n\tats: All Tall Small\n\tfire: Fire Bet\n\tbb: Add bankroll from the ATM\n\th: Show this Help Menu\n\tx or r: Roll the Dice!")
		return returnCommandResult(shouldRoll=False, handled=True)
	if cmd in ["x", "r"]:
		writeOutput("Rolling the dice!")
		return returnCommandResult(shouldRoll=True, handled=True)
	writeOutput("That's not an option, silly!")
	return returnCommandResult(shouldRoll=False, handled=False)

def submitCommand(commandText, pointPhase=False, autoCapture=False):
	commandValue = str(commandText).strip().lower()
	if autoCapture:
		captureResult = runWithCapture(lambda: handleBettingCommand(commandValue, pointPhase=pointPhase))
		commandResult = captureResult["result"]
		capturedOutput = list(captureResult["capturedOutput"])
		capturedPrompts = list(captureResult["capturedPrompts"])
	else:
		commandResult = handleBettingCommand(commandValue, pointPhase=pointPhase)
		capturedOutput = getCapturedOutput()
		capturedPrompts = getCapturedPrompts()
	resultPayload = withApiVersion({
		"command": commandValue,
		"pointPhase": bool(pointPhase),
		"shouldRoll": bool(commandResult.shouldRoll),
		"handled": bool(commandResult.handled),
		"runtimeState": getRuntimeState(),
		"capturedOutput": capturedOutput,
		"capturedPrompts": capturedPrompts
	})
	emitEvent("commandProcessed", resultPayload)
	return resultPayload

def step(commandText=None, pointPhase=False, autoCapture=False):
	if commandText is not None:
		commandPayload = submitCommand(commandText=commandText, pointPhase=pointPhase, autoCapture=autoCapture)
		stepPayload = withApiVersion({
			"stepType": "command",
			"commandResult": commandPayload,
			"cycleResult": None,
			"runtimeState": commandPayload["runtimeState"],
			"capturedOutput": list(commandPayload["capturedOutput"]),
			"capturedPrompts": list(commandPayload["capturedPrompts"])
		})
		emitEvent("stepCompleted", stepPayload)
		return stepPayload
	if pointPhase:
		raise ValueError("pointPhase can only be used with commandText.")
	if autoCapture:
		captureResult = runWithCapture(lambda: runOneCycle())
		cyclePayload = captureResult["result"]
		capturedOutput = list(captureResult["capturedOutput"])
		capturedPrompts = list(captureResult["capturedPrompts"])
	else:
		cyclePayload = runOneCycle()
		capturedOutput = getCapturedOutput()
		capturedPrompts = getCapturedPrompts()
	stepPayload = withApiVersion({
		"stepType": "cycle",
		"commandResult": None,
		"cycleResult": dict(cyclePayload),
		"runtimeState": getRuntimeState(),
		"capturedOutput": capturedOutput,
		"capturedPrompts": capturedPrompts
	})
	emitEvent("stepCompleted", stepPayload)
	return stepPayload

def resolveComeOutRoll():
	global comeOut, throws, working, pointIsOn
	syncRuntimeFromGlobals()
	comeOut = roll()
	outcome = evaluateRoll(gameState, comeOut)
	throws += 1
	comeCheck(comeOut)
	layCheck(comeOut)
	fieldCheck(comeOut)
	if working:
		placeCheck(comeOut)
		hardCheck(comeOut)
	propPay(comeOut)
	if atsOn == True:
		ats(comeOut)
	if outcome == RollOutcome.natural:
		if comeOut == 7:
			throws = 0
		lineCheck(comeOut, p2)
		working = False
		syncGameState(gameState=gameState, bank=bank, chipsOnTable=chipsOnTable, throws=throws, pointIsOn=pointIsOn, comeOut=comeOut, p2=p2)
		syncRuntimeFromGlobals()
		return comeOutRollResult(enteredPointPhase=False, outcome=outcome)
	if outcome == RollOutcome.craps:
		lineCheck(comeOut, p2)
		working = False
		syncGameState(gameState=gameState, bank=bank, chipsOnTable=chipsOnTable, throws=throws, pointIsOn=pointIsOn, comeOut=comeOut, p2=p2)
		syncRuntimeFromGlobals()
		return comeOutRollResult(enteredPointPhase=False, outcome=outcome)
	pointIsOn = True
	working = False
	syncGameState(gameState=gameState, bank=bank, chipsOnTable=chipsOnTable, throws=throws, pointIsOn=pointIsOn, comeOut=comeOut, p2=p2)
	syncRuntimeFromGlobals()
	return comeOutRollResult(enteredPointPhase=True, outcome=outcome)

def resolvePointRoll():
	global p2, throws, placeOff, layOff, hardOff, pointIsOn
	syncRuntimeFromGlobals()
	p2 = roll()
	syncGameState(gameState=gameState, bank=bank, chipsOnTable=chipsOnTable, throws=throws, pointIsOn=pointIsOn, comeOut=comeOut, p2=p2)
	outcome = evaluateRoll(gameState, p2)
	throws += 1
	comeCheck(p2)
	if placeOff:
		placeOff = False
	else:
		placeCheck(p2)
	if layOff:
		layOff = False
	else:
		layCheck(p2)
	fieldCheck(p2)
	if hardOff:
		hardOff = False
	else:
		hardCheck(p2)
	lineCheck(comeOut, p2)
	propPay(p2)
	if fireBet > 0:
		fireCheck()
	if atsOn == True:
		ats(p2)
	if outcome == RollOutcome.sevenOut:
		throws = 0
		pointIsOn = False
		syncGameState(gameState=gameState, bank=bank, chipsOnTable=chipsOnTable, throws=throws, pointIsOn=pointIsOn, comeOut=comeOut, p2=p2)
		syncRuntimeFromGlobals()
		return pointRollResult(pointRoundEnded=True, outcome=outcome)
	if outcome == RollOutcome.pointHit:
		writeOutput("Point Hit! Front line winner!")
		pointIsOn = False
		syncGameState(gameState=gameState, bank=bank, chipsOnTable=chipsOnTable, throws=throws, pointIsOn=pointIsOn, comeOut=comeOut, p2=p2)
		syncRuntimeFromGlobals()
		return pointRollResult(pointRoundEnded=True, outcome=outcome)
	syncGameState(gameState=gameState, bank=bank, chipsOnTable=chipsOnTable, throws=throws, pointIsOn=pointIsOn, comeOut=comeOut, p2=p2)
	syncRuntimeFromGlobals()
	return pointRollResult(pointRoundEnded=False, outcome=outcome)

def runPointPhaseBettingMenu():
	while True:
		writeOutput("Place your bets!\n")
		round2 = readInput(">  ").strip().lower()
		stepResult = step(commandText=round2, pointPhase=True)
		if stepResult["commandResult"]["shouldRoll"]:
			return {"shouldRoll": True}

def runComeOutBettingMenu():
	while True:
		writeOutput("Place your Bets!\n")
		round1 = readInput(">  ").strip().lower()
		stepResult = step(commandText=round1, pointPhase=False)
		if stepResult["commandResult"]["shouldRoll"]:
			return {"shouldRoll": True}

def runComeOutRound():
	runComeOutBettingMenu()
	comeOutRoll = resolveComeOutRoll()
	return comeOutRoundResult(enteredPointPhase=comeOutRoll.enteredPointPhase, outcome=comeOutRoll.outcome)

def showPointPhaseStatus():
	runtime = syncRuntimeFromGlobals()
	if runtime.chipsOnTable > 0:
		writeOutput(f"You have ${runtime.bank:,} in the bank with ${runtime.chipsOnTable:,} out on the table.")
	else:
		writeOutput(f"You have ${runtime.bank:,} in the bank.")
	if runtime.bank <= 0 and runtime.chipsOnTable <= 0:
		outOfMoney()
	writeOutput(f"\n{runtime.comeOut} is the Point!\n")
	writeOutput(f"Throws: {runtime.throws}")

def runPointPhaseRound():
	while True:
		showPointPhaseStatus()

#Phase 2 Betting

		runPointPhaseBettingMenu()
		pointRollResult = resolvePointRoll()
		if pointRollResult.pointRoundEnded:
			return pointPhaseRoundResult(roundEnded=True, outcome=pointRollResult.outcome)
		continue

def runOneCycle():
	runtime = syncRuntimeFromGlobals()
	emitEvent("cycleStarted", withApiVersion({"point": int(runtime.comeOut), "throws": int(runtime.throws), "gameMode": runtime.gameMode}))
	comeOutResult = runComeOutRound()
	runtime = syncRuntimeFromGlobals()
	emitEvent("comeOutResolved", withApiVersion({"enteredPointPhase": bool(comeOutResult.enteredPointPhase), "outcome": comeOutResult.outcome, "runtimeState": getRuntimeState()}))
	cycleResult = withApiVersion({
		"enteredPointPhase": bool(comeOutResult.enteredPointPhase),
		"comeOutOutcome": comeOutResult.outcome,
		"pointPhaseOutcome": None,
		"pointRoundEnded": False,
		"point": int(runtime.comeOut),
		"throws": int(runtime.throws)
	})
	if not comeOutResult.enteredPointPhase:
		emitEvent("cycleCompleted", withApiVersion({"cycleResult": dict(cycleResult), "runtimeState": getRuntimeState()}))
		return cycleResult
	pointPhaseResult = runPointPhaseRound()
	runtime = syncRuntimeFromGlobals()
	emitEvent("pointPhaseResolved", withApiVersion({"roundEnded": bool(pointPhaseResult.roundEnded), "outcome": pointPhaseResult.outcome, "runtimeState": getRuntimeState()}))
	cycleResult["pointPhaseOutcome"] = pointPhaseResult.outcome
	cycleResult["pointRoundEnded"] = bool(pointPhaseResult.roundEnded)
	cycleResult["point"] = int(runtime.comeOut)
	cycleResult["throws"] = int(runtime.throws)
	emitEvent("cycleCompleted", withApiVersion({"cycleResult": dict(cycleResult), "runtimeState": getRuntimeState()}))
	return cycleResult

#Additional Global Variables
p2 = 0
pointIsOn = False
working = plWork = hdWork = lyWork = coWork = False
throws = 0
comeOut = 0
gameMode = GameMode.craps
gameRuntime = GameRuntime(bank=bank, chipsOnTable=chipsOnTable, throws=throws, comeOut=comeOut, pointIsOn=pointIsOn, p2=p2, gameMode=gameMode)


def selectGameMode():
	global gameMode
	writeOutput("Choose game mode:")
	writeOutput("1. Craps")
	writeOutput("2. Crapless Craps")
	while True:
		choice = str(readInput("> ")).strip()
		selectedMode = parseGameModeChoice(choice)
		if selectedMode is None:
			writeOutput("Invalid choice. Enter 1 or 2.")
			continue
		gameMode = selectedMode
		selectedProfile = getRulesProfile(gameMode)
		writeOutput(f"{selectedProfile.displayName} selected.")
		break

def setGameMode(modeValue):
	global gameMode
	gameMode = normalizedGameMode(modeValue)
	syncGameState(gameState=gameState, bank=bank, chipsOnTable=chipsOnTable, throws=throws, pointIsOn=pointIsOn, comeOut=comeOut, p2=p2, gameMode=gameMode)
	syncRuntimeFromGlobals()
	return gameMode

def initializeGame(startBank, selectedMode):
	global bank, initBank
	bankroll = int(startBank)
	if bankroll <= 0:
		raise ValueError("Starting bank must be greater than zero.")
	mode = normalizedGameMode(selectedMode)
	resetRuntimeState()
	setGameMode(mode)
	initBank = bankroll
	bank = bankroll
	syncGameState(gameState=gameState, bank=bank, chipsOnTable=chipsOnTable, throws=throws, pointIsOn=pointIsOn, comeOut=comeOut, p2=p2, gameMode=gameMode)
	syncRuntimeFromGlobals()
	emitEvent("gameInitialized", withApiVersion({"startBank": bankroll, "gameMode": gameMode, "runtimeState": getRuntimeState()}))
	return withApiVersion(getRuntimeState())

gameState = createGameState(
	bank=bank,
	chipsOnTable=chipsOnTable,
	throws=throws,
	pointIsOn=pointIsOn,
	comeOut=comeOut,
	p2=p2,
	gameMode=gameMode
)

def runGame():
	writeOutput(f"Oh Craps! v.{version}\nBy: Marco Salsiccia")
	selectGameMode()
	cashIn()
	initializeGame(startBank=initBank, selectedMode=gameMode)
	while True:
		runtime = syncRuntimeFromGlobals()
		if runtime.chipsOnTable <= 0:
			writeOutput(f"You have ${runtime.bank:,} in the bank.")
		else:
			writeOutput(f"You have ${runtime.bank:,} in the bank with ${runtime.chipsOnTable:,} out on the table.")
		if runtime.bank <= 0 and runtime.chipsOnTable <= 0:
			outOfMoney()
		writeOutput(f"Throws: {runtime.throws}\n")

	# Initial bets

		runOneCycle()

# Game Start
if __name__ == "__main__":
	runGame()
