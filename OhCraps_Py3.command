#!/usr/bin/env python3

from random import *
import math
import os

#Version Number
version = "6.2.6"

#Roll and Dice Setup
die1 = 0
die2 = 0

def roll():
	global rollHard, pointIsOn, die1, die2
	rollHard = False
	d1 = randrange(1, 7)
	d2 = randrange(1, 7)
	if d1 > d2 or d1 == d2:
		die1 = d1
		die2 = d2
	else:
		die1 = d2
		die2 = d1

	total = die1 + die2
	if die1 == die2 and total in [4, 6, 8, 10]:
		rollHard = True
		print("\n{} the Hard Way!\n".format(total))
		print("\n" + stickman(total))
	elif total in [7, 11] and pointIsOn == False:
		print("\n{total} winner! Pay the line, take the don't!\n".format(total=total))
	else:
		call = randrange(1, 21)

# Call picks a random number between 1 and 20. If the number is 10 or below, it triggers one of the random dealer calls based on the roll. Otherwise it calls out a standard dice call.

		if call <=10 or total in [2, 3, 11, 12]:
			print("\n{tot}, {call}!\n".format(tot=total, call=stickman(total)))
		else:
			print("\n{tot}, a {d1} {d2} {tot}!\n".format(tot=total, d1=die1, d2=die2))
	return total

dealerCalls = {
2: ["Craps!", "eye balls.", "two aces.", "rats eyes.", "snake eyes.", "eleven in a shoe store.", "twice in the rice.", "two craps two, two bad boys from Illinois.", "two crap aces.", "aces in both places.", "a spot and a dot.", "dimples.", "double the Field!"],
3: ["Craps!", "ace-deuce.", "three craps, ace caught a deuce, no use.", "divorce roll, come up single.", "winner on the dark side!", "three craps three, the indicator.", "crap and a half.", "small ace deuce, can't produce.", "2 , 1, son of a gun."],
4: ["Little Joe.", "Little Joe from Kokomo.", "Ace Tres.", "Ace Tres the easy way.", "Little Billy from Piccadilly.", "Little Joe from Idaho."],
5: ["After 5 the Field's alive.", "Fiver Fiver Racecar Driver.", "No Field 5.", "Little Phoebe.", "We got the fiver.", "Five 5.", "Take a dive!"],
6: ["The national average.", "Catch 'em in the corner.", "Sixie from Dixie."],
7: ["Line Away, grab the money!", "the bruiser.", "point 7.", "Out!", "Loser 7.", "Nevada Breakfast, two rolls and no coffee.", "Cinco Dos, Adios!", "Adios.", "3 4 on the floor.", "Big Red!"],
8: ["eighter from the theater.", "the Great!", "get yer mate."],
9: ["niner 9.", "center field 9.", "Center of the garden.", "ocean liner niner.", "Nina from Pasadena.", "nina Niner, wine and dine her!", "El Nine-O.", "Niner, nothing finer.", "Neener Neener from Pasadeener."],
10: ["The big one on the end!", "64 out the door.", "The Big One!"],
11: ["Yo Eleven.", "Yo!", "6 5, no drive.", "yo 'leven.", "It's not my eleven, it's Yo Eleven.", "Bow wow wow yippie Yo yippie yay!"],
12: ["craps!", "midnight.", "a whole lotta crap!", "craps to the max.", "boxcars.", "all the spots we gots!", "triple field!", "atomic craps.", "Hobo's delight."]
}

hardCalls = {
4: ["Double deuce.", "2 2 Ballerina Special.", "Hit us in the tutu.", "2 spots and 2 dots.", "It's little but it came Hard!"],
6: ["Sixie from Dixie.", "tree tre.", "Pair of trees.", "Double 3s"],
8: ["Double 4s", "Ozzy and Harriet.", "A square pair!", "A square pair will take ya there.", "Pair of windows.", "Windows."],
10: ["Pair of sunflowers.", "Two stars from Mars.", "Double 5s", "A Hard 10 to please 'er.", "Girl's best friend.", "Puppy paws.", "55 to stay alive.",  "Pair of roses."]
}

def stickman(roll):
	global rollHard
	if rollHard:
		return hardCalls[roll][randrange(0, len(hardCalls[roll]))]
	else:
		return dealerCalls[roll][randrange(0, len(dealerCalls[roll]))]

# Fire Bet Setup

fire = []
fireBet = 0

def fireBetting():
	global fireBet
	print("\tHow much on the Fire Bet?")
	fireBet = betPrompt()
	print("\tOk, ${} on the Fire Bet. Good Luck!".format(fireBet))

def fireCheck():
	global bank, fire, fireBet, comeOut, p2, chipsOnTable
	if p2 == 7:
		chipsOnTable -= fireBet
		if len(fire) < 4:
			print("You lost ${} from the Fire Bet.".format(fireBet))
			#bank -= fireBet
			fireBet = 0
			fire = []
		elif len(fire) == 4:
			print("You won ${} on the Fire Bet! Great job!".format(fireBet * 25))
			bank += fireBet * 25
			fireBet = 0
			fire = []
		elif len(fire) == 5:
			print("You won ${} on the Fire Bet! Holy Crap!".format(fireBet * 250))
			bank += fireBet * 250
			fireBet = 0
			fire = []
		elif len(fire) == 6:
			print("Wowsers! You nailed the Fire Bet Jackpot and won ${}!!!".format(fireBet * 1000))
			bank += fireBet * 1000
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
	global hardWays, bank, chipsOnTable
	madeBet = True
	for key in hardWays:
		if hardWays[key] > 0:
			print("You have ${bet} on the hard {num}.".format(bet=hardWays[key], num=key))
		print("How much on the Hard {}?".format(key))
		while True:
			bet = 0
			try:
				bet = int(input("$>"))
				if bet > bank + chipsOnTable:
					print("You don't have enough money to make that bet! Try again.")
					outOfMoney()
					print("How much on the Hard {}?".format(key))
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
			print("${bet} on the Hard {num}.".format(bet=bet, num=key))
		elif hardWays[key] > 0 and bet == 0:
			print("Ok, taking down your Hard {num} bet.".format(num=key))
			chipsOnTable -= hardWays[key]
			bank += place[key]
			hardWays[key] = 0


"""
		bet = betPrompt()
		if bet > 0:
			bank += hardWays[key]
			chipsOnTable -= hardWays[key]
			hardWays[key] = bet
			print("Ok, ${bet} on the Hard {num}.".format(bet=hardWays[key], num=key))
		elif hardWays[key] > 0 and bet == 0:
			print("Taking down your Hard {}.".format(key))
			chipsOnTable -= hardWays[key]
			bank += hardWays[key]
			hardWays[key] = bet
"""
def hardTakeDown():
	global hardWays, bank, chipsOnTable
	print("Taking down your Hard Ways.")
	for key in hardWays:
		chipsOnTable -= hardWays[key]
		bank += hardWays[key]
		hardWays[key] = 0

def hardAuto():
	global chipsOnTable, bank, hardWays
	print("How many $1 units on each of the Hard Ways?")
	hardAcr = betPrompt()
	chipsOnTable -= hardAcr
	bank += hardAcr
	for key in hardWays:
		chipsOnTable -= hardWays[key]
		bank += hardWays[key]
		hardWays[key] = hardAcr
		chipsOnTable += hardAcr
		bank -= hardAcr
	print("Ok, ${} on each of the Hard Ways.".format(hardAcr))

def hardHigh(num):
	global chipsOnTable, bank, hardWays
	number = int(num[1:])
	print("How much to spread across the Hard Ways, high on the {}?".format(number))
	bet = betPrompt()
	#chipsOnTable -= bet
	for key in hardWays:
		chipsOnTable -= hardWays[key]
		bank += hardWays[key]
		if key == number:
			hardWays[key] = bet - (bet//5*3)
		else:
			hardWays[key] = bet//5
	print("Ok, ${a} on the Hard {number}, ${b} each on the other Hard Ways for a total of ${bet}.".format(a=(bet-(bet//5*3)), b=(bet//5), number=number, bet=bet))


"""
algorithm for spreading weird bets across with a high number:
bet - (bet//5 * 3) = high bet
bet//5 = low bets

"""

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
			#bank -= loss
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
				#bank += hardWays[roll]
				hardWays[roll] = betPrompt()
				if hardWays[roll] == 0:
					print("Ok, taking down your Hard {} bet.".format(roll))
				else:
					print("Ok, bumping up your Hard {num} bet to ${bet}.".format(num=roll, bet=hardWays[roll]))
			else:
				pass
		elif hardWays[roll] > 0 and rollHard == False:
			print("You lost ${loss} from the Hard {num}.".format(loss=hardWays[roll], num=roll))
			#bank -= hardWays[roll]
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
	global lineBets, bank, chipsOnTable
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
			bank += lineBets["Pass"]
			print("How much on the Pass Line?")
			lineBets["Pass"] = betPrompt()
			print("Ok, ${} on the Pass Line.".format(lineBets["Pass"]))
			continue
		elif lBet.lower() in ["d", "dp", "don't pass", "don't"]:
			chipsOnTable -= lineBets["Don't Pass"]
			bank += lineBets["Don't Pass"]
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
				bank += lineBets["Pass"] * 2
				chipsOnTable -= lineBets["Pass"]
				lineBets["Pass"] = 0
			if lineBets["Don't Pass"] > 0:
				print("You lost ${} from the Don't Pass Line.".format(lineBets["Don't Pass"]))
				#bank -= lineBets["Don't Pass"]
				chipsOnTable -= lineBets["Don't Pass"]
				lineBets["Don't Pass"] = 0
		elif roll in [2, 3, 12]:
			if lineBets["Pass"] > 0:
				print("You lost ${} from the Pass Line.".format(lineBets["Pass"]))
				#bank -= lineBets["Pass"]
				chipsOnTable -= lineBets["Pass"]
				lineBets["Pass"] = 0
			if lineBets["Don't Pass"] > 0:
				if roll in [2, 3]:
					print("You won ${} on the Don't Pass Line!".format(lineBets["Don't Pass"]))
					bank += lineBets["Don't Pass"] * 2
				elif roll == 12:
					print("12 is a Push!")
					bank += lineBets["Don't Pass"]
				chipsOnTable -= lineBets["Don't Pass"]
				lineBets["Don't Pass"] = 0
	elif pointIsOn == True:
		if p2roll == roll:
			if lineBets["Pass"] > 0:
				print("You won ${} on the Pass Line!".format(lineBets["Pass"]))
				bank += lineBets["Pass"] * 2
				chipsOnTable -= lineBets["Pass"]
				lineBets["Pass"] = 0
			if lineBets["Don't Pass"] > 0:
				print("You lost ${} from the Don't Pass Line.".format(lineBets["Don't Pass"]))
				#bank -= lineBets["Don't Pass"]
				chipsOnTable -= lineBets["Don't Pass"]
				lineBets["Don't Pass"] = 0
			oddsCheck(p2roll)
		elif p2roll == 7:
			if lineBets["Pass"] > 0:
				print("You lost ${} from the Pass Line.".format(lineBets["Pass"]))
				#bank -= lineBets["Pass"]
				chipsOnTable -= lineBets["Pass"]
				lineBets["Pass"] = 0
			if lineBets["Don't Pass"] > 0:
				print("You won ${} on the Don't Pass Line!".format(lineBets["Don't Pass"]))
				bank += lineBets["Don't Pass"] * 2
				chipsOnTable -= lineBets["Don't Pass"]
				lineBets["Don't Pass"] = 0
			oddsCheck(p2roll)

def dpPhase2():
	global lineBets, bank, chipsOnTable
	print("Take down Don't Pass Bet and Odds?")
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
		bank += lineBets["Don't Pass"] + lineBets["Don't Pass Odds"]
		lineBets["Don't Pass"] = lineBets["Don't Pass Odds"] =  0
	elif takeDown.lower() in ['n', 'no']:
		print("Ok leaving your Don't Pass bets up.")
	else:
		pass

# Odds Betting

def odds():
	global lineBets, bank, chipsOnTable, comeOut
	pOddsChange = dpOddsChange = 0
	if comeOut in [4, 10]:
		maxOdds = lineBets["Pass"] * 3
	elif comeOut in [5, 9]:
		maxOdds = lineBets["Pass"] * 4
	elif comeOut in [6, 8]:
		maxOdds = lineBets["Pass"] * 5
	maxDP = lineBets["Don't Pass"] * 10
	if lineBets["Pass"] > 0:
		print("You have ${} for your odds.".format(lineBets["Pass Odds"]))
		while True:
			chipsOnTable -= lineBets["Pass Odds"]
			bank += lineBets["Pass Odds"]
			print("How Much for your Pass Line Odds? Max Odds for the {num} is ${max}.".format(num=comeOut, max=maxOdds))
			pOddsChange = betPrompt()
			if pOddsChange > 0 and pOddsChange <= maxOdds:
				lineBets["Pass Odds"] = pOddsChange
				print("Ok, ${} on your Pass Line Odds.".format(lineBets["Pass Odds"]))
				break
			elif pOddsChange > maxOdds:
				print("Nope, that bet is over the Max Odds. Try again!")
				chipsOnTable -= pOddsChange
				continue
			elif lineBets["Pass Odds"] > 0 and pOddsChange == 0:
				print("Ok, taking down your Pass Line Odds.")
				lineBets["Pass Odds"] = pOddsChange
				break
			else:
				print("No change to your Pass Line Odds.")
				break

	if lineBets["Don't Pass"] > 0:
		print("You have $0 for your lay odds.".format(lineBets["Don't Pass Odds"]))
		while True:
			chipsOnTable -= lineBets["Don't Pass Odds"]
			bank += lineBets["Don't Pass Odds"]
			print("How much to Lay for your Odds? Max Odds for the {num} is ${max}.".format(num=comeOut, max=maxDP))
			dpOddsChange = betPrompt()
			if dpOddsChange > 0 and dpOddsChange <= maxDP:
				lineBets["Don't Pass Odds"] = dpOddsChange
				print("Ok, ${} laid against the Point.".format(lineBets["Don't Pass Odds"]))
				break
			elif dpOddsChange > maxDP:
				print("Nope, you laid too much! Try again.")
				chipsOnTable -= dpOddsChange
				bank -= lineBets["Don't Pass Odds"]
				continue
			elif lineBets["Don't Pass Odds"] > 0 and dpOddsChange == 0:
				print("Ok, taking down your Don't Pass Odds.")
				lineBets["Don't Pass Odds"] = dpOddsChange
				break
			else:
				print("Leaving your Don't Pass Odds as is.")
				break

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
		bank += payout + lineBets["Pass Odds"]
		chipsOnTable -= lineBets["Pass Odds"]
		lineBets["Pass Odds"] = 0
	elif lineBets["Pass Odds"] > 0 and roll == 7:
		print("You lost ${} from your Pass Line Odds.".format(lineBets["Pass Odds"]))
		#bank -= lineBets["Pass Odds"]
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
		bank += payout + lineBets["Don't Pass Odds"]
		chipsOnTable -= lineBets["Don't Pass Odds"]
		lineBets["Don't Pass Odds"] = 0
	elif lineBets["Don't Pass Odds"] > 0 and roll == comeOut:
		print("You lost ${} from your Don't Pass Odds.".format(lineBets["Don't Pass Odds"]))
		#bank -= lineBets["Don't Pass Odds"]
		chipsOnTable -= lineBets["Don't Pass Odds"]
		lineBets["Don't Pass Odds"] = 0

# Come Betting

comeBets = {
4: 0,
5: 0,
6: 0,
8: 0,
9: 0,
10: 0,
	"Come": 0
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
10: 0,
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
	global comeBet, dComeBet, chipsOnTable, bank
	while True:
		print("Come or Don't Come?")
		choice = input(">")
		if choice.lower() in ['c', 'come']:
			print("How much on the Come?")
			chipsOnTable -= comeBet
			bank += comeBet
			comeBet = betPrompt()
			print("Ok, ${} on the Come.".format(comeBet))
			break
		elif choice.lower() in ["dc", "d", "don't", "don't come", "dontcome"]:
			print("How much on the Don't Com?")
			chipsOnTable -= dComeBet
			bank += dComeBet
			dComeBet = betPrompt()
			print("Ok, ${} on the Don't Come.".format(dComeBet))
			break
		elif choice.lower() == "x":
			print("Finished betting the Come.")
			break
		else:
			print("Invalid choice, try again.")
			continue

def dComeDown():
	global dComeBets, dComeOdds, chipsOnTable, bank
	checkVal = 0
	for bet in dComeBets:
		checkVal += dComeBets[bet]
		if dComeBets[bet] > 0:
			chipsOnTable -= dComeBets[bet] + dComeOdds[bet]
			bank += dComeBets[bet] + dComeOdds[bet]
			if dComeOdds[bet] > 0:
				print("Taking down your No {num} and Odds. Returning ${ret} to your rack.".format(num=bet, ret=dComeBets[bet] + dComeOdds[bet]))
			else:
				print("Taking down your No {num} bet. Returning ${bet} to your rack.".format(num=bet, bet=dComeBets[bet]))
			dComeBets[bet] = dComeOdds[bet] = 0
	if checkVal == 0:
		print("Nothing to take down, silly!")


def comeShow():
	global comeBets, dComeBets, comeOdds, dComeOdds
	for key in comeBets:
		if comeBets[key] > 0:
			print("You have ${bet} on the Come {num} with ${odds} in Odds.".format(bet=comeBets[key], num=key, odds=comeOdds[key]))
	for key in dComeBets:
		if dComeBets[key] > 0:
			print("You have ${bet} on the Don't Come {num} with ${odds} in odds.".format(bet=dComeBets[key], num=key, odds=dComeOdds[key]))

def comeOddsChange():
	global comeBets, dComeBets, comeOdds, dComeOdds, chipsOnTable, bank
	cO = dCO = 0
	for value in comeBets:
		cO += comeBets[value]
	for value in dComeBets:
		dCO += dComeBets[value]
	if cO > 0:
		print("Change your Come Odds?")
		changeCome = input("> ")
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
	global chipsOnTable, bank
	maxDC = 10
	maxC = 0
	for key in dict:
		if dict[key] > 0:
			if key in [4, 10]:
				maxC = 3
			elif key in [5, 9]:
				maxC = 4
			elif key in [6, 8]:
				maxC = 5
			if 'Come' in dict:
				print("How much for Odds on the {num}? Max Odds is ${odds}; you have ${current} in Odds.".format(num=key, odds=maxC * dict[key], current=dict2[key]))
			else:
				print("How much to Lay against the {num}? Max Lay is ${lay}; you have ${current} in Lay Odds.".format(num=key, lay=maxDC*dict[key], current=dict2[key]))
			while True:
				try:
					bet = int(input("$>"))
					if bet > bank:
						print("You don't have enough money to make that bet! Try again.")
						outOfMoney()
						print("Change your Odds?")
						continue
					break
				except ValueError:
					bet = dict2[key]
					break
			if bet > 0:
				chipsOnTable -= dict2[key]
				bank += dict2[key]
				print("Ok, you have ${bet} Odds for your {num}.".format(bet=bet, num=key))
				dict2[key] = bet
				chipsOnTable += bet
				bank -= bet
			elif dict2[key] > 0 and bet == 0:
				print("Ok, taking down your Odds.")
				chipsOnTable -= dict2[key]
				bank += dict2[key]
				dict2[key] = bet


def comeCheck(roll):
	global comeBet, comeBets, dComeBet, dComeBets, bank, chipsOnTable, comeOdds, dComeOdds, pointIsOn
	comePay(roll)
	if comeBet > 0:
		if roll in [7, 11]:
			print("You won ${} on the Come!".format(comeBet))
			bank += comeBet * 2
			chipsOnTable -= comeBet
			comeBet = 0
		elif roll in [2, 3, 12]:
			print("You lost ${} from the Come Bet.".format(comeBet))
			chipsOnTable -= comeBet
			comeBet = 0
		else:
			print("Moving your Come Bet to the {}.".format(roll))
			comeBets[roll] = comeBet
			comeBet = 0
			print("Odds on your Come Bet?")
			oddChoice = input(">")
			if oddChoice.lower() in ['y', 'yes']:
				max = 0
				if roll in [4, 10]:
					max = comeBets[roll] * 3
				elif roll in [5, 9]:
					max = comeBets[roll] * 4
				elif roll in [6, 8]:
					max = comeBets[roll] * 5
				print("How much on the Come {num}? Max Odds is ${max}.".format(num=roll, max=max))
				while True:
					comeOdds[roll] = betPrompt()
					if comeOdds[roll] > max:
						print("Way too high on your Odds, there. Try again.")
						chipsOnTable -= comeOdds[roll]
						bank += comeOdds[roll]
						comeOdds[roll] = 0
						continue
					else:
						print("Ok, ${oBet} on your Come {num} odds.".format(oBet=comeOdds[roll], num=roll))
						break
	elif dComeBet > 0:
		if roll in [7, 11]:
			print("You lost ${} from the Don't Come.".format(dComeBet))
			chipsOnTable -= dComeBet
			dComeBet = 0
		elif roll in [2, 3, 12]:
			if roll in [2, 3]:
				print("You won ${} on the Don't Come!".format(dComeBet))
				bank += dComeBet * 2
			elif roll == 12:
				print("12 is a Push!")
			chipsOnTable -= dComeBet
			bank += dComeBet
			dComeBet = 0
		else:
			print("Moving your Don't Come bet to the {}.".format(roll))
			dComeBets[roll] = dComeBet
			dComeBet = 0
			print("Lay odds on your Don't Come {}?".format(roll))
			dcOdds = input(">")
			if dcOdds.lower() in ['y', 'yes']:
				dMax = dComeBets[roll] * 10
				print("How much to lay for your Don't Come Odds? Max Lay is ${}.".format(dMax))
				while True:
					dComeOdds[roll] = betPrompt()
					if dComeOdds[roll] > dMax:
						print("Way too much for your Lay Odds! Try again.")
						chipsOnTable -= dComeOdds[roll]
						bank += dComeOdds[roll]
						dComeOdds[roll] = 0
						continue
					else:
						print("Ok, ${bet} laid on the Don't Come {num}.".format(bet=dComeOdds[roll], num=roll))
						break

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
				bank += lossOdds
			chipsOnTable -= loss + lossOdds
			for key in comeBets:
				comeBets[key] = 0
			for key in comeOdds:
				comeOdds[key] = 0
		win = winOdds = 0
		for key in dComeBets:
			win += dComeBets[key] * 2
			chipsOnTable -= dComeBets[key]
		for key in dComeOdds:
			if dComeOdds[key] > 0 and pointIsOn:
				chipsOnTable -= dComeOdds[key]
				if key in [4, 10]:
					winOdds += dComeOdds[key]//2
				elif key in [5, 9]:
					winOdds += dComeOdds[key]//3*2
				elif key in [6, 8]:
					winOdds += dComeOdds[key]//6*5
			else:
				chipsOnTable -= dComeOdds[key]
				winOdds += dComeOdds[key]
				dComeOdds[key] = 0
		if win > 0:
			print("You won ${} from your Don't Come Bets!".format(win//2))
			if winOdds > 0 and pointIsOn:
				print("You won ${} from your Don't Come Bet Odds!".format(winOdds))
			elif winOdds > 0 and pointIsOn == False:
				print("Returning ${odds} to you from your Don't Come odds.".format(odds=winOdds))
			bank += win + winOdds + dComeOdds[key]
		for key in dComeBets:
			dComeBets[key] = 0
		for key in dComeOdds:
			dComeOdds[key] = 0
	if roll in [4, 5, 6, 8, 9, 10]:
		if comeBets[roll] > 0:
			print("You won ${win} on the Come {num}!".format(win=comeBets[roll], num=roll))
			bank += comeBets[roll] * 2
			chipsOnTable -= comeBets[roll]
			comeBets[roll] = 0
			if comeOdds[roll] > 0 and pointIsOn:
				cOddsWin = 0
				if roll in [4, 10]:
					cOddsWin = comeOdds[roll] * 2
				elif roll in [5, 9]:
					cOddsWin += comeOdds[roll]//2*3
				elif roll in [6, 8]:
					cOddsWin += comeOdds[roll]//5*6
				print("You won ${oddwin} on the Come {num} Odds!".format(oddwin=cOddsWin, num=roll))
				bank += cOddsWin + comeOdds[roll]
				chipsOnTable -= comeOdds[roll]
				comeOdds[roll] = 0
			elif comeOdds[roll] > 0 and pointIsOn == False:
				print("Returning ${bet} to you from your Come {num} odds.".format(bet=comeOdds[roll], num=roll))
				chipsOnTable -= comeOdds[roll]
				bank += comeOdds[roll]
				comeOdds[roll] = 0

		if dComeBets[roll] > 0:
			print("You lost ${dcloss} from the Don't Come {num}.".format(dcloss=dComeBets[roll], num=roll))
			#bank -= dComeBets[roll]
			chipsOnTable -= dComeBets[roll]
			dComeBets[roll] = 0
			if dComeOdds[roll] > 0:
				print("You lost ${dco} from the Don't Come {num} Odds.".format(dco=dComeOdds[roll], num=roll))
				#bank -= dComeOdds[roll]
				chipsOnTable -= dComeOdds[roll]
				dComeOdds[roll] = 0

#Field Betting

fieldBet = 0

def fieldShow():
	if fieldBet > 0:
		print("You have ${} on the Field.".format(fieldBet))

def field():
	global fieldBet, chipsOnTable, bank
	print("How much on the Field?")
	bet = betPrompt()
	if bet > 0:
		chipsOnTable -= fieldBet
		fieldBet = bet
		print("Ok, ${} on the Field.".format(fieldBet))
	elif fieldBet > 0 and bet == 0:
		bank += fieldBet
		chipsOnTable -= fieldBet
		print("Taking down your Field bet.")
		fieldBet = 0

def fieldTakeDown():
	global fieldBet, bank, chipsOnTable
	chipsOnTable -= fieldBet
	bank += fieldBet
	fieldBet = 0
	print("Taking down your Field Bet.")

def fieldCheck(roll):
	global fieldBet, bank, chipsOnTable
	if fieldBet > 0:
		payout = fieldBet
		if roll in [2, 3, 4, 9, 10, 11, 12]:
			if roll == 2:
				payout *= 2
				print("Double in the bubble!")
			elif roll == 12:
				payout *= 3
				print("Triple in the Field!")
			print("You won ${} on the Field!".format(payout))
			bank += payout
			print("Change your Field bet?")
			fChange = input(">")
			if fChange.lower() in ['y', 'yes']:
				chipsOnTable -= fieldBet
				bank += fieldBet
				fieldBet = 0
				field()
			else:
				pass
		else:
			print("You lost ${} from the Field.".format(fieldBet))
			#bank -= fieldBet
			chipsOnTable -= fieldBet
			fieldBet = 0
			print("Go back up on the Field?")
			fChoice = input(">")
			if fChoice in ['y', 'yes']:
				field()
			else:
				pass

propBets = {
"Snake Eyes": 0,
"Acey Deucey": 0,
"Eleven": 0,
"Boxcars": 0,
"Any Craps": 0,
"Any Seven": 0,
"C and E": 0,
"Horn": 0,
"World": 0,
"Buffalo": 0,
"Hi Low": 0,
"Hop 4": 0,
"Hop 4 Easy": 0,
"Hop 5": 0,
"Hop 6": 0,
"Hop 6 Easy": 0,
"Hop 7": 0,
"Hop 8": 0,
"Hop 8 Easy": 0,
"Hop 9": 0,
"Hop 10": 0,
"Hop 10 Easy": 0,
"Hop EZ": 0
}

def propHelp():
	print("Proposition Bet Codes:\n\t'a': Aces\n\t'ad': Acey-Deucey\n\t'ce': C and E\n\t'cr': Any Craps\n\t'seven': Any 7'\n\t'b': Boxcars\n\t'h4-h10': Hop bets\n\t'h6e, h8e': Hop 6 or 8 Easies\n\t'h': Horn Bet\n\t'hl': Hi-Low\n\t'wh': Whirl/World Bet\n\t'bf': Buffalo Bet\n\t'bf11': Buffalo Yo\n\t'all': Show all bets\n\t'help': Show this menu\n\t'x': Finish betting")

def propBetting():
	global propBets, chipsOnTable, bank
	while True:
		print("Type in your Prop Bet:")
		bet = input(">")
		if bet.lower() in ['2', 's']:
			print("How much on Snake Eyes?")
			bank += propBets["Snake Eyes"]
			chipsOnTable -= propBets["Snake Eyes"]
			propBets["Snake Eyes"] = betPrompt()
			print("Ok, ${} on Snake Eyes.".format(propBets["Snake Eyes"]))
			continue
		elif bet.lower() in ['ad', '3']:
			print("How much on Acey Deucey?")
			bank += propBets["Acey Deucey"]
			chipsOnTable -= propBets["Acey Deucey"]
			propBets["Acey Deucey"] = betPrompt()
			print("Ok, ${} on Acey-Deucey.".format(propBets["Acey Deucey"]))
			continue
		elif bet.lower() in ['7', 'a7']:
			print("How much on Any 7?")
			bank += propBets["Any Seven"]
			chipsOnTable -= propBets["Any Seven"]
			propBets["Any Seven"] = betPrompt()
			print("Ok, ${} on Any Seven.".format(propBets["Any Seven"]))
			continue
		elif bet.lower() in ['ac', 'c', 'cr']:
			print("How much on Any Craps?")
			bank += propBets["Any Craps"]
			chipsOnTable -= propBets["Any Craps"]
			propBets["Any Craps"] = betPrompt()
			print("Ok, ${} on Any Craps.".format(propBets["Any Craps"]))
			continue
		elif bet.lower() == 'ce':
			print("How much on C and E?")
			bank += propBets["C and E"]
			chipsOnTable -= propBets["C and E"]
			propBets["C and E"] = betPrompt()
			print("Ok, ${} on C and E.".format(propBets["C and E"]))
			continue
		elif bet.lower() in ['h', 'horn']:
			print("How much on the Horn Bet?")
			bank += propBets["Horn"]
			chipsOnTable -= propBets["Horn"]
			propBets["Horn"] = betPrompt()
			print("Ok, ${} on the Horn Bet.".format(propBets["Horn"]))
			continue
		elif bet.lower() == 'hh2':
			print("How much on the Horn High Deuce? Must be multiple of 5.")
			bank += propBets["Snake Eyes"] + propBets["Acey Deucey"] + propBets["Eleven"] + propBets["Boxcars"]
			chipsOnTable -= propBets["Snake Eyes"] + propBets["Acey Deucey"] + propBets["Eleven"] + propBets["Boxcars"]
			while True:
				hornHigh2 = betPrompt()
				if hornHigh2%5 == 0:
					break
				else:
					print("That wasn't a multiple of 5, try again!")
					bank += hornHigh2
					chipsOnTable -= hornHigh2
					continue
			propBets["Snake Eyes"] = hornHigh2//5*2
			propBets["Acey Deucey"] = propBets["Eleven"] = propBets["Boxcars"] = hornHigh2//5
			print("Ok, ${} on the Horn High Deuce.".format(hornHigh2))
			continue
		elif bet.lower() == 'hh3':
			print("How much on the Horn High Ace-Deuce?")
			bank += propBets["Snake Eyes"] + propBets["Acey Deucey"] + propBets["Eleven"] + propBets["Boxcars"]
			chipsOnTable -= propBets["Snake Eyes"] + propBets["Acey Deucey"] + propBets["Eleven"] + propBets["Boxcars"]
			while True:
				hornHigh3 = betPrompt()
				if hornHigh3%5 == 0:
					break
				else:
					print("That wasn't a multiple of 5, doofus. Try again!")
					bank += hornHigh3
					chipsOnTable -= hornHigh3
					continue
			propBets["Acey Deucey"] = hornHigh3//5*2
			propBets["Snake Eyes"] = propBets["Eleven"] = propBets["Boxcars"] = hornHigh3//5
			print("Ok, ${} on the Horn High Ace-Deuce.".format(hornHigh3))
			continue
		elif bet.lower() in ['hhy', 'hh11']:
			print("How much on the Horn High Yo?")
			bank += propBets["Snake Eyes"] + propBets["Acey Deucey"] + propBets["Eleven"] + propBets["Boxcars"]
			chipsOnTable -= propBets["Snake Eyes"] + propBets["Acey Deucey"] + propBets["Eleven"] + propBets["Boxcars"]
			while True:
				hornHigh11 = betPrompt()
				if hornHigh11%5 == 0:
					break
				else:
					print("Not a multiple of 5, try again!")
					bank += hornHigh11
					chipsOnTable -= hornHigh11
					continue
			propBets["Eleven"] = hornHigh11//5*2
			propBets["Snake Eyes"] = propBets["Acey Deucey"] = propBets["Boxcars"] = hornHigh11//5
			print("Ok, ${} on the Horn High Yo!".format(hornHigh11))
			continue
		elif bet.lower() in ['hh12', 'hhm', 'hhb']:
			print("How much on the Horn High 12?")
			bank += propBets["Snake Eyes"] + propBets["Acey Deucey"] + propBets["Eleven"] + propBets["Boxcars"]
			chipsOnTable -= propBets["Snake Eyes"] + propBets["Acey Deucey"] + propBets["Eleven"] + propBets["Boxcars"]
			while True:
				hornHigh12 = betPrompt()
				if hornHigh12%5 == 0:
					break
				else:
					print("That wasn't a multiple of 5, try again!")
					bank += hornHigh12
					chipsOnTable -= hornHigh12
					continue
			propBets["Boxcars"] = hornHigh12//5*2
			propBets["Snake Eyes"] = propBets["Acey Deucey"] = propBets["Eleven"] = hornHigh12//5
			print("Ok, ${} on the Horn High Midnight.".format(hornHigh12))
			continue
		elif bet.lower() in ['b', '12']:
			print("How much on Boxcars?")
			bank += propBets["Boxcars"]
			chipsOnTable -= propBets["Boxcars"]
			propBets["Boxcars"] = betPrompt()
			print("Ok, ${} on Boxcars.".format(propBets["Boxcars"]))
			continue
		elif bet in ['11', 'e', 'yo']:
			print("How much on Yo Eleven?")
			bank += propBets["Eleven"]
			chipsOnTable -= propBets["Eleven"]
			propBets["Eleven"] = betPrompt()
			print("Ok, ${} on Eleven.".format(propBets["Eleven"]))
			continue
		elif bet.lower() == 'w':
			print("How much on the World bet? Must be a multiple of 5.")
			bank += propBets["Any Seven"] + propBets["Horn"]
			chipsOnTable -= propBets["Any Seven"] + propBets["Horn"]
			while True:
				chipsOnTable -= propBets["World"]
				propBets["World"] = betPrompt()
				if propBets["World"]%5 == 0:
					break
				else:
					print("That wasn't a multiple of 5! Try again, genius.")
					bank += propBets["World"]
					continue
			propBets["Any Seven"] = propBets["World"]//5
			propBets["World"] -= propBets["World"]//5
			propBets["Horn"] = propBets["World"]
			print("Ok, you have ${seven} bet on the Any Seven and ${horn} on the Horn.".format(seven=propBets["Any Seven"], horn=propBets["Horn"]))
			propBets["World"] = 0
			if propBets["Buffalo"] > 0 and propBets["Eleven"] > 0:
				print("You've got yourself a Whirly Buffalo!")
		elif bet.lower() == 'bf':
			print("How much for the Buffalo bet? Must be a multiple of 5.")
			bank += propBets["Any Seven"] + propBets["Buffalo"]
			chipsOnTable -= propBets["Any Seven"]
			while True:
				chipsOnTable -= propBets["Buffalo"]
				propBets["Buffalo"] = betPrompt()
				if propBets["Buffalo"]%5 == 0:
					break
				else:
					print("That wasn't a multiple of 5! Try again, genius.")
					bank += propBets["Buffalo"]
					continue
			print("Ok, ${} each on the Any 7 and hard ways hopping.".format(propBets["Buffalo"]//5))
			propBets["Any Seven"] = propBets["Buffalo"]//5
			propBets["Buffalo"] -= propBets["Buffalo"]//5
			if propBets["Horn"] > 0 and propBets["Any Seven"] > 0:
				print("You've got yourself a Whirly Buffalo!")
		elif bet.lower() in ['bf11', 'by']:
			print("How much for the Buffalo bet with the Yo? Must be a multiple of 5.")
			bank += propBets["Eleven"] + propBets["Buffalo"]
			chipsOnTable -= propBets["Eleven"]
			while True:
				chipsOnTable -= propBets["Buffalo"]
				propBets["Buffalo"] = betPrompt()
				if propBets["Buffalo"]%5 == 0:
					break
				else:
					print("That wasn't a multiple of 5! Try again, genius.")
					bank += propBets["Buffalo"]
					continue
			print("Ok, ${} each on the Yo Eleven and hard ways hopping.".format(propBets["Buffalo"]//5))
			propBets["Eleven"] = propBets["Buffalo"]//5
			propBets["Buffalo"] -= propBets["Buffalo"]//5
			if propBets["Horn"] > 0 and propBets["Any Seven"] > 0:
				print("You've got yourself a Whirly Buffalo!")
		elif bet.lower() == 'hl':
			print("How much on the Hi-Low? Must be a multiple of 2.")
			bank += propBets["Snake Eyes"] + propBets["Boxcars"]
			chipsOnTable -= propBets["Snake Eyes"] + propBets["Boxcars"]
			while True:
				chipsOnTable -= propBets["Hi Low"]
				propBets["Hi Low"] = betPrompt()
				if propBets["Hi Low"]%2 == 0:
					break
				else:
					print("That wasn't a multiple of 2! Try again, genius.")
					bank += propBets["Hi Low"]
					continue
			print("Ok, ${} each on the 2 and 12.".format(propBets["Hi Low"]//2))
			propBets["Snake Eyes"] = propBets["Hi Low"]//2
			propBets["Boxcars"] = propBets["Hi Low"]//2
			propBets["Hi Low"] = 0

		elif bet.lower() == 'h4':
			print("How much to Hop the 4? Must be an even number.")
			while True:
				bank += propBets["Hop 4"]
				chipsOnTable -= propBets["Hop 4"]
				propBets["Hop 4"] = betPrompt()
				if propBets["Hop 4"]%2 == 0:
					break
				else:
					print("That wasn't an even number! You can't even!")
					continue
			print("Ok, ${} hopping the 4s.".format(propBets["Hop 4"]))
			continue
		elif bet.lower() == 'h10':
			print("How much to Hop the 10? Must be an even number.")
			while True:
				bank += propBets["Hop 10"]
				chipsOnTable -= propBets["Hop 10"]
				propBets["Hop 10"] = betPrompt()
				if propBets["Hop 10"]%2 == 0:
					break
				else:
					print("That wasn't an even number! You can't even!")
					continue
			print("Ok, ${} hopping the 10s.".format(propBets["Hop 10"]))
			continue
		elif bet.lower() == 'h5':
			print("How much to Hop the 5? Must be an even number.")
			while True:
				bank += propBets["Hop 5"]
				chipsOnTable -= propBets["Hop 5"]
				propBets["Hop 5"] = betPrompt()
				if propBets["Hop 5"]%2 == 0:
					break
				else:
					print("That wasn't an even number! You can't even!")
					continue
			print("Ok, ${} hopping the 5s.".format(propBets["Hop 5"]))
			continue
		elif bet.lower() == 'h9':
			print("How much to Hop the 9? Must be an even number.")
			while True:
				bank += propBets["Hop 9"]
				chipsOnTable -= propBets["Hop 9"]
				propBets["Hop 9"] = betPrompt()
				if propBets["Hop 9"]%2 == 0:
					break
				else:
					print("That wasn't an even number! You can't even!")
					continue
			print("Ok, ${} hopping the 9s.".format(propBets["Hop 9"]))
			continue
		elif bet.lower() == 'h6':
			print("How much to Hop the 6? Must be a multiple of 3.")
			while True:
				bank += propBets["Hop 6"]
				chipsOnTable -= propBets["Hop 6"]
				propBets["Hop 6"] = betPrompt()
				if propBets["Hop 6"]%3 == 0:
					break
				else:
					print("That's not a multiple of 3! Can't you math?")
					continue
			print("Ok, ${} hopping the 6s.".format(propBets["Hop 6"]))
			continue
		elif bet.lower() == 'h6e':
			print("How much to Hop the 6 Easies? Must be a multiple of 2.")
			while True:
				bank += propBets["Hop 6 Easy"]
				chipsOnTable -= propBets["Hop 6 Easy"]
				propBets["Hop 6 Easy"] = betPrompt()
				if propBets["Hop 6 Easy"]%2 == 0:
					break
				else:
					print("That's not a multiple of 2! Can't you math?")
					continue
			print("Ok, ${} hopping the 6 Easies.".format(propBets["Hop 6 Easy"]))
			continue
		elif bet.lower() == 'h7':
			print("How much to Hop Big Red? Must be a multiple of 3.")
			while True:
				bank += propBets["Hop 7"]
				chipsOnTable -= propBets["Hop 7"]
				propBets["Hop 7"] = betPrompt()
				if propBets["Hop 7"]%3 == 0:
					break
				else:
					print("That's not a multiple of 3! Can't you math?")
					continue
			print("Ok, ${} hopping the 7s.".format(propBets["Hop 7"]))
			continue
		elif bet.lower() == 'h8':
			print("How much to Hop the 8? Must be a multiple of 3.")
			while True:
				bank += propBets["Hop 8"]
				chipsOnTable -= propBets["Hop 8"]
				propBets["Hop 8"] = betPrompt()
				if propBets["Hop 8"]%3 == 0:
					break
				else:
					print("That's not a multiple of 3! Can't you math?")
					continue
			print("Ok, ${} hopping the 8s.".format(propBets["Hop 8"]))
			continue
		elif bet.lower() == 'h8e':
			print("How much to Hop the 8 Easies? Must be a multiple of 2.")
			while True:
				bank += propBets["Hop 8 Easy"]
				chipsOnTable -= propBets["Hop 8 Easy"]
				propBets["Hop 8 Easy"] = betPrompt()
				if propBets["Hop 8 Easy"]%2 == 0:
					break
				else:
					print("That's not a multiple of 2! Can't you math?")
					continue
			print("Ok, ${} hopping the 8 Easies.".format(propBets["Hop 8 Easy"]))
			continue
		elif bet.lower() == 'hez':
			print("How much to Hop the Easies? Must be a multiple of 15.")
			while True:
				bank += propBets["Hop EZ"]
				chipsOnTable -= propBets["Hop EZ"]
				propBets["Hop EZ"] = betPrompt()
				if propBets["Hop EZ"]%15 == 0:
					break
				else:
					print("That's not a multiple of 15! Can't you math?")
					continue
			print("Ok, ${} hopping the Easies.".format(propBets["Hop EZ"]))
			continue
		elif bet.lower() == 'a':
			print("Showing your Prop Bets:\n")
			for key in propBets:
				if propBets[key] > 0:
					print("\t${bet} on {prop}.".format(bet=str(propBets[key]), prop=key))
			continue
		elif bet.lower() == 'help':
			propHelp()
			continue 
		elif bet.lower() == 'x':
			print("Done Prop Betting.")
			break
		else:
			print("That's simply not an option! Try again...")
			continue

def propPay(roll):
	global propBets, bank, chipsOnTable, die1, die2
	multiplier = 0
	for key in propBets:
		sub = 0
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
				sub = propBets[key]//4 * 3
				propBets[key] = propBets[key]//4
			elif key == "Horn" and roll in [3, 11]:
				multiplier = 15
				sub = propBets[key]//4*3
				propBets[key] = propBets[key]//4
			elif key == "Buffalo" and roll in [4, 6, 8, 10] and die1 == die2:
				multiplier = 30
				sub = propBets[key]//4*3
				propBets[key] = propBets[key]//4
			elif key == "Hop 4" and roll == 4:
				if die1 == 3:
					multipler = 15
				else:
					multipler = 30
				sub = propBets[key]//2
				propBets[key] = propBets[key]//2
			elif key == "Hop 10" and roll == 10:
				if die1 == 6:
					multipler = 15
				else:
					multipler = 30
				sub = propBets[key]//2
				propBets[key] = propBets[key]//2
			elif key == "Hop 5" and roll == 5:
				multiplier = 15
				sub = propBets[key]//2
				propBets[key] = propBets[key]//2
			elif key == "Hop 9" and roll == 9:
				multiplier = 15
				sub = propBets[key]//2
				propBets[key] = propBets[key]//2
			elif key == "Hop 6" and roll == 6:
				if (die1, die2) in [(5, 1), (4, 2)]:
					multiplier = 15
				else:
					multiplier = 30
				sub = propBets[key]//3*2
				propBets[key] = propBets[key]//3
			elif key == "Hop 6 Easy" and roll == 6:
				if (die1, die2) in [(5, 1), (4, 2)]:
					multiplier = 15
					sub = propBets[key]//2
					propBets[key] = propBets[key]//2
				else:
					multiplier = 0
			elif key == "Hop 8" and roll == 8:
				if (die1, die2) in [(5, 3), (6, 2)]:
					multiplier = 15
				else:
					multiplier = 30
				sub = propBets[key]//3*2
				propBets[key] = propBets[key]//3
			elif key == "Hop 8 Easy" and roll == 8:
				if (die1, die2) in [(5, 3), (6, 2)]:
					multiplier = 15
					sub = propBets[key]//2
					propBets[key] = propBets[key]//2
				else:
					multiplier = 0
			elif key == "Hop 7" and roll == 7:
				multiplier = 15
				sub = propBets[key]//3*2
				propBets[key] = propBets[key]//3
			elif key == "Hop EZ" and roll in range(3, 12):
				multiplier = 15
				sub = propBets[key]//15*14
				propBets[key] = propBets[key]//15
			else:
				multiplier = 0
			if multiplier > 0:
				print("You won ${win} on the {bet} bet!".format(win=(propBets[key]*multiplier)-sub, bet=key))
				bank += (propBets[key] * multiplier) - sub
				chipsOnTable -= propBets[key] + sub
				propBets[key] = 0
			else:
				print("You lost ${loss} from the {bet}.".format(loss=propBets[key], bet=key))
				#bank -= propBets[key]
				chipsOnTable -= propBets[key]
				propBets[key] = 0


#All Tall Small setup
atsAll = atsSmall = atsTall = 0
allNums = []
smallNums = []
tallNums = []
atsOn = False

def atsBetting():
	global atsAll, atsSmall, atsTall, atsOn, bank
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
		#bank -= atsAll + atsTall + atsSmall
		chipsOnTable -= atsAll + atsTall + atsSmall
		atsAll = atsSmall = atsTall = 0
		allNums = []
		smallNums = []
		tallNums = []
	elif (atsAll + atsSmall + atsTall) > 0:
		allNums.sort()
		print("All Tall Small: {}".format(allNums))

	if set(smallNums) == set(smallSet):
		print("You won ${} on the Small!".format(atsSmall * 34))
		bank += atsSmall * 34
		chipsOnTable -= atsSmall
		atsSmall = 0
		smallNums = []
	if set(tallNums) == set(tallSet):
		print("You won ${} from the Tall!".format(atsTall*34))
		bank += atsTall * 34
		chipsOnTable -= atsTall
		atsTall = 0
		tallNums = []
	if set(allNums) == set(allSet):
		print("You won ${} on the All! Holy Crap!".format(atsAll*175))
		bank += atsAll * 175
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

def layAll():
	global chipsOnTable, bank, layBets
	total = 0
	outlay = 0
	for number in layBets:
		outlay += layBets[number]
	while True:
		print("How many units across the Lay Numbers?")
		try:
			unit = int(input("> "))
		except ValueError:
			print("That wasn't even a unit! Try again.")
			continue
		if (unit*5)*6 > bank + outlay:
			print("You don't have enough money for that! Egads!")
			outOfMoney()
			continue
		else:
			break
	for key in layBets:
		chipsOnTable -= layBets[key]
		bank += layBets[key]
		layBets[key] = 5 * unit
		chipsOnTable += layBets[key]
		bank -= layBets[key]
		total += layBets[key]
	print("Laying ${} Across.".format(total))

def layBetting():
	global layBets, bank, chipsOnTable
	for key in layBets:
		print("You have ${bet} on the Lay {key}.".format(bet=layBets[key], key=key))
		print("How much on the Lay {}?".format(key))
		while True:
			try:
				bet = int(input("$>"))
				if bet > bank + chipsOnTable - chipsOnTable:
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
			bank += layBets[key]
			layBets[key] = bet
			chipsOnTable += bet
			bank -= bet
			print("Ok, ${bet} on the Lay {num}.".format(bet=bet, num=key))
		elif layBets[key] > 0 and bet == 0:
			print("Ok, taking down your Lay {num} bet.".format(num=key))
			chipsOnTable -= layBets[key]
			bank += layBets[key]
			layBets[key] = 0

def layTakeDown():
	global layBets, bank, chipsOnTable
	for key in layBets:
		chipsOnTable -= layBets[key]
		bank += layBets[key]
		layBets[key] = 0

def layShow():
	global layBets
	for key in layBets:
		if layBets[key] > 0:
			print("You have ${value} on the Lay {key}.".format(value=layBets[key], key=key))

def layCheck(roll):
	global layBets, bank, chipsOnTable
	vigPay = 0
	if roll in [4, 5, 6, 8, 9, 10]:
		if layBets[roll] > 0:
			print("You lost ${loss} from the Lay {num}.".format(loss=layBets[roll], num=roll))
			chipsOnTable -= layBets[roll]
			layBets[roll] = 0
			print("Go back up on your Lay {}?".format(roll))
			layAgain = input("> ")
			if layAgain.lower() == 'y':
				print("How much on the Lay {}?".format(roll))
				layBets[roll] = betPrompt()
				print("Ok, ${amount} on the Lay {num}.".format(amount=layBets[roll], num=roll))
			else:
				pass

	elif roll == 7:
		for key in layBets:
			win = 0
			if layBets[key] > 0:
				if key in [4, 10]:
					win = layBets[key]//2
				elif key in [5, 9]:
					win = layBets[key]//3*2
				elif key in [6, 8]:
					win = layBets[key]//6*5
				vig = layBets[key]*0.05
				if vig < 1:
					vigPay += math.ceil(vig)
				else:
					vigPay += math.floor(vig)
				print("You won ${win} on the Lay {num}!".format(win=win, num=key))
				bank += win - vig
		if vigPay > 0:
			print("Taking out ${} for the vig.".format(vigPay))

# Bank and bet setup
bank = 0
initBank = 0
chipsOnTable = 0

def cashIn():
	global bank, initBank
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
			initBank = cash
			break
	print("Great, starting you off with ${}.".format(bank))

def quitGame():
	global bank, chipsOnTable, initBank
	if bank+chipsOnTable > initBank:
		print("\nNice work coloring up! Come back soon!\n")
	elif bank+chipsOnTable == initBank:
		print("\nWell, at least you didn't lose anything! Try again soon!\n")
	else:
		print("\nOops, tough loss today. Better luck next time!\n")
	raise SystemExit

def betPrompt():
	global bank, chipsOnTable
	while True:
		try:
			playerBet =  int(input("\t$> "))
		except ValueError:
			print("\tThat wasn't a number!")
			continue
		if playerBet > bank:
			print("\tYou simply don't have enough money to do that! DO you want to add more to your bankroll?")
			addMore = input(">")
			if addMore.lower() == "y":
				outOfMoney()
			continue
		else:
			chipsOnTable += playerBet
			bank -= playerBet
			return playerBet

def outOfMoney():
	global bank
	if bank <= 0:
		print("\tYou are totally out of money.\n\tLet's hit the ATM again and get you more cash.\n\tHow much do you want?")
	else:
		print("\tYour chips are getting really low.\n\tHow much would you like to add to your bankroll?")
	while True:
		try:
			cash = int(input("\t$>"))
		except ValueError:
			print("\tYou forgot what numbers were and the ATM beeps at you in annoyance.\n\tTry again.")
			continue
		if cash < 0:
			print("\tWhat am I, a bank?\n\tThis is for withdrawals only! Try again.")
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
	outlay = 0
	for number in place:
		outlay += place[number]
	if pre.lower() == 'a':
		while True:
			print("How many units across the Place Numbers?")
			try:
				unit = int(input("> "))
			except ValueError:
				print("That wasn't even a unit! Try again.")
				continue
			if ((unit*5)*4 + (unit*6)*2) > bank + outlay:
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
			bank += place[key]
			if key in [4, 5, 9, 10]:
				place[key] = 5 * unit
			elif key in [6, 8]:
				place[key] = 6 * unit
			if pointIsOn and point not in ['y', 'yes']:
				if key == comeOut:
					place[key] = 0
			chipsOnTable += place[key]
			bank -= place[key]
			total += place[key]
		print("Placing ${} Across.".format(total))
	elif pre.lower() == 'i':
		print("How many units Inside?")
		while True:
			try:
				unit = int(input("> "))
			except ValueError:
				print("Invalid entry, try again.")
				continue
			if ((unit*5)*2 + (unit*6)*2) > bank + outlay:
				print("You don't have enough money for that! Egads!")
				outOfMoney()
				continue
			else:
				break

		if pointIsOn:
			print("Include the Point?")
			try:
				insidePoint = input("> ")
			except ValueError:
				insidePoint = "n"
				pass
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
			else:
				chipsOnTable += place[key]
				bank -= place[key]
				total += place[key]
		print("Ok, placing ${} inside.".format(total))

	elif pre.lower() == "c":
		print("How many units on the 6 and 8?")
		while True:
			try:
				unit = int(input("> "))
			except ValueError:
				print("Invalid entry, try again.")
				continue
			if (unit*6)*2 > bank + outlay:
				print("You don't have enough money for that! Egads!")
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
		print("Ok, placing ${} on the 6 and 8.".format(total))


def placeMover():
	global place, chipsOnTable, bank, comeOut
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
			bank += place[comeOut]
			chipsOnTable += place[key]
			bank -= place[key]
			place[comeOut] = 0

def placeBets():
	global place, chipsOnTable, bank
	madeBet = True
	for key in place:
		print("You have ${bet} on the Place {key}.".format(bet=place[key], key=key))
		print("How much on the Place {}?".format(key))
		while True:
			bet = 0
			try:
				bet = int(input("$>"))
				if bet > bank + chipsOnTable:
					print("You don't have enough money to make that bet! Try again.")
					outOfMoney()
					print("How much on the Place {}?".format(key))
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
			if key in [4, 10] and bet >= 10:
				print("Buying the {num} for ${bet}.".format(bet=bet, num=key))
			else:
				print("${bet} on the Place {num}.".format(bet=bet, num=key))
		elif place[key] > 0 and bet == 0:
			print("Ok, taking down your Place {num} bet.".format(num=key))
			chipsOnTable -= place[key]
			bank += place[key]
			place[key] = 0

def placeShow():
	global place
	for key in place:
		if place[key] > 0:
			print("You have ${value} on the Place {key}.".format(value=place[key], key=key))

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
				win = (place[roll]//6) * 7 + place[roll]%6

# Modulo accounts for improper bets, such as $@5 on the 6 or 8. Dealers would pay odds on the first $24 and then the remainder would get paid out as $1.

			bank += win
			print("You won ${win} on the Place {num}!".format(win=win, num=roll))
			print("Change your bet?")
			change = input(">")
			if change.lower() in ['y', 'yes']:
				print("How much on the Place {}?".format(roll))
				bank += place[roll]
				bet = betPrompt()
				if bet == 0:
					chipsOnTable -= place[roll]
					#bank += place[roll]
					place[roll] = bet
					print("Ok, taking down your Place {} bet.".format(roll))
				else:
					chipsOnTable -= place[roll]
					#bank += place[roll]
					place[roll] = bet
					print("Ok, ${bet} on the Place {num}.".format(bet=place[roll], num=roll))
	elif roll == 7:
		loss = 0
		for key in place:
			loss += place[key]
			place[key] = 0
		#bank -= loss
		chipsOnTable -= loss
		if loss > 0:
			print("You lost ${} from the Place bets.".format(loss))
	else:
		pass

def showAllBets():
	global comeBet, dComeBet, fireBet, lineBets, propBets, atsAll, atsTall, atsSmall
	for value in lineBets:
		if lineBets[value] > 0:
			print("You have ${val} on the {bet}.".format(val=lineBets[value], bet=value))
	if comeBet > 0:
		print("You have ${} on the Come.".format(comeBet))
	if dComeBet > 0:
		print("You have ${} on the Don't Come.".format(dComeBet))
	comeShow()
	placeShow()
	layShow() 
	fieldShow()
	hardShow()
	for value in propBets:
		if propBets[value] > 0:
			print("${val} on {bet}.".format(val=propBets[value], bet=value))
	if atsAll + atsSmall + atsTall > 0:
		print("You have ${a} on the All, ${t} on the Tall, and ${s} on the Small.".format(a=atsAll, t=atsTall, s=atsSmall))
	if fireBet > 0:
		print("You have ${} on the Fire Bet.".format(fireBet))

#Additional Global Variables
p2 = 0
pointIsOn = False
working = False
throws = 0

# Game Start
print("Oh Craps! v.{version}\nBy: Marco Salsiccia".format(version=version))
cashIn()
while True:
	if chipsOnTable <= 0:
		print("You have ${} in the bank.".format(bank))
	else:
		print("You have ${bank} in the bank with ${table} out on the table.".format(bank=bank, table=chipsOnTable))
	if bank <= 0 and chipsOnTable <= 0:
		outOfMoney()
	print("Throws: {}\n".format(throws))

# Initial bets

	while True:
		print("Place your Bets!\n")
		round1 = input("> ")
		if round1.lower() in ["l", "line", "line bets"]:
			print("Line Bets:\n")
			lineBetting()
			continue

		elif round1.lower() == "q":
			quitGame()
		elif round1.lower() == "p":
			while True:
				placeShow()
				print("Place Bets:\n")
				plBet = input(">\n")
				if plBet == "y":
					placeBets()
					continue
				elif plBet.lower() == "d":
					print("Taking down your Place Bets.")
					placeTakeDown()
					continue
				elif plBet.lower() in ['a', 'i', 'c']:
					placePreset(plBet)
					continue
				elif plBet.lower() == "h":
					print("Place Betting Codes:\n\ty: Enter individual Place Betting mode.\n\td: Take down all Place Bets.\n\ta: Auto-bet Across all the numbers.\n\ti: Auto-bet on the Inside numbers.\n\tc: Auto-bet on the 6 and 8\n\th: Show this Help Menu.\n\tx: Exit Place Betting.\n")
				elif plBet.lower() == "x":
					print("Done Place Betting!")
					break

		elif round1.lower() in ["ly", "lay"]:
			while True:
				layShow()
				print("Lay Bets?")
				lyBet = input(">\n")
				if lyBet.lower() in ['y', 'yes']:
					layBetting()
					continue
				elif lyBet.lower() == "d":
					print("Taking down your Lay Bets.")
					layTakeDown()
					continue
				elif lyBet.lower() == "a":
					layAll()
					continue 
				elif lyBet.lower() == "h":
					print("Lay Bet Codes:\n\n\ty: Enter Individual Lay Betting mode.\n\ta: Lay Bets across all numbers.\n\td: Take down all Lay Bets.\n\th: Show this Help menu.\n\tx: Finish Lay Betting.\n")
				elif lyBet.lower() == "x":
					print("Done Lay Betting!")
					break

		elif round1.lower() in ["f", "field"]:
			fieldShow()
			print("Field Bet?")
			fBet = input(">\n")
			if fBet.lower() in ['y', 'yes']:
				field()
			elif fBet.lower() in ['d', 'td', 'takedown']:
				fieldTakeDown()
			continue

		elif round1.lower() in ["hd", "hard", "hw"]:
			while True:
				hardShow()
				print("Hard Ways Bets?")
				hWays = input(">\n")
				if hWays.lower() in ['y', 'yes']:
					hardWaysBetting()
					continue
				elif hWays.lower() in ['d', 'td', 'takedown']:
					hardTakeDown()
					continue
				elif hWays.lower() in ['a', 'across', 'all']:
					hardAuto()
					continue
				elif hWays in ["h4", "h6", "h8", "h10"]:
					hardHigh(hWays)
					continue
				elif hWays.lower() == "h":
					print("Hard Ways Codes:\n\n\ty: Enter Individual Hard Ways Betting mode.\n\td: Take down all Hard Ways bets.\n\ta: Auto-bet across all Hard Ways numbers.\n\th4: Bet all numbers, Hard 4 high.\n\th6: Bet all numbers, Hard 6 high.\n\th8: Bet all numbers, Hard 8 high.\n\th10: Bet all numbers, Hard 10 high.\n\th: Show this Help Menu.\n\tx: Finish Hard Ways betting.\n")
					continue
				elif hWays.lower() == "x":
					print("Done betting the Hard Ways!")
					break

# Working Bets Setup
		elif round1.lower() in ["w", "work", "working"]:
			plCheck = hCheck = lCheck = 0
			for value in place.values():
				plCheck += value
			for value in hardWays.values():
				hCheck += value
			for value in layBets.values():
				lCheck += value

			if plCheck > 0 or hCheck > 0 or lCheck > 0:
				if working:
					working = False
					print("Ok, all bets are Off.")
				else:
					working = True
					print("Ok, all bets are Working!")
			else:
				print("Make some bets first so they can Work!")
			continue

		elif round1.lower() in ["pr", "prop"]:
			propBetting()
			continue

		elif round1.lower() == "dcd":
			dComeDown()
			continue

		elif round1.lower() == "ats":
			if atsOn == True:
				print("All Tall Small: {}".format(allNums))
			elif throws == 0:
				print("All Tall Small:\n")
				atsBetting()
			else:
				print("All Tall Small will be available after the next 7 rolls.")
			continue

# Fire Bet
		elif round1.lower() == "fire":
			if fireBet == 0:
				print("Fire Bet:\n")
				fireBetting()
			else:
				print("You have ${bet} on the Fire Bet; Numbers Hit: {fire}.".format(bet=fireBet, fire=fire))
			continue
#Coming Out Roll
		elif round1.lower() in ["x", "r"]:
			print("Rolling the dice!")
			break

		elif round1.lower() == "h":
			print("Betting Codes:\n\tl: Line Bets\n\tp: Place Bets\n\tly: Lay Bets\n\tf: Field Bet\n\thd: Hard Ways Bets\n\tpr: Prop Bets\n\tw: Toggle if Bets are Working\n\tdcd: Take down Don't Come bet\n\tats: All Tall Small\n\tfire: Fire Bet\n\th: Show this Help Menu\n\tx or r: Roll the Dice!")
			continue
		elif round1.lower() == "b":
			print("You have ${bank} in the Bank and ${chips} out on the table.".format(bank=bank, chips=chipsOnTable))
			continue
		elif round1.lower() == "a":
			showAllBets()
			continue
		else:
			print("That's not an option, silly!")
			continue


	comeOut  = roll()
	throws += 1
	comeCheck(comeOut)
	fieldCheck(comeOut)
	if working == True:
		placeCheck(comeOut)
		layCheck(comeOut)
		hardCheck(comeOut)

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

			if bank <= 0 and chipsOnTable <= 0:
				outOfMoney()

			print("\n{} is the Point!\n".format(comeOut))
			print("Throws: {}".format(throws))

#Phase 2 Betting

			while True:
				print("Place your bets!\n")
				round2 = input("> ")

				if round2.lower() in ["o", "po", "dpo"]:
					if lineBets["Pass"] > 0 or lineBets["Don't Pass"] > 0:
						odds()
					else:
						print("You don't have a Line bet, silly!")
					continue

				if round2.lower() == "b":
					print("You have ${bank} in your rack with ${chips} on the table. The Point is {p}.".format(bank=bank, chips=chipsOnTable, p=comeOut))
					continue

				if round2.lower() == "dp":
					if lineBets["Don't Pass"] > 0:
						dpPhase2()
					else:
						print("You don't have a Don't Pass bet!")
					continue

				if round2.lower() == "c":
					comeShow()
					print("Come Bet:\n")
					come()
					continue

				if round2.lower() == "co":
					comeOddsChange()
					continue

				if round2.lower() == "dcd":
					dComeDown()
					continue

				elif round2.lower() == "q":
					quitGame()

				elif round2.lower() == "p":
					while True:
						placeShow()
						print("Place Bets?")
						pl2 = input(">")
						if pl2.lower() == "y":
							placeBets()
							continue
						elif pl2.lower() == "o":
							if placeOff:
								placeOff = False
								print("Ok, your Place Bets are back on.")
							else:
								placeOff = True
								print("All your Place Bets are Off.")
							continue
						elif pl2.lower() == "d":
							print("Taking down all of your Place Bets.")
							placeTakeDown()
							continue
						elif pl2.lower() in ['a', 'i', 'c']:
							placePreset(pl2)
							continue
						elif pl2.lower() == "m":
							placeMover()
							continue
						elif pl2.lower() == "p":
							chipsOnTable -= place[comeOut]
							bank += place[comeOut]
							place[comeOut] = 0
							print("Taking down the Place {} bet.".format(comeOut))
							continue
						elif pl2.lower() == "h":
							print("Place Bet Codes:\n\n\ty: Enter individual Place Betting mode.\n\ta: Auto-bet across all numbers.\n\ti: Auto-bet inside numbers.\n\tc: Auto-bet on the 6 and 8\n\to: Turn Place Bets Off for next roll.\n\td: Take down all Place Bets.\n\tm: Move Point number to empty Place Bet.\n\tp: Take down Point number place bet.\n\th: Show this Help menu.\n\tx: Finish Place Betting.")
							continue
						elif pl2.lower() == "x":
							print("Done Place Betting!")
							break
						else:
							print("That's not a valid option!")
						continue
					continue
				elif round2  in ["ly", "lay"]:
					while True:
						layShow()
						print("Lay Bets?\n")
						ly2Bet = input(">")
						if ly2Bet.lower() in ['y', 'yes']:
							layBetting()
							continue
						elif ly2Bet.lower() == "o":
							if layOff == False:
								layOff = True
								print("Your Lay Bets are Off.")
							else:
								layOff = False
								print("Your Lay Bets are On.")
							continue
						elif ly2Bet.lower() == "a":
							layAll()
							continue
						elif ly2Bet.lower() in "d":
							print("Taking down all of your Lay Bets.")
							layTakeDown()
							continue
						elif ly2Bet.lower() == "h":
							print("Lay Bet Codes:\n\n\ty: Enter Lay Betting Mode\n\ta: Lay Bets across all numbers.\n\to: Toggle Lay Bets Off or On for next roll\n\td: Take all Lay Bets down.\n\th: Show this Help menu\n\tx: Finish Lay Betting")
							continue
						elif ly2Bet.lower() == "x":
							print("Done Lay Betting!")
							break
						else:
							print("That's not an option!")
							continue
					continue

				elif round2 == "f":
					fieldShow()
					print("Field Bet?\n")
					fb2 = input(">")
					if fb2.lower() in ['y', 'yes']:
						field()
					elif fb2.lower() in ['d', 'td', 'takedown']:
						fieldTakeDown()
					continue

				elif round2 == "hd":
					while True:
						hardShow()
						print("Hard Ways bets?\n")
						hard2 = input(">")
						if hard2.lower() in ['y', 'yes']:
							hardWaysBetting()
							continue
						elif hard2.lower() in ['o', 'off']:
							if hardOff == False:
								hardOff = True
								print("Your Hard Ways are Off.")
							else:
								hardOff = True
								print("Hard Ways are On.")
							continue
						elif hard2.lower() in ['d', 'td', 'takedown']:
							hardTakeDown()
							continue
						elif hard2.lower() in ['a', 'all', 'across']:
							hardAuto()
							continue
						elif hard2.lower() in ["h4", "h6", "h8", "h10"]:
							hardHigh(hard2)
							continue
						elif hard2.lower() == "h":
							print("Hard Ways Codes:\n\n\ty: Enter Hard Ways betting mode\n\to: Toggle Hard Ways Bets On or Off for next roll\n\td: Take down Hard Ways bets\n\ta: Auto-bet Across all Hard Ways\n\t:h4: Bet all Hard Ways High 4\n\th6: Bet all Hard Ways High 6\n\th8: Bet all Hard Ways High 8\n\th10: Bet all Hard Ways High 10\n\th: Show this Help Menu\n\tx: Finish Hard Ways Betting")
							continue
						elif hard2.lower() == "x":
							print("Finished betting on the Hard Ways!")
							break
						else:
							print("That's not an option!")
							continue
					continue

				elif round2.lower() in ["pr", "prop"]:
					propBetting()
					continue

				elif round2.lower() == "a":
					showAllBets()
					continue
# phase 2 roll
				elif round2.lower() in ["r", "x"]:
					print("Dice are rolling!")
					break
				elif round2.lower() == "h":
					print("Betting Codes:\n\n\to: Line and Lay Odds\n\tdp: Take Down Don't Pass Bet\n\tp: Place Bets\n\tly: Lay Bets\n\tc: Come Bets\n\tdcd: Take down DC and Odds\n\tf: Field Bet\n\thd: Hard Ways Bets\n\tpr: Prop Bets\n\th: Show this Help Menu\n\tx: Finish betting and Roll the Dice")
					continue

				else:
					print("That's not a betting option, silly!")
					continue
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
				os.system("clear")
				break
			elif p2 == comeOut:
				print("Point Hit! Front line winner!")
				pointIsOn = False
				break
			else:
				continue

	continue