#!/usr/bin/env python

from random import *

# General Bet variable designation
four = five = six = eight = nine = ten = hard4 = hard6 = hard8 = hard10 = come4 = come5 = come6 = come8 = come9 = come10 = c4Odds = c5Odds = c6Odds = c8Odds = c9Odds = c10Odds = any7 = anyCraps = cAndE = snakeEyes = aceDeuce = boxcars = horn = eleven = passOdds = 0

# Don't Come variable designation
dCome4 = dCome5 = dCome6 = dCome8 = dCome9 = dCome10 = dC4Odds = dC5Odds = dC6Odds = dC8Odds = dC9Odds = dC10Odds = lay4 = lay5 = lay6 = lay8 = lay9 = lay10 = atsAll = atsSmall = atsTall = 0
smallNumbers = []
tallNumbers = []
ats = []
atsOn = False

def setClear():
	global ats, smallNumbers, tallNumbers
	smallSet = [2, 3, 4, 5, 6]
	tallSet = [8, 9, 10, 11, 12]
	allSet = smallSet + tallSet
	if set(smallNumbers) == set(smallSet):
		smallNumbers = []
	if set(tallNumbers) == set(tallSet):
		tallNumbers = []
	if set(ats) == set(allSet):
		ats = []

def allTallSmall():
	global atsAll, atsTall, atsSmall
	print "How much on the All?"
	atsAll = input("$>")
	print "Ok, ${} on the All.".format(atsAll)
	print "How much on the Tall?"
	atsTall = input("$>")
	print "Ok, ${} on the Tall.".format(atsTall)
	print "How much on the Small?"
	atsSmall = input("$>")
	print "Ok ${} on the Small.".format(atsSmall)

def atsCheck(roll):
	global atsAll, atsTall, atsSmall, bank, ats, smallNumbers, tallNumbers

	allSet = [2, 3, 4, 5, 6, 8, 9, 10, 11, 12]
	tallSet = [8, 9, 10, 11, 12]
	smallSet = [2, 3, 4, 5, 6]
	if set(smallNumbers) == set(smallSet):
		print "You hit the Small and won ${}!".format(atsSmall * 35)
		bank += atsSmall * 35
		atsSmall = 0
		smallNumbers = []
	if set(tallNumbers) == set(tallSet):
		print "You hit the Tall and won ${}!".format(atsTall * 35)
		bank += atsTall * 35
		atsTall = 0
		tallNumbers = []
	if set(ats) == set(allSet):
		print "You hit the All and won ${}".format(atsAll * 176)
		bank += atsAll * 176
		atsAll = 0
		ats= smallNumbers = tallNumbers = []
	if roll == 7 and (atsAll + atsTall + atsSmall) > 0:
		ats = smallNumbers = tallNumbers = []
		bank -= atsAll + atsSmall + atsTall
		print("You lost ${} from the All Tall Small.".format(atsAll+atsSmall+atsTall))
		atsAll = atSmall = atsTall = 0

def atsAdd(roll):
	global ats, smallNumbers, tallNumbers
	if roll in [2, 3, 4, 5, 6]:
		if roll not in smallNumbers:
			smallNumbers.append(roll)
	elif roll in [8, 9, 10, 11, 12]:
		if roll not in tallNumbers:
			tallNumbers.append(roll)
	if roll not in ats:
		ats.append(roll)

def betInput():
	global bank
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
				print "Great, starting you off again with ${}.".format(bank)
				break

	while True:
		while True:
			try:
				bet = int(raw_input("$>"))
				break
			except ValueError:
				print "That wasn't a number! The stickman whaps you upside the head with his stick."
				continue
		if bet > bank:
			print "You simply can't bet that much! You only have ${} in the bank.".format(bank)
			continue
		elif bet < 0:
			print "Nice try, but that's not gonna work!"
			continue
		else:
			break

	return bet

def hardPay(roll, hard, hard4, hard6, hard8, hard10):
	payout = 0
	if roll == 4 and hard == True and hard4 > 0:
		print "You win ${} on the Hard 4!".format(hard4 * 7)
		payout += hard4 * 7
	elif roll == 4 and hard == False and hard4 > 0:
		print "You lose ${} on the Hard 4.".format(hard4)
		payout -= hard4

	if roll == 6 and hard == True and hard6 > 0:
		print "You win ${} on the Hard 6!".format(hard6 * 9)
		payout += hard6 * 9
	elif roll == 6 and hard == False and hard6 >0:
		print "You lose ${} on the Hard 6.".format(hard6)
		payout -= hard6

	if roll == 8 and hard == True and hard8 > 0:
		print "You win ${} on the Hard 8!".format(hard8 * 9)
		payout += hard8 * 9
	elif roll == 8 and hard == False and hard8 > 0:
		print "You lose ${} on the Hard 8.".format(hard8)
		payout -= hard8

	if roll == 10 and hard == True and hard10 > 0:
		print "You win ${} on the Hard 10!".format(hard10 * 7)
		payout += hard10 * 7
	elif roll == 10 and hard == False and hard10 > 0:
		print "You lose ${} on the Hard 10.".format(hard10)
		payout -= hard10

	return payout

