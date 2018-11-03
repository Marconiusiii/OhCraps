from random import *

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
	bet1 = raw_input("(p)ass or (d)on't pass?")
	if bet1 == 'p':
		passLine = input("How much on the Pass Line? $ >")
		print "Great, $%d on the Pass Line." %passLine
	elif bet1 == 'd':
		dPass = input("How much on the Don't Pass line? $ >")
		print "Great, $%d on the Don't Pass Line." %dPass
	else:
		print "That won't work!"
		continue
	print "Dice are coming out!"
	comingOut, coHard = roll(pointIsOn)
	if comingOut in [7, 11]:
		if bet1 == 'p':
			print "You won $%d!" %passLine
			bank += passLine
		elif bet1 == 'd':
			print "You lost $%d." %dPass
			bank -= dPass
		print "You now have $%d in your bank." %bank
		continue
	elif comingOut in [2, 3, 12]:
		if bet1 == 'p':
			print "You lost $%d." %passLine
			bank -= passLine
		elif bet1 == 'd':
			print "You win $%d!" %dPass
			bank += dPass
		print "You now have $%d in your bank." %bank
		continue
	else:
		pointIsOn = True
		print "The point is %d." %comingOut
		pOddsBet = raw_input("Odds on your Line bet? y/n")
		if pOddsBet == 'y':
			passOdds = input("How much for your line odds?")
		else:
			passOdds = 0
		#Betting
		while True:
			placeBet = raw_input("Place bets? y/n")
			if placeBet == 'y':
				four = input("How much on Place 4?")
				five = input("How much on 5?")
				six = input("How much on Six?")
				eight = input("How much on Eight?")
				nine = input("How much on 9?")
				ten = input("How much on 10?")
	
			#comeBet = "How much on the Come bet?")
			fBet = raw_input("Bet the Field? y/n")
			if fBet == 'y':
				fieldBet = input("How much on the Field?")
			else:
				fieldBet = 0
			#hWays = raw_input("Bet the hard ways? y/n")
			#if hWays == 'y':
				#hard4 = input("How much on Hard 4?")
				#hard6 = input("How much on Hard 6?")
				#hard8 = input("How much on Hard 8?")
				#hard10 = input("How much on Hard 10?")
			#	print "Ok, $%d, $%d, $%d, $%d on the 4, 6, 8, and 10!" %(hard4, hard6, hard8, hard10)
			raw_input("Hit Enter to roll again.")

			p2, p2Hard = roll(pointIsOn)
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
	
#Hard Ways
#			if p2 == 

			if p2 == 4 and four > 0:
				win4 = (four/5) * 9
				print "You win $%d on the place 4." %win4
				bank += win4
				#four = press(four)
			if p2 == 5 and five > 0:
				win5 = (five/5) * 7
				print "You win $%d on the place 5." %win5
				bank += win5
				#five = press(5)
			if p2 == 6 and six > 0:
				print "You win $%d on the place 6." %(six/6 * 7)
				bank += six/6 * 7
				six = press(six)

			if p2 == 8 and eight > 0:
				print "You win $%d on the place Eight." %(eight/6 * 7)
				bank += eight/6 * 7
				eight = press(eight)
			if p2 == 9 and nine > 0:
				win9 = (nine/5) * 7
				print "You win $%d on the place 9!" %win9
				bank += win9
				#nine = press(nine)

			if p2 == 10 and ten > 0:
				win10 = (ten/5) * 9
				print "You win $%d on the place 10." %win10
				bank += win10
				#ten = press(ten)
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
			elif p2 == 7:
				print "You lose $%d from the place bets." %(four + five + six + eight + nine + ten)
				bank -= (four + five + six + eight + nine + ten)
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
				break
			else:
				print "Bank = $%d. The point is %d." %(bank, comingOut)
				#raw_input("Roll Again!")
				continue
		print "You have $%d in your bank!" %bank
	continue