# OhCraps! v.5.3
Python-based Craps game for Terminal.

## About

Craps is one of the best games you can play in a casino and contains a variety of bets that have some of the lowest house advantage percentages over you. This game is built to run within a Terminal environment and is accessible for blind players.

Craps is entirely based on the randomness of thrown dice. When the game starts, a bet on the Pass Line will win if a 7 or 11 is thrown with the first roll, also known as the Coming Out roll. A 2, 3, or 12 will lose on the first roll. Any other number thrown on the first roll becomes the Point number, and then the shooter continues to roll until they either roll the Point number or throw a 7. Hitting the Point number is a Pass Line win, the game resets and everything starts up again. Rolling a 7 on the other hand after a Point is established is a loss, and all bets on the table lose, with the exception of Don't Pass/Don't Come bets and Any 7 proposition bets.

## How to Play

After downloading the OhCraps_Py3.command file, double-click or Open the file and it will open the Terminal app and run. Alternatively, with Terminal open, cd to the directory where the command file was downloaded and run:
$ python3 OhCraps_Py3.command

The game starts off asking you to set up a bankroll. Enter a numeric amount to start.

### Coming Out Roll

You've established your bankroll and are now ready to start betting. You have a few options for the very first roll, and all options are accessed by typing the letter 'y' and then hitting Enter to proceed. You can bypass any of the bets by simply hitting Enter to move on through the game.

#### Line Bets

Bet on the Pass Line by typing 'p' and hitting Enter, then follow the prompt to put in a bet amount.

Bet on the Don't Pass Line by typing 'd' and hitting Enter, then follow the prompts to place your bet.

Once you've set your Line Bets, type 'x' and hit Enter to continue on with the game.

#### Place Bets

Typing 'y' and hitting Enter when prompted with the Place Bets will take you through the Place Bet flow, asking you for a bet on each of the place numbers (4, 5, 6, 8, 9, 10). Enter a 0 if you want to keep the bet clear, otherwise enter your bet to Place the number. Typing Enter will bypass the current Place Number and leave the bet alone and move you to the next number.

If the Place Bet number is rolled, you'll be prompted to Press your Bet. Hit Enter to decline, or enter 'y' to edit the Place Bet. Enter 0 to remove it.

Emulating how Craps works in Las Vegas, Placing the 4 or 10 for $10 or more will automatically Buy those bets, and the 5% commission is factored into what you win if they hit. For example, Buying the Place 4 for $25 will win 2 for 1, so you pay a $1 vig to win $50, and will end up collecting $49. The vig will round up to the nearest dollar for bets under $20, and will round down to the nearest dollar for everything else.

In the Place Bet prompt, if you type 'd' or 'td' instead of 'y' and hit Enter, this will take down all your bets. A quick and simple way to 0 them all out. This works both in the Come Out phase and also after a Point has been established.

After a Point has been established, when you are prompted with the Place Bet option, typing 'o' or 'off' and hitting Enter will turn your Place Bets Off for the next roll. This means that hitting any of the numbers or a 7 Out will not affect your bets and you will not get paid. The bets stay Off for only this one roll, so you'll need to turn them off after each roll if you want them to stay off for an extended period of rolls.

#### Lay Bets

Lay Bets are the opposite of Place Bets. You will be wagering money that the 7 rolls before the number you are betting on hits. This functionality works the same way as the Place Betting system, where you will be asked how much you'd like to Lay against each number. Enter a 0 or just hit Enter to leave the bet alone.

At the Lay Bet prompt, typing 'd' or 'td' and hitting Enter will take down all your Lay Bets.

After  point has been established, you'll be able to turn your Lay bets Off when prompted for the Lay Bets. Type 'o' or 'off' and hit Enter to turn your Lay Bets Off for the next roll. Just like the Place Bets, they will only be Off for the very next roll. Wht the Lay bets Off, they will not be affected by a 7 out or by rolling the Lay number.

Check the Pay Table to see how each of the Lay Bets pays out. There is a 5% commission paid back to the House when a Lay bet wins.