def prop():
	any7 = anyCraps = cAndE = snakeEyes = aceDeuce = boxcars = horn = eleven = 0

	while True:
		propPick = raw_input("Type in your Prop Bet: ")
		if propPick in ['7', 'seven', 'big red', 'Seven', 'any 7', 'Any 7', 'Any Seven', 'Any seven', 'any seven']:
			print "How much on Any 7?"
			any7 = betInput()
			print "Ok, ${} on Any 7.".format(any7)
			continue
		elif propPick in ['cr', 'CR', 'Cr', 'any craps', 'Any Craps', 'Any craps', 'craps', 'Craps']:
			print "How much on Any Craps?"
			anyCraps = betInput()
			print "Ok, ${} on Any Craps.".format(anyCraps)
			continue
		elif propPick in ['ce', 'CE', 'craps and eleven', 'Craps and Eleven', 'craps and 11', 'c and e', 'C and E', "C&E"]:
			print "How much on C & E?"
			cAndE = betInput()
			print "Ok, ${} on C&E.".format(cAndE)
			continue
		elif propPick == "sn" or propPick in ['s', 'S', 'snake', 'snakeyes', 'snake eyes', 'Snake Eyes', 'snakeeyes', 'aces', 'Aces', 'ace ace', '2']:
			print "How much on Snake Eyes?"
			snakeEyes = betInput()
			print "Ok, ${} on Snake Eyes.".format(snakeEyes)
			continue
		elif propPick in ['ad', 'three', '3', 'AD', 'ace deuce', 'acey deucey', 'Three', '3']:
			print "How much on Acey-Deucey?"
			aceDeuce = betInput()
			print "Ok, ${} on Acey-Deucey.".format(aceDeuce)
			continue
		elif propPick in ['b', 'B', 'boxcars', 'Boxcars', 'Box Cars', 'box cars', '12', 'twelve', 'Twelve', 'six six', '66']:
			print "How much on Boxcars?"
			boxcars = betInput()
			print "Ok, ${} on Boxcars.".format(boxcars)
			continue
		elif propPick in ["h", 'horn', 'H', 'Horn']:
			print "How much on the Horn?"
			horn = betInput()
			print "Ok, ${} on the Horn Bet!".format(horn)
			continue
		elif propPick in ['11', 'eleven', '56', 'Eleven', 'yo', 'Yo', 'Yo Eleven']:
			print "How much on the Eleven?"
			eleven = betInput()
			print "Ok, ${} on the Eleven.".format(eleven)
			continue
		elif propPick in ['all', 'All', 'all bets', 'All Bets', 'Show All Bets', 'show all bets']:
			print "Current prop bets:"
			if any7 > 0:
				print "${} on Any 7.".format(any7)
			if anyCraps > 0:
				print "${} on Any Craps.".format(anyCraps)
			if cAndE > 0:
				print "${} on C&E.".format(cAndE)
			if snakeEyes > 0:
				print "${} on Snake Eyes.".format(snakeEyes)
			if aceDeuce > 0:
				print "${} on Acey-Deucey.".format(aceDeuce)
			if horn > 0:
				print "${} on the Horn.".format(horn)
			if eleven > 0:
				print "${} on the Eleven.".format(eleven)
			raw_input("Hit Enter to continue >")
			continue
		elif propPick == "help":
			print "Use the following codes in the bet prompt to place that specific bet:\n\t7 - Any Seven\n\tcr - Any Craps\n\tce - Craps and Eleven\n\ts, 2 - Snake Eyes\n\tad, 3 - Acey Deucey\n\tb, 12 - Boxcars\n\th, horn - Horn Bet\n\t11, eleven, 56 - Yo Eleven\n\tall - Show all bets\n\tx - Exit prop betting and return to game"
			raw_input("Hit Enter to continue >")
			continue
		elif propPick in ["x", 'X', 'exit', 'Exit']:
			break
		else:
			print "That's not a valid bet, and the boxman glares at you in disgust. Try again, or type 'x' and hit Enter to exit."

	return any7, anyCraps, cAndE, snakeEyes, aceDeuce, boxcars, horn, eleven

def come(roll, comeBet, come4, come5, come6, come8, come9, come10):
	print "Moving Come Bet to the {}.".format(roll)
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
	print "Moving Don't Come Bet to the {}.".format(roll)
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

def comePayout(roll, come4, come5, come6, come8, come9, come10, c4Odds, c5Odds, c6Odds, c8Odds, c9Odds, c10Odds, pointIsOn):
	payout = 0
	if roll == 4 and come4 > 0:
		print "You win ${} from the 4 come Bet.".format(come4)
		if c4Odds > 0:
			print "You win ${} on the 4 from your Odds.".format(c4Odds * 2)
		else:
			c4Odds = 0
		payout += come4 +  c4Odds * 2
	elif roll == 5 and come5 > 0:
		print "You win ${} from the Come 5.".format(come5)
		if c5Odds > 0:
			print "You win ${} from your Odds on the 5.".format(c5Odds/2 * 3)
		else:
			c5Odds = 0
		payout += come5 + c5Odds/2 * 3
	elif roll == 6 and come6 > 0:
		print "You win ${} on the Come 6.".format(come6)
		if c6Odds > 0:
			print "You win ${} from your Odds on the 6.".format(c6Odds/5 * 6)
		else:
			c6Odds = 0
		payout += come6 + c6Odds/5 * 6
	elif roll == 8 and come8 > 0:
		print "You win ${} on the Come 8.".format(come8)
		if c8Odds > 0:
			print "You win ${} from your Odds on the 8.".format(c8Odds/5 * 6)
		else:
			c8Odds = 0
		payout += come8 + c8Odds/5 * 6
	elif roll == 9 and come9 > 0:
		print "You win ${} on the Come 9.".format(come9)
		if c9Odds > 0:
			print "You win ${} from your Odds on the 9.".format(c9Odds/2 * 3)
		else:
			c9Odds = 0
		payout += come9 + c9Odds/2 * 3
	elif roll == 10 and come10 > 0:
		print "You win ${} on the Come 10.".format(come10)
		if c10Odds > 0:
			print "You win ${} from your Odds on the 10.".format(c10Odds * 2)
		else:
			c10Odds = 0
		payout += come10 + c10Odds * 2
	elif roll == 7 and (come4 + come5 + come6 + come8 + come9 + come10) > 0 and pointIsOn == True:
		allCome = come4 + come5 + come6 + come8 + come9 + come10 + c4Odds + c5Odds + c6Odds + c8Odds + c9Odds + c10Odds
		print "You lost ${} from your Come bets and Odds. All bets cleared.".format(allCome)
		payout -= allCome
	elif roll == 7 and (come4 + come5 + come6 + come8 + come9 + come10) > 0 and pointIsOn == False:
		onlyCome = (come4 + come5 + come6 + come8 + come9 + come10)
		print "You lost ${} from your Come bets. All Odds were off and returned to you.".format(onlyCome)
		payout -= onlyCome

	return payout

