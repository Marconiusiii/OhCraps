#!/usr/bin/env python3
from random import *
import math

die1 = 0
die2 = 0

def roll():
	global rollHard, pointIsOn, die1, die2
	rollHard = False
	d1 = randint(1, 6)
	d2 = randint(1, 6)
	if d1 > d2 or d1 == d2:
		die1 = d1
		die2 = d2
	else:
		die1 = d2
		die2 = d1

	total = die1 + die2
	if die1 == die2 and total in [4, 6, 8, 10]:
		rollHard = True
		print("{} the Hard Way!".format(total))
	elif total in [7, 11] and pointIsOn == False:
		print("{total} winner! Pay the line, take the don't!".format(total=total))
	else:
		call = randint(1, 10)
		if call <=5:
			print("{tot}, {call}!".format(tot=total, call=stickman(total)))
		else:
			print("{tot}, a {d1} {d2} {tot}!".format(tot=total, d1=die1, d2=die2))

	return total


dealerCalls = {
2: ["Craps", "eye balls", "two aces", "rats eyes", "snake eyes", "push the don't", "eleven in a shoe store", "twice in the rice", "two craps two, two bad boys from Illinois", "two crap aces", "aces in both places", "a spot and a dot", "dimples", "double the Field"],
3: ["Craps", "ace-deuce", "three craps, ace caught a deuce, no use", "divorce roll, come up single", "winner on the dark side", "three craps three, the indicator", "crap and a half", "small ace deuce, can't produce", "2 , 1, son of a gun"],
4: ["Double deuce", "Little Joe", "Little Joe from Kokomo", "Hit us in the 2 2", "2 spots and 2 dots", "Ace Tres"],
5: ["After 5 the Field's alive", "Fiver Fiver Race Track Driver", "No Field 5", "Little Phoebe", "We got the fiver", "Five 5"],
6: ["The national average", "Big Red, catch 'em in the corner", "Sixie from Dixie"],
7: ["Line Away, grab the money", "the bruiser", "point 7", "Out", "Loser 7", "Nevada Breakfast", "Cinco Dos, Adios", "Adios", "3 4 on the floor"],
8: ["a square pair", "eighter from the theater", "windows", "the Great!", "get yer mate"],
9: ["niner 9", "center field 9", "Center of the garden", "ocean liner niner", "Nina from Pasadena", "nina Niner, wine and dine her", "El Nine-O", "Niner, nothing finer"],
10: ["puppy paws", "pair o' roses", "The big one on the end", "55 to stay alive", "pair of sunflowers", "two stars from Mars", "64 out the door"],
11: ["Yo Eleven", "Yo", "6 5, no drive", "yo 'leven", "It's not my eleven, it's Yo Eleven"],
12: ["craps", "midnight", "a whole lotta crap", "craps to the max", "boxcars", "all the spots we gots", "triple field", "atomic craps", "Hobo's delight"]
}

def stickman(roll):
	return dealerCalls[roll][randint(0, len(dealerCalls[roll])-1)]


# Fire Bet Setup

fire = []
fireBet = 0

"""
win 4 numbers : 24:1
win 5 numbers: 249:1
win 6 numbers: 999:1

2, 3, 7, 11, 12 do not affect fire bet, only 7 outs in phase 2.
Once point is hit, the same point does not add to the fire bet. Fire bet must hit all 6 different point numbers.
Payout starts at 4 point numbers on a 7 out. 3 or less is a full loss.
"""

def fireBetting():
	global fireBet
	print("How much on the Fire Bet?")
	fireBet = betPrompt()
	print("Ok, ${} on the Fire Bet. Good Luck!".format(fireBet))

def fireCheck():
	global bank, fire, fireBet, comeOut, p2, chipsOnTable
	if p2 == 7:
		chipsOnTable -= fireBet
		if len(fire) < 4:
			print("You lost ${} from the Fire Bet.".format(fireBet))
			bank -= fireBet
			fireBet = 0
			fire = []
		elif len(fire) == 4:
			print("You won ${} on the Fire Bet! Great job!".format(fireBet * 24))
			bank += fireBet * 24
			fireBet = 0
			fire = []
		elif len(fire) == 5:
			print("You won ${} on the Fire Bet! Holy Crap!".format(fireBet * 249))
			bank += fireBet * 249
			fireBet = 0
			fire = []
		elif len(fire) == 6:
			print("Wowsers! You nailed the Fire Bet Jackpot and won ${}!!!".format(fireBet * 999))
			bank += fireBet * 999
			fireBet = 0
			fire = []
	elif p2 in [4, 5, 6, 8, 9, 10] and p2 == comeOut:
		if p2 not in fire:
			fire.append(p2)
			fire.sort()
			print("Fire Bet Point Numbers: {}".format(fire))

	


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
	global hardWays, chipsOnTable
	for key in hardWays:
		if hardWays[key] > 0:
			print("You have ${bet} on the hard {num}.".format(bet=hardWays[key], num=key))
		print("How much on the Hard {}?".format(key))
		bet = betPrompt()
		if bet > 0:
			chipsOnTable -= hardWays[key]
			hardWays[key] = bet
			print("Ok, ${bet} on the Hard {num}.".format(bet=hardWays[key], num=key))
		elif hardWays[key] > 0 and bet == 0:
			print("Taking down your Hard {}.".format(key))
			chipsOnTable -= hardWays[key]

			hardWays[key] = bet

def hardTakeDown():
	global hardWays, chipsOnTable
	print("Taking down your Hard Ways.")
	for key in hardWays:
		chipsOnTable -= hardWays[key]
		hardWays[key] = 0