#### Field Bet

The Field Bet is a bet on the numbers 2, 3, 4, 9, 10, 11, and 12. If a 2 is rolled, you win double your bet, and if a 12 is rolled, you will win triple your bet. All other numbers win even money. A 5, 6, 7, or 8 will lose.

Type 'y' if you'd like to bet on the Field, otherwise hit Enter to bypass it. Follow the prompts to place your bet.

Field Bets stay up on the table after winning. To take down a Field Bet, type 'd' or 'td' at the Field Bet prompt and hit Enter. You can also go into the prompt and enter a Field Bet of $0.

#### Hard Ways

The Hard Ways bets are Proposition Bets that are not Single-Roll bets. These are bets that a 4, 6, 8, or 10 are rolled  the Hard Way, or with double numbers. Rolling a 4 and 4 will make a Hard 8, for example. Rolling a 6 and 2 is an Easy 8. A Hard Ways bet wins if any of the double numbers are rolled and will lose on either a 7 Out or if the Easy variant of the number is rolled. If you win a Hard Way bet, you'll be prompted to change your bet. Hit Enter to leave your current bet alone as is, type a number to change the bet, or enter 0 to take the bet down. Alternatively, if you lose the Hard Way bet, you'll be prompted to go back up on the bet; enter a number to bet again on that Hard Way number, or hit Enter to bypass the bet and leave it blank.

At any point, entering 'd' or 'td' at the Hard Ways bet prompt and hitting Enter will take down all your Hard Ways bets.

After a Point has been established, you can turn your Hard Ways bets Off by typing 'o' or 'off' and hitting Enter when you are prompted with the "Hard Ways?" option. This will take your bets out of action for the next roll. Hitting a Hard Way number, and Easy number, or a 7 Out will not affect your bets when they are Off.

Much like the Place Bets, you will be prompted to bet on the 4, 6, 8, and 10 in order, then you will get a confirmation on what you've bet before the game continues on. Enter 0 to clear a bet or not bet on any of the numbers.

#### Working  Bets

If you've made Place Bets, Lay Bets, or Hard Ways bets, you can have them Working on the Come Out roll. Generally, when you make a Place Bet or Hard Ways bet before a Point is established, the bets are Off by default, meaning they will not be affected by the roll of the dice. Having your bets "Working" means that you are turning them on and they will be affected by the next roll of the dice.

If you've Placed, Laid, or made Hard Ways Bets, the "Place and Hard Ways Bets Working?" option will appear in the list, and entering 'y' and hitting Enter will set them all to be Working on the Come Out Roll.

#### Proposition Bets

These bets are all single-roll bets. If they do not come up on the very next roll, they will lose. When you activate the Prop Bet by typing "y", another text prompt will come up asking you for which specific bet you'd like to add. Type in the bet code and hit Enter to bring up the betting prompt for your choice. After you've entered your bet, you'll be returned to the Prop Bet prompt. Type in another code to make another bet, type "all" to see all the bets you've made, type 'help' to see a list of all commands, or type 'x' and hit Enter to finish up and move onwards with the game.

1. Any 7 - Bet on any 7 to come up.
	• Bet Code: "7"
2. Any Craps - Bet on a 2, 3, or 12 to come up.
	• Bet Code: "cr"
3. C & E - Bet on a 2, 3, 11, or 12 to come up.
	• Bet Code: "ce"
4. Snake Eyes - Bet that a 2 comes up.
	• Bet Code: "s" or "2"
5. Acey-Deucey - Bet on a 3 to come up.
	• Bet Code: "ad" or "3"
6. Boxcars - Bet that a 12 comes up.
	• Bet Code: "b" or "12"
7. Horn - Bet that a 2, 3, 11, or 12 comes up.
	• Bet Code: "h", "horn"
8. Yo - Betting that an Eleven will be the next roll outcome.
	• BetCodes: "11", "eleven", "56"
9. All - See all prop bets you've placed.
	• Code: all
10. Help - See a list of all Prop Bet commands.
	• Code: help
