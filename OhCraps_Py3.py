from random import *

dealerCalls = {
2: ["Craps", "eye balls", "two aces", "rats eyes", "snake eyes", "push the don't", "eleven in a shoe store", "twice in the rice", "two craps two, two bad boys from Illinois", "two crap aces", "aces in both places", "a spot and a dot", "dimples"],
3: ["Craps", "ace-deuce", "three craps, ace caught a deuce, no use", "divorce roll, come up single", "winner on the dark side", "three craps three, the indicator", "crap and a half", "small ace deuce, can't produce", "2 , 1, son of a gun"],
4: ["Double deuce", "Little Joe", "Little Joe from Kokomo", "Hit us in the 2 2", "2 spots and 2 dots"],
5: ["After 5 the Field's alive", "Fiver Fiver Race Track Driver", "No Field 5", "Little Phoebe", "We got the fiver"],
6: ["The national average", "Big Red, catch 'em in the corner", "Sixie from Dixie"],
7: ["Line Away, grab the money", "the bruiser", "point 7", "Out", "Loser 7", "Nevada Breakfast", "Cinco Dos, Adios", "Adios", "3 4 on the floor"],
8: ["a square pair", "eighter from the theater", "windows"],
9: ["niner 9", "center field 9", "Center of the garden", "ocean liner niner", "Nina from Pasadena", "nina Niner, wine and dine her"],
10: ["puppy paws", "pair o' roses", "The big one on the end", "55 to stay alive", "pair of sunflowers", "64 out the door"],
11: ["Yo Eleven", "Yo", "6 5, no drive", "yo 'leven", "It's not my eleven, it's Yo Eleven"],
12: ["craps", "midnight", "a whole lotta crap", "craps to the max", "boxcars", "all the spots we gots", "triple field", "atomic craps", "Hobo's delight"]
}

def stickman(roll):
	return dealerCalls[roll][randint(0, len(dealerCalls[roll])-1)]

def roll():
	global rollHard, pointIsOn
	rollHard = False
	d1 = randint(1, 6)
	d2 = randint(1, 6)
	total = d1 + d2
	if d1 == d2 and total in [4, 6, 8, 10]:
		rollHard = True
		print("{} the Hard Way!".format(total))
	elif total in [7, 11] and pointIsOn == False:
		print("{total} winner! Pay the line, take the don't!".format(total=total))
	else:
		print("{tot}, {call}!".format(tot=total, call=stickman(total)))
	return total

# Hard Ways Setup
rollHard = False

hardWays = {
4: 0,
6: 0,
8: 0,
10: 0
}

def hardWaysBetting():
	global hardWays
	for key in hardWays:
		if hardWays[key] > 0:
			print("You have ${bet} on the hard {num}.".format(bet=hardWays[key], num=key))
		print("How much on the Hard {}?".format(key))
		while True:
			try:
				hardWays[key] = int(input(">"))
				break
			except ValueError:
				break
		if hardWays[key] > 0:
			print("Ok, ${bet} on the Hard {num}.".format(bet=hardWays[key], num=key))

def hardCheck(roll):
	global bank, hardWays, rollHard
	if roll == 7:
		loss = 0
		for key in hardWays:
			if hardWays[key] > 0:
				loss += hardWays[key]
				hardWays[key] = 0
		if loss > 0:
			print("You lost ${} from the Hard Ways.".format(loss))
			bank -= loss
	elif roll in [4, 6, 8, 10]:
		if hardWays[roll] > 0 and rollHard == True:
			if roll in [4, 10]:
				win = hardWays[roll] * 7
			elif roll in [6, 8]:
				win = hardWays[roll] * 9
			print("You won ${win} on the Hard {num}!".format(win=win, num=roll))
			bank += win
		elif hardWays[roll] > 0 and rollHard == False:
			print("You lost ${loss} from the Hard {num}.".format(loss=hardWays[roll], num=roll))
			bank -= hardWays[roll]
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

def betPrompt():
	while True:
		try:
			return int(input(">"))
		except ValueError:
			print("That wasn't a number!")
			continue

def lineBetting():
	global lineBets
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
			print("How much on the Pass Line?")
			lineBets["Pass"] = betPrompt()
			print("Ok, ${} on the Pass Line.".format(lineBets["Pass"]))
			continue
		elif lBet.lower() in ["d", "dp", "don't pass", "don't"]:
			print("How much on the Don't Pass line?")
			lineBets["Don't Pass"] = betPrompt()
			print("Ok, ${} on the Don't Pass Line.".format(lineBets["Don't Pass"]))
			continue
		elif lBet.lower() in ['x', 'close', 'esc', 'exit', 'done']:
			print("Ok, moving on!")
			break
		else:
			print("Invalid entry, try again!")
			continue

def lineCheck(roll, p2roll):
	global lineBets, bank, pointIsOn
	if pointIsOn == False:
		if roll in [7, 11]:
			if lineBets["Pass"] > 0:
				print("You won ${} on the Pass Line!.".format(lineBets["Pass"]))
				bank += lineBets["Pass"]
				lineBets["Pass"] = 0
			if lineBets["Don't Pass"] > 0:
				print("You lost ${} from the Don't Pass Line.".format(lineBets["Don't Pass"]))
				bank -= lineBets["Don't Pass"]
				lineBets["Don't Pass"] = 0
		elif roll in [2, 3, 12]:
			if lineBets["Pass"] > 0:
				print("You lost ${} from the Pass Line.".format(lineBets["Pass"]))
				bank -= lineBets["Pass"]
				lineBets["Pass"] = 0
			if lineBets["Don't Pass"] > 0:
				print("You won ${} on the Don't Pass Line!".format(lineBets["Don't Pass"]))
				bank += lineBets["Don't Pass"]
				lineBets["Don't Pass"] = 0
	elif pointIsOn == True:
		if p2roll == roll:
			if lineBets["Pass"] > 0:
				print("You won ${} on the Pass Line!".format(lineBets["Pass"]))
				bank += lineBets["Pass"]
			if lineBets["Don't Pass"] > 0:
				print("You lost ${} from the Don't Pass Line.".format(lineBets["Don't Pass"]))
				bank -= lineBets["Don't Pass"]
			oddsCheck(p2roll)
		elif p2roll == 7:
			if lineBets["Pass"] > 0:
				print("You lost ${} from the Pass Line.".format(lineBets["Pass"]))
				bank -= lineBets["Pass"]
				lineBets["Pass"] = 0
			if lineBets["Don't Pass"] > 0:
				print("You won ${} on the Don't Pass Line!".format(lineBets["Don't Pass"]))
				bank += lineBets["Don't Pass"]
				lineBets["Don't Pass"] = 0
			oddsCheck(p2roll)

def dpPhase2():
	global lineBets
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
		lineBets["Don't Pass"] = lineBets["Don't Pass Odds"] =  0
	elif takeDown.lower() in ['n', 'no']:
		print("Ok leaving your Don't Pass bets up.")
	else:
		pass

# Odds Betting

def odds():
	global lineBets
	if lineBets["Pass"] > 0:
		print("How Much for your Pass Line Odds?")
		lineBets["Pass Odds"] = betPrompt()
		print("Ok, ${} on your Pass Line Odds.".format(lineBets["Pass Odds"]))
	if lineBets["Don't Pass"] > 0:
		print("How much to Lay for your Odds?")
		lineBets["Don't Pass Odds"] = betPrompt()
		print("Ok, ${} laid against the Point.".format(lineBets["Don't Pass Odds"]))

def oddsCheck(roll):
	global bank, lineBets, comeOut
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
		lineBets["Pass Odds"] = 0
	elif lineBets["Pass Odds"] > 0 and roll == 7:
		print("You lost ${} from your Pass Line Odds.".format(lineBets["Pass Odds"]))
		bank -= lineBets["Pass Odds"]
		lineBets["Pass Odds"] = 0
	if lineBets["Don't Pass Odds"] > 0 and roll == 7:
		if comeOut in [4, 10]:
			payout += lineBets["Don't Pass Odds"]//2
		elif comeOut in [5, 9]:
			payout += (lineBets["Don't Pass Odds"]//3) * 2
		elif comeOut in [6, 8]:
			payout += (lineBets["Don't Pass Odds"]//6) * 5
		print("You won ${} on your Don't Pass Odds!".format(payout))
		lineBets["Don't Pass Odds"] = 0
	elif lineBets["Don't Pass"] > 0 and roll == comeOut:
		print("You lost ${} from your Don't Pass Odds.".format(lineBets["Don't Pass Odds"]))
		bank -= lineBets["Don't Pass Odds"]
		lineBets["Don't Pass Odds"] = 0

#Place Betting

place = {
4: 0,
5: 0,
6: 0,
8: 0,
9: 0,
10: 0
}

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

def comeCheck(roll):
	global comeBet, comeBets, dComeBet, dComeBets, bank, comeOdds, dComeOdds
	comePay(roll)
	if comeBet > 0:
		if roll in [7, 11]:
			print("You won ${} on the Come!".format(comeBet))
			bank += comeBet
			comeBet = 0
		elif roll in [2, 3, 12]:
			print("You lost ${} from the Come Bet.".format(comeBet))
			bank -= comeBet
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
			dComeBet = 0
		elif roll in [2, 3, 12]:
			print("You won ${} on the Don't Come!".format(dComeBet))
			bank += dComeBet
			dComeBet = 0
		else:
			print("Moving your Don't Come bet to the {}.".format(roll))
			dComeBets[roll] = dComeBet
			dComeBet = 0
			print("Odds on your Don't Come {}?".format(roll))
			dcOdds = input(">")
			if dcOdds.lower() in ['y', 'yes']:
				print("How much for your Don't Come Odds?")
				dComeOdds[roll] = betPrompt()
				print("Ok, ${bet} on the Don't Come {num}.".format(bet=dComeOdds[roll], num=roll))

def comePay(roll):
	global bank, comeBets, dComeBets, comeOdds, dComeOdds, pointIsOn
	if roll == 7:
		loss = lossOdds = 0
		for key in comeBets:
			loss += comeBets[key]
		if pointIsOn == True:
			for key in comeOdds:
				lossOdds += comeOdds[key]
		if loss > 0:
			print("You lost ${} from your Come Bets.".format(loss))
			if lossOdds > 0:
				print("You lost ${} from your Come Bet Odds.".format(lossOdds))
			bank -= loss + lossOdds
			for key in comeBets:
				comeBets[key] = 0
			for key in comeOdds:
				comeOdds[key] = 0
		win = winOdds = 0
		for key in dComeBets:
			win += dComeBets[key]
		for key in dComeOdds:
			if dComeOdds[key] > 0:
				if key in [4, 10]:
					winOdds += dComeOdds[key]*2
				elif key in [5, 9]:
					winOdds += dComeOdds[key]//2*3
				elif key in [6, 8]:
					winOdds += dComeOdds[key]//5*6
		if win > 0:
			print("You won ${} from your Don't Come Bets!".format(win))
			if winOdds > 0:
				print("You won ${} from your Don't Come Bet Odds!".format(winodds))
			bank += win + winOdds
	if roll in [4, 5, 6, 8, 9, 10]:
		if comeBets[roll] > 0:
			print("You won ${win} on the Come {num}!".format(win=comeBets[roll], num=roll))
			bank += comeBets[roll]
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
		if dComeBets[roll] > 0:
			print("You lost ${dcloss} from the Don't Come {num}.".format(dcloss=dComeBets[roll], num=roll))
			bank -= dComeBets[roll]
			dComeBets[roll] = 0
			if dComeOdds[roll] > 0:
				print("You lost ${dco} from the Don't Come {num} Odds.".format(dco=dComeOdds[roll], num=roll))
				bank -= dComeOdds[roll]
				dComeOdds[roll] = 0


#Field Betting
fieldBet = 0


def fieldShow():
	if fieldBet > 0:
		print("You have ${} on the Field.".format(fieldBet))

def field():
	global fieldBet
	print("How much on the Field?")
	fieldBet = betPrompt()
	print("Ok, ${} on the Field.".format(fieldBet))

def fieldCheck(roll):
	global fieldBet, bank
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
			fieldBet = 0

propBets = {
"Snake Eyes": 0,
"Acey Deucey": 0,
"Any Craps": 0,
"Any Seven": 0,
"C and E": 0,
"Horn": 0,
"Boxcars": 0,
"Eleven": 0
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
	global propBets, bank
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
				propBets[key] = 0
			else:
				print("You lost ${loss} from the {bet}.".format(loss=propBets[key], bet=key))
				bank -= propBets[key]
				propBets[key] = 0


#All Tall Small setup
atsAll = atsSmall = atsTall = 0
allNums = smallNums = tallNums = []
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
	global allNums, smallNums, tallNums, bank, atsAll, atsSmall, atsTall, atsOn
	smallSet = [2, 3, 4, 5, 6]
	tallSet = [8, 9, 10, 11, 12]
	allSet = smallSet + tallSet

	if roll in smallSet and roll not in smallNums:
		smallNums.append(roll)
	elif roll in tallSet and roll not in tallNums:
		tallNums.append(roll)
	if roll in allSet and roll not in allNums:
		allNums.append(roll)

	if roll == 7:
		atsOn = False
		print("You lost ${} from the ALl Tall Small.".format(atsAll+atsTall+atsSmall))
		bank -= atsAll + atsTall + atsSmall
		atsAll = atsSmall = atsTall = 0
		allNums = smallNums = tallNums = []
	else:
		allNums.sort()
		print("All Tall Small: {}".format(allNums))

	if set(smallNums) == set(smallSet):
		print("You won ${} on the Small!".format(atsSmall * 35))
		bank += atsSmall * 35
		atsSmall = 0
		smallNums = []
	if set(tallNums) == set(tallSet):
		print("You won ${} from the Tall!".format(atsTall*35))
		bank += atsTall * 35
		atsTall = 0
		tallNums = []
	if set(allNums) == set(allSet):
		print("You won ${} on the All! Holy Crap!".format(atsAll*176))
		bank += atsAll * 176
		atsAll = 0
		allNums = []

# Lay Bet Setup
layBets = {
4: 0,
5: 0,
6: 0,
8: 0,
9: 0,
10: 0
}

def layBetting():
	global layBets
	for key in layBets:
		print("You have ${bet} on the Lay {key}.".format(bet=layVets[key], key=key))
		print("How much on the Lay {}?".format(key))
		while True:
			try:
				bet = int(input(">"))
				break
			except ValueError:
				bet = 0
				break
		if bet > 0:
			layBets[key] = bet
			print("Ok, ${bet} on the Lay {num}.".format(bet=bet, num=key))

def layShow():
	global layBets
	for key in layBets:
		if layBets[key] > 0:
			print("You have ${value} on the Lay {key}.".format(value=layBets[key], key=key))

def layCheck(roll):
	global layBets, bank
	if roll in [4, 5, 6, 8, 9, 10]:
		if layBets[roll] > 0:
			print("You lost ${loss} from the Lay {num}.".format(loss=layBets[roll], num=roll))
			bank -= layBets[roll]
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
				layBets[key] = 0



# Bank setup
bank = 0

def cashIn():
	global bank
	print("How much are you cashing in for your bankroll?")
	while True:
		try:
			bank = int(input("$>"))
			break
		except ValueError:
			print("That wasn't a number, doofus!")
			continue
	print("Great, starting you off with ${}.".format(bank))

def placeBets():
	global place
	for key in place:
		print("You have ${bet} on the Place {key}.".format(bet=place[key], key=key))
		print("How much on the Place {}?".format(key))
		while True:
			try:
				bet = int(input(">"))
				break
			except ValueError:
				bet = place[key]
				break
		if bet > 0:
			place[key] = bet
			if key in [4, 10] and bet >= 25:
				print("Buying the {num} for ${bet}.".format(bet=bet, num=key))
			else:
				print("${bet} on the Place {num}.".format(bet=bet, num=key))
		elif place[key] > 0 and bet == 0:
			print("Ok, taking down your Place {num} bet.".format(num=key))
			place[key] = 0


def placeShow():
	global place
	for key in place:
		if place[key] > 0:
			print("You have ${value} on the Place {key}.".format(value=place[key], key=key))

def vig(bet):
	print("${vig} paid to the House for the Buy Bet vig.".format(vig=int(bet*0.05)))
	return int(bet*0.05)

def placeCheck(roll):
	global place, bank
	if roll in [4, 5, 6, 8, 9, 10]:
		if place[roll] > 0:
			win = 0
			if roll in [4, 10] and place[roll] >= 25:
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
				place[roll] = betPrompt()
				if place[roll] == 0:
					print("Ok, taking down your Place {} bet.".format(roll))
				else:
					print("Ok, ${bet} on the Place {num}.".format(bet=place[roll], num=roll))
	elif roll == 7:
		loss = 0
		for key in place:
			loss += place[key]
			place[key] = 0
		bank -= loss
		if loss > 0:
			print("You lost ${} from the Place bets.".format(loss))
	else:
		pass


p2 = 0
pointIsOn = False
working = False
throws = 0

# Game Start
print("Oh Craps! v.5.0\nBy: Marco Salsiccia")
cashIn()
while True:
	print("You have ${} in the bank.".format(bank))
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


	print("Lay Bets?")
	lyBet = input(">")
	if lyBet.lower() in ['y', 'yes']:
		layBetting()


	fieldShow()
	print("Field Bet?")
	fBet = input(">")
	if fBet.lower() in ['y', 'yes']:
		field()

	hardShow()
	print("Hard Ways Bets?")
	hWays = input(">")
	if hWays.lower() in ['y', 'yes']:
		hardWaysBetting()
	if plBet in ['y', 'yes'] or lyBet in ['y', 'yes'] or hWays in ['y', 'yes']:
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
	else:
		print("All Tall Small?")
		atsChoice = input(">")
		if atsChoice.lower() in ['y', 'yes']:
			atsBetting()

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
			print("{} is the Point.".format(comeOut))
			print("Rolls: {}".format(throws))
#Phase 2 Betting
			if lineBets["Pass"] > 0 or lineBets["Don't Pass"] > 0:
				if lineBets["Pass Odds"] > 0:
					print("You have ${} on your Pass Line Odds.".format(lineBets["Pass Odds"]))
				elif lineBets["Don't Pass Odds"] > 0:
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

			placeShow()
			print("Place Bets?")
			pl2 = input(">")
			if pl2.lower() in ['y', 'yes']:
				placeBets()

			layShow()
			print("Lay Bets?")
			ly2Bet = input(">")
			if ly2Bet.lower() in ['y', 'yes']:
				layBetting()

			fieldShow()
			print("FIeld Bet?")
			fb2 = input(">")
			if fb2.lower() in ['y', 'yes']:
				field()

			hardShow()
			print("Hard Ways bets?")
			hard2 = input(">")
			if hard2.lower() in ['y', 'yes']:
				hardWaysBetting()

			print("Prop Bets?")
			pr2Bet = input(">")
			if pr2Bet.lower() in ['y', 'yes']:
				propBetting()
# phase 2 roll
			input("Hit Enter to Roll!")

			p2 = roll()

			throws += 1
			comeCheck(p2)
			placeCheck(p2)
			layCheck(p2)
			fieldCheck(p2)
			hardCheck(p2)
			lineCheck(comeOut, p2)
			propPay(p2)
			if atsOn == True:
				ats(p2)

			if p2 == 7:
				throws = 0
				pointIsOn = False
				break
			elif p2 == comeOut:
				print("Point Hit!")
				pointIsOn = False
				break
			else:
				continue

	continue
