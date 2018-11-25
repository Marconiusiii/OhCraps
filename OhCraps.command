import os

from random import *

four = five = six = eight = nine = ten = hard4 = hard6 = hard8 = hard10 = come4 = come5 = come6 = come8 = come9 = come10 = c4Odds = c5Odds = c6Odds = c8Odds = c9Odds = c10Odds = any7 = anyCraps = cAndE = snakeEyes = aceDeuce = boxcars = horn = 0

dCome4 = dCome5 = dCome6 = dCome8 = dCome9 = dCome10 = dC4Odds = dC5Odds = dC6Odds = dC8Odds = dC9Odds = dC10Odds = 0

def clearScreen():
	os.system('cls' if os.name == 'nt' else 'clear')

def betInput(bank):
	if bank <= 0:
		print "You are totally out of money!"
		print "Add more to your bank or hit Ctrl-C to exit the game, walking away with a sad, empty wallet."
		while True:
			try:
				bank += +int(raw_input("$"))
			except ValueError:
				print "That wasn't a number, try again."
				continue
			if bank < 0:
				print "You fail at math. Try again!"
				bank = 0
				continue
			else:
				print "Great, starting you off again with $%d." %bank
				break
	else:
		pass

	while True:
		while True:
			try:
				bet = int(raw_input("$>"))
				break
			except ValueError:
				print "That wasn't a number! The stickman whaps you upside the head with his stick."
				continue
		if bet > bank:
			print "You simply can't bet that much! You only have $%d in the bank." %bank
			continue
		elif bet < 0:
			print "Nice try, but that's not gonna work!"
			continue
		else:
			break

	return bet

def prop():
	any7 = anyCraps = cAndE = snakeEyes = aceDeuce = boxcars = horn = 0

	pr1 = raw_input("Bet on Any 7?")
	if pr1 == 'y':
		print "How much on Any 7?"
		any7 = betInput(bank)
		print "Ok, $%d on Any 7." %any7
	pr2 = raw_input("Bet on Any Craps?")
	if pr2 == 'y':
		print "How much on Any Craps?"
		anyCraps = betInput(bank)
		print "Ok, $%d on Any Craps." %anyCraps
	pr3 = raw_input("Bet on C&E?")
	if pr3 == 'y':
		print "How much on C & E?"
		cAndE = betInput(bank)
		print "Ok, $%d on C&E." %cAndE
	pr4 = raw_input("Bet on Snake Eyes?")
	if pr4 == 'y':
		print "How much on Snake Eyes?"
		snakeEyes = betInput(bank)
		print "Ok, $%d on Snake Eyes." %snakeEyes
	pr5 = raw_input("Bet on Acey-Deucey?")
	if pr5 == 'y':
		print "How much on Acey-Deucey?"
		aceDeuce = betInput(bank)
		print "Ok, $%d on Acey-Deucey." %aceDeuce
	pr6 = raw_input("Bet on Boxcars?")
	if pr6 == 'y':
		print "How much on Boxcars?"
		boxcars = betInput(bank)
		print "Ok, $%d on Boxcars." %boxcars
	pr7 = raw_input("Bet the Horn?")
	if pr7 == 'y':
		print "How much on the Horn?"
		horn = betInput(bank)
		print "Ok, $%d on the Horn Bet!" %horn
	return any7, anyCraps, cAndE, snakeEyes, aceDeuce, boxcars, horn

def come(roll, comeBet, come4, come5, come6, come8, come9, come10):
	print "Moving Come Bet to the %d." %roll
	if roll == 4:
		come4 = comeBet
	elif roll == 5:
		come5 = comeBet
	elif roll == 6:
		come6 = comeBet
	elif roll == 8:
		come8 = comeBet
	elif roll == 9:
		come9 = comeBet
	elif roll == 10:
		come10 = comeBet
	return come4, come5, come6, come8, come9, come10


def dCome(roll, comeBet, dCome4, dCome5, dCome6, dCome8, dCome9, dCome10):
	print "Moving Don't Come Bet to the %d." %roll
	if roll == 4:
		dCome4 = comeBet
	elif roll == 5:
		dCome5 = comeBet
	elif roll == 6:
		dCome6 = comeBet
	elif roll == 8:
		dCome8 = comeBet
	elif roll == 9:
		dCome9 = comeBet
	elif roll == 10:
		dCome10 = comeBet
	return dCome4, dCome5, dCome6, dCome8, dCome9, dCome10