def dComePayout(roll, dCome4, dCome5, dCome6, dCome8, dCome9, dCome10, dC4Odds, dC5Odds, dC6Odds, dC8Odds, dC9Odds, dC10Odds, pointIsOn):
	payout = 0
	if dCome4 > 0:
		if roll == 7:
			print "You win ${} on your Don't Come for the 4!".format(dCome4)
			if dC4Odds > 0:
				print "You win ${} from your Don't Come 4 Odds.".format(dC4Odds / 2)
				payout += dC4Odds / 2
			payout += dCome4
		elif roll == 4:
			print "You lose ${} on your Don't Come 4.".format(dCome4)
			if dC4Odds > 0 and pointIsOn == True:
				print "You lose ${} from your Don't Come 4 Odds.".format(dC4Odds)
				payout -= dC4Odds
			payout -= dCome4

	if dCome5 > 0:
		if roll == 7:
			print "You win ${} on your Don't Come for the 5!".format(dCome5)
			if dC5Odds > 0:
				print "You win ${} from your Don't Come 5 Odds.".format(dC5Odds/3 * 2)
				payout += dC5Odds/3 * 2
			payout += dCome5
		elif roll == 5:
			print "You lose ${} on your Don't Come 5.".format(dCome5)
			if dC5Odds > 0 and pointIsOn == True:
				print "You lose ${} from your Don't Come 5 Odds.".format(dC5Odds)
				payout -= dC5Odds
			payout -= dCome5

	if dCome6 > 0:
		if roll == 7:
			print "You win ${} on your Don't Come for the 6!".format(dCome6)
			if dC6Odds > 0:
				print "You win ${} from your Don't Come 6 Odds.".format(dC6Odds/6 * 5)
				payout += dC6Odds/6 * 5
			payout += dCome6
		elif roll == 6:
			print "You lose ${} on your Don't Come 6.".format(dCome6)
			if dC6Odds > 0 and pointIsOn == True:
				print "You lose ${} from your Don't Come 6 Odds.".format(dC6Odds)
				payout -= dC6Odds
			payout -= dCome6

	if dCome8 > 0:
		if roll == 7:
			print "You win ${} on your Don't Come for the 8!".format(dCome8)
			if dC8Odds > 0:
				print "You win ${} from your Don't Come 8 Odds.".format(dC8Odds/6 * 5)
				payout += dC8Odds/6 * 5
			payout += dCome8
		elif roll == 8:
			print "You lose ${} on your Don't Come 8.".format(dCome8)
			if dC8Odds > 0 and pointIsOn == True:
				print "You lose ${} from your Don't Come 8 Odds.".format(dC8Odds)
				payout -= dC8Odds
			payout -= dCome8

	if dCome9 > 0:
		if roll == 7:
			print "You win ${} on your Don't Come for the 9!".format(dCome9)
			if dC9Odds > 0:
				print "You win ${} from your Don't Come 9 Odds.".format(dC9Odds/3 * 2)
				payout += dC9Odds/3 * 2
			payout += dCome9
		elif roll == 9:
			print "You lose ${} on your Don't Come 9.".format(dCome9)
			if dC9Odds > 0 and pointIsOn == True:
				print "You lose ${} from your Don't Come 9 Odds.".format(dC9Odds)
				payout -= dC9Odds
			payout -= dCome9

	if dCome10 > 0:
		if roll == 7:
			print "You win ${} on your Don't Come for the 10!".format(dCome10)
			if dC10Odds > 0:
				print "You win ${} from your Don't Come 10 Odds.".format(dC10Odds / 2)
				payout += dC10Odds / 2
			payout += dCome10
		elif roll == 10:
			print "You lose ${} on your Don't Come 10.".format(dCome10)
			if dC10Odds > 0 and pointIsOn == True:
				print "You lose ${} from your Don't Come 10 Odds.".format(dC10Odds)
				payout -= dC10Odds
			payout -= dCome10
	return payout

def propPayout(roll, any7, anyCraps, cAndE, snakeEyes, aceDeuce, boxcars, horn, eleven):
	payout = 0
	if any7 > 0:
		if roll == 7:
			print "You win ${} on Any Seven!".format(any7 * 4)
			payout += any7 * 4
		else:
			print "You lose ${} on Any 7.".format(any7)
			payout -= any7
	if anyCraps > 0:
		if roll in [2, 3, 12]:
			print "You win ${} on Any Craps!".format(anyCraps * 7)
			payout += anyCraps * 7
		else:
			print "You lose ${} on Any Craps.".format(anyCraps)
			payout -= anyCraps
	if cAndE > 0:
		if roll in [2, 3, 12]:
			print "You win ${} for your C&E bet!".format(cAndE * 3)
			payout+= cAndE * 3
		elif roll == 11:
			print "You win ${} on your C&E bet!".format(cAndE * 7)
			payout += cAndE * 7
		else:
			print "You lose ${} on your C&E.".format(cAndE)
			payout -= cAndE
	if snakeEyes > 0:
		if roll == 2:
			print "You win ${} on your Aces bet!".format(snakeEyes * 30)
			payout += snakeEyes * 30
		else:
			print "You lose ${} on your Aces bet.".format(snakeEyes)
			payout -= snakeEyes
	if aceDeuce > 0:
		if roll == 3:
			print "You win ${} on your Acey-Deucey!".format(aceDeuce * 15)
			payout += aceDeuce * 15
		else:
			print "You lose ${} on your Acey-Deucey.".format(aceDeuce)
			payout -= aceDeuce
	if boxcars > 0:
		if roll == 12:
			print "You win ${} on the Boxcars!".format(boxcars * 30)
			payout += boxcars * 30
		else:
			print "You lose ${} on the Boxcars bet.".format(boxcars)
			payout -= boxcars
	if horn > 0:
		if roll in [2, 12]:
			print "You win ${}  on the Horn Bet!".format(((horn/4) * 30) - ((horn/4) * 3))
			payout += ((horn/4) * 30) - ((horn/4) * 3)
		elif roll in [3, 11]:
			print "You win ${} on the Horn bet!".format(((horn/4) * 15) - ((horn/4) * 3))
			payout += ((horn/4) * 15) - ((horn/4) * 3)
		else:
			print "You lose ${} from the Horn Bet.".format(horn)
			payout -= horn
	if eleven > 0:
		if roll == 11:
			print "You won ${} on the 11!".format(eleven * 15)
			payout += eleven * 15
		else:
			print "You lost ${} from the Yo Eleven bet.".format(eleven)
			payout -= eleven

	return payout


def roll(point):
	hard = False
	d1 = randint(1,6)
	d2 = randint(1, 6)
	roll = d1 + d2
	print "You rolled {} and {} for a total of {}.".format(d1, d2, roll)
	if d1 == d2 and roll in [4, 6, 8, 10]:
		print "{} the Hard Way!".format(roll)
		hard = True
	elif roll in [4, 6, 8, 10] and d1 != d2:
		print "{a} Easy {a}!".format(a=roll)
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
	press = raw_input("Change this bet? >")
	if press in ['y', 'Y', 'yes', 'Yes']:
		print "What's your new bet?"
		p = betInput()
		print "You now bet  ${}.".format(p)
	return p

def placeCall():
	if four > 0:
		print "You have ${} placed on the 4.".format(four)
	if five > 0:
		print "You have ${} placed on the 5.".format(five)
	if six > 0:
		print "You have ${} placed on the 6.".format(six)
	if eight > 0:
		print "You have ${} placed on the 8.".format(eight)
	if nine > 0:
		print "You have ${} placed on the 9.".format(nine)
	if ten > 0:
		print "You have ${} placed on the 10.".format(ten)
	if lay4 > 0:
		print "You have ${} laid against the 4.".format(lay4)
	if lay5 > 0:
		print "You have ${} laid against the 5.".format(lay5)
	if lay6 > 0:
		print "You have ${} laid against the 6.".format(lay6)
	if lay8 > 0:
		print "You have ${} laid against the 8.".format(lay8)
	if lay9 > 0:
		print "You have ${} laid against the 9.".format(lay9)
	if lay10 > 0:
		print "You have ${} laid against the 10.".format(lay10)