def hardCheck(roll):
	global bank, chipsOnTable, hardWays, rollHard
	if roll == 7:
		loss = 0
		for key in hardWays:
			if hardWays[key] > 0:
				loss += hardWays[key]
				hardWays[key] = 0
		if loss > 0:
			print("You lost ${} from the Hard Ways.".format(loss))
			bank -= loss
			chipsOnTable -= loss
	elif roll in [4, 6, 8, 10]:
		if hardWays[roll] > 0 and rollHard == True:
			if roll in [4, 10]:
				win = hardWays[roll] * 7
			elif roll in [6, 8]:
				win = hardWays[roll] * 9
			print("You won ${win} on the Hard {num}!".format(win=win, num=roll))
			bank += win
			print("Press your bet?")
			hardPress = input(">")
			if hardPress.lower() in ['y', 'yes']:
				print("How much on the Hard {}?".format(roll))
				chipsOnTable -= hardWays[roll]
				hardWays[roll] = betPrompt()
				if hardWays[roll] == 0:
					print("Ok, taking down your Hard {} bet.".format(roll))
				else:
					print("Ok, bumping up your Hard {num} bet to ${bet}.".format(num=roll, bet=hardWays[roll]))
			else:
				pass
		elif hardWays[roll] > 0 and rollHard == False:
			print("You lost ${loss} from the Hard {num}.".format(loss=hardWays[roll], num=roll))
			bank -= hardWays[roll]
			chipsOnTable -= hardWays[roll]
			print("Go back up on your Hard {} bet?".format(roll))
			hardBack = input(">")
			if hardBack.lower() in ['y', 'yes']:
				print("How much on the Hard {}?".format(roll))
				hardWays[roll] = betPrompt()
				print("Ok, going back up on the Hard {num} for ${bet}.".format(num=roll, bet=hardWays[roll]))
			else:
				hardWays[roll] = 0


def hardShow():
	global hardWays
	for key in hardWays:
		if hardWays[key] > 0:
			print("You have ${bet} on the Hard {num}.".format(bet=hardWays[key], num=key))

#Line Bets

lineBets = {
"Pass": 0,
"Pass Odds": 0,
"Don't Pass": 0,
"Don't Pass Odds": 0
}


def lineBetting():
	global lineBets, chipsOnTable
	print("Enter the Line Bet you'd like to make, or type 'x' and hit Enter to finish Line Betting.")
	while True:
		if lineBets["Pass"] > 0:
			print("You have ${} on the Pass Line.".format(lineBets["Pass"]))
		if lineBets["Don't Pass"] > 0:
			print("You have ${} on the Don't Pass Line.".format(lineBets["Don't Pass"]))
		try:
			lBet = input(">")
		except ValueError:
			print("That won't work, try again.")
			continue
		if lBet.lower() in ['p', 'pass', 'passline', 'pass line']:
			chipsOnTable -= lineBets["Pass"]
			print("How much on the Pass Line?")
			lineBets["Pass"] = betPrompt()
			print("Ok, ${} on the Pass Line.".format(lineBets["Pass"]))
			continue
		elif lBet.lower() in ["d", "dp", "don't pass", "don't"]:
			chipsOnTable -= lineBets["Don't Pass"]
			print("How much on the Don't Pass line?")
			lineBets["Don't Pass"] = betPrompt()
			print("Ok, ${} on the Don't Pass Line.".format(lineBets["Don't Pass"]))
			continue
		elif lBet.lower() in ['x', 'close', 'esc', 'exit', 'done']:
			print("Ok, moving on!")
			break
		else:
			print("Invalid entry, try again or type 'x' and hit Enter!")
			continue

def lineCheck(roll, p2roll):
	global lineBets, bank, chipsOnTable, pointIsOn
	if pointIsOn == False:
		if roll in [7, 11]:
			if lineBets["Pass"] > 0:
				print("You won ${} on the Pass Line!.".format(lineBets["Pass"]))
				bank += lineBets["Pass"]
				chipsOnTable -= lineBets["Pass"]
				lineBets["Pass"] = 0
			if lineBets["Don't Pass"] > 0:
				print("You lost ${} from the Don't Pass Line.".format(lineBets["Don't Pass"]))
				bank -= lineBets["Don't Pass"]
				chipsOnTable -= lineBets["Don't Pass"]
				lineBets["Don't Pass"] = 0
		elif roll in [2, 3, 12]:
			if lineBets["Pass"] > 0:
				print("You lost ${} from the Pass Line.".format(lineBets["Pass"]))
				bank -= lineBets["Pass"]
				chipsOnTable -= lineBets["Pass"]
				lineBets["Pass"] = 0
			if lineBets["Don't Pass"] > 0:
				print("You won ${} on the Don't Pass Line!".format(lineBets["Don't Pass"]))
				bank += lineBets["Don't Pass"]
				chipsOnTable -= lineBets["Don't Pass"]
				lineBets["Don't Pass"] = 0
	elif pointIsOn == True:
		if p2roll == roll:
			if lineBets["Pass"] > 0:
				print("You won ${} on the Pass Line!".format(lineBets["Pass"]))
				bank += lineBets["Pass"]
				chipsOnTable -= lineBets["Pass"]
				lineBets["Pass"] = 0
			if lineBets["Don't Pass"] > 0:
				print("You lost ${} from the Don't Pass Line.".format(lineBets["Don't Pass"]))
				bank -= lineBets["Don't Pass"]
				chipsOnTable -= lineBets["Don't Pass"]
				lineBets["Don't Pass"] = 0
			oddsCheck(p2roll)
		elif p2roll == 7:
			if lineBets["Pass"] > 0:
				print("You lost ${} from the Pass Line.".format(lineBets["Pass"]))
				bank -= lineBets["Pass"]
				chipsOnTable -= lineBets["Pass"]
				lineBets["Pass"] = 0
			if lineBets["Don't Pass"] > 0:
				print("You won ${} on the Don't Pass Line!".format(lineBets["Don't Pass"]))
				bank += lineBets["Don't Pass"]
				chipsOnTable -= lineBets["Don't Pass"]
				lineBets["Don't Pass"] = 0
			oddsCheck(p2roll)