11. Exit Prop betting and return to the game.
	• Code: x

Check the Pay Table section to understand the various payouts for all these bets.

#### All Tall Small

The All Tall Small bet is an interesting persistent bet where you are betting that a set of numbers will all appear before the 7. Small means you are betting that the 2, 3, 4, 5, and 6 will appear before the 7; Tall means you are betting that the 8. 9. 10, 11, and 12 will appear; All is a bet that both the small and tall numbers will all appear before the 7.

This bet is made at the Come Out roll and will not appear again until a 7 out. The game will keep track of your rolls and display them each time you roll the dice. You will only lose this bet on a 7 Out or a 7 on the Come Out roll.

#### FIre Bet

This is the bet for players who think they can hit a hot streak of Point numbers before a 7 out. Like the All Tall Small, the Fire Bet is a persistent bet made in the Come Out phase. This is a bet on how many Point numbers the shooter hits before a 7. For example, if the shooter rolls a Point of 5 in the Come Out roll, and then rolls a 5 and wins the Point, the 5 is marked in the Fire Bet and it now counts as 1 Point Hit. Then if the shooter rolls a 4 on the Come Out, then wins the hand by rolling the Point 4 again, the 4 gets marked in the Fire Bet, counting as 2 Points won. If a Point number is rolled again, such as the shooter rolling a 5 after all of this, that Point will not count if the shooter wins. 

Once a shooter wins 4 Points, the Fire Bet will pay out on the next 7 Out. If the shooter 7s Out while 3 or less points have been hit in the Fire Bet, you lose the Fire Bet and have to start over. This is a risky bet, but can pay off big with just a $1 bet and a lot of luck. If the shooter rolls 4 Points and then 7s out, you win 24:1. If the shooter rolls 5 points and then 7s out, you win 249:1, and if the Fire Bet is at the maximum of 6 points rolled, you will win 999:1!

### Point Phase

If a 4, 5, 6, 8, 9, or 10 is rolled on the Coming Out roll, that number becomes the Point. Roll the dice until the Point is hit to win on the Pass Line and reset the game, or until a 7 is rolled, clearing all the bets in a loss and returning to the Come Out roll.

New betting modes appear in the Point phase:

#### Line Odds

When a point is established, you'll have the ability to add Pass Line Odds or a Lay Bet to your initial Line Bet. If you bet on the Pass Line before the Coming Out roll, you'll be asked if you want Pass Line Odds. If you bet on the Don't Pass Line, you'll be prompted for a Lay Bet. Both are optional and can be bypassed by hitting Enter.

#### Take Down Don't Pass Bet

Due to the overall low House edge that Don't Pass bets have in casinos, the Don't Pass Bet and Don't Pass Odds can actually be taken down at any point of game play. It is not a contractual bet like the Pass Line, which has to stay up until a Point is hit or a 7 out. This game option will only appear if you make a Don't Pass bet before the Come Out roll. Type 'y' and hit Enter to take down the bet, and your DOn't Pass Bet and Odds will be returned to you, and you will not be able to make another Don't Pass bet until the next Come Out roll.

#### Come and Don't Come

The Come and Don't Come Fields act like additional Pass Line Bets after a Point has been established. Placing these bets is only possible after the Point Phase has started. Enter 'y' if you want to bet on these fields when prompted, then Enter a 'c' for Come or a 'd' for Don't Come.

##### Come Bet
A Come Bet will win if a 7 or 11 is rolled, and lose with a 2, 3, or 12. If any other number is rolled, the Come Bet moves to that number, and you will be prompted for Come Bet Odds.  If that Come Bet number is rolled before a 7, you will win. If a 7 is rolled before any of the Come Bet numbers are hit, all Come bets are cleared and you lose.

##### Don't Come Bet
The Don't Come is the opposite of the Come. A bet here wins on a 2, 3 or 12 and loses with a 7 or 11. If any other number is rolled, the Don't Come moves to that number and you are prompted to add Odds, which are always optional. Should a 7 roll before the Don't Come number is rolled, you win on all Don't Come bets. If the Don't Come number is rolled before a 7, you lose that bet.

