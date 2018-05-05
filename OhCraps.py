from random import *

def roll(pointOn):
	isItHard = False
	d1 = randint(1, 6)
	d2 = randint(1, 6)
	total = d1 + d2

	if d1 == d2:
		isItHard = True
		if total == 2:
			print "Snake Eyes!"
		elif total == 4 or total == 6 or total == 8 or total == 10:
			print "Hard %d!" %total
		else:
			print "12, Boxcars!"
	else:
		if total == 11:
			print "Yo 11 yo!"
		elif total == 7:
			if pointOn == False:
				print "Winner 7!"
			else:
				print "7 Out."
		else:
			print "%d easy %d!" %(total, total)

	return total


#Initial bet

lineBets = [0, 0, 0, 0, 0]

# 0 - Pass Line
# 1 - Don't Pass
# 2 - Pass Line Odds
# 3 - Field Bet
# 4 - Come
#5 - Don't Come

placeBets = [0, 0, 0, 0, 0, 0]

# 0 - place 4
# 1 - place 5
# 2 - place 6
# 3 - place 8
#4 - place 9
# 5 - place 10

hardBets = [0, 0, 0, 0]

# 0 - Hard 4
# 1 - Hard 6
# 2 - Hard 8
# 3 - Hard 10

singleBets = [0, 0, 0, 0, 0, 0, 0]

# 0 - Craps & Eleven
# 1 - Any 7
# 2 - 1 and 1, snake eyes
# 3  - 1 and 2, Three craps
# 4 - hard 12, Boxcars, 6 and 6
# 5 - Horn bet, 2, 3, 11, 12
# 6 - Any Craps
# Line Bet Function

def line():
	pl = dpl = fld = come = dcome = 0
	while True:
		print "1. Pass Line 2. Don't Pass Line 3. Field Bet 4. Come Bet 5. Don't Come 6. Cancel/Done"
		lb = input(">")
		if lb == 1:
			print "How much on the Pass Line?"
			pl = input("$")
			continue
		elif lb == 2:
			print "How much on the Don't Pass Line?"
			dpl = raw_input("$>")
			continue
		elif lb == 3:
			print "How much on the Field?"
			fld = input("$>")
			continue
		elif lb == 4:
			print "How much on the Come Line?"
			come = raw_input("$>")
			continue
		elif lb == 5:
			print "How much on the Don't Come Line?"
			dcome = raw_input("$>")
			continue
		elif lb == 6:
			print "Finished betting."
			break
	if pl > 0:
		print "You've bet $%d on the Pass Line." %pl
	else:
		pass
	if dpl > 0:
		print "You've bet $%d on the Don't Pass Line." %dpl
	else:
		pass
	if fld > 0:
		print "You've bet $%d on the Field." %fld
	else:
		pass
	if come > 0:
		print "You've bet $%d on the Come Line."
	else:
		pass
	if dcome > 0:
		print "You've bet $%d on the Don't Come Field."
	else:
		pass
	return pl, dpl, fld, come, dcome

def place():
	four = five = six = eight = nine = ten = 0
	while True:
		print "1. Place 4 2. Place 5 3. Place 6 4. Place 8 5. Place 9 6. Place 10 7. Done"
		plChoice = input("Pick a number >")
		if plChoice == 1:
			print "How much on 4?"
			four = input("$>")
			continue
		elif plChoice == 2:
			print "How much on 5?"
			five = input("$>")
			continue
		elif plChoice == 3:
			print "How much on 6?"
			six = input("$>")
			continue
		elif plChoice == 4:
			print "How much on 8?"
			eight = input("$>")
			continue
		elif plChoice == 5:
			print "How much on 9?"
			nine = input("$>")
			continue
		elif plChoice == 6:
			print "How much on 10?"
			ten = input("$>")
			continue
		elif plChoice == 7:
			print "Finished betting."
			break
	return four, five, six, eight, nine, ten

def hard():
	h4 = h6 = h8 = h10 = 0
	while True:
		print "1. Hard 4 2. Hard 6 3. Hard 8 4. Hard 10 5. All the hard Ways/Bump 6. Done"
		hChoice = input("Pick a number!")
		if hChoice == 1:
			h4 = input("$>")
			print "YOu bet $%d on Hard 4." %h4
			continue
		elif hChoice == 2:
			print "How much on hard 6?"
			h6 = input("$>")
			print "Ok, $%d on Hard 6." %h6
			continue
		elif hChoice == 3:
			print "How much on Hard 8?"
			h8 = input("$>")
			print "Ok, $%d on Hard 8." %h8
			continue
		elif hChoice == 4:
			print "How much on hard 10?"
			h10 = input("$>")
			print "Ok, $%d on Hard 10." %h10
			continue
		elif hChoice == 5:
			print "How much would you like to bump up the Hard Ways?"
			bump = input("$ on each >")
			h4 += bump
			h6 += bump
			h8 += bump
			h10 += bump
			print "Alright, you've got $%d on each of the Hard Ways." %bump
			continue
		elif hChoice == 6:
			print "Finished betting."
			break
		else:
			pass
	return h4, h6, h8, h10
	