def dpPhase2():
	global lineBets, chipsOnTable
	print("Take down Don't Pass Bet?")
	while True:
		try:
			takeDown = input(">")
			break
		except ValueError:
			print("Invalid entry, try again!")
			continue
	if takeDown.lower() in ['y', 'yes']:
		print("Ok, taking down your Don't Pass.")
		chipsOnTable -= lineBets["Don't Pass"] + lineBets["Don't Pass Odds"]
		lineBets["Don't Pass"] = lineBets["Don't Pass Odds"] =  0
	elif takeDown.lower() in ['n', 'no']:
		print("Ok leaving your Don't Pass bets up.")
	else:
		pass

# Odds Betting

def odds():
	global lineBets, chipsOnTable
	pOddsChange = dpOddsChange = 0
	if lineBets["Pass"] > 0:
		chipsOnTable -= lineBets["Pass Odds"]
		print("How Much for your Pass Line Odds?")
		pOddsChange = betPrompt()
		if pOddsChange > 0:
			lineBets["Pass Odds"] = pOddsChange
			print("Ok, ${} on your Pass Line Odds.".format(lineBets["Pass Odds"]))
		elif lineBets["Pass Odds"] > 0 and pOddsChange == 0:
			print("Ok, taking down your Pass Line Odds.")
			lineBet["Pass Odds"] = pOddsChange
		else:
			print("No change to your Pass Line Odds.")

	if lineBets["Don't Pass"] > 0:
		chipsOnTable -= lineBets["Don't Pass Odds"]
		print("How much to Lay for your Odds?")
		dpOddsChange = betPrompt()
		if dpOddsChange > 0:
			lineBets["Don't Pass Odds"] = dpOddsChange
			print("Ok, ${} laid against the Point.".format(lineBets["Don't Pass Odds"]))
		elif lineBets["Don't Pass Odds"] > 0 and dpOddsChange == 0:
			print("Ok, taking down your Don't Pass Odds.")
			lineBets["Don't Pass Odds"] = dpOddsChange
		else:
			print("Leaving your Don't Pass Odds as is.")