If Come or Don't Come bets are working during the Coming Out roll, all Come and Don't Come Odds bets are Off, or are not counted on the Coming Out Roll. If a 7 is rolled for the Coming Out roll, Come bets will lose but the Odds will be ignored, while a Don't Come bet will win but will also have the Odds ignored until a Point is established.

#### going Off on your bets

As mentioned in the Place Lay, and Hard Ways sections, you can take these bets Off for the next roll by typing 'o' or 'off' and hitting Enter when you are prompted for those bets. After the very next roll, those bets will turn back On.

#### Field and Proposition Bets

These bets are available at all times. If there is a bet on the Field, the Field Bet prompt will announce it.

## Pay Table

<table>
<caption>Line, Field, and Come Payouts</caption>
<tr>
<th>Bet</th>
<th>Payout</th>
</tr>
<tr>
<td>Pass/Don't Pass Line</td><td>1:1</td>
</tr>
<tr>
<td>Pass Line Odds 4 and 10</td><td>2:1</td>
</tr>
<tr>
<td>Pass Line Odds 5 and 9</td><td>3:2</td>
</tr>
<tr>
<td>Pass Line Odds 6 and 8</td><td>6:5</td>
</tr>
<tr>
<td>Field Bet</td><td>1:1</td>
</tr>
<tr>
<td>Field Bet 2</td><td>2:1</td>
</tr>
<tr>
<td>Field Bet 12</td><td>3:1</td>
</tr>
<tr>
<td>Place 4 and 10</td><td>9:5</td>
</tr>
<tr>
<td>Place 5 and 9</td><td>7:5</td>
</tr>
<tr>
<td>Place 6 and 8</td><td>7:6</td>
</tr>
<tr>
<td>Come/Don't Come Bet</td><td>1:1</td>
</tr>
<tr>
<td>Come/DC Odds 4 and 10</td><td>2:1</td>
</tr>
<tr>
<td>Come/DC Odds 5 and 9</td><td>3:2</td>
</tr>
<tr>
<td>Come/DC Odds 6 and 8</td><td>6:5</td>
</tr>
<tr>
<td>Lay 4, 10</td><td>1:2</td>
</tr>
<tr>
<td>Lay 5, 9</td><td>2:3</td>
</tr>
<tr>
<td>Lay 6, 8</td><td>5:6</td>
</tr>
</table>
<table>
<caption>Proposition Bet Payouts</caption>
<tr>
<th>Bet</th><th>Payout</th>
</tr>
<tr>
<td>Any 7</td><td>4:1</td>
</tr>
<tr>
<td>Any Craps</td><td>7:1</td>
</tr>
<tr>
<td>C & E with Craps</td><td>3:1</td>
</tr>
<tr>
<td>C&E with 11</td><td>7:1</td>
</tr>
<tr>
<td>Snake Eyes</td><td>30:1</td>
<tr>
<tr>
<td>Acey-Deucey</td><td>15:1</td>
</tr>
<tr>
<td>Boxcars</td><td>30:1</td>
</tr>
<tr>
<td>Horn Bet on 2, 12</td><td>30:1 - 3/4 of initial bet</td>
</tr>
<tr>
<td>Horn Bet on 3, 11</td><td>15:1 - 3/4 of initial bet</td>
</tr>
<tr>
<td>Yo Eleven</td>
<td>15:1</td>
</tr>
<tr>
<td>Hard 4 and 10</td><td>7:1</td>
</tr>
<tr>
<td>Hard 6 and 8</td><td>9:1</td>
</tr>
<tr>
<td>Small and Tall</td><td>35:1</td>
</tr>
<tr>
<td>The All</td><td>176:1</td>
</tr>
<tr>
<td>4 Fire Bet Points</td><td>24:1</td>
</tr>
<tr>
<td>5 Fire Bet Points</td><td>249:1</td>
</tr>
<tr>
<td>6 Fire Bet Points</td><td>999:1</td>
</tr>
</table>