def place(four, five, six, eight, nine, ten):
	if four > 0:
		print "You have ${} wagered on the Place 4. Change your bet?".format(four)
		editFour = raw_input(">")
		if editFour in ['y', 'Y', 'yes', 'Yes']:
			four = betInput()
	else:
		print "How much on the Place 4?"
		four = betInput()
	if five > 0:
		print "You have ${} wagered on the Place 5. Change your bet?".format(five)
		editFive = raw_input(">")
		if editFive in ['y', 'Y', 'yes', 'Yes']:
			five = betInput()
	else:
		print "How much on the Place 5?"
		five = betInput()
	if six > 0:
		print "You have ${} wagered on the Place 6. Change your bet?".format(six)
		editSix = raw_input(">")
		if editSix in ['y', 'Y', 'yes', 'Yes']:
			six = betInput()
	else:
		print "How much on the Place 6?"
		six = betInput()
	if eight > 0:
		print "You have ${} wagered on the Place 8. Change your bet?".format(eight)
		editEight = raw_input(">")
		if editEight in ['y', 'Y', 'yes', 'Yes']:
			eight = betInput()
	else:
		print "How much on the place 8?"
		eight = betInput()
	if nine > 0:
		print "Yu have ${} wagered on the Place 9. Change your bet?".format(nine)
		editNine = raw_input("")
		if editNine in ['y', 'Y', 'yes', 'Yes']:
			nine = betInput()
	else:
		print "How much on the Place 9?"
		nine = betInput()
	if ten > 0:
		print "You have ${} wagered on the Place 10. Change your bet?".format(ten)
		editTen = raw_input(">")
		if editTen in ['y', 'Y', 'yes', 'Yes']:
			ten = betInput()
	else:
		print "How much on the Place 10?"
		ten = betInput()
	return four, five, six, eight, nine, ten

#Lay Bet Function
def lay(lay4, lay5, lay6, lay8, lay9, lay10):
	if lay4 > 0:
		print "You have ${} laid against the 4. Change your bet?".format(lay4)
		editFour = raw_input(">")
		if editFour in ['y', 'Y', 'yes', 'Yes']:
			lay4 = betInput()
	else:
		print "How much to lay against the 4?"
		lay4 = betInput()
	if lay5 > 0:
		print "You have ${} laid against the 5. Change your bet?".format(lay5)
		editFive = raw_input(">")
		if editFive in ['y', 'Y', 'yes', 'Yes']:
			lay5 = betInput()
	else:
		print "How much to lay against the 5?"
		lay5 = betInput()
	if lay6 > 0:
		print "You have ${} laud against the 6. Change your bet?".format(lay6)
		editSix = raw_input(">")
		if editSix in ['y', 'Y', 'yes', 'Yes']:
			lay6 = betInput()
	else:
		print "How much to lay against the 6?"
		lay6 = betInput()
	if lay8 > 0:
		print "You have ${} laud against the 8. Change your bet?".format(lay8)
		editEight = raw_input(">")
		if editEight in ['y', 'Y', 'yes', 'Yes']:
			lay8 = betInput()
	else:
		print "How much to lay against the 8?"
		lay8 = betInput()
	if lay9 > 0:
		print "Yu have ${} laud against the 9. Change your bet?".format(lay9)
		editNine = raw_input("")
		if editNine in ['y', 'Y', 'yes', 'Yes']:
			lay9 = betInput()
	else:
		print "How much to lay against the 9?"
		lay9 = betInput()
	if lay10 > 0:
		print "You have ${} laud against the 10. Change your bet?".format(lay10)
		editTen = raw_input(">")
		if editTen in ['y', 'Y', 'yes', 'Yes']:
			lay10 = betInput()
	else:
		print "How much to lay against the 10?"
		lay10 = betInput()
	return lay4, lay5, lay6, lay8, lay9, lay10



def hardCall():
	if hard4 > 0:
		print "You have ${} on the Hard 4.".format(hard4)
	if hard6 > 0:
		print "You have ${} on the Hard 6.".format(hard6)
	if hard8 > 0:
		print "You have ${} on the Hard 8.".format(hard8)
	if hard10 > 0:
		print "You have ${} on the Hard 10.".format(hard10)

def hardCheck(roll, isHard, hard4, hard6, hard8, hard10):
	if hard4 > 0 and roll == 4 and isHard == False:
		hard4 = 0
	if hard6 > 0 and roll == 6 and isHard == False:
		hard6 = 0
	if hard8 > 0 and roll == 8 and isHard == False:
		hard8 = 0
	if hard10 > 0 and roll == 10 and isHard == False:
		hard10 = 0

	return hard4, hard6, hard8, hard10

def hardWays(hard4, hard6, hard8, hard10):
	print "How much on Hard 4?"
	hard4 = betInput()
	print "How much on Hard 6?"
	hard6 = betInput()
	print "How much on Hard 8?"
	hard8 = betInput()
	print "How much on Hard 10?"
	hard10 = betInput()
	return hard4, hard6, hard8, hard10

stickman = [
"Hot Shooter! Keep 'er goin!",
"Let's go Shooter!",
"Keep on rolling! Place your bets!",
"Dice are hot tonight and the Shooter is on fire!",
"Well done! Pay the Line, take the Don't!",
"Alright, alright, alright, that's how we do it!"
]

#Game Start
print '{:^30}'.format('Oh Craps! v.4.98')
print "{:^27}".format('By: Marco Salsiccia')
print "How much would you like to cash in for your bank?"
while True:
	try:
		bank = int(raw_input("$"))
		break
	except ValueError:
		print "That wasn't a number, doofus."
		continue
print "Great, starting off with ${}.".format(bank)

comeBet = dComeBet = 0
throws = 0
comingOut = 1
p2 = 4
while True:
	pointIsOn = False
	bet1 = 'a'
	passLine = 0
	dPass = 0
	fieldBet = 0
	working = False

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
				print "Great, starting you off again with ${}.".format(bank)
				break

# Phase 1
	if throws == 0:
		print "Here comes a new shooter!"
	else:
		print stickman[randint(0, len(stickman)-1)]

	lineBets = raw_input("Line Bets? >")
	if lineBets in ['y', 'Y', 'yes', 'Yes']:
		bet1 = raw_input("Pass or Don't pass?")
		if bet1 in ['p', 'P', 'pass', 'Pass Line', 'Pass']:
			print "How much on the Pass Line?"
			passLine = betInput()
			print "Great, ${} on the Pass Line.".format(passLine)
		elif bet1 in ['d', 'D', 'dp', 'DP', 'dont', "Don't Pass", "don't pass"]:
			print "How much on the Don't Pass Line?"
			dPass = betInput()
			print "Great, ${} on the Don't Pass Line.".format(dPass)
		else:
			print "Pass or Don't Pass, there is nothing else!"
			continue

	placeCall()
	plBet = raw_input("Place Bets? >")
	if plBet in ['y', 'Y', 'yes', 'Yes']:
		four, five, six, eight, nine, ten = place(four, five, six, eight, nine, ten)

	lBet = raw_input("Lay Bets? >")
	if lBet in ['y', 'Y', 'yes', 'Yes']:
		lay4, lay5, lay6, lay8, lay9, lay10 = lay(lay4, lay5, lay6, lay8, lay9, lay10)

	hardCall()
	hardBet = raw_input("Hard Ways? >")
	if hardBet in ['y', 'Y', 'yes', 'Yes']:
		hard4, hard6, hard8, hard10 = hardWays(hard4, hard6, hard8, hard10)

	fBet = raw_input("Bet the Field? >")
	if fBet in ['y', 'Y', 'yes', 'Yes']:
		print "How much on the Field?"
		fieldBet = betInput()
		print "Ok, ${} on the Field.".format(fieldBet)

	if (four + five + six + eight + nine + ten + hard4 + hard6 + hard8 + hard10) > 0:
		workPlace = raw_input("Place and Hard Ways Bets working? >")
		if workPlace in ['y', 'Y', 'yes', 'Yes']:
			working = True
		else:
			working = False

	propStart = raw_input("Proposition Bets? >")
	if propStart in ['y', 'Y', 'yes', 'Yes']:
		any7, anyCraps, cAndE, snakeEyes, aceDeuce, boxcars, horn, eleven = prop()

