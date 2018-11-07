from random import *
four = five = six = eight = nine = ten = hard4 = hard6 = hard8 = hard10 = any7 = anyCraps = cAndE = snakeEyes = aceDeuce = boxcars = 0

def prop():
	any7 = anyCraps = cAndE = snakeEyes = aceDeuce = boxcars = 0

	pr1 = raw_input("Bet on Any 7?")
	if pr1 == 'y':
		any7 = input("How Much on Any 7? $>")
		print "Ok, $%d on Any 7." %any7
	pr2 = raw_input("Bet on Any Craps?")
	if pr2 == 'y':
		anyCraps = input("How much on Any Craps? $<")
		print "Ok, $%d on Any Craps." %anyCraps
	pr3 = raw_input("Bet on C&E?")
	if pr3 == 'y':
		cAndE = input("How much on C&E? $>")
		print "Ok, $%d on C&E." %cAndE
	pr4 = raw_input("Bet on Snake Eyes?")
	if pr4 == 'y':
		snakeEyes = input("How much on Snake Eyes? $>")
		print "Ok, $%d on Snake Eyes." %snakeEyes
	pr5 = raw_input("Bet on Acey-Deucey?")
	if pr5 == 'y':
		aceDeuce = input("How much on Acey-Deucey? $>")
		print "Ok, $%d on Acey-Deucey." %aceDeuce
	pr6 = raw_input("Bet on Boxcars?")
	if pr6 == 'y':
		boxcars = input("How much on Boxcars? $>")
		print "Ok, $%d on Boxcars." %boxcars
	return any7, anyCraps, cAndE, snakeEyes, aceDeuce, boxcars

def propPayout(roll, any7, anyCraps, cAndE, snakeEyes, aceDeuce, boxcars):
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
			print "You win $%d on your Aces bet!" %(snakeEyes * 31)
			payout += snakeEyes * 31
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
			lpayout += boxcars * 30
		else:
			print "You lose $%d on the Boxcars bet." %boxcars
			payout -= boxcars
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

def odds(comingOut, bet):
	oddsOut = 0
	if comingOut in [4, 10]:
		oddsOut = bet * 2
	elif comingOut in [5, 9]:
		oddsOut = bet/2 * 3
	elif comingOut in [6, 8]:
		oddsOut = bet/5 * 6

	return oddsOut

def press(x):
	press = raw_input("Press this bet? y/n")
	if press == 'y':
		x = input("New bet >")
		print "You now bet  $%d." %x
	else:
		pass
	return x

#Game Start
print "Craps Craps Craps!"

bank = input("How much do you want to start with? $ >")
print "Ok, starting off with $%d." %bank

comeBet = 0
come = []

while True:
	pointIsOn = False
	passLine = 0
	dPass = 0
	fieldBet = 0
	bet1 = raw_input("Pass or Don't pass?")
	if bet1 == 'p':
		passLine = input("How much on the Pass Line? $ >")
		print "Great, $%d on the Pass Line." %passLine
	elif bet1 == 'd':
		dPass = input("How much on the Don't Pass line? $ >")
		print "Great, $%d on the Don't Pass Line." %dPass
	else:
		print "That won't work!"
		continue
	fBet = raw_input("Bet the Field? y/n")
	if fBet == 'y':
		fieldBet = input("How much on the Field?")
		print "Ok, $%d on the Field." %fieldBet
	propStart = raw_input("Proposition Bets?")
	if propStart == 'y':
		any7, anyCraps, cAndE, snakeEyes, aceDeuce, boxcars = prop()

	print "Dice are coming out!"
	comingOut, coHard = roll(pointIsOn)
	bank += propPayout(comingOut, any7, anyCraps, cAndE, snakeEyes, aceDeuce, boxcars)
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
			passOdds = input("How much for your line odds?")
		else:
			passOdds = 0
		#Betting
		while True:
			any7 = anyCraps = cAndE = snakeEyes = aceDeuce = boxcars = 0
			placeBet = raw_input("Place bets? y/n")
			if placeBet == 'y':
				four = input("How much on Place 4?")
				five = input("How much on 5?")
				six = input("How much on Six?")
				eight = input("How much on Eight?")
				nine = input("How much on 9?")
				ten = input("How much on 10?")

#Come Bet
	#		cmBet = raw_input("Come bet? y/n")
#			if cmBet == 'y':
			#	comeBet = "How much on the Come bet?")
		#		print "Ok, $%d in the Come." %comeBet
#Field Bet

			fBet = raw_input("Bet the Field? You have $%d wagered. y/n" %fieldBet)
			if fBet == 'y':
				fieldBet = input("How much on the Field?")
			#else:
				#fieldBet = 0

#Hard Ways
			hWays = raw_input("Bet the hard ways? y/n")
			if hWays == 'y':
				hard4 = input("How much on Hard 4?")
				hard6 = input("How much on Hard 6?")
				hard8 = input("How much on Hard 8?")
				hard10 = input("How much on Hard 10?")
				print "Ok, $%d, $%d, $%d, $%d on the 4, 6, 8, and 10!" %(hard4, hard6, hard8, hard10)
#Prop Bets
			#props = raw_input("Proposition Bets? y/n")
		#	if props == 'y':
	#			any7, anyCraps, cAndE, snakeEyes, aceDeuce, boxcars = prop()

			print "Dice are rolling!"
			#raw_input("Hit Enter to roll again.")
#Phase 2 Roll
			p2, p2Hard = roll(pointIsOn)

		#	if comeBet > 0:
	#			come.append(p2)

#Prop Bet Payout
			bank += propPayout(p2, any7, anyCraps, cAndE, snakeEyes, aceDeuce, boxcars)


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
				print "You win $%d on the Hard 4!" %(hard4 * 10)
				bank += hard4 * 10
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
				print "You win $%d on the Hard 10!" %(hard10 * 10)
				bank += hard10 * 10
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
						oddsWin = odds(comingOut, passOdds)
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
				if hard4 + hard6 + hard8 + hard10 > 0:
					print "You lose $%d from the Hard Ways." %(hard4 + hard6 + hard8 + hard10)
					bank -= (hard4 + hard6 + hard8 + hard10)
					hard4 = hard6 = hard8 = hard10 = 0
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
						dOdds = odds(comingOut, dPass)
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
	continue