def single():
	ce = any7 = snake = three = boxcars = horn = anyCraps = 0
	while True:
		print "1. Craps and Eleven 2. Any 7 3. Snake Eyes 4. Acey-Deucey 5. Boxcars 6. Horn Bet 7. Any Craps 8. Done"
		sChoice = input("Pick a number >")
		if sChoice == 1:
			print "How much on C&E?"
			ce = input("$>")
			print "GOt it, $%d on Craps and Eleven." %ce
			continue
		elif sChoice == 2:
			print "How much on Any 7?"
			any7 = input("$>")
			print "Ok, $%d on Any Seven." %any7
			continue
		elif sChoice == 3:
			print "How much on Snake Eyes?"
			snake = input("$>")
			print "Alright, you have $%d on a pair of Aces." %snake
			continue
		elif sChoice == 4:
			print "How much on Acey-Deucey?"
			three = input("$>")
			print "Ok, you have $%d on a Three." %three
			continue
		elif sChoice == 5:
			print "How much would you like on Boxcars?"
			boxcars = input("$>")
			print "Ok, you have $%d on the 6 double." %boxcars
			continue
		elif sChoice == 6:
			print "How much on the Horn Bet?"
			horn = input("$>")
			print "Got it, $%d riding on the Horn." %horn
			continue
		elif sChoice == 7:
			print "How much on Any Craps?"
			anyCraps = input("$>")
			print "You got it. $%d on Any Craps." %anyCraps
			continue
		elif sChoice == 8:
			print "finished betting."
			break
		else:
			print "Did you forget to make a choice?"
			continue
	return ce, any7, snake, three, boxcars, horn, anyCraps

# Full Betting Engine

def bet(lineBets, placeBets, hardBets, singleBets):
	while True:
		print "1. Line Bets 2. Place Bets 3. Hard Ways 4. Single Bets 5. Finished Betting"
		betChoice = input(">")
		if betChoice == 1:
			lineBets = line()
			continue
		elif betChoice == 2:
			placeBets = place()
			continue
		elif betChoice == 3:
			hardBets = hard()
			continue
		elif betChoice == 4:
			singleBets = single()
			continue
		elif betChoice == 5:
			print "All done? Let's roll!"
			break
		else:
			print "You didn't choose a betting option!"
			continue
	return lineBets, placeBets, hardBets, singleBets



	
# Begin game

print "Craps! v.1.2"

print "How much would you like to cash in for your bank?"
while True:
	try:
		bank = int(raw_input("$"))
		break
	except ValueError:
		print "That wasn't a number, doofus."
		continue
print "Great, starting off with $%d." %bank

while True:
	print "you have $%d left in your bank." %bank
	pointOn = False
	bets = []
	print "Place your bets!"

	lineBets, placeBets, hardBets, singleBets = bet(lineBets, placeBets, hardBets, singleBets)
	
	print "Dice are coming out!"
	raw_input("Hit Enter for your Coming Out roll!")

	comingOut = roll(pointOn)

	if comingOut == 7:
		print "Winner!"
		if lineBets[0] > 0:
			bank += lineBets[0]
			print "You won $%d!" %lineBets[0]
		else:
			pass
		continue
	elif comingOut == 11:
		print "Yo 11 Winner!"
		if lineBets[0] > 0:
			bank += lineBets[0]
			print "You won $%d!" %lineBets[0]
		else:
			pass
		continue
	elif comingOut == 2 or comingOut == 3 or comingOut == 12:
		print "Craps!"
		if lineBets[0] > 0:
			bank -= lineBets[0]
			print "You lost $%d." %lineBets[0]
		else:
			pass
		continue
	else:
		pointOn = True
		print "The point is %d!" %comingOut
		while True:
			raw_input("Hit Enter to roll again!")
			p2 = roll(pointOn)
			if p2 == 7:
				print "That's a loss. Resetting the table."
				if lineBets[0] > 0:
					bank -= lineBets[0]
					print "You lost $%d." %lineBets[0]
				break
			elif p2 == comingOut:
				print "We have a winner!"
				if lineBets[0] > 0:
					bank += lineBets[0]
					print "You won $%d!" %lineBets[0]
				else:
					pass
				break
			else:
				continue

		continue