# ATS
	if atsOn == False and throws == 0:
		atsChoice = raw_input("All Tall Small? >")
		if atsChoice in ['y', 'Y', 'yes', 'Yes']:
			atsOn = True
			allTallSmall()
	if atsOn == True:
		ats.sort()
		print "All Tall Small\n"
		print ats

# Coming Out Roll
	if throws == 1:
		print "Dice are coming out! {} roll.".format(throws)
	else:
		print "Dice are coming out! {} rolls.".format(throws)
	comingOut, coHard = roll(pointIsOn)
# Use this for specific number testing
#	comingOut = 1
#	coHard = False
	throws += 1
	atsAdd(comingOut)
	if (come4 + come5 + come6 + come8 + come9 + come10) > 0:
		bank += comePayout(comingOut, come4, come5, come6, come8, come9, come10, c4Odds, c5Odds, c6Odds, c8Odds, c9Odds, c10Odds, pointIsOn)
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
		throws = 0
		come4 = come5 = come6 = come8 = come9 = come10 = c4Odds = c5Odds = c6Odds = c8Odds = c9Odds = c10Odds = dCome4 = dCome5 = dCome6 = dCome8 = dCome9 = dCome10 = dC4Odds = dC5Odds = dC6Odds = dC8Odds = dC9Odds = dC10Odds = 0

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

	bank += propPayout(comingOut, any7, anyCraps, cAndE, snakeEyes, aceDeuce, boxcars, horn, eleven)

#Zero Out all Prop bets

	any7 = anyCraps = cAndE = snakeEyes = aceDeuce = boxcars = horn = eleven =  0

	if comingOut in [7, 11]:
		if working == True and comingOut == 7:
			bank -= (four + five  + six + eight + nine + ten)
			print "You lost ${} on the Place Bets.".format(four + five + six + eight + nine + ten)
			four = five = six = eight = nine = ten = 0
			if (hard4 + hard6 + hard8 + hard10) > 0:
				print "You lost ${} on the Hard Ways.".format(hard4 + hard6 + hard8 + hard10)
				bank -= (hard4 + hard6 + hard8 + hard10)
				hard4 = hard6 = hard8 = hard10 = 0
#Working Lay Bets
			if lay4 > 0:
				print "You won ${} on the Lay 4.".format(lay4 / 2)
				bank += (lay4 / 2)
				lay4 = 0
			if lay5 > 0:
				print "You won ${} on the lay 5!".format((lay5 / 3) * 2)
				bank += (lay5 / 3) * 2
				lay5 = 0
			if lay6 > 0:
				print "You won ${} on the Lay 6!".format((lay6/6) * 5)
				bank += (lay6 / 6) * 5
				lay6 = 0
			if lay8 > 0:
				print "You won ${} on the Lay 8!".format((lay8/6) * 5)
				bank += (lay8 / 6) * 5
				lay8 = 0
			if lay9 > 0:
				print "You won ${} on the lay 9!".format((lay9 / 3) * 2)
				bank += (lay9 / 3) * 2
				lay9 = 0
			if lay10 > 0:
				print "You won ${} on the Lay 10!".format(lay10 / 2)
				bank += lay10 / 2
				lay10 = 0

# ATS clean up on 7 out
		if atsOn == True and (atsAll + atsSmall + atsTall) > 0:
			atsCheck(comingOut)
			if comingOut == 7:
				atsOn = False
			elif comingOut == 11:
				atsAdd(comingOut)
		if bet1 == 'p':
			print "You won ${} on the Pass Line!".format(passLine)
			bank += passLine
		elif bet1 == 'd':
			print "You lost ${} from the Don't Pass Line.".format(dPass)
			bank -= dPass
		if comingOut == 7 and fieldBet > 0:
			print "You lose ${} on the Field.".format(fieldBet)
			bank -= fieldBet
			fieldBet = 0
		elif comingOut == 11 and fieldBet > 0:
			print "You win ${} on the Field!".format(fieldBet)
			bank += fieldBet
		print "You now have ${} in your bank.".format(bank)
		continue
	elif comingOut in [2, 3, 12]:
		atsAdd(comingOut)
		print "Oh Craps!"
		if bet1 == 'p':
			print "You lost ${}.".format(passLine)
			bank -= passLine
		elif bet1 == 'd':
			print "You win ${} from the Don't Pass Line!".format(dPass)
			bank += dPass
		if fieldBet > 0 and comingOut == 2:
			print "You win double on the Field! ${} coming to you.".format(fieldBet * 2)
			bank += fieldBet * 2
		elif fieldBet > 0 and comingOut == 12:
			print "You win triple on the Field! ${} coming to you.".format(fieldBet * 3)
			bank += fieldBet * 3
		elif fieldBet > 0 and comingOut == 3:
			print "You win ${} on the Field!".format(fieldBet)
			bank += fieldBet
		print "You now have ${} in your bank.".format(bank)

		atsCheck(comingOut)
		setClear()

		continue
	else:
		atsAdd(comingOut)
		pointIsOn = True


		print "The point is {}.\n".format(comingOut)