def comePayout(roll, come4, come5, come6, come8, come9, come10, c4Odds, c5Odds, c6Odds, c8Odds, c9Odds, c10Odds):
	payout = 0
	if roll == 4 and come4 > 0:
		print "You win $%d from the 4 come Bet." %come4
		if c4Odds > 0:
			print "You win $%d on the 4 from your Odds." %(c4Odds * 2)
		else:
			c4Odds = 0
		payout += come4 +  c4Odds * 2
	elif roll == 5 and come5 > 0:
		print "You win $%d from the Come 5." %come5
		if c5Odds > 0:
			print "You win $%d from your Odds on the 5." %(c5Odds/2 * 3)
		else:
			c5Odds = 0
		payout += come5 + c5Odds/2 * 3
	elif roll == 6 and come6 > 0:
		print "You win $%d on the Come 6." %come6
		if c6Odds > 0:
			print "You win $%d from your Odds on the 6." %(c6Odds/5 * 6)
		else:
			c6Odds = 0
		payout += come6 + c6Odds/5 * 6
	elif roll == 8 and come8 > 0:
		print "You win $%d on the Come 8." %come8
		if c8Odds > 0:
			print "You win $%d from your Odds on the 8." %(c8Odds/5 * 6)
		else:
			c8Odds = 0
		payout += come8 + c8Odds/5 * 6
	elif roll == 9 and come9 > 0:
		print "You win $%d on the Come 9." %come9
		if c9Odds > 0:
			print "You win $%d from your Odds on the 9." %(c9Odds/2 * 3)
		else:
			c9Odds = 0
		payout += come9 + c9Odds/2 * 3
	elif roll == 10 and come10 > 0:
		print "You win $%d on the Come 10." %come10
		if c10Odds > 0:
			print "You win $%d from your Odds on the 10." %(c10Odds * 2)
		else:
			c10Odds = 0
		payout += come10 + c10Odds * 2
	elif roll == 7 and (come4 + come5 + come6 + come8 + come9 + come10) > 0:
		allCome = come4 + come5 + come6 + come8 + come9 + come10 + c4Odds + c5Odds + c6Odds + c8Odds + c9Odds + c10Odds
		print "You lost $%d from your Come bets. All bets cleared." %allCome
		payout -= allCome
	return payout

def dComePayout(roll, dCome4, dCome5, dCome6, dCome8, dCome9, dCome10, dC4Odds, dC5Odds, dC6Odds, dC8Odds, dC9Odds, dC10Odds, pointIsOn):
	payout = 0
	if dCome4 > 0:
		if roll == 7:
			print "You win $%d on your Don't Come for the 4!" %dCome4
			if dC4Odds > 0:
				print "You win $%d from your Don't Come 4 Odds." %(dC4Odds * 2)
				payout += dC4Odds * 2
			payout += dCome4
		elif roll == 4:
			print "You lose $%d on your Don't Come 4." %dCome4
			if dC4Odds > 0 and pointIsOn == True:
				print "You lose $%d from your Don't Come 4 Odds." %dC4Odds
				payout -= dC4Odds
			payout -= dCome4

	if dCome5 > 0:
		if roll == 7:
			print "You win $%d on your Don't Come for the 5!" %dCome5
			if dC5Odds > 0:
				print "You win $%d from your Don't Come 5 Odds." %(dC5Odds/2 * 3)
				payout += dC5Odds/2 * 3
			payout += dCome5
		elif roll == 5:
			print "You lose $%d on your Don't Come 5." %dCome5
			if dC5Odds > 0 and pointIsOn == True:
				print "You lose $%d from your Don't Come 5 Odds." %dC5Odds
				payout -= dC5Odds
			payout -= dCome5

	if dCome6 > 0:
		if roll == 7:
			print "You win $%d on your Don't Come for the 6!" %dCome6
			if dC6Odds > 0:
				print "You win $%d from your Don't Come 6 Odds." %(dC6Odds/5 * 6)
				payout += dC6Odds/5 * 6
			payout += dCome6
		elif roll == 6:
			print "You lose $%d on your Don't Come 6." %dCome6
			if dC6Odds > 0 and pointIsOn == True:
				print "You lose $%d from your Don't Come 6 Odds." %dC6Odds
				payout -= dC6Odds
			payout -= dCome6

	if dCome8 > 0:
		if roll == 7:
			print "You win $%d on your Don't Come for the 8!" %dCome8
			if dC8Odds > 0:
				print "You win $%d from your Don't Come 8 Odds." %(dC8Odds/5 * 6)
				payout += dC8Odds/5 * 6
			payout += dCome8
		elif roll == 8:
			print "You lose $%d on your Don't Come 8." %dCome8
			if dC8Odds > 0 and pointIsOn == True:
				print "You lose $%d from your Don't Come 8 Odds." %dC8Odds
				payout -= dC8Odds
			payout -= dCome8

	if dCome9 > 0:
		if roll == 7:
			print "You win $%d on your Don't Come for the 9!" %dCome9
			if dC9Odds > 0:
				print "You win $%d from your Don't Come 9 Odds." %(dC9Odds/2 * 3)
				payout += dC9Odds/2 * 3
			payout += dCome9
		elif roll == 9:
			print "You lose $%d on your Don't Come 9." %dCome9
			if dC9Odds > 0 and pointIsOn == True:
				print "You lose $%d from your Don't Come 9 Odds." %dC9Odds
				payout -= dC9Odds
			payout -= dCome9

	if dCome10 > 0:
		if roll == 7:
			print "You win $%d on your Don't Come for the 10!" %dCome10
			if dC10Odds > 0:
				print "You win $%d from your Don't Come 10 Odds." %(dC10Odds * 2)
				payout += dC10Odds * 2
			payout += dCome10
		elif roll == 10:
			print "You lose $%d on your Don't Come 10." %dCome10
			if dC10Odds > 0 and pointIsOn == True:
				print "You lose $%d from your Don't Come 10 Odds." %dC10Odds
				payout -= dC10Odds
			payout -= dCome10
	return payout

