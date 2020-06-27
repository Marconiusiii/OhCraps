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

def setClear(x, y, z):
	smallSet = [2, 3, 4, 5, 6]
	tallSet = [8, 9, 10, 11, 12]
	allSet = smallSet + tallSet
	if set(x) == set(smallSet):
		x = []
	if set(y) == set(tallSet):
		y = []
	if set(z) == set(allSet):
		z = []
	return x, y, z


def allTallSmall():
	print "How much on the All?"
	a = input("$>")
	print "Ok, $%d on the All." %a
	print "How much on the Tall?"
	t = input("$>")
	print "Ok, $%d on the Tall." %t
	print "How much on the Small?"
	s = input("$>")
	print "Ok $%d on the Small." %s
	return a, t, s

def atsCheck(i, inSmall, inTall, all, tall, small):
	payout = 0
	allSet = [2, 3, 4, 5, 6, 8, 9, 10, 11, 12]
	tallSet = [8, 9, 10, 11, 12]
	smallSet = [2, 3, 4, 5, 6]
	if set(i) == set(allSet):
		print "You hit the All and won $%d!" %(all * 176)
		payout += all * 176
	if set(inSmall) == set(smallSet):
		print "You hit the Small and won $%d!" %(small * 35)
		payout += small * 35
	if set(inTall) == set(tallSet):
		print "You hit the Tall and won $%d!" %(tall * 35)
		payout += tall * 35
	return payout

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

def hardPay(roll, hard, hard4, hard6, hard8, hard10):
	payout = 0
	if roll == 4 and hard == True and hard4 > 0:
		print "You win $%d on the Hard 4!" %(hard4 * 7)
		payout += hard4 * 7
	elif roll == 4 and hard == False and hard4 > 0:
		print "You lose $%d on the Hard 4." %hard4
		payout -= hard4

	if roll == 6 and hard == True and hard6 > 0:
		print "You win $%d on the Hard 6!" %(hard6 * 9)
		payout += hard6 * 9
	elif roll == 6 and hard == False and hard6 >0:
		print "You lose $%d on the Hard 6." %hard6
		payout -= hard6

	if roll == 8 and hard == True and hard8 > 0:
		print "You win $%d on the Hard 8!" %(hard8 * 9)
		payout += hard8 * 9
	elif roll == 8 and hard == False and hard8 > 0:
		print "You lose $%d on the Hard 8." %hard8
		payout -= hard8

	if roll == 10 and hard == True and hard10 > 0:
		print "You win $%d on the Hard 10!" %(hard10 * 7)
		payout += hard10 * 7
	elif roll == 10 and hard == False and hard10 > 0:
		print "You lose $%d on the Hard 10." %hard10
		payout -= hard10

	return payout