# Working Bets
		if working == True:
			if lay4 > 0 and comingOut == 4:
				print "You lose ${} from the Lay 4.".format(lay4)
				bank -= lay4
				lay4 = 0
			if lay5 > 0 and comingOut == 5:
				print "You lost ${} from the lay 5.".format(lay5)
				bank -= lay5
				lay5 = 0
			if lay6 > 0 and comingOut == 6:
				print "You lost ${} from the Lay 6.".format(lay6)
				bank -= lay6
				lay6 = 0
			if lay8 > 0 and comingOut == 8:
				print "You lost ${} from the Lay 8.".format(lay8)
				bank -= lay8
				lay8 = 0
			if lay9 > 0 and comingOut == 9:
				print "You lost ${} from the Lay 9.".format(lay9)
				bank -= lay9
				lay9 = 0
			if lay10 > 0 and comingOut == 10:
				print "You lost ${} from the Lay 10.".format(lay10)
				bank -= lay10
				lay10 = 0
			if four > 0 and comingOut == 4:
				if four < 25:
					bank += four/5 * 9
					print "You won ${} on the 4.".format(four/5 * 9)
				elif four >= 25:
					bank += (four * 2) - (four * 0.02)
					print "You won ${} on the Place 4.".format((four * 2) - (four * 0.02))
				four = press(four)
			elif five > 0 and comingOut == 5:
				bank += five/5 * 7
				print "You won ${} on the 5.".format(five/5 * 7)
				five = press(five)
			elif six > 0 and comingOut == 6:
				bank += six/6 * 7
				print "Yu won ${} on the 6.".format(six/6 * 7)
				six = press(six)
			elif eight > 0 and comingOut == 8:
				bank += eight/6 * 7
				print "You won ${} on the 8.".format(eight/6 * 7)
				eight = press(eight)
			elif nine > 0 and comingOut == 9:
				bank += nine/5 * 7
				print "You won ${} on the 9.".format(nine/5 * 7)
				nine = press(nine)
			elif ten > 0 and comingOut == 10:
				if ten < 25:
					bank += (ten/5) * 9
					print "You won ${} on the 10.".format((ten/5) * 9)
				elif ten >= 25:
					bank += (ten * 2) - (ten * 0.02)
					print "You won ${} on the Place 10.".format((ten * 2) - (ten * 0.02))
				ten = press(ten)

		if working == True and (hard4 + hard6 + hard8 + hard10) > 0:
			bank += hardPay(comingOut, coHard, hard4, hard6, hard8, hard10)
			hard4, hard6, hard8, hard10 = hardCheck(comingOut, coHard, hard4, hard6, hard8, hard10)

		if comingOut in [4, 9, 10] and fieldBet > 0:
			print "You win ${} on the Field!".format(fieldBet)
			bank += fieldBet
		elif comingOut in [5, 6, 8] and fieldBet > 0:
			print "You lose ${} on the Field.".format(fieldBet)
			bank -= fieldBet
			fieldBet = 0
		atsCheck(comingOut)
		setClear()
		#Betting
		while True:
			if atsOn == True:
				ats.sort()
				print "All Tall Small\n"
				print ats
			any7 = anyCraps = cAndE = snakeEyes = aceDeuce = boxcars = horn = eleven = 0
#Pass/Don't Pass Odds
			if passLine > 0 or dPass > 0:
				if passOdds > 0:
					print "You have ${} bet for your Odds.".format(passOdds)
				pOddsBet = raw_input("Pass/Don't Pass Line Odds? >")
				if pOddsBet in ['y', 'Y', 'yes', 'Yes']:
					if bet1 in ['p', 'P', 'pass', 'Pass Line', 'Pass']:
						print "How much for your Pass Line Odds?"
						passOdds = betInput()
					elif bet1 in ['d', 'D', 'dp', 'DP', 'dont', "Don't Pass", "don't pass"]:
						print "How much to Lay against the {}?".format(comingOut)
						passOdds = betInput()

#Come Bet
			if come4 > 0 and c4Odds == 0:
				print "You have ${} on the 4.".format(come4)
			elif c4Odds > 0:
				print "You have ${} on the 4 with ${} in Odds.".format(come4, c4Odds)
			if come5 > 0 and c5Odds == 0:
				print "You have ${} on the 5.".format(come5)
			elif c5Odds > 0:
				print "You have ${} on the 5 with ${} in Odds.".format(come5, c5Odds)
			if come6 > 0 and c6Odds == 0:
				print "You have ${} on the 6.".format(come6)
			elif c6Odds > 0:
				print "You have ${} on the 6 with ${} in Odds.".format(come6, c6Odds)
			if come8 > 0 and c8Odds == 0:
				print "You have ${} on the 8.".format(come8)
			elif c8Odds > 0:
				print "You have ${} on the 8 with ${} in Odds.".format(come8, c8Odds)
			if come9 > 0 and c9Odds == 0:
				print "You have ${} on the 9.".format(come9)
			elif c9Odds > 0:
				print "You have ${} on the 9 with ${} in Odds.".format(come9, c9Odds)
			if come10 > 0 and c10Odds == 0:
				print "You have ${} on the 10.".format(come10)
			elif c10Odds > 0:
				print "You have ${} on the 10 with ${} in Odds.".format(come10, c10Odds)
#Don't Come
			if dCome4 > 0 and dC4Odds == 0:
				print "You have ${} on the Don't Come 4.".format(dCome4)
			elif dC4Odds > 0:
				print "You have ${} on the Don't Come 4 with ${} in Odds.".format(dCome4, dC4Odds)
			if dCome5 > 0 and dC5Odds == 0:
				print "You have ${} on the Don't Come 5.".format(dCome5)
			elif dC5Odds > 0:
				print "You have ${} on the Don't Come 5 with ${} in Odds.".format(dCome5, dC5Odds)
			if dCome6 > 0 and dC6Odds == 0:
				print "You have ${} on the Don't Come 6.".format(dCome6)
			elif dC6Odds > 0:
				print "You have ${} on the Don't Come 6 with ${} in Odds.".format(dCome6, dC6Odds)
			if dCome8 >0 and dC8Odds == 0:
				print "You have ${} on the Don't Come 8.".format(dCome8)
			elif dC8Odds > 0:
				print "You have ${} on the Don't Come 8 with ${} in Odds.".format(dCome8, dC8Odds)
			if dCome9 > 0 and dC9Odds == 0:
				print "You have ${} on the Don't Come 9.".format(dCome9)
			elif dC9Odds > 0:
				print "You have ${} on the Don't Come 9 with ${} in Odds.".format(dCome9, dC9Odds)
			if dCome10 > 0 and dC10Odds == 0:
				print "You have ${} on the Don't Come 10.".format(dCome10)
			elif dC10Odds > 0:
				print "You have ${} on the Don't Come 10 with ${} in Odds.".format(dCome10, dC10Odds)
#			print "Come Bet?"
			cmBet = raw_input("Come Bet? >")
			if cmBet in ['y', 'Y', 'yes', 'Yes']:

				while True:
					comeChoice = raw_input("Come or Don't Come?")
					if comeChoice in ['c', 'C', 'come', 'Come']:
						print "How much on the Come?"
						comeBet = betInput()
						print "Ok, ${} in the Come.".format(comeBet)
						break
					elif comeChoice in ['d', 'dc', 'dont', "Don't Come", "don't come"]:
						print "How much on the Don't Come?"
						dComeBet = betInput()
						print "Ok, ${} on the Don't Come.".format(dComeBet)
						break
					elif comeChoice in ['x', 'exit', 'esc', 'n']:
						break
					else:
						print "Come or Don't Come, there is no try!"
						continue

#Place and Lay Bets