def propPayout(roll, any7, anyCraps, cAndE, snakeEyes, aceDeuce, boxcars, horn):
	payout = 0
	if any7 > 0:
		if roll == 7:
			print "You win $%d on Any Seven!" %(any7 * 4)
			payout += any7 * 4
		else:
			print "You lose $%d on Any 7." %any7
			payout -= any7
	if anyCraps > 0:
		if roll in [2, 3, 12]:
			print "You win $%d on Any Craps!" %(anyCraps * 7)
			payout += anyCraps * 7
		else:
			print "You lose $%d on Any Craps." %anyCraps
			payout -= anyCraps
	if cAndE > 0:
		if roll in [2, 3, 12]:
			print "You win $%d for your C&E bet!" %(cAndE * 3)
			payout+= cAndE * 3
		elif roll == 11:
			print "You win $%d on your C&E bet!" %(cAndE * 7)
			payout += cAndE * 7
		else:
			print "You lose $%d on your C&E." %cAndE
			payout -= cAndE
	if snakeEyes > 0:
		if roll == 2:
			print "You win $%d on your Aces bet!" %(snakeEyes * 30)
			payout += snakeEyes * 30
		else:
			print "You lose $%d on your Aces bet." %snakeEyes
			payout -= snakeEyes
	if aceDeuce > 0:
		if roll == 3:
			print "You win $%d on your Acey-Deucey!" %(aceDeuce * 15)
			payout += aceDeuce * 15
		else:
			print "You lose $%d on your Acey-Deucey." %aceDeuce
			payout -= aceDeuce
	if boxcars > 0:
		if roll == 12:
			print "You win $%d on the Boxcars!" %(boxcars * 30)
			payout += boxcars * 30
		else:
			print "You lose $%d on the Boxcars bet." %boxcars
			payout -= boxcars
	if horn > 0:
		if roll in [2, 12]:
			print "You win $%d  on the Horn Bet!" %(horn * 30)
			payout += horn * 30
		elif roll in [3, 11]:
			print "You win $%d on the Horn bet!" %(horn * 15)
			payout += horn * 15
		else:
			print "You lose $%d from the Horn Bet." %horn
			payout -= horn

	return payout



def roll(point):
	hard = False
	d1 = randint(1,6)
	d2 = randint(1, 6)
	roll = d1 + d2
	print "You rolled %d and %d, a total of %d." %(d1, d2, roll)
	if d1 == d2 and roll in [4, 6, 8, 10]:
		print "%d the Hard Way!" %roll
		hard = True
	elif roll in [4, 6, 8, 10] and d1 != d2:
		print "%d Easy %d!" %(roll, roll)
		hard = False
	elif roll == 2:
		print "Snake Eyes!"
	elif roll == 12:
		print "Boxcars!"
	if roll == 3:
		print "Acey-Deucey!"
	elif roll == 5:
		print "5 No Field 5!"
	elif roll == 9:
		print "9 Niner!"
	elif roll == 11:
		print "Yo Eleven Yo!"

	if roll == 7:
		if point == False:
			print "7 Winner!"
		elif point == True:
			print "7 Out."

	return roll, hard

