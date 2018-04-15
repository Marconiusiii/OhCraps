from random import *

def roll(pointOn):
	d1 = randint(1, 6)
	d2 = randint(1, 6)
	total = d1 + d2
	diceCallOut(d1, d2, total, pointOn)
	return total,

def diceCallOut(d1, d2, total, pointOn):
	if d1 == d2:
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

print "Craps! v.1.2"

print "Dice are coming out!"

while True:
	raw_input("Hit Enter for your Coming Out roll!")
	pointOn = False
	comingOut = roll(pointOn)
	if comingOut == 7 or comingOut == 11:
		print "Winner!"
		continue
	elif comingOut == 2 or comingOut == 3 or comingOut == 12:
		print "Craps!"
		continue
	else:
		print "The point is %d!" %comingOut
		raw_input("Hit Enter to roll again!")
		while True:
			pointOn = True
			phase2 = roll(pointOn)
			if phase2 == 7:
				print "Loser!"
				break
			elif phase2 == comingOut:
				print "We have a winner!"
				break
			else:
				print "Hit Enter to roll again!"
				raw_input(">")
				continue
	continue