#			print "Place Bets?"
			placeCall()
			placeBet = raw_input("Place Bets? >")
			if placeBet in ['y', 'Y', 'yes', 'Yes']:
				four, five, six, eight, nine, ten = place(four, five, six, eight, nine, ten)
			lyBets = raw_input("Lay Bets? >")
			if lyBets in ['y', 'Y', 'yes', 'Yes']:
				lay4, lay5, lay6, lay8, lay9, lay10 = lay(lay4, lay5, lay6, lay8, lay9, lay10)


#Come Odds
			if (come4 + come5 + come6 + come8 + come9 + come10) > 0:
				alterOdds = raw_input("Change Come Odds? >")
				if alterOdds in ['y', 'Y', 'yes', 'Yes']:
					if come4 > 0:
						print "You have $% in Odds for the 4. Enter a new amount." %c4Odds
						c4Odds = betInput()
					if come5 > 0:
						print "You have $% in Odds for the 5. Enter a new amount." %c5Odds
						c5Odds =	 betInput()
					if come6 > 0:
						print "You have $% in Odds for the 6. Enter a new amount." %c6Odds
						c6Odds = betInput()
					if come8 > 0:
						print "You have $% in Odds for the 8. Enter a new amount." %c8Odds
						c8Odds = betInput()
					if come9 > 0:
						print "You have $% in Odds for the 9. Enter a new amount." %c9Odds
						c9Odds = betInput()
					if come10 > 0:
						print "You have $% in Odds for the 10. Enter a new amount." %c10Odds
						c10Odds = betInput()

# Don't Come Odds

			if (dCome4 + dCome5 + dCome6 + dCome8 + dCome9 + dCome10) > 0:
				alterDont = raw_input("Change Don't Come Odds? >")
				if alterDont in ['y', 'Y', 'yes', 'Yes']:
					if dCome4 > 0:
						print "Your Lay 4 has ${} in Odds. Enter the new amount.".format(dC4Odds)
						dC4Odds = betInput()
					if dCome5 > 0:
						print "Your Lay 5 has ${} in Odds. Enter the new amount.".format(dC5Odds)
						dC5Odds = betInput()
					if dCome6 > 0:
						print "Your Lay 6 has ${} in Odds. Enter the new amount.".format(dC6Odds)
						dC6Odds = betInput()
					if dCome8 > 0:
						print "Your Lay 8 has ${} in Odds. Enter the new amount.".format(dC8Odds)
						dC8Odds = betInput()
					if dCome9 > 0:
						print "Your Lay 9 has ${} in Odds. Enter the new amount.".format(dC9Odds)
						dC9Odds = betInput()
					if dCome10 > 0:
						print "Your Lay 10 has ${} in Odds. Enter the new amount.".format(dC10Odds)
						dC10Odds = betInput()

#Field Bet

			fBet = raw_input("Bet the Field? You have ${} wagered. >".format(fieldBet))
			if fBet in ['y', 'Y', 'yes', 'Yes']:
				print "How much on the Field?"
				fieldBet = betInput()
			#else:
				#fieldBet = 0

#Hard Ways
			hardCall()
			hWays = raw_input("Bet the hard ways? >")
			if hWays in ['y', 'Y', 'yes', 'Yes']:
				hard4, hard6, hard8, hard10 = hardWays(hard4, hard6, hard8, hard10)
#Prop Bets
			props = raw_input("Proposition Bets? >")
			if props in ['y', 'Y', 'yes', 'Yes']:
				any7, anyCraps, cAndE, snakeEyes, aceDeuce, boxcars, horn, eleven = prop()
			if throws == 1:
				print "Dice are rolling! {} roll.".format(throws)
			else:
				print "Dice are rolling! {} rolls.".format(throws)
			#raw_input("Hit Enter to roll again.")
#Phase 2 Roll
			p2, p2Hard = roll(pointIsOn)
# Use this for specific number testing
#			p2 += 1
#			p2Hard = True

			throws += 1
			atsAdd(p2)

			bank += comePayout(p2, come4, come5, come6, come8, come9, come10, c4Odds, c5Odds, c6Odds, c8Odds, c9Odds, c10Odds, pointIsOn)

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
					print "You win ${} on the Come!".format(comeBet)
					bank += comeBet
				elif p2 in [2, 3, 12]:
					print "You lose ${} from the Come.".format(comeBet)
					bank -= comeBet
				else:
					come4, come5, come6, come8, come9, come10 = come(p2, comeBet, come4, come5, come6, come8, come9, come10)
					cOdds = raw_input("Odds on your Come bet? >")
					if cOdds in ['y', 'Y', 'yes', 'Yes']:
						if p2 == 4:
							print "Odds on the 4?"
							c4Odds = betInput()
							print "Ok, ${} on the 4.".format(c4Odds)
						elif p2 == 5:
							print "Odds on the 5?"
							c5Odds = betInput()
							print "Ok, ${} on the 5.".format(c5Odds)
						elif p2 == 6:
							print "Odds on the 6?"
							c6Odds = betInput()
							print "Ok,${} on the 6.".format(c6Odds)
						elif p2 == 8:
							print "Odds on the 8?"
							c8Odds = betInput()
							print "Ok, ${} on the 8.".format(c8Odds)
						elif p2 == 9:
							print "Odds on the 9?"
							c9Odds = betInput()
							print "Ok, ${} on the 9.".format(c9Odds)
						elif p2 == 10:
							print "Odds on the 10?"
							c10Odds = betInput()
							print "Ok, ${} on the 10.".format(c10Odds)
				comeBet = 0

#Don't Come
			if dComeBet > 0:
				if p2 in [2, 3, 12]:
					print "You win ${} on the Don't Come!".format(dComeBet)
					bank += dComeBet
				elif p2 in [7, 11]:
					print "You lose ${} from the Don't Come.".format(dComeBet)
					bank -= dComeBet
				else:
					dCome4, dCome5, dCome6, dCome8, dCome9, dCome10 = dCome(p2, dComeBet, dCome4, dCome5, dCome6, dCome8, dCome9, dCome10)
					dcOdds = raw_input("Odds on your Don't Come bet? >")
					if dcOdds in ['y', 'Y', 'yes', 'Yes']:
						if p2 == 4:
							print "Odds on the Don't Come 4?"
							dC4Odds = betInput()
							print "Ok, ${} on the 4.".format(dC4Odds)
						elif p2 == 5:
							print "Odds on the Don't Come 5?"
							dC5Odds = betInput()
							print "Ok, ${} on the 5.".format(dC5Odds)
						elif p2 == 6:
							print "Odds on the Don't Come 6?"
							dC6Odds = betInput()
							print "Ok,${} on the 6.".format(dC6Odds)
						elif p2 == 8:
							print "Odds on the Don't Come 8?"
							dC8Odds = betInput()
							print "Ok, ${} on the 8.".format(dC8Odds)
						elif p2 == 9:
							print "Odds on the Don't Come 9?"
							dC9Odds = betInput()
							print "Ok, ${} on the 9.".format(dC9Odds)
						elif p2 == 10:
							print "Odds on the Don't Come 10?"
							dC10Odds = betInput()
							print "Ok, ${} on the 10.".format(dC10Odds)
				dComeBet = 0