def odds(comingOut, bet, line):
	oddsOut = 0
	if comingOut in [4, 10]:
		if line == 'p':
			oddsOut = bet * 2
		elif line == 'd':
			oddsOut = bet/2
	elif comingOut in [5, 9]:
		if line == 'p':
			oddsOut = bet/2 * 3
		elif line == 'd':
			oddsOut = bet/3 * 2
	elif comingOut in [6, 8]:
		if line == 'p':
			oddsOut = bet/5 * 6
		elif line == 'd':
			oddsOut = bet/6 * 5

	return oddsOut

def press(p):
	press = raw_input("Press this bet? y/n")
	if press == 'y':
		print "What's your new bet?"
		p = betInput(bank)
		print "You now bet  $%d." %p
	else:
		pass
	return p

#Game Start
print "Oh Craps v.3.0"
print "How much would you like to cash in for your bank?"
while True:
	try:
		bank = int(raw_input("$"))
		break
	except ValueError:
		print "That wasn't a number, doofus."
		continue
print "Great, starting off with $%d." %bank


comeBet = dComeBet = 0
gameLoops = 0

while True:
	pointIsOn = False
	bet1 = 'a'
	passLine = 0
	dPass = 0
	fieldBet = 0

#Empty Bank check
	if bank <= 0:
		print "You are totally out of money!"
		print "Add more to your bank or hit Ctrl-C to exit the game, walking away with a sad, empty wallet."
		while True:
			try:
				bank += +int(raw_input("$"))
			except ValueError:
				print "That wasn't a number, try again."
				continue
			if bank < 0:
				print "You fail at math. Try again!"
				bank = 0
				continue
			else:
				print "Great, starting you off again with $%d." %bank
				break
	else:
		pass



	lineBets = raw_input("Line Bets? y/n")
	if lineBets == 'y':
		bet1 = raw_input("Pass or Don't pass?")
		if bet1 == 'p':
			print "How much on the Pass Line?"
			passLine = betInput(bank)
			print "Great, $%d on the Pass Line." %passLine
		elif bet1 == 'd':
			print "How much on the Don't Pass Line?"
			dPass = betInput(bank)
			print "Great, $%d on the Don't Pass Line." %dPass
		else:
			print "Pass or Don't Pass, there is nothing else!"
			continue
	fBet = raw_input("Bet the Field? y/n")
	if fBet == 'y':
		print "How much on the Field?"
		fieldBet = betInput(bank)
		print "Ok, $%d on the Field." %fieldBet

	propStart = raw_input("Proposition Bets?")
	if propStart == 'y':
		any7, anyCraps, cAndE, snakeEyes, aceDeuce, boxcars, horn = prop()

	print "Dice are coming out!"
	comingOut, coHard = roll(pointIsOn)

	if (come4 + come5 + come6 + come8 + come9 + come10) > 0:
		bank += comePayout(comingOut, come4, come5, come6, come8, come9, come10, c4Odds, c5Odds, c6Odds, c8Odds, c9Odds, c10Odds)
	if (dCome4 + dCome5 + dCome6 + dCome8 + dCome9 + dCome10) > 0:
		bank += dComePayout(comingOut, dCome4, dCome5, dCome6, dCome8, dCome9, dCome10, dC4Odds, dC5Odds, dC6Odds, dC8Odds, dC9Odds, dC10Odds, pointIsOn)
		if comingOut == 4 and dCome4 > 0:
			dCome4 = dC4Odds = 0
		elif comingOut == 5 and dCome5 > 0:
			dCome5 = dC5Odds = 0
		elif comingOut == 6 and dCome6 > 0:
			dCome6 = dC6Odds = 0
		elif comingOut == 8 and dCome8 > 0:
			dCome8 = dC8Odds = 0
		elif comingOut == 9 and dCome9 > 0:
			dCome9 = dC9Odds = 0
		elif comingOut == 10 and dCome10 > 0:
			dCome10 = dC10Odds = 0
	if comingOut == 7:
		come4 = come5 = come6 = come8 = come9 = come10 = c4Odds = c5Odds = c6Odds = c8Odds = c9Odds = c10Odds = 0

	if comingOut == 4 and come4 > 0:
		come4 = c4Odds = 0
	if comingOut == 5 and come5 > 0:
		come5 = c5Odds = 0
	if comingOut == 6 and come6 > 0:
		come6 = c6Odds = 0
	if comingOut == 8 and come8 > 0:
		come8 = c8Odds = 0
	if comingOut == 9 and come9 > 0:
		come9 = c9Odds = 0
	if comingOut == 10 and come10 > 0:
		come10 = come10Odds = 0
			
		
	bank += propPayout(comingOut, any7, anyCraps, cAndE, snakeEyes, aceDeuce, boxcars, horn)
	if comingOut in [7, 11]:
		if bet1 == 'p':
			print "You won $%d!" %passLine
			bank += passLine
		elif bet1 == 'd':
			print "You lost $%d." %dPass
			bank -= dPass
		if comingOut == 7 and fieldBet > 0:
			print "You lose $%d on the Field." %fieldBet
			bank -= fieldBet
			fieldBet = 0
		elif comingOut == 11 and fieldBet > 0:
			print "You win $%d on the Field!" %fieldBet
			bank += fieldBet
		print "You now have $%d in your bank." %bank
		continue
	elif comingOut in [2, 3, 12]:
		if bet1 == 'p':
			print "You lost $%d." %passLine
			bank -= passLine
		elif bet1 == 'd':
			print "You win $%d!" %dPass
			bank += dPass
		if fieldBet > 0 and comingOut == 2:
			print "You win double on the Field! $%d coming to you." %(fieldBet * 2)
			bank += fieldBet * 2
		elif fieldBet > 0 and comingOut == 12:
			print "You win triple on the Field! $%d coming to you." %(fieldBet * 3)
			bank += fieldBet * 3
		elif fieldBet > 0 and comingOut == 3:
			print "You win $%d on the Field!" %fieldBet
			bank += fieldBet
		print "You now have $%d in your bank." %bank
		continue
	else:
		pointIsOn = True
		print "The point is %d." %comingOut
		if comingOut in [4, 9, 10] and fieldBet > 0:
			print "You win $%d on the Field!" %fieldBet
			bank += fieldBet
		elif comingOut in [5, 6, 8] and fieldBet > 0:
			print "You lose $%d on the Field." %fieldBet
			bank -= fieldBet
			fieldBet = 0
		pOddsBet = raw_input("Odds on your Line bet? y/n")
		if pOddsBet == 'y':
			if bet1 == 'p':
				print "How much for your Pass Line Odds?"
				passOdds = betInput(bank)
			elif bet1 == 'd':
				print "How much to Lay against the %d?" %comingOut
				passOdds = betInput(bank)
		else:
			passOdds = 0
		#Betting
		while True:
			gameLoops += 1
			if gameLoops == 14:
				clearScreen()
				gameLoops = 0
			any7 = anyCraps = cAndE = snakeEyes = aceDeuce = boxcars = horn = 0
			placeBet = raw_input("Place bets? y/n")
			if placeBet == 'y':
				if four > 0:
					print You have $%d wagered on the Place 4. What's your new bet?" %four
				else:
					print "How much on the Place 4?"
				four = betInput(bank)
				if five > 0:
					print "You have $%d wagered on the Place 5. What's your new bet?" %five
				else:
					print "How much on the Place 5?"
				five = betInput(bank)
				if six > 0:
					print "You have $%d wagered on the Place 6. What's your new bet?" %six
				else:
					print "How much on the Place 6?"
				six = betInput(bank)
				if eight > 0:
					print "You have $%d wagered on the Place 8. What's your new bet?" %eight
				else:
					print "How much on the place 8?"
				eight = betInput(bank)
				if nine > 0:
					print "Yu have $%d wagered on the Place 9. What's your new bet?" %nine
				else:
					print "How much on the Place 9?"
				nine = betInput(bank)
				if ten > 0:
					print "You have $%d wagered on the Place 10. What's your new bet?" %ten
				else:
					print "How much on the Place 10?"
				ten = betInput(bank)