def prop():
	any7 = anyCraps = cAndE = snakeEyes = aceDeuce = boxcars = horn = eleven = 0

	while True:
		propPick = raw_input("Type in your Prop Bet: ")
		if propPick in ['7', 'seven', 'big red', 'Seven', 'any 7', 'Any 7', 'Any Seven', 'Any seven', 'any seven']:
			print "How much on Any 7?"
			any7 = betInput(bank)
			print "Ok, $%d on Any 7." %any7
			continue
		elif propPick in ['cr', 'CR', 'Cr', 'any craps', 'Any Craps', 'Any craps', 'craps', 'Craps']:
			print "How much on Any Craps?"
			anyCraps = betInput(bank)
			print "Ok, $%d on Any Craps." %anyCraps
			continue
		elif propPick in ['ce', 'CE', 'craps and eleven', 'Craps and Eleven', 'craps and 11', 'c and e', 'C and E', "C&E"]:
			print "How much on C & E?"
			cAndE = betInput(bank)
			print "Ok, $%d on C&E." %cAndE
			continue
		elif propPick == "sn" or propPick in ['s', 'S', 'snake', 'snakeyes', 'snake eyes', 'Snake Eyes', 'snakeeyes', 'aces', 'Aces', 'ace ace', '2']:
			print "How much on Snake Eyes?"
			snakeEyes = betInput(bank)
			print "Ok, $%d on Snake Eyes." %snakeEyes
			continue
		elif propPick in ['ad', 'three', '3', 'AD', 'ace deuce', 'acey deucey', 'Three', '3']:
			print "How much on Acey-Deucey?"
			aceDeuce = betInput(bank)
			print "Ok, $%d on Acey-Deucey." %aceDeuce
			continue
		elif propPick in ['b', 'B', 'boxcars', 'Boxcars', 'Box Cars', 'box cars', '12', 'twelve', 'Twelve', 'six six', '66']:
			print "How much on Boxcars?"
			boxcars = betInput(bank)
			print "Ok, $%d on Boxcars." %boxcars
			continue
		elif propPick in ["h", 'horn', 'H', 'Horn']:
			print "How much on the Horn?"
			horn = betInput(bank)
			print "Ok, $%d on the Horn Bet!" %horn
			continue
		elif propPick in ['11', 'eleven', '56', 'Eleven', 'yo', 'Yo', 'Yo Eleven']:
			print "How much on the Eleven?"
			eleven = betInput(bank)
			print "Ok, $%d on the Eleven." %eleven
			continue
		elif propPick in ['all', 'All', 'all bets', 'All Bets', 'Show All Bets', 'show all bets']:
			print "Current prop bets:"
			if any7 > 0:
				print "$%d on Any 7." %any7
			if anyCraps > 0:
				print "$%d on Any Craps." %anyCraps
			if cAndE > 0:
				print "$%d on C&E." %cAndE
			if snakeEyes > 0:
				print "$%d on Snake Eyes." %snakeEyes
			if aceDeuce > 0:
				print "$%d on Acey-Deucey." %aceDeuce
			if horn > 0:
				print "$%d on the Horn." %horn
			if eleven > 0:
				print "$%d on the Eleven." %eleven
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

def comePayout(roll, come4, come5, come6, come8, come9, come10, c4Odds, c5Odds, c6Odds, c8Odds, c9Odds, c10Odds, pointIsOn):
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
	elif roll == 7 and (come4 + come5 + come6 + come8 + come9 + come10) > 0 and pointIsOn == True:
		allCome = come4 + come5 + come6 + come8 + come9 + come10 + c4Odds + c5Odds + c6Odds + c8Odds + c9Odds + c10Odds
		print "You lost $%d from your Come bets and Odds. All bets cleared." %allCome
		payout -= allCome
	elif roll == 7 and (come4 + come5 + come6 + come8 + come9 + come10) > 0 and pointIsOn == False:
		onlyCome = (come4 + come5 + come6 + come8 + come9 + come10)
		print "You lost $%d from your Come bets. All Odds were off and returned to you." %onlyCome
		payout -= onlyCome

	return payout

def dComePayout(roll, dCome4, dCome5, dCome6, dCome8, dCome9, dCome10, dC4Odds, dC5Odds, dC6Odds, dC8Odds, dC9Odds, dC10Odds, pointIsOn):
	payout = 0
	if dCome4 > 0:
		if roll == 7:
			print "You win $%d on your Don't Come for the 4!" %dCome4
			if dC4Odds > 0:
				print "You win $%d from your Don't Come 4 Odds." %(dC4Odds / 2)
				payout += dC4Odds / 2
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
				print "You win $%d from your Don't Come 5 Odds." %(dC5Odds/3 * 2)
				payout += dC5Odds/3 * 2
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
				print "You win $%d from your Don't Come 6 Odds." %(dC6Odds/6 * 5)
				payout += dC6Odds/6 * 5
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
				print "You win $%d from your Don't Come 8 Odds." %(dC8Odds/6 * 5)
				payout += dC8Odds/6 * 5
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
				print "You win $%d from your Don't Come 9 Odds." %(dC9Odds/3 * 2)
				payout += dC9Odds/3 * 2
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
				print "You win $%d from your Don't Come 10 Odds." %(dC10Odds / 2)
				payout += dC10Odds / 2
			payout += dCome10
		elif roll == 10:
			print "You lose $%d on your Don't Come 10." %dCome10
			if dC10Odds > 0 and pointIsOn == True:
				print "You lose $%d from your Don't Come 10 Odds." %dC10Odds
				payout -= dC10Odds
			payout -= dCome10
	return payout