#Prop Bet Payout
			bank += propPayout(p2, any7, anyCraps, cAndE, snakeEyes, aceDeuce, boxcars, horn, eleven)
			any7 = anyCraps = cAndE = snakeEyes = aceDeuce = boxcars = horn = eleven = 0

			if fieldBet != 0:
				if p2 == 2:
					print "You win double on the Field! ${} coming to you.".format(fieldBet * 2)
					bank += fieldBet * 2
				elif p2 == 12:
					print "You win triple on the Field! ${} coming to you.".format(fieldBet * 3)
					bank += fieldBet * 3
				elif p2 in [3, 4, 9, 10, 11]:
					print "You win on the Field! ${} coming to you.".format(fieldBet)
					bank += fieldBet
				else:
					print "You lose ${} on the Field.".format(fieldBet)
					bank -= fieldBet
					fieldBet = 0
	
#Hard Ways payout

			bank += hardPay(p2, p2Hard, hard4, hard6, hard8, hard10)
			hard4, hard6, hard8, hard10 = hardCheck(p2, p2Hard, hard4, hard6, hard8, hard10)

			if p2 == 4 and four > 0:
				if 0 < four < 25:
					win4 = (four/5) * 9
				elif four >= 25:
					win4 = (four * 2) - (four * 0.02)
				print "You win ${} on the place 4.".format(win4)
				bank += win4
				if comingOut != 4:
					four = press(four)
			if p2 == 5 and five > 0:
				win5 = (five/5) * 7
				print "You win ${} on the place 5.".format(win5)
				bank += win5
				if comingOut != 5:
					five = press(five)
			if p2 == 6 and six > 0:
				print "You win ${} on the place 6.".format(six/6 * 7)
				bank += six/6 * 7
				if comingOut != 6:
					six = press(six)

			if p2 == 8 and eight > 0:
				print "You win ${} on the place Eight.".format(eight/6 * 7)
				bank += eight/6 * 7
				if comingOut != 8:
					eight = press(eight)
			if p2 == 9 and nine > 0:
				win9 = (nine/5) * 7
				print "You win ${} on the place 9!".format(win9)
				bank += win9
				if comingOut != 9:
					nine = press(nine)

			if p2 == 10 and ten > 0:
				if 0 < ten < 25:
					win10 = (ten/5) * 9
				elif ten >= 25:
					win10 = (ten * 2) - (ten * 0.02)
				print "You win ${} on the place 10.".format(win10)
				bank += win10
				if comingOut != 10:
					ten = press(ten)
# Lay Bets Loss
			if lay4 > 0 and p2 == 4:
				print "You lose ${} from the Lay 4.".format(lay4)
				bank -= lay4
				lay4 = 0
			if lay5 > 0 and p2 == 5:
				print "You lost ${} from the lay 5.".format(lay5)
				bank -= lay5
				lay5 = 0
			if lay6 > 0 and p2 == 6:
				print "You lost ${} from the Lay 6.".format(lay6)
				bank -= lay6
				lay6 = 0
			if lay8 > 0 and p2 == 8:
				print "You lost ${} from the Lay 8.".format(lay8)
				bank -= lay8
				lay8 = 0
			if lay9 > 0 and p2 == 9:
				print "You lost ${} from the Lay 9.".format(lay9)
				bank -= lay9
				lay9 = 0
			if lay10 > 0 and p2 == 10:
				print "You lost ${} from the Lay 10.".format(lay10)
				bank -= lay10
				lay10 = 0

			atsCheck(p2)
			setClear()
			if p2 == comingOut:
				print "Point hit!"
				if bet1 == 'p':
					print "You win ${}!".format(passLine)
					if passOdds > 0:
						oddsWin = odds(comingOut, passOdds, bet1)
						print "You win ${} on your odds.".format(oddsWin)
						bank += oddsWin
					bank += passLine
				elif bet1 == 'd':
					print "You lose ${}.".format(dPass)
					if passOdds > 0:
						print "You lose ${} from your odds.".format(passOdds)
						bank -= passOdds
					bank -= dPass
					passOdds = 0
				break
#Seven Out
			elif p2 == 7:
				if lay4 > 0:
					print "You won ${} on the Lay 4.".format(lay4 / 2)
					bank += (lay4 / 2)
					lay4 = 0
				if lay5 > 0:
					print "You won ${} on the lay 5!".format((lay5 / 3) * 2)
					bank += (lay5 / 3) * 2
					lay5 = 0
				if lay6 > 0:
					print "You won ${} on the Lay 6!".format((lay6/6) * 5)
					bank += (lay6 / 6) * 5
					lay6 = 0
				if lay8 > 0:
					print "You won ${} on the Lay 8!".format((lay8/6) * 5)
					bank += (lay8 / 6) * 5
					lay8 = 0
				if lay9 > 0:
					print "You won ${} on the lay 9!".format((lay9 / 3) * 2)
					bank += (lay9 / 3) * 2
					lay9 = 0
				if lay10 > 0:
					print "You won ${} on the Lay 10!".format(lay10 / 2)
					bank += lay10 / 2
					lay10 = 0

				come4 = come5 = come6 = come8 = come9 = come10 = c4Odds = c5Odds  = c6Odds = c8Odds = c9Odds = c10Odds = dCome4 = dCome5 = dCome6 = dCome8 = dCome9 = dCome10 = dC4Odds = dC5Odds = dC6Odds = dC8Odds = dC10Odds = 0
				if hard4 + hard6 + hard8 + hard10 > 0:
					print "You lose ${} from the Hard Ways.".format(hard4 + hard6 + hard8 + hard10)
					bank -= (hard4 + hard6 + hard8 + hard10)
					hard4 = hard6 = hard8 = hard10 = 0
				if (four + five + six + eight + nine + ten) > 0:
					print "You lose ${} from the place bets.".format(four + five + six + eight + nine + ten)
					bank -= (four + five + six + eight + nine + ten)
				four = five = six = eight = nine = ten = 0
				if bet1 == 'p':
					print "You lost ${} from the Pass Line.".format(passLine)
					if passOdds > 0:
						print "You lose ${} from your Pass Line odds.".format(passOdds)
						bank -= passOdds
						passOdds = 0
					bank -= passLine
				elif bet1 == 'd':
					print "You win ${} from the Don't Pass Line!".format(dPass)
					if passOdds > 0:
						dOdds = odds(comingOut, passOdds, bet1)
						print "You won ${} on your Don't Pass Odds.".format(dOdds)
						bank += dOdds
						passOdds = 0
					bank += dPass
				if any7 > 0:
					print "You win ${} on Any 7!".format(any7 * 4)
					bank += any7 * 4
					any7 = 0
				throws = 0
				break
			else:
				print "Bank = ${}. The point is {}.".format(bank, comingOut)

				continue
		print "You have ${} in your bank!".format(bank)
	continue