def oddsCheck(roll):
	global bank, chipsOnTable, lineBets, comeOut
	payout = 0
	if lineBets["Pass Odds"] > 0 and roll != 7:
		if roll in [4, 10]:
			payout = lineBets["Pass Odds"] * 2
		elif roll in [5, 9]:
			payout += (lineBets["Pass Odds"]//2) * 3
		elif roll in [6, 8]:
			payout += (lineBets["Pass Odds"]//5) * 6
		print("You won ${} from your Pass Line Odds!".format(payout))
		bank += payout
		chipsOnTable -= lineBets["Pass Odds"]
		lineBets["Pass Odds"] = 0
	elif lineBets["Pass Odds"] > 0 and roll == 7:
		print("You lost ${} from your Pass Line Odds.".format(lineBets["Pass Odds"]))
		bank -= lineBets["Pass Odds"]
		chipsOnTable -= lineBets["Pass Odds"]
		lineBets["Pass Odds"] = 0
	if lineBets["Don't Pass Odds"] > 0 and roll == 7:
		if comeOut in [4, 10]:
			payout += lineBets["Don't Pass Odds"]//2
		elif comeOut in [5, 9]:
			payout += (lineBets["Don't Pass Odds"]//3) * 2
		elif comeOut in [6, 8]:
			payout += (lineBets["Don't Pass Odds"]//6) * 5
		print("You won ${} on your Don't Pass Odds!".format(payout))
		bank += payout
		chipsOnTable -= lineBets["Don't Pass Odds"]
		lineBets["Don't Pass Odds"] = 0
	elif lineBets["Don't Pass Odds"] > 0 and roll == comeOut:
		print("You lost ${} from your Don't Pass Odds.".format(lineBets["Don't Pass Odds"]))
		bank -= lineBets["Don't Pass Odds"]
		chipsOnTable -= lineBets["Don't Pass Odds"]
		lineBets["Don't Pass Odds"] = 0

# Come Betting

comeBets = {
4: 0,
5: 0,
6: 0,
8: 0,
9: 0,
10: 0
}

comeOdds = {
4: 0,
5: 0,
6: 0,
8: 0,
9: 0,
10: 0
}

dComeBets = {
4: 0,
5: 0,
6: 0,
8: 0,
9: 0,
10: 0
}

dComeOdds = {
4: 0,
5: 0,
6: 0,
8: 0,
9: 0,
10: 0
}

comeBet = 0
dComeBet = 0

def come():
	global comeBet, dComeBet
	print("Come or Don't Come?")
	choice = input(">")
	if choice.lower() in ['c', 'come']:
		print("How much on the Come?")
		comeBet = betPrompt()
		print("Ok, ${} on the Come.".format(comeBet))
	elif choice.lower() in ["dc", "d", "don't", "don't come", "dontcome"]:
		print("How much on the Don't Com?")
		dComeBet = betPrompt()
		print("Ok, ${} on the Don't Come.".format(dComeBet))

def comeShow():
	global comeBets, dComeBets, comeOdds, dComeOdds
	for key in comeBets:
		if comeBets[key] > 0:
			print("You have ${bet} on the Come {num} with ${odds} in Odds.".format(bet=comeBets[key], num=key, odds=comeOdds[key]))
	for key in dComeBets:
		if dComeBets[key] > 0:
			print("You have ${bet} on the Don't Come {num} with ${odds} in odds.".format(bet=dComeBets[key], num=key, odds=dComeOdds[key]))

def comeOddsChange():
	global comeBets, dComeBets, comeOdds, dComeOdds, chipsOnTable
	cO = dCO = 0
	for value in comeBets.values():
		cO += value
	for value in dComeBets.values():
		dCO += value
	if cO > 0:
		print("Change your Come Odds?")
		changeCome = input(">")
		if changeCome.lower() in ['y', 'yes']:
			cdcOddsChange(comeBets, comeOdds)
	if dCO > 0:
		print("Change your Don't Come odds?")
		while True:
			try:
				changeDCO = input(">")
				break
			except ValueError:
				pass
		if changeDCO.lower() in ['y', 'yes']:
			cdcOddsChange(dComeBets, dComeOdds)

def cdcOddsChange(dict, dict2):
	global chipsOnTable
	for key in dict:
		if dict[key] > 0:
			print("How much for Odds on the {}?".format(key))
			while True:
				try:
					bet = int(input("$>"))
					if bet > bank - chipsOnTable:
						print("You don't have enough money to make that bet! Try again.")
						outOfMoney()
						print("Change your Odds?")
						continue
					break
				except ValueError:
					bet = dict[key]
					break
			if bet > 0:
				chipsOnTable -= dict2[key]
				print("Ok, you have ${bet} Odds for your {num}.".format(bet=bet, num=key))
				dict2[key] = bet
				chipsOnTable += bet
			elif dict2[key] > 0 and bet == 0:
				print("Ok, taking down your Odds.")
				chipsOnTable -= dict2[key]
				dict2[key] = bet


def comeCheck(roll):
	global comeBet, comeBets, dComeBet, dComeBets, bank, chipsOnTable, comeOdds, dComeOdds, pointIsOn
	comePay(roll)
	if comeBet > 0:
		if roll in [7, 11]:
			print("You won ${} on the Come!".format(comeBet))
			bank += comeBet
			chipsOnTable -= comeBet
			comeBet = 0
		elif roll in [2, 3, 12]:
			print("You lost ${} from the Come Bet.".format(comeBet))
			bank -= comeBet
			chipsOnTable -= comeBet
			comeBet = 0
		else:
			print("Moving your Come Bet to the {}.".format(roll))
			comeBets[roll] = comeBet
			comeBet = 0
			print("Odds on your Come Bet?")
			oddChoice = input(">")
			if oddChoice.lower() in ['y', 'yes']:
				print("How much on the Come {}?".format(roll))
				comeOdds[roll] = betPrompt()
				print("Ok, ${oBet} on your Come {num} odds.".format(oBet=comeOdds[roll], num=roll))
	elif dComeBet > 0:
		if roll in [7, 11]:
			print("You lost ${} from the Don't Come.".format(dComeBet))
			bank -= dComeBet
			chipsOnTable -= dComeBet
			dComeBet = 0
		elif roll in [2, 3, 12]:
			print("You won ${} on the Don't Come!".format(dComeBet))
			bank += dComeBet
			chipsOnTable -= dComeBet
			dComeBet = 0
		else:
			print("Moving your Don't Come bet to the {}.".format(roll))
			dComeBets[roll] = dComeBet
			dComeBet = 0
			print("Lay odds on your Don't Come {}?".format(roll))
			dcOdds = input(">")
			if dcOdds.lower() in ['y', 'yes']:
				print("How much to lay for your Don't Come Odds?")
				dComeOdds[roll] = betPrompt()
				print("Ok, ${bet} laid on the Don't Come {num}.".format(bet=dComeOdds[roll], num=roll))

def comePay(roll):
	global bank, chipsOnTable, comeBets, dComeBets, comeOdds, dComeOdds, pointIsOn
	if roll == 7:
		loss = lossOdds = 0
		for key in comeBets:
			loss += comeBets[key]
		for key in comeOdds:
			lossOdds += comeOdds[key]
		if loss > 0:
			print("You lost ${} from your Come Bets.".format(loss))
			if lossOdds > 0 and pointIsOn == True:
				print("You lost ${} from your Come Bet Odds.".format(lossOdds))
			elif lossOdds > 0 and pointIsOn == False:
				print("${odds} returned to you from Come Odds.".format(odds=lossOdds))
			bank -= loss + lossOdds
			chipsOnTable -= loss + lossOdds
			for key in comeBets:
				comeBets[key] = 0
			for key in comeOdds:
				comeOdds[key] = 0
		win = winOdds = 0
		for key in dComeBets:
			win += dComeBets[key]
			chipsOnTable -= dComeBets[key]
		for key in dComeOdds:
			if dComeOdds[key] > 0:
				chipsOnTable -= dComeOdds[key]
				if key in [4, 10]:
					winOdds += dComeOdds[key]//2
				elif key in [5, 9]:
					winOdds += dComeOdds[key]//3*2
				elif key in [6, 8]:
					winOdds += dComeOdds[key]//6*5
		if win > 0:
			print("You won ${} from your Don't Come Bets!".format(win))
			if winOdds > 0:
				print("You won ${} from your Don't Come Bet Odds!".format(winOdds))
			bank += win + winOdds
		for key in dComeBets:
			dComeBets[key] = 0
		for key in dComeOdds:
			dComeOdds[key] = 0
	if roll in [4, 5, 6, 8, 9, 10]:
		if comeBets[roll] > 0:
			print("You won ${win} on the Come {num}!".format(win=comeBets[roll], num=roll))
			bank += comeBets[roll]
			chipsOnTable -= comeBets[roll]
			comeBets[roll] = 0
			if comeOdds[roll] > 0:
				cOddsWin = 0
				if roll in [4, 10]:
					cOddsWin = comeOdds[roll] * 2
				elif roll in [5, 9]:
					cOddsWin += comeOdds[roll]//2*3
				elif roll in [6, 8]:
					cOddsWin += comeOdds[roll]//5*6
				print("You won ${oddwin} on the Come {num} Odds!".format(oddwin=cOddsWin, num=roll))
				bank += cOddsWin
				chipsOnTable -= comeOdds[roll]
				comeOdds[roll] = 0
		if dComeBets[roll] > 0:
			print("You lost ${dcloss} from the Don't Come {num}.".format(dcloss=dComeBets[roll], num=roll))
			bank -= dComeBets[roll]
			chipsOnTable -= dComeBets[roll]
			dComeBets[roll] = 0
			if dComeOdds[roll] > 0:
				print("You lost ${dco} from the Don't Come {num} Odds.".format(dco=dComeOdds[roll], num=roll))
				bank -= dComeOdds[roll]
				chipsOnTable -= dComeOdds[roll]
				dComeOdds[roll] = 0


#Field Betting

fieldBet = 0

def fieldShow():
	if fieldBet > 0:
		print("You have ${} on the Field.".format(fieldBet))

def field():
	global fieldBet, chipsOnTable
	print("How much on the Field?")
	bet = betPrompt()
	if bet > 0:
		chipsOnTable -= fieldBet
		fieldBet = bet
		print("Ok, ${} on the Field.".format(fieldBet))
	elif fieldBet > 0 and bet == 0:
		chipsOnTable -= fieldBet
		print("Taking down your Field bet.")
		fieldBet = 0

def fieldTakeDown():
	global fieldBet, chipsOnTable
	chipsOnTable -= fieldBet
	fieldBet = 0
	print("Taking down your Field Bet.")

def fieldCheck(roll):
	global fieldBet, bank, chipsOnTable
	if fieldBet > 0:
		if roll in [3, 4, 9, 10, 11]:
			print("You won ${} on the FIeld!".format(fieldBet))
			bank += fieldBet
		elif roll == 2:
			print("Double in the Bubble! You win ${} on the 2!".format(fieldBet * 2))
			bank += fieldBet * 2
		elif roll == 12:
			print("Triple in the Field! You win ${} on the 12!".format(fieldBet * 3))
			bank += fieldBet * 3
		else:
			print("You lost ${} from the Field.".format(fieldBet))
			bank -= fieldBet
			chipsOnTable -= fieldBet
			fieldBet = 0

propBets = {
"Snake Eyes": 0,
"Acey Deucey": 0,
"Any Craps": 0,
"Any Seven": 0,
"C and E": 0,
"Horn": 0,
"Boxcars": 0,
"Eleven": 0,
"World": 0,
"Buffalo": 0
}


def propBetting():
	global propBets
	while True:
		print("Type in your Prop Bet:")
		bet = input(">")
		if bet.lower() in ['aces', 'snakeeyes', 'snake eyes', 2, 'a', 's', 'sn']:
			print("How much on Snake Eyes?")
			propBets["Snake Eyes"] = betPrompt()
			print("Ok, ${} on Snake Eyes.".format(propBets["Snake Eyes"]))
			continue
		elif bet.lower() in ['ad', 'acedeuce', 3, 'ace deuce', 'acey deucey']:
			print("How much on Acey Deucey?")
			propBets["Acey Deucey"] = betPrompt()
			print("Ok, ${} on Acey-Deucey.".format(propBets["Acey Deucey"]))
			continue
		elif bet.lower() in [7, 'a7', 'any 7', 'seven', 'any seven', 'big red']:
			print("How much on Any 7?")
			propBets["Any Seven"] = betPrompt()
			print("Ok, ${} on Any Seven.".format(propBets["Any Seven"]))
			continue
		elif bet.lower() in ['craps', 'anycraps', 'ac', 'any craps', 'cr']:
			print("How much on Any Craps?")
			propBets["Any Craps"] = betPrompt()
			print("Ok, ${} on Any Craps.".format(propBets["Any Craps"]))
			continue
		elif bet.lower() in ['ce', 'cande', 'c and e', 'craps and eleven']:
			print("How much on C and E?")
			propBets["C and E"] = betPrompt()
			print("Ok, ${} on C and E.".format(propBets["C and E"]))
			continue
		elif bet.lower() in ['h', 'horn', 'horn bet']:
			print("How much on the Horn Bet?")
			propBets["Horn"] = betPrompt()
			print("Ok, ${} on the Horn Bet.".format(propBets["Horn"]))
			continue
		elif bet.lower() in ['boxcars', 'b', 12, 'midnight']:
			print("How much on Boxcars?")
			propBets["Boxcars"] = betPrompt()
			print("Ok, ${} on Boxcars.".format(propBets["Boxcars"]))
			continue
		elif bet in [11, 'eleven', 'e', 'yo', 'el']:
			print("How much on Yo Eleven?")
			propBets["Eleven"] = betPrompt()
			print("Ok, ${} on Eleven.".format(propBets["Eleven"]))
			continue
		elif bet.lower() in ['show', 'all', 'show all', 'bets']:
			for key in propBets:
				if propBets[key] > 0:
					print("${bet} on {prop}.".format(bet=str(propBets[key]), prop=key))
			continue
		elif bet.lower() in ['x', 'close', 'exit', 'done']:
			break

def propPay(roll):
	global propBets, bank, chipsOnTable
	multiplier = 0
	for key in propBets:
		if propBets[key] > 0:
			if (key == "Snake Eyes" and roll == 2) or (key == "Boxcars" and roll == 12):
				multiplier = 30
			elif (key == "Acey Deucey" and roll == 3) or (key == "Eleven" and roll == 11):
				multiplier = 15
			elif key == "Any Seven" and roll == 7:
				multiplier = 4
			elif key == "Any Craps" and roll in [2, 3, 12]:
				multiplier = 7
			elif key == "C and E" and roll in [2, 3, 12]:
				multiplier = 3
			elif key == "C and E" and roll == 11:
				multiplier = 7
			elif key == "Horn" and roll in [2, 12]:
				multiplier = 30
				propBets[key] = propBets[key]//4
			elif key == "Horn" and roll in [3, 11]:
				multiplier = 15
				propBets[key] = propBets[key]//4
			else:
				multiplier = 0
			if multiplier > 0:
				print("You won ${win} on the {bet} bet!".format(win=propBets[key]*multiplier, bet=key))
				bank += propBets[key] * multiplier
				chipsOnTable -= propBets[key]

				propBets[key] = 0
			else:
				print("You lost ${loss} from the {bet}.".format(loss=propBets[key], bet=key))
				bank -= propBets[key]
				chipsOnTable -= propBets[key]
				propBets[key] = 0


#All Tall Small setup
atsAll = atsSmall = atsTall = 0
allNums = []
smallNums = []
tallNums = []
atsOn = False

def atsBetting():
	global atsAll, atsSmall, atsTall, atsOn
	atsOn = True
	print("How much on the All?")
	atsAll = betPrompt()
	print("Ok, ${} on the All.".format(atsAll))
	print("How much on the Tall?")
	atsTall = betPrompt()
	print("Ok, ${} on the Tall.".format(atsTall))
	print("How much on the Small?")
	atsSmall = betPrompt()
	print("Ok, ${} on the Small.".format(atsSmall))

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
		print("You lost ${} from the All Tall Small.".format(atsAll+atsTall+atsSmall))
		bank -= atsAll + atsTall + atsSmall
		chipsOnTable -= atsAll + atsTall + atsSmall
		atsAll = atsSmall = atsTall = 0
		allNums = []
		smallNums = []
		tallNums = []
	elif (atsAll + atsSmall + atsTall) > 0:
		allNums.sort()
		print("All Tall Small: {}".format(allNums))

	if set(smallNums) == set(smallSet):
		print("You won ${} on the Small!".format(atsSmall * 35))
		bank += atsSmall * 35
		chipsOnTable -= atsSmall
		atsSmall = 0
		smallNums = []
	if set(tallNums) == set(tallSet):
		print("You won ${} from the Tall!".format(atsTall*35))
		bank += atsTall * 35
		chipsOnTable -= atsTall
		atsTall = 0
		tallNums = []
	if set(allNums) == set(allSet):
		print("You won ${} on the All! Holy Crap!".format(atsAll*176))
		bank += atsAll * 176
		chipsOnTable -= atsAll
		atsAll = 0
		allNums = []
		atsOn = False

# Lay Bet Setup

layOff = False

layBets = {
4: 0,
5: 0,
6: 0,
8: 0,
9: 0,
10: 0
}

def layBetting():
	global layBets, chipsOnTable
	for key in layBets:
		print("You have ${bet} on the Lay {key}.".format(bet=layBets[key], key=key))
		print("How much on the Lay {}?".format(key))
		while True:
			try:
				bet = int(input("$>"))
				if bet > bank - chipsOnTable:
					print("You don't have enough money to make that bet! Try again.")
					outOfMoney()
					print("How much on the Place {}?".format(key))
					continue
				break
			except ValueError:
				bet = layBets[key]
				break
		if bet > 0:
			chipsOnTable -= layBets[key]
			layBets[key] = bet
			chipsOnTable += bet
			print("Ok, ${bet} on the Lay {num}.".format(bet=bet, num=key))
		elif layBets[key] > 0 and bet == 0:
			print("Ok, taking down your Lay {num} bet.".format(num=key))
			chipsOnTable -= layBets[key]
			layBets[key] = 0

def layTakeDown():
	global layBets, chipsOnTable
	for key in layBets:
		chipsOnTable -= layBets[key]
		layBets[key] = 0


def layShow():
	global layBets
	for key in layBets:
		if layBets[key] > 0:
			print("You have ${value} on the Lay {key}.".format(value=layBets[key], key=key))

def layCheck(roll):
	global layBets, bank, chipsOnTable
	if roll in [4, 5, 6, 8, 9, 10]:
		if layBets[roll] > 0:
			print("You lost ${loss} from the Lay {num}.".format(loss=layBets[roll], num=roll))
			bank -= layBets[roll]
			chipsOnTable -= layBets[roll]
			layBets[roll] = 0
	elif roll == 7:
		for key in layBets:
			if layBets[key] > 0:
				if key in [4, 10]:
					print("You won ${win} on the Lay {num}!".format(win=layBets[key]//2, num=key))
					bank += layBets[key]//2
				elif key in [5, 9]:
					print("You won ${win} on the Lay {num}!".format(win=layBets[key]//3*2, num=key))
					bank += layBets[key]//3*2
				elif key in [6, 8]:
					print("You won ${win} on the Lay {num}!".format(win=layBets[key]//6*5, num=key))
					bank += layBets[key]//6*5
				chipsOnTable -= layBets[key]
				bank -= vig(layBets[key])
				layBets[key] = 0

# Bank and bet setup
bank = 0
chipsOnTable = 0

def cashIn():
	global bank
	print("How much are you cashing in for your bankroll?")
	while True:
		try:
			cash = int(input("$>"))
		except ValueError:
			print("That wasn't a number, doofus!")
			continue
		if cash <= 0:
			print("You won't get very far trying to play without any money, come on now...")
			continue
		else:
			bank += cash
			break
	print("Great, starting you off with ${}.".format(bank))

def betPrompt():
	global bank, chipsOnTable
	while True:
		try:
			playerBet =  int(input("$>"))
		except ValueError:
			print("That wasn't a number!")
			continue
		if playerBet > bank - chipsOnTable:
			print("You simply don't have enough money to do that! DO you want to add more to your bankroll?")
			addMore = input(">")
			if addMore.lower() in ['y', 'yes', 'atm', 'help', 'more money']:
				outOfMoney()
			continue
		else:
			chipsOnTable += playerBet
			return playerBet

def outOfMoney():
	global bank
	if bank <= 0:
		print("\tYou are totally out of money. Let's hit the ATM again and get you more cash. How much do you want?")
	else:
		print("Your chips are getting really low. How much would you like to add to your bankroll?")
	while True:
		try:
			cash = int(input("\t$>"))
		except ValueError:
			print("\tYou forgot what numbers were and the ATM beeps at you in annoyance. Try again.")
			continue
		if cash <= 0:
			print("What am I, a bank? This is for withdrawals only! Try again.")
			continue
		else:
			bank += cash
			break
	print("\tAlright, starting you off again with ${}. Don't lose it all this time!".format(bank))

#Place Betting

place = {
4: 0,
5: 0,
6: 0,
8: 0,
9: 0,
10: 0
}

placeOff = False

def placePreset(pre):
	global chipsOnTable, bank, pointIsOn, place, comeOut
	total = 0
	if pre.lower() in ['a', 'across', 'acr']:
		while True:
			print("How many units across the Place Numbers?")
			unit = int(input("> "))
			if (unit*5*4) + (unit*6*2) > bank:
				print("You don't have enough money for that! Egads!")
				outOfMoney()
				continue
			else:
				break
		if pointIsOn:
			print("Include the Point?")
			try:
				point = input("> ")
			except ValueError:
				pass
		for key in place:
			chipsOnTable -= place[key]
			if key in [4, 5, 9, 10]:
				place[key] = 5 * unit
			elif key in [6, 8]:
				place[key] = 6 * unit
			if pointIsOn and point not in ['y', 'yes']:
				if key == comeOut:
					place[key] = 0
			chipsOnTable += place[key]
			total += place[key]
		print("Placing ${} Across.".format(total))
	elif pre.lower() in ['i', 'inside']:
		print("How many units Inside?")
		unit = int(input("> "))
		for key in place:
			chipsOnTable -= place[key]
			if key in [5, 9]:
				place[key] = 5 * unit
			elif key in [6, 8]:
				place[key] = 6 * unit
			else:
				place[key] = 0
			chipsOnTable += place[key]
			total += place[key]
		print("Placing ${} Inside.".format(total))

def placeMover():
	global place, chipsOnTable, comeOut
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
			print("Moving your ${original} Place {num1} bet. You now have ${new} on the {num2}.".format(original=place[comeOut], num1=comeOut, new=place[key], num2=key))
			chipsOnTable -= place[comeOut]
			chipsOnTable += place[key]
			place[comeOut] = 0


def placeBets():
	global place, chipsOnTable
	for key in place:
		print("You have ${bet} on the Place {key}.".format(bet=place[key], key=key))
		print("How much on the Place {}?".format(key))
		while True:
			try:
				bet = int(input("$>"))
				if bet > bank - chipsOnTable:
					print("You don't have enough money to make that bet! Try again.")
					outOfMoney()
					print("How much on the Place {}?".format(key))
					continue
				break
			except ValueError:
				bet = place[key]
				break
		if bet > 0:
			chipsOnTable -= place[key]
			place[key] = bet
			chipsOnTable += bet
			if key in [4, 10] and bet >= 10:
				print("Buying the {num} for ${bet}.".format(bet=bet, num=key))
			else:
				print("${bet} on the Place {num}.".format(bet=bet, num=key))
		elif place[key] > 0 and bet == 0:
			print("Ok, taking down your Place {num} bet.".format(num=key))
			chipsOnTable -= place[key]
			place[key] = 0

def placeShow():
	global place
	for key in place:
		if place[key] > 0:
			print("You have ${value} on the Place {key}.".format(value=place[key], key=key))

def placeTakeDown():
	global place, chipsOnTable
	for key in place:
		chipsOnTable -= place[key]
		place[key] = 0


def vig(bet):
	total = bet * 0.05
	if bet < 25:
		commission = math.ceil(total)
	else:
		commission = math.floor(total)
	print("${vig} paid to the House for the vig.".format(vig=commission))
	return commission

def placeCheck(roll):
	global place, bank, chipsOnTable
	if roll in [4, 5, 6, 8, 9, 10]:
		if place[roll] > 0:
			win = 0
			if roll in [4, 10] and place[roll] >= 10:
				win = place[roll] * 2 - vig(place[roll])
			elif roll in [4, 10]:
				win = (place[roll]//5) * 9
			elif roll in [5, 9]:
				win = (place[roll]//5) * 7
			elif roll in [6, 8]:
				win = (place[roll]//6) * 7
			bank += win
			print("You won ${win} on the Place {num}!".format(win=win, num=roll))
			print("Change your bet?")
			change = input(">")
			if change.lower() in ['y', 'yes']:
				print("How much on the Place {}?".format(roll))
				bet = betPrompt()
				if bet == 0:
					chipsOnTable -= place[roll]
					place[roll] = bet
					print("Ok, taking down your Place {} bet.".format(roll))
				else:
					chipsOnTable -= place[roll]
					place[roll] = bet
					print("Ok, ${bet} on the Place {num}.".format(bet=place[roll], num=roll))
	elif roll == 7:
		loss = 0
		for key in place:
			loss += place[key]
			place[key] = 0
		bank -= loss
		chipsOnTable -= loss
		if loss > 0:
			print("You lost ${} from the Place bets.".format(loss))
	else:
		pass

#Additional Global Variables
p2 = 0
pointIsOn = False
working = False
throws = 0

# Game Start
print("Oh Craps! v.5.4\nBy: Marco Salsiccia")
cashIn()
while True:
	if chipsOnTable <= 0:
		print("You have ${} in the bank.".format(bank))
	else:
		print("You have ${bank} in the bank with ${table} out on the table.".format(bank=bank, table=chipsOnTable))
	if bank <= 0:
		outOfMoney()
	print("Rolls: {}\n".format(throws))

# Initial bets
	lbet = input("Line Bets? >")
	if lbet in ['y', 'yes']:
		lineBetting()

	placeShow()
	print("Place Bets?")
	plBet = input(">")
	if plBet in ['y', 'Yes']:
		placeBets()
	elif plBet.lower() in ['d', 'td', 'takedown']:
		print("Taking down your Place Bets.")
		placeTakeDown()
	elif plBet.lower() in ['a', 'i']:
		placePreset(plBet)

	print("Lay Bets?")
	lyBet = input(">")
	if lyBet.lower() in ['y', 'yes']:
		layBetting()
	elif lyBet.lower() in ['d', 'td', 'takedown']:
		print("Taking down your Lay Bets.")
		layTakeDown()

	fieldShow()
	print("Field Bet?")
	fBet = input(">")
	if fBet.lower() in ['y', 'yes']:
		field()
	elif fBet.lower() in ['d', 'td', 'takedown']:
		fieldTakeDown()

	hardShow()
	print("Hard Ways Bets?")
	hWays = input(">")
	if hWays.lower() in ['y', 'yes']:
		hardWaysBetting()
	elif hWays.lower() in ['d', 'td', 'takedown']:
		hardTakeDown()

# Working Bets Setup
	plCheck = hCheck = lCheck = 0
	for value in place.values():
		plCheck += value
	for value in hardWays.values():
		hCheck += value
	for value in layBets.values():
		lCheck += value

	if plCheck > 0 or hCheck > 0 or lCheck > 0:
		print("All Bets Working?")
		work = input(">")
		if work.lower() in ['y', 'yes']:
			working = True
			print("Ok, all bets are working.")

	print("Prop Bets?")
	prBet = input(">")
	if prBet.lower() in ['y', 'yes']:
		propBetting()

	if atsOn == True:
		print("All Tall Small: {}".format(allNums))
	elif throws == 0:
		print("All Tall Small?")
		atsChoice = input(">")
		if atsChoice.lower() in ['y', 'yes']:
			atsBetting()

# Fire Bet
	if fireBet == 0:
		print("Fire Bet?")
		fireChoice = input("> ")
		if fireChoice.lower() in ['y', 'yes']:
			fireBetting()
	else:
		print("You have ${bet} on the Fire Bet; Numbers Hit: {fire}.".format(bet=fireBet, fire=fire))

#Coming Out Roll
	input("Hit Enter to roll!")

	comeOut  = roll()
	throws += 1
	comeCheck(comeOut)
	if working == True:
		placeCheck(comeOut)
		layCheck(comeOut)
		hardCheck(comeOut)
	fieldCheck(comeOut)
	propPay(comeOut)
	if atsOn == True:
		ats(comeOut)

	if comeOut in [7, 11]:
		if comeOut == 7:
			throws = 0
		lineCheck(comeOut, p2)
		working = False
		continue
	elif comeOut in [2, 3, 12]:
		lineCheck(comeOut, p2)
		working = False
		continue
	else:
		pointIsOn = True
		working = False
		while True:
			if chipsOnTable > 0:
				print("You have ${bank} in the bank with ${table} out on the table.".format(bank=bank, table=chipsOnTable))
			else:
				print("You have ${bank} in the bank.".format(bank=bank))

			if bank <= 0:
				outOfMoney()
			print("{} is the Point!".format(comeOut))
			print("Rolls: {}".format(throws))
#Phase 2 Betting
			if lineBets["Pass"] > 0 or lineBets["Don't Pass"] > 0:
				if lineBets["Pass Odds"] > 0:
					print("You have ${} on your Pass Line Odds.".format(lineBets["Pass Odds"]))
				if lineBets["Don't Pass Odds"] > 0:
					print("You have ${} on your Don't Pass Odds.".format(lineBets["Don't Pass Odds"]))
				print("Line Bet Odds?")
				oddsPrompt = input(">")
				if oddsPrompt.lower() in ['y', 'yes']:
					odds()

			if lineBets["Don't Pass"] > 0:
				dpPhase2()

			comeShow()
			print("Come Bet?")
			cChoice = input(">")
			if cChoice.lower() in ['y', 'yes']:
				come()
			comeOddsChange()

			placeShow()
			print("Place Bets?")
			pl2 = input(">")
			if pl2.lower() in ['y', 'yes']:
				placeBets()
			elif pl2.lower() in ['o', 'off']:
				placeOff = True
				print("All your Place Bets are Off.")
			elif pl2.lower() in ['d', 'td', 'takedown', 'take down']:
				print("Taking down all of your Place Bets.")
				placeTakeDown()
			elif pl2.lower() in ['a', 'i']:
				placePreset(pl2)
			elif pl2.lower() in ['m', 'move']:
				placeMover()
			elif pl2.lower() in ['p', 'point']:
				chipsOnTable -= place[comeOut]
				place[comeOut] = 0
				print("Taking down the Place {} bet.".format(comeOut))

			layShow()
			print("Lay Bets?")
			ly2Bet = input(">")
			if ly2Bet.lower() in ['y', 'yes']:
				layBetting()
			elif ly2Bet.lower() in ['o', 'off']:
				layOff = True
				print("Your Lay Bets are Off.")
			elif ly2Bet.lower() in ['d', 'td', 'takedown']:
				print("Taking down all of your Lay Bets.")
				layTakeDown()


			fieldShow()
			print("FIeld Bet?")
			fb2 = input(">")
			if fb2.lower() in ['y', 'yes']:
				field()
			elif fb2.lower() in ['d', 'td', 'takedown']:
				fieldTakeDown()

			hardShow()
			print("Hard Ways bets?")
			hard2 = input(">")
			if hard2.lower() in ['y', 'yes']:
				hardWaysBetting()
			elif hard2.lower() in ['o', 'off']:
				hardOff = True
				print("Your Hard Ways are Off.")
			elif hard2.lower() in ['d', 'td', 'takedown']:
				hardTakeDown()

			print("Prop Bets?")
			pr2Bet = input(">")
			if pr2Bet.lower() in ['y', 'yes']:
				propBetting()
# phase 2 roll
			input("Hit Enter to Roll!")

			p2 = roll()

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

			if p2 == 7:
				throws = 0
				pointIsOn = False
				break
			elif p2 == comeOut:
				print("Point Hit! Front line winner!")
				pointIsOn = False
				break
			else:
				continue

	continue