def propPayout(roll, any7, anyCraps, cAndE, snakeEyes, aceDeuce, boxcars, horn, eleven):
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
			print "You win $%d  on the Horn Bet!" %(((horn/4) * 30) - ((horn/4) * 3))
			payout += ((horn/4) * 30) - ((horn/4) * 3)
		elif roll in [3, 11]:
			print "You win $%d on the Horn bet!" %(((horn/4) * 15) - ((horn/4) * 3))
			payout += ((horn/4) * 15) - ((horn/4) * 3)
		else:
			print "You lose $%d from the Horn Bet." %horn
			payout -= horn
	if eleven > 0:
		if roll == 11:
			print "You won $%d on the 11!" %(eleven * 15)
			payout += eleven * 15
		else:
			print "You lost $%d from the Yo Eleven bet." %eleven
			payout -= eleven

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
	press = raw_input("Change this bet? >")
	if press in ['y', 'Y', 'yes', 'Yes']:
		print "What's your new bet?"
		p = betInput(bank)
		print "You now bet  $%d." %p
	return p

def placeCall():
	if four > 0:
		print "You have $%d placed on the 4." %four
	if five > 0:
		print "You have $%d placed on the 5." %five
	if six > 0:
		print "You have $%d placed on the 6." %six
	if eight > 0:
		print "You have $%d placed on the 8." %eight
	if nine > 0:
		print "You have $%d placed on the 9." %nine
	if ten > 0:
		print "You have $%d placed on the 10." %ten
	if lay4 > 0:
		print "You have $%d laid against the 4." %lay4
	if lay5 > 0:
		print "You have $%d laid against the 5." %lay5
	if lay6 > 0:
		print "You have $%d laid against the 6." %lay6
	if lay8 > 0:
		print "You have $%d laid against the 8." %lay8
	if lay9 > 0:
		print "You have $%d laid against the 9." %lay9
	if lay10 > 0:
		print "You have $%d laid against the 10." %lay10

def place(four, five, six, eight, nine, ten):
	if four > 0:
		print "You have $%d wagered on the Place 4. Press the 4?" %four
		editFour = raw_input(">")
		if editFour in ['y', 'Y', 'yes', 'Yes']:
			four = betInput(bank)
	else:
		print "How much on the Place 4?"
		four = betInput(bank)
	if five > 0:
		print "You have $%d wagered on the Place 5. Press the 5?" %five
		editFive = raw_input(">")
		if editFive in ['y', 'Y', 'yes', 'Yes']:
			five = betInput(bank)
	else:
		print "How much on the Place 5?"
		five = betInput(bank)
	if six > 0:
		print "You have $%d wagered on the Place 6. Press the 6?" %six
		editSix = raw_input(">")
		if editSix in ['y', 'Y', 'yes', 'Yes']:
			six = betInput(bank)
	else:
		print "How much on the Place 6?"
		six = betInput(bank)
	if eight > 0:
		print "You have $%d wagered on the Place 8. Press the 8?" %eight
		editEight = raw_input(">")
		if editEight in ['y', 'Y', 'yes', 'Yes']:
			eight = betInput(bank)
	else:
		print "How much on the place 8?"
		eight = betInput(bank)
	if nine > 0:
		print "Yu have $%d wagered on the Place 9. Press the 9?" %nine
		editNine = raw_input("")
		if editNine in ['y', 'Y', 'yes', 'Yes']:
			nine = betInput(bank)
	else:
		print "How much on the Place 9?"
		nine = betInput(bank)
	if ten > 0:
		print "You have $%d wagered on the Place 10. Press the 10?" %ten
		editTen = raw_input(">")
		if editTen in ['y', 'Y', 'yes', 'Yes']:
			ten = betInput(bank)
	else:
		print "How much on the Place 10?"
		ten = betInput(bank)
	return four, five, six, eight, nine, ten

