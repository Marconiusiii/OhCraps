from random import *

def roll():
	global rollHard
	d1 = randint(1, 6)
	d2 = randint(1, 6)
	total = d1 + d2
	print("You rolled {d1} and {d2} for {total}.".format(d1=d1, d2=d2, total=total))
	if d1 == d2:
		rollHard = True
	return total

rollHard = False

#Line Bets

lineBets = {
"Pass": 0,
"Pass Odds": 0,
"Don't Pass": 0,
"Don't Pass Odds": 0
}

def lineBetting():
	global lineBets
	print("Pass or Don't Pass?")
	while True:
		try:
			lBet = input(">")
			break
		except ValueError:
			print("That won't work, try again.")
			continue
	if lBet.lower() in ['p', 'pass', 'passline', 'pass line']:
		print("How much on the Pass Line?")
		lineBets["Pass"] = int(input(">"))
		print("Ok, ${} on the Pass Line.".format(lineBets["Pass"]))
	elif lBet.lower() in ["d", "dp", "don't pass", "don't"]:
		print("How much on the Don't Pass line?")
		lineBets["Don't Pass"] = int(input(">"))
		print("Ok, ${} on the Don't Pass Line.".format(lineBets["Don't Pass"]))

def lineCheck(roll, p2roll):
	global lineBets, bank, pointIsOn
	if pointIsOn == False:
		if roll in [7, 11] and lineBets["Pass"] > 0:
			print("You won ${} on the Pass Line!.".format(lineBets["Pass"]))
			bank += lineBets["Pass"]
			lineBets["Pass"] = 0
		elif roll in [7, 11] and lineBets["Don't Pass"] > 0:
			print("You lost ${} from the Don't Pass Line.".format(lineBets["Don't Pass"]))
			bank -= lineBets["Don't Pass"]
			lineBets["Don't Pass"] = 0
		elif roll in [2, 3, 12] and lineBets["Pass"] > 0:
			print("You lost ${} from the Pass Line.".format(lineBets["Pass"]))
			bank -= lineBets["Pass"]
			lineBets["Pass"] = 0
		elif roll in [2, 3, 12] and lineBets["Don't Pass"] > 0:
			print("You won ${} on the Don't Pass Line!".format(lineBets["Don't Pass"]))
			bank += lineBets["Don't Pass"]
			lineBets["Don't Pass"] = 0
	elif pointIsOn == True:
		if p2roll == roll and lineBets["Pass"] > 0:
			print("You won ${} on the Pass Line!".format(lineBets["Pass"]))
			bank += lineBets["Pass"]
			oddsCheck(p2roll)
		elif p2roll == roll and lineBets["Don't Pass"] > 0:
			print("You lost ${} from the Don't Pass Line.".format(lineBets["Don't Pass"]))
			bank -= lineBets["Don't Pass"]
			oddsCheck(p2roll)
		elif p2roll == 7 and lineBets["Pass"] > 0:
			print("You lost ${} from the Pass Line.".format(lineBets["Pass"]))
			bank -= lineBets["Pass"]
			oddsCheck(p2roll)
			lineBets["Pass"] = 0
		elif p2roll == 7 and lineBets["Don't Pass"] > 0:
			print("You won ${} on the Don't Pass Line!".format(lineBets["Don't Pass"]))
			bank += lineBets["Don't Pass"]
			oddsCheck(p2roll)
			lineBets["Don't Pass"] = 0
# Odds Betting

def odds():
	global lineBets
	if lineBets["Pass"] > 0:
		print("How Much for your Pass Line Odds?")
		lineBets["Pass Odds"] = int(input(">"))
		print("Ok, ${} on your Pass Line Odds.".format(lineBets["Pass Odds"]))
	elif lineBets["Don't Pass"] > 0:
		print("How much to Lay for your Odds?")
		lineBets["Don't Pass Odds"] = int(input(">"))
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
		comeBet = int(input(">"))		
		print("Ok, ${} on the Come.".format(comeBet))
	elif choice.lower() in ["dc", "d", "don't", "don't come", "dontcome"]:
		print("How much on the Don't Com?")
		dComeBet = int(input(">"))
		print("Ok, ${} on the Don't Come.".format(dComeBet))
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
				comeOdds[roll] = int(input(">"))
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
				dComeOdds[roll] = int(input(">"))
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
					winOdds += dComeOdds[key]//2
				elif key in [5, 9]:
					winOdds += dComeOdds[key]//3*2
				elif key in [6, 8]:
					winOdds += dComeOdds[key]//6*5
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

def field():
	global fieldBet
	print("How much on the Field?")
	fieldBet = int(input(">"))
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
"aces": 0,
"aceDeuce": 0,
"anyCraps": 0,
"any7": 0,
"cAndE": 0,
"horn": 0,
"boxcars": 0
}

def propBetting():
	global propBets
	while True:
		bet = input("Type in your Prop Bet >")
		if bet.lower() in ['aces', 'snakeeyes', 'snake eyes', 2, 'a']:
			propBets["aces"] = input("How much on Snake Eyes? >")
			print("Ok, ${} on Snake Eyes.".format(propBets["aces"]))
			continue
		elif bet.lower() in ['ad', 'acedeuce', 3, 'ace deuce', 'acey deucey']:
			propBets["aceDeuce"] = input("How much on Acey-Deucey?")
			print("Ok, ${} on Acey-Deucey.".format(propBets["aceDeuce"]))
			continue
		elif bet.lower() in [7, 'a7', 'any 7', 'seven', 'any seven', 'big red']:
			propBets["any7"] = input("How much on Any Seven? >")
			print("Ok, ${} on Any Seven.".format(propBets["any7"]))
			continue
		elif bet.lower() in ['craps', 'anycraps', 'ac', 'any craps']:
			propBets["anyCraps"] = input("How much on Any Craps? >")
			print("Ok, ${} on Any Craps.".format(propBets["anyCraps"]))
			continue
		elif bet.lower() in ['ce', 'cande', 'c and e', 'craps and eleven']:
			propBets["cAndE"] = input("How much on C and E? >")
			print("Ok, ${} on C and E.".format(propBets["cAndE"]))
			continue
		elif bet.lower() in ['h', 'horn', 'horn bet']:
			propBets["horn"] = input("How much on the Horn? >")
			print("Ok, ${} on the Horn Bet.".format(propBets["horn"]))
			continue
		elif bet.lower() in ['boxcars', 'b', 12, 'midnight']:
			propBets["boxcars"] = input("How much on Boxcars? >")
			print("Ok, ${} on Boxcars.".format(propBets["boxcars"]))
			continue
		elif bet.lower() in ['show', 'all', 'show all', 'bets']:
			for key, value in propBets:
				if propBets[key] > 0:
					print("${bet} on {prop}.".format(bet=value, prop=key))
			continue
		elif bet.lower() in ['x', 'close', 'exit', 'done']:
			break

layBets = {
4: 0,
5: 0,
6: 0,
8: 0,
9: 0,
10: 0
}

bank = 1000

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
				bet = 0
				break
		if bet > 0:
			place[key] = bet
			print("Ok, ${bet} on the Place {num}.".format(bet=bet, num=key))

def placeShow():
	global place
	for key in place:
		if place[key] > 0:
			print("You have ${value} on the Place {key}.".format(value=place[key], key=key))

def placeCheck(roll):
	global place, bank
	if roll in [4, 5, 6, 8, 9, 10]:
		if place[roll] > 0:
			if roll in [4, 10]:
				bank += (place[roll]//5) * 9
				print("You won ${win} on the Place {num}!".format(win=(place[roll]//5)*9, num=roll))
			elif roll in [5, 9]:
				bank += (place[roll]//5) * 7
				print("You won ${win} on the Place {num}!".format(win=(place[roll]//5)*7, num=roll))
			elif roll in [6, 8]:
				bank += (place[roll]//6) * 7
				print("You won ${win} on the Place {num}!".format(win=(place[roll]//6)*7, num=roll))
			print("Change your bet?")
			change = input(">")
			if change.lower() in ['y', 'yes']:
				print("How much on the Place {}?".format(roll))
				place[roll] = int(input(">"))
				print("Ok, ${} on the Place {}.".format(place[roll], roll))
	elif roll == 7:
		loss = 0
		for key in place:
			loss += place[key]
			place[key] = 0
		bank -= loss
		print("You lost ${} from the Place bets.".format(loss))
	else:
		pass


p2 = 0
pointIsOn = False
working = False
# Game Start
print("Oh Craps! v.5.0")
print("Starting off with ${} bankroll.".format(bank))
while True:
	print("You have ${} in the bank.".format(bank))

# Initial bets
	lbet = input("Line Bets? >")
	if lbet in ['y', 'yes']:
		lineBetting()
	print("Place Bets?")
	plBet = input(">")
	if plBet in ['y', 'Yes']:
		placeBets()

		print("Place Bets Working?")
		work = input(">")
		if work.lower() in ['y', 'yes']:
			working = True
			print("Ok, all bets working.")
	print("Field Bet?")
	fBet = input(">")
	if fBet.lower() in ['y', 'yes']:
		field()

#Coming Out Roll
	input("Hit Enter to roll!")

	comeOut  = roll()

	comeCheck(comeOut)
	if working == True:
		placeCheck(comeOut)
	fieldCheck(comeOut)
	if comeOut in [7, 11]:
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

			print("Come Bet?")
			cChoice = input(">")
			if cChoice.lower() in ['y', 'yes']:
				come()

			placeShow()
			print("Place Bets?")
			pl2 = input(">")
			if pl2.lower() in ['y', 'yes']:
				placeBets()

			if fieldBet > 0:
				print("You have ${} on the Field.".format(fieldBet))
			print("FIeld Bet?")
			fb2 = input(">")
			if fb2.lower() in ['y', 'yes']:
				field()
			input("Hit Enter to Roll!")
			p2 = roll()

			comeCheck(p2)
			placeCheck(p2)
			fieldCheck(p2)
			lineCheck(comeOut, p2)
			if p2 == 7:
				pointIsOn = False
				print("7 Out.")
				break
			elif p2 == comeOut:
				print("Point Hit!")
				pointIsOn = False
				break
			else:
				continue

	continue