#Come Bet
			if come4 > 0 and c4Odds == 0:
				print "You have $%d on the 4." %come4
			elif c4Odds > 0:
				print "You have $%d on the 4 with $%d in Odds." %(come4, c4Odds)
			if come5 > 0 and c5Odds == 0:
				print "You have $%d on the 5." %come5
			elif c5Odds > 0:
				print "You have $%d on the 5 with $%d in Odds." %(come5, c5Odds)
			if come6 > 0 and c6Odds == 0:
				print "You have $%d on the 6." %come6
			elif c6Odds > 0:
				print "You have $%d on the 6 with $%d in Odds." %(come6, c6Odds)
			if come8 > 0 and c8Odds == 0:
				print "You have $%d on the 8." %come8
			elif c8Odds > 0:
				print "You have $%d on the 8 with $%d in Odds." %(come8, c8Odds)
			if come9 > 0 and c9Odds == 0:
				print "You have $%d on the 9." %come9
			elif c9Odds > 0:
				print "You have $%d on the 9 with $%d in Odds." %(come9, c9Odds)
			if come10 > 0 and c10Odds == 0:
				print "You have $%d on the 10." %come10
			elif c10Odds > 0:
				print "You have $%d on the 10 with $%d in Odds." %(come10, c10Odds)
#Don't Come
			if dCome4 > 0 and dC4Odds == 0:
				print "You have $%d on the Don't Come 4." %dCome4
			elif dC4Odds > 0:
				print "You have $%d on the Don't Come 4 with $%d in Odds." %(dCome4, dC4Odds)
			if dCome5 > 0 and dC5Odds == 0:
				print "You have $%d on the Don't Come 5." %dCome5
			elif dC5Odds > 0:
				print "You have $%d on the Don't Come 5 with $%d in Odds." %(dCome5, dC5Odds)
			if dCome6 > 0 and dC6Odds == 0:
				print "You have $%d on the Don't Come 6." %dCome6
			elif dC6Odds > 0:
				print "You have $%d on the Don't Come 6 with $%d in Odds." %(dCome6, dC6Odds)
			if dCome8 >0 and dC8Odds == 0:
				print "You have $%d on the Don't Come 8.." %dCome8
			elif dC8Odds > 0:
				print "You have $%d on the Don't Come 8 with $%d in Odds." %(dCome8, dC8Odds)
			if dCome9 > 0 and dC9Odds == 0:
				print "You have $%d on the Don't Come 9." %dCome9
			elif dC9Odds > 0:
				print "You have $%d on the Don't Come 9 with $%d in Odds." %(dCome9, dC9Odds)
			if dCome10 > 0 and dC10Odds == 0:
				print "You have $%d on the Don't Come 10." %dCome10
			elif dC10Odds > 0:
				print "You have $%d on the Don't Come 10 with $%d in Odds." %(dCome10, dC10Odds)

			cmBet = raw_input("Come bet? y/n")
			if cmBet == 'y':
				comeChoice = raw_input("Come or Don't Come?")
				if comeChoice == 'c':
					print "How much on the Come?"
					comeBet = betInput(bank)
					print "Ok, $%d in the Come." %comeBet
				elif comeChoice == 'd':
					print "How much on the Don't Come?"
					dComeBet = betInput(bank)
					print "Ok, $%d on the Don't Come." %dComeBet

#Field Bet

			fBet = raw_input("Bet the Field? You have $%d wagered. y/n" %fieldBet)
			if fBet == 'y':
				print "How much on the Field?"
				fieldBet = betInput(bank)
			#else:
				#fieldBet = 0

#Hard Ways
			hWays = raw_input("Bet the hard ways? y/n")
			if hWays == 'y':
				print "How much on Hard 4?"
				hard4 = betInput(bank)
				print "How much on Hard 6?"
				hard6 = betInput(bank)
				print "How much on Hard 8?"
				hard8 = betInput(bank)
				print "How much on Hard 10?"
				hard10 = betInput(bank)
				print "Ok, $%d, $%d, $%d, $%d on the 4, 6, 8, and 10!" %(hard4, hard6, hard8, hard10)
#Prop Bets
			props = raw_input("Proposition Bets? y/n")
			if props == 'y':
				any7, anyCraps, cAndE, snakeEyes, aceDeuce, boxcars, horn = prop()

			print "Dice are rolling!"
			#raw_input("Hit Enter to roll again.")
#Phase 2 Roll
			p2, p2Hard = roll(pointIsOn)


			bank += comePayout(p2, come4, come5, come6, come8, come9, come10, c4Odds, c5Odds, c6Odds, c8Odds, c9Odds, c10Odds)

			bank += dComePayout(p2, dCome4, dCome5, dCome6, dCome8, dCome9, dCome10, dC4Odds, dC5Odds, dC6Odds, dC8Odds, dC9Odds, dC10Odds, pointIsOn)

			if p2 == 4:
				if come4 > 0:
					come4 = c4Odds = 0
				if dCome4 > 0:
					dCome4 = dC4Odds = 0
			elif p2 == 5:
				if come5 > 0:
					come5 = c5Odds = 0
				if dCome5 > 0:
					dCome5 = dC5Odds = 0
			elif p2 == 6:
				if come6 > 0:
					come6 = c6Odds = 0
				if dCome6 > 0:
					dCome6 = dC6Odds = 0
			elif p2 == 8:
				if come8 > 0:
					come8 = c8Odds = 0
				if dCome8 > 0:
					dCome8 = dC8Odds = 0
			elif p2 == 9:
				if come9 > 0:
					come9 = c9Odds = 0
				if dCome9 > 0:
					dCome9 = dC9Odds = 0
			elif p2 == 10:
				if come10 > 0:
					come10 = c10Odds = 0
				if dCome10 > 0:
					dCome10 = dC10Odds = 0

			if comeBet > 0:
				if p2 in [7, 11]:
					print "You win $%d on the Come!" %comeBet
					bank += comeBet
				elif p2 in [2, 3, 12]:
					print "You lose $%d from the Come." %comeBet
					bank -= comeBet
				else:
					come4, come5, come6, come8, come9, come10 = come(p2, comeBet, come4, come5, come6, come8, come9, come10)
					cOdds = raw_input("Odds on your Come bet? y/n")
					if cOdds == 'y':
						if p2 == 4:
							print "Odds on the 4?"
							c4Odds = betInput(bank)
							print "Ok, $%d on the 4." %c4Odds
						elif p2 == 5:
							print "Odds on the 5?"
							c5Odds = betInput(bank)
							print "Ok, $%d on the 5." %c5Odds
						elif p2 == 6:
							print "Odds on the 6?"
							c6Odds = betInput(bank)
							print "Ok,$%d on the 6." %c6Odds
						elif p2 == 8:
							print "Odds on the 8?"
							c8Odds = betInput(bank)
							print "Ok, $%d on the 8." %c8Odds
						elif p2 == 9:
							print "Odds on the 9?"
							c9Odds = betInput(bank)
							print "Ok, $%d on the 9." %c9Odds
						elif p2 == 10:
							print "Odds on the 10?"
							c10Odds = betInput(bank)
							print "Ok, $%d on the 10." %c10Odds
				comeBet = 0

#Don't Come
			if dComeBet > 0:
				if p2 in [2, 3, 12]:
					print "You win $%d on the Don't Come!" %dComeBet
					bank += dComeBet
				elif p2 in [7, 11]:
					print "You lose $%d from the Don't Come." %dComeBet
					bank -= dComeBet
				else:
					dCome4, dCome5, dCome6, dCome8, dCome9, dCome10 = dCome(p2, dComeBet, dCome4, dCome5, dCome6, dCome8, dCome9, dCome10)
					dcOdds = raw_input("Odds on your Don't Come bet? y/n")
					if dcOdds == 'y':
						if p2 == 4:
							print "Odds on the Don't Come 4?"
							dC4Odds = betInput(bank)
							print "Ok, $%d on the 4." %dC4Odds
						elif p2 == 5:
							print "Odds on the Don't Come 5?"
							dC5Odds = betInput(bank)
							print "Ok, $%d on the 5." %dC5Odds
						elif p2 == 6:
							print "Odds on the Don't Come 6?"
							dC6Odds = betInput(bank)
							print "Ok,$%d on the 6." %dC6Odds
						elif p2 == 8:
							print "Odds on the Don't Come 8?"
							dC8Odds = betInput(bank)
							print "Ok, $%d on the 8." %dC8Odds
						elif p2 == 9:
							print "Odds on the Don't Come 9?"
							dC9Odds = betInput(bank)
							print "Ok, $%d on the 9." %dC9Odds
						elif p2 == 10:
							print "Odds on the Don't Come 10?"
							dC10Odds = betInput(bank)
							print "Ok, $%d on the 10." %dC10Odds
				dComeBet = 0

#Prop Bet Payout
			bank += propPayout(p2, any7, anyCraps, cAndE, snakeEyes, aceDeuce, boxcars, horn)


			if fieldBet != 0:
				if p2 == 2:
					print "You win double on the Field! $%d coming to you." %(fieldBet * 2)
					bank += fieldBet * 2
				elif p2 == 12:
					print "You win triple on the Field! $%d coming to you." %(fieldBet * 3)
					bank += fieldBet * 3
				elif p2 in [3, 4, 9, 10, 11]:
					print "You win on the Field! $%d coming to you." %fieldBet
					bank += fieldBet
				else:
					print "You lose $%d on the Field." %fieldBet
					bank -= fieldBet
					fieldBet = 0
	