#Lay Bet Function
def lay(lay4, lay5, lay6, lay8, lay9, lay10):
	if lay4 > 0:
		print "You have $%d laid against the 4. Change your bet?" %lay4
		editFour = raw_input(">")
		if editFour in ['y', 'Y', 'yes', 'Yes']:
			lay4 = betInput(bank)
	else:
		print "How much to lay against the 4?"
		lay4 = betInput(bank)
	if lay5 > 0:
		print "You have $%d laid against the 5. Change your bet?" %lay5
		editFive = raw_input(">")
		if editFive in ['y', 'Y', 'yes', 'Yes']:
			lay5 = betInput(bank)
	else:
		print "How much to lay against the 5?"
		lay5 = betInput(bank)
	if lay6 > 0:
		print "You have $%d laud against the 6. Change your bet?" %lay6
		editSix = raw_input(">")
		if editSix in ['y', 'Y', 'yes', 'Yes']:
			lay6 = betInput(bank)
	else:
		print "How much to lay against the 6?"
		lay6 = betInput(bank)
	if lay8 > 0:
		print "You have $%d laud against the 8. Change your bet?" %lay8
		editEight = raw_input(">")
		if editEight in ['y', 'Y', 'yes', 'Yes']:
			lay8 = betInput(bank)
	else:
		print "How much to lay against the 8?"
		lay8 = betInput(bank)
	if lay9 > 0:
		print "Yu have $%d laud against the 9. Change your bet?" %lay9
		editNine = raw_input("")
		if editNine in ['y', 'Y', 'yes', 'Yes']:
			lay9 = betInput(bank)
	else:
		print "How much to lay against the 9?"
		lay9 = betInput(bank)
	if lay10 > 0:
		print "You have $%d laud against the 10. Change your bet?" %lay10
		editTen = raw_input(">")
		if editTen in ['y', 'Y', 'yes', 'Yes']:
			lay10 = betInput(bank)
	else:
		print "How much to lay against the 10?"
		lay10 = betInput(bank)
	return lay4, lay5, lay6, lay8, lay9, lay10



def hardCall():
	if hard4 > 0:
		print "You have $%d on the Hard 4." %hard4
	if hard6 > 0:
		print "You have $%d on the Hard 6." %hard6
	if hard8 > 0:
		print "You have $%d on the Hard 8." %hard8
	if hard10 > 0:
		print "You have $%d on the Hard 10." %hard10

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
	hard4 = betInput(bank)
	print "How much on Hard 6?"
	hard6 = betInput(bank)
	print "How much on Hard 8?"
	hard8 = betInput(bank)
	print "How much on Hard 10?"
	hard10 = betInput(bank)
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
print "Oh Craps v.4.95"
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
throws = 0
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
				print "Great, starting you off again with $%d." %bank
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
			passLine = betInput(bank)
			print "Great, $%d on the Pass Line." %passLine
		elif bet1 in ['d', 'D', 'dp', 'DP', 'dont', "Don't Pass", "don't pass"]:
			print "How much on the Don't Pass Line?"
			dPass = betInput(bank)
			print "Great, $%d on the Don't Pass Line." %dPass
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
		fieldBet = betInput(bank)
		print "Ok, $%d on the Field." %fieldBet

	if (four + five + six + eight + nine + ten + hard4 + hard6 + hard8 + hard10) > 0:
		workPlace = raw_input("All bets working? >")
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
			atsAll, atsTall, atsSmall = allTallSmall()
	if atsOn == True:
		ats.sort()
		print "All Tall Small\n"
		print ats
# Coming Out Roll
	if throws == 1:
		print "Dice are coming out! %d roll." %throws
	else:
		print "Dice are coming out! %d rolls." %throws
	comingOut, coHard = roll(pointIsOn)
# Use this for specific number testing
#	comingOut = 4
#	coHard = False
	throws += 1
	if comingOut in [2, 3, 4, 5, 6]:
		if comingOut not in smallNumbers:
			smallNumbers.append(comingOut)
	elif comingOut in [8, 9, 10, 11, 12]:
		if comingOut not in tallNumbers:
			tallNumbers.append(comingOut)
	if comingOut not in ats:
		ats.append(comingOut)

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
			print "You lost $%d on the Place Bets." %(four + five + six + eight + nine + ten)
			four = five = six = eight = nine = ten = 0
			if (hard4 + hard6 + hard8 + hard10) > 0:
				print "You lost $%d on the Hard Ways." %(hard4 + hard6 + hard8 + hard10)
				bank -= (hard4 + hard6 + hard8 + hard10)
				hard4 = hard6 = hard8 = hard10 = 0
#Working Lay Bets
			if lay4 > 0:
				print "You won $%d on the Lay 4." %(lay4 / 2)
				bank += (lay4 / 2)
				lay4 = 0
			if lay5 > 0:
				print "You won $%d on the lay 5!" %((lay5 / 3) * 2)
				bank += (lay5 / 3) * 2
				lay5 = 0
			if lay6 > 0:
				print "You won $%d on the Lay 6!" %((lay6/6) * 5)
				bank += (lay6 / 6) * 5
				lay6 = 0
			if lay8 > 0:
				print "You won $%d on the Lay 8!" %((lay8/6) * 5)
				bank += (lay8 / 6) * 5
				lay8 = 0
			if lay9 > 0:
				print "You won $%d on the lay 9!" %((lay9 / 3) * 2)
				bank += (lay9 / 3) * 2
				lay9 = 0
			if lay10 > 0:
				print "You won $%d on the Lay 10!" %(lay10 / 2)
				bank += lay10 / 2
				lay10 = 0

# ATS clean up on 7 out
		if atsOn == True and (atsAll + atsSmall + atsTall) > 0:
			if comingOut == 7:
				print "You lost $%d from the All Tall Small!" %(atsAll + atsTall + atsSmall)
				bank -= (atsAll + atsTall + atsSmall)
				atsOn = False
				atsAll = atsTall = atsSmall = 0
				if len(ats) > 0:
					ats = smallNumbers = tallNumbers =  []
			elif comingOut == 11:
				if comingOut not in tallNumbers:
					tallNumbers.append(comingOut)
				if comingOut not in ats:
					ats.append(comingOut)
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
		if comingOut in [2, 3, 4, 5, 6]:
			if comingOut not in smallNumbers:
				smallNumbers.append(comingOut)
		elif comingOut in [8, 9, 10, 11, 12]:
			if comingOut not in tallNumbers:
				tallNumbers.append(comingOut)
		if comingOut not in ats:
			ats.append(comingOut)

		print "Oh Craps!"
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

		bank += atsCheck(ats, smallNumbers, tallNumbers, atsAll, atsTall, atsSmall)
		smallNumbers, tallNumbers, ats = setClear(smallNumbers, tallNumbers, ats)

		continue
	else:
		if comingOut in [2, 3, 4, 5, 6]:
			if comingOut not in smallNumbers:
				smallNumbers.append(comingOut)
		elif comingOut in [8, 9, 10, 11, 12]:
			if comingOut not in tallNumbers:
				tallNumbers.append(comingOut)
		if comingOut not in ats:
			ats.append(comingOut)
		pointIsOn = True

		print "The point is %d.\n" %comingOut

# Working Bets
		if working == True:
			if lay4 > 0 and comingOut == 4:
				print "You lose $%d from the Lay 4." %lay4
				bank -= lay4
				lay4 = 0
			if lay5 > 0 and comingOut == 5:
				print "You lost $%d from the lay 5." %lay5
				bank -= lay5
				lay5 = 0
			if lay6 > 0 and comingOut == 6:
				print "You lost $%d from the Lay 6." %lay6
				bank -= lay6
				lay6 = 0
			if lay8 > 0 and comingOut == 8:
				print "You lost $%d from the Lay 8." %lay8
				bank -= lay8
				lay8 = 0
			if lay9 > 0 and comingOut == 9:
				print "You lost $%d from the Lay 9." %lay9
				bank -= lay9
				lay9 = 0
			if lay10 > 0 and comingOut == 10:
				print "You lost $%d from the Lay 10." %lay10
				bank -= lay10
				lay10 = 0
			if four > 0 and comingOut == 4:
				if four < 25:
					bank += four/5 * 9
					print "You won $%d on the 4." %(four/5 * 9)
				elif four >= 25:
					bank += (four * 2) - (four * 0.02)
					print "You won $%d on the Place 4." %((four * 2) - (four * 0.02))
				four = press(four)
			elif five > 0 and comingOut == 5:
				bank += five/5 * 7
				print "You won $%d on the 5." %(five/5 * 7)
				five = press(five)
			elif six > 0 and comingOut == 6:
				bank += six/6 * 7
				print "Yu won $%d on the 6." %(six/6 * 7)
				six = press(six)
			elif eight > 0 and comingOut == 8:
				bank += eight/6 * 7
				print "You won $%d on the 8." %(eight/6 * 7)
				eight = press(eight)
			elif nine > 0 and comingOut == 9:
				bank += nine/5 * 7
				print "You won $%d on the 9." %(nine/5 * 7)
				nine = press(nine)
			elif ten > 0 and comingOut == 10:
				if ten < 25:
					bank += (ten/5) * 9
					print "You won $%d on the 10." %((ten/5) * 9)
				elif ten >= 25:
					bank += (ten * 2) - (ten * 0.02)
					print "You won $%d on the Place 10." %((ten * 2) - (ten * 0.02))
				ten = press(ten)

		if working == True and (hard4 + hard6 + hard8 + hard10) > 0:
			bank += hardPay(comingOut, coHard, hard4, hard6, hard8, hard10)
			hard4, hard6, hard8, hard10 = hardCheck(comingOut, coHard, hard4, hard6, hard8, hard10)

		if comingOut in [4, 9, 10] and fieldBet > 0:
			print "You win $%d on the Field!" %fieldBet
			bank += fieldBet
		elif comingOut in [5, 6, 8] and fieldBet > 0:
			print "You lose $%d on the Field." %fieldBet
			bank -= fieldBet
			fieldBet = 0
		bank += atsCheck(ats, smallNumbers, tallNumbers, atsAll, atsTall, atsSmall)
		smallNumbers, tallNumbers, ats = setClear(smallNumbers, tallNumbers, ats)
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
					print "You have $%d bet for your Odds." %passOdds
				pOddsBet = raw_input("Pass/Don't Pass Line Odds? >")
				if pOddsBet in ['y', 'Y', 'yes', 'Yes']:
					if bet1 in ['p', 'P', 'pass', 'Pass Line', 'Pass']:
						print "How much for your Pass Line Odds?"
						passOdds = betInput(bank)
					elif bet1 in ['d', 'D', 'dp', 'DP', 'dont', "Don't Pass", "don't pass"]:
						print "How much to Lay against the %d?" %comingOut
						passOdds = betInput(bank)

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
#			print "Come Bet?"
			cmBet = raw_input("Come Bet? >")
			if cmBet in ['y', 'Y', 'yes', 'Yes']:

				while True:
					comeChoice = raw_input("Come or Don't Come?")
					if comeChoice in ['c', 'C', 'come', 'Come']:
						print "How much on the Come?"
						comeBet = betInput(bank)
						print "Ok, $%d in the Come." %comeBet
						break
					elif comeChoice in ['d', 'dc', 'dont', "Don't Come", "don't come"]:
						print "How much on the Don't Come?"
						dComeBet = betInput(bank)
						print "Ok, $%d on the Don't Come." %dComeBet
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
						c4Odds = betInput(bank)
					if come5 > 0:
						print "You have $% in Odds for the 5. Enter a new amount." %c5Odds
						c5Odds =	 betInput(bank)
					if come6 > 0:
						print "You have $% in Odds for the 6. Enter a new amount." %c6Odds
						c6Odds = betInput(bank)
					if come8 > 0:
						print "You have $% in Odds for the 8. Enter a new amount." %c8Odds
						c8Odds = betInput(bank)
					if come9 > 0:
						print "You have $% in Odds for the 9. Enter a new amount." %c9Odds
						c9Odds = betInput(bank)
					if come10 > 0:
						print "You have $% in Odds for the 10. Enter a new amount." %c10Odds
						c10Odds = betInput(bank)

# Don't Come Odds

			if (dCome4 + dCome5 + dCome6 + dCome8 + dCome9 + dCome10) > 0:
				alterDont = raw_input("Change Don't Come Odds? >")
				if alterDont in ['y', 'Y', 'yes', 'Yes']:
					if dCome4 > 0:
						print "Your Lay 4 has $% in Odds. Enter the new amount." %dC4Odds
						dC4Odds = betInput(bank)
					if dCome5 > 0:
						print "Your Lay 5 has $% in Odds. Enter the new amount." %dC5Odds
						dC5Odds = betInput(bank)
					if dCome6 > 0:
						print "Your Lay 6 has $% in Odds. Enter the new amount." %dC6Odds
						dC6Odds = betInput(bank)
					if dCome8 > 0:
						print "Your Lay 8 has $% in Odds. Enter the new amount." %dC8Odds
						dC8Odds = betInput(bank)
					if dCome9 > 0:
						print "Your Lay 9 has $% in Odds. Enter the new amount." %dC9Odds
						dC9Odds = betInput(bank)
					if dCome10 > 0:
						print "Your Lay 10 has $% in Odds. Enter the new amount." %dC10Odds
						dC10Odds = betInput(bank)

#Field Bet

			fBet = raw_input("Bet the Field? You have $%d wagered. >" %fieldBet)
			if fBet in ['y', 'Y', 'yes', 'Yes']:
				print "How much on the Field?"
				fieldBet = betInput(bank)
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
				print "Dice are rolling! %d roll." %throws
			else:
				print "Dice are rolling! %d rolls." %throws
			#raw_input("Hit Enter to roll again.")
#Phase 2 Roll
			p2, p2Hard = roll(pointIsOn)
# Use this for specific number testing
#			p2 = 4
#			p2Hard = True

			throws += 1

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
					print "You win $%d on the Come!" %comeBet
					bank += comeBet
				elif p2 in [2, 3, 12]:
					print "You lose $%d from the Come." %comeBet
					bank -= comeBet
				else:
					come4, come5, come6, come8, come9, come10 = come(p2, comeBet, come4, come5, come6, come8, come9, come10)
					cOdds = raw_input("Odds on your Come bet? >")
					if cOdds in ['y', 'Y', 'yes', 'Yes']:
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
					dcOdds = raw_input("Odds on your Don't Come bet? >")
					if dcOdds in ['y', 'Y', 'yes', 'Yes']:
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
			bank += propPayout(p2, any7, anyCraps, cAndE, snakeEyes, aceDeuce, boxcars, horn, eleven)
			any7 = anyCraps = cAndE = snakeEyes = aceDeuce = boxcars = horn = eleven = 0

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

			bank += hardPay(p2, p2Hard, hard4, hard6, hard8, hard10)
			hard4, hard6, hard8, hard10 = hardCheck(p2, p2Hard, hard4, hard6, hard8, hard10)

			if p2 == 4 and four > 0:
				if 0 < four < 25:
					win4 = (four/5) * 9
				elif four >= 25:
					win4 = (four * 2) - (four * 0.02)
				print "You win $%d on the place 4." %win4
				bank += win4
				if comingOut != 4:
					four = press(four)
			if p2 == 5 and five > 0:
				win5 = (five/5) * 7
				print "You win $%d on the place 5." %win5
				bank += win5
				if comingOut != 5:
					five = press(five)
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
				if 0 < ten < 25:
					win10 = (ten/5) * 9
				elif ten >= 25:
					win10 = (ten * 2) - (ten * 0.02)
				print "You win $%d on the place 10." %win10
				bank += win10
				if comingOut != 10:
					ten = press(ten)
# Lay Bets Loss
			if lay4 > 0 and p2 == 4:
				print "You lose $%d from the Lay 4." %lay4
				bank -= lay4
				lay4 = 0
			if lay5 > 0 and p2 == 5:
				print "You lost $%d from the lay 5." %lay5
				bank -= lay5
				lay5 = 0
			if lay6 > 0 and p2 == 6:
				print "You lost $%d from the Lay 6." %lay6
				bank -= lay6
				lay6 = 0
			if lay8 > 0 and p2 == 8:
				print "You lost $%d from the Lay 8." %lay8
				bank -= lay8
				lay8 = 0
			if lay9 > 0 and p2 == 9:
				print "You lost $%d from the Lay 9." %lay9
				bank -= lay9
				lay9 = 0
			if lay10 > 0 and p2 == 10:
				print "You lost $%d from the Lay 10." %lay10
				bank -= lay10
				lay10 = 0

			if p2 in [2, 3, 4, 5, 6]:
				if p2 not in smallNumbers:
					smallNumbers.append(p2)
			elif p2 in [8, 9, 10, 11, 12]:
				if p2 not in tallNumbers:
					tallNumbers.append(p2)
			if p2 not in ats:
				ats.append(p2)


			if p2 == comingOut:
				print "Point hit!"
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
					passOdds = 0
				break
#Seven Out
			elif p2 == 7:
				if atsOn == True and (atsAll + atsTall + atsSmall) > 0:
					print "You lost $%d from the All Tall Small!" %(atsAll + atsTall + atsSmall)
					bank -= (atsAll + atsTall + atsSmall)
					atsAll = atsTall = atsSmall = 0
					if len(ats) > 0:
						ats = smallNumbers = tallNumbers =  []
					atsOn = False


				if lay4 > 0:
					print "You won $%d on the Lay 4." %(lay4 / 2)
					bank += (lay4 / 2)
					lay4 = 0
				if lay5 > 0:
					print "You won $%d on the lay 5!" %((lay5 / 3) * 2)
					bank += (lay5 / 3) * 2
					lay5 = 0
				if lay6 > 0:
					print "You won $%d on the Lay 6!" %((lay6/6) * 5)
					bank += (lay6 / 6) * 5
					lay6 = 0
				if lay8 > 0:
					print "You won $%d on the Lay 8!" %((lay8/6) * 5)
					bank += (lay8 / 6) * 5
					lay8 = 0
				if lay9 > 0:
					print "You won $%d on the lay 9!" %((lay9 / 3) * 2)
					bank += (lay9 / 3) * 2
					lay9 = 0
				if lay10 > 0:
					print "You won $%d on the Lay 10!" %(lay10 / 2)
					bank += lay10 / 2
					lay10 = 0

				come4 = come5 = come6 = come8 = come9 = come10 = c4Odds = c5Odds  = c6Odds = c8Odds = c9Odds = c10Odds = dCome4 = dCome5 = dCome6 = dCome8 = dCome9 = dCome10 = dC4Odds = dC5Odds = dC6Odds = dC8Odds = dC10Odds = 0
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
						passOdds = 0
					bank -= passLine
				elif bet1 == 'd':
					print "You win $%d!" %dPass
					if passOdds > 0:
						dOdds = odds(comingOut, passOdds, bet1)
						print "You won $%d on your Don't Pass Odds." %dOdds
						bank += dOdds
						passOdds = 0
					bank += dPass
				if any7 > 0:
					print "You win $%d on Any 7!" %(any7 * 4)
					bank += any7 * 4
					any7 = 0
				throws = 0
				break
			else:
				print "Bank = $%d. The point is %d." %(bank, comingOut)
				bank += atsCheck(ats, smallNumbers, tallNumbers, atsAll, atsTall, atsSmall)
				smallNumbers, tallNumbers, ats = setClear(smallNumbers, tallNumbers, ats)
				#raw_input("Roll Again!")
				continue
		print "You have $%d in your bank!" %bank
	bank += atsCheck(ats, smallNumbers, tallNumbers, atsAll, atsTall, atsSmall)
	smallNumbers, tallNumbers, ats = setClear(smallNumbers, tallNumbers, ats)
	continue