#Hard Ways payout
			if p2 == 4 and p2Hard == True and hard4 > 0:
				print "You win $%d on the Hard 4!" %(hard4 * 7)
				bank += hard4 * 7
			elif p2 == 4 and p2Hard == False and hard4 > 0:
				print "You lose $%d on the Hard 4." %hard4
				bank -= hard4
				hard4 = 0
			else:
				pass
			if p2 == 6 and p2Hard == True and hard6 > 0:
				print "You win $%d on the Hard 6!" %(hard6 * 9)
				bank += hard6 * 9
			elif p2 == 6 and p2Hard == False and hard6 >0:
				print "You lose $%d on the Hard 6." %hard6
				bank -= hard6
				hard6 = 0
			else:
				pass
			if p2 == 8 and p2Hard == True and hard8 > 0:
				print "You win $%d on the Hard 8!" %(hard8 * 9)
				bank += hard8 * 9
			elif p2 == 8 and p2Hard == False and hard8 > 0:
				print "You lose $%d on the Hard 8." %hard8
				bank -= hard8
				hard8 = 0
			else:
				pass
			if p2 == 10 and p2Hard == True and hard10 > 0:
				print "You win $%d on the Hard 10!" %(hard10 * 7)
				bank += hard10 * 7
			elif p2 == 10 and p2Hard == False and hard10 > 0:
				print "You lose $%d on the Hard 10." %hard10
				bank -= hard10
				hard10 = 0
			else:
				pass

			if p2 == 4 and four > 0:
				win4 = (four/5) * 9
				print "You win $%d on the place 4." %win4
				bank += win4
				if comingOut != 4:
					four = press(four)
			if p2 == 5 and five > 0:
				win5 = (five/5) * 7
				print "You win $%d on the place 5." %win5
				bank += win5
				if comingOut != 5:
					five = press(5)
			if p2 == 6 and six > 0:
				print "You win $%d on the place 6." %(six/6 * 7)
				bank += six/6 * 7
				if comingOut != 6:
					six = press(six)

			if p2 == 8 and eight > 0:
				print "You win $%d on the place Eight." %(eight/6 * 7)
				bank += eight/6 * 7
				if comingOut != 8:
					eight = press(eight)
			if p2 == 9 and nine > 0:
				win9 = (nine/5) * 7
				print "You win $%d on the place 9!" %win9
				bank += win9
				if comingOut != 9:
					nine = press(nine)

			if p2 == 10 and ten > 0:
				win10 = (ten/5) * 9
				print "You win $%d on the place 10." %win10
				bank += win10
				if comingOut != 10:
					ten = press(ten)
			if p2 == comingOut:
				if bet1 == 'p':
					print "You win $%d!" %passLine
					if passOdds > 0:
						oddsWin = odds(comingOut, passOdds, bet1)
						print "You win $%d on your odds." %oddsWin
						bank += oddsWin
					bank += passLine
				elif bet1 == 'd':
					print "You lose $%d." %dPass
					if passOdds > 0:
						print "You lose $%d from your odds." %passOdds
						bank -= passOdds
					bank -= dPass
				break
#Seven Out
			elif p2 == 7:
				come4 = come5 = come6 = come8 = come9 = come10 = c4Odds = c5Odds  = c6Odds = c8Odds = c9Odds = c10Odds = 0
				if hard4 + hard6 + hard8 + hard10 > 0:
					print "You lose $%d from the Hard Ways." %(hard4 + hard6 + hard8 + hard10)
					bank -= (hard4 + hard6 + hard8 + hard10)
					hard4 = hard6 = hard8 = hard10 = 0
				if (four + five + six + eight + nine + ten) > 0:
					print "You lose $%d from the place bets." %(four + five + six + eight + nine + ten)
					bank -= (four + five + six + eight + nine + ten)
					four = five = six = eight = nine = ten = 0
				if bet1 == 'p':
					print "You lose $%d." %passLine
					if passOdds > 0:
						print "You lose $%d from your odds." %passOdds
						bank -= passOdds
					bank -= passLine
				elif bet1 == 'd':
					print "You win $%d!" %dPass
					if passOdds > 0:
						dOdds = odds(comingOut, passOdds, bet1)
						print "You won $%d on your Don't Pass Odds." %dOdds
						bank += dOdds
					bank += dPass
				if any7 > 0:
					print "You win $%d on Any 7!" %(any7 * 4)
					bank += any7 * 4
					any7 = 0
					

				break
			else:
				print "Bank = $%d. The point is %d." %(bank, comingOut)
				#raw_input("Roll Again!")
				continue
		print "You have $%d in your bank!" %bank
	clearScreen()
	continue