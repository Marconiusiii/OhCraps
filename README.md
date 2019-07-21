# OhCraps
Python-based Craps game for Terminal.

## About

Craps is one of the best games you can play in a casino and contains a variety of bets that have some of the lowest house advantage percentages over you. This game is built to run within a Terminal environment and is accessible for blind players.

Craps is entirely based on the randomness of thrown dice. When the game starts, a bet on the Pass Line will win if a 7 or 11 is thrown with the first roll, also known as the Coming Out roll. A 2, 3, or 12 will lose on the first roll. Any other number thrown on the first roll becomes the Point number, and then the shooter continues to roll until they either roll the Point number or throw a 7. Hitting the Point number is a Pass Line win, the game resets and everything starts up again. Rolling a 7 on the other hand after a Point is established is a loss, and all bets on the table lose, with the exception of Don't Pass/Don't Come bets and Any 7 proposition bets.

## How to Play

The game starts off asking you to set up a bankroll. Enter a numeric amount to start.

### Coming Out Roll

You've established your bankroll and are now ready to start betting. You have a few options for the very first roll:

#### Line Bets

Bet on the Pass Line by typing 'p' and hitting Enter, then follow the prompt to put in a bet amount.

Bet on the Don't Pass Line by typing 'd' and hitting Enter, then follow the prompts to place your bet.

#### Field Bet

The Field Bet is a bet on the numbers 2, 3, 4, 9, 10, 11, and 12. If a 2 is rolled, you win double your bet, and if a 12 is rolled, you will win triple your bet. All other numbers win even money. A 5, 6, 7, or 8 will lose.

Type 'y' if you'd like to bet on the Field, otherwise hit Enter to bypass it. Follow the prompts to place your bet.

#### Working Place Bets

If you had Place Bets and hit the previous point number, entering "y" here will turn all your bets On/Working for the Come Out roll. If you roll any Place number on the Coming Out roll, it will pay out, but if you roll a 7, you will lose all your Place bets. This option only appears if you have Place Bets already set up.

#### Proposition Bets

These bets are all single-roll bets. If they do not come up on the very next roll, they will lose. When you activate the Prop Bet by typing "y", another text prompt will come up asking you for which specific bet you'd like to add. Type in the bet code and hit Enter to bring up the betting prompt for your choice. After you've entered your bet, you'll be returned to the Prop Bet prompt. Type in another code to make another bet, type "all" to see all the bets you've made, or just hit Enter to finish up and move onwards with the game.

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
	• Bet Code: "h"

Check the Pay Table section to understand the various payouts for all these bets.

### Point Phase

If a 4, 5, 6, 8, 9, or 10 is rolled on the Coming Out roll, that number becomes the Point. Roll the dice until the Point is hit to win on the Pass Line and reset the game, or until a 7 is rolled, clearing all the bets in a loss and returning to the Come Out roll.

New betting modes appear in the Point phase:

#### Line Odds

When a point is established, you'll have the ability to add Pass Line Odds or a Lay Bet to your initial Line Bet. If you bet on the Pass Line before the Coming Out roll, you'll be asked if you want Pass Line Odds. If you bet on the Don't Pass Line, you'll be prompted for a Lay Bet. Both are optional and can be bypassed by hitting Enter.

#### Place Bets

Typing 'y' and hitting Enter when prompted with the Place Bets will take you through the Place Bet flow, asking you for a bet on each of the place numbers. Enter a 0 if you want to keep the bet clear, otherwise enter your bet to Place the number.

If the Place Bet number is rolled, you'll be prompted to Press your Bet. Hit Enter to decline, or enter 'y' to edit the Place Bet. Enter 0 to remove it.

Place Bets are always off on the Coming Out roll, so they will not be paid until after the Point Phase has started unless you enter "y" in the Place Bets Working prompt between the Field and Proposition bet prompts in the Coming Out phase.

Placing the 4 or 10 for $25 or more will automatically Buy those bets, and the 2% commission is factored into what you win if they hit. For example, Buying the 4 for $25 will win 2 for 1, so you pay $1 to win $50, and will end up collecting $49.

#### Come and Don't Come

The Come and Don't Come Fields act like additional Pass Line Bets after a Point has been established. Placing these bets is only possible after the Point Phase has started. Enter 'y' if you want to bet on these fields when prompted, then Enter a 'c' for Come or a 'd' for Don't Come.

##### Come Bet
A Come Bet will win if a 7 or 11 is rolled, and lose with a 2, 3, or 12. If any other number is rolled, the Come Bet moves to that number, and you will be prompted for Come Bet Odds.  If that Come Bet number is rolled before a 7, you will win. If a 7 is rolled before any of the Come Bet numbers are hit, all Come bets are cleared and you lose.

##### Don't Come Bet
The Don't Come is the opposite of the Come. A bet here wins on a 2, 3 or 12 and loses with a 7 or 11. If any other number is rolled, the Don't Come moves to that number and you are prompted to add Odds, which are always optional. Should a 7 roll before the Don't Come number is rolled, you win on all Don't Come bets. If the Don't Come number is rolled before a 7, you lose that bet.

If Come or Don't Come bets are working during the Coming Out roll, all Come and Don't Come Odds bets are Off, or are not counted on the Coming Out Roll. If a 7 is rolled for the Coming Out roll, Come bets will lose but the Odds will be ignored, while a Don't Come bet will win but will also have the Odds ignored until a Point is established.

#### Hard Ways

The Hard Ways bets are Proposition Bets that are not Single-Roll bets. These are bets that a 4, 6, 8, or 10 are rolled  the Hard Way, or with double numbers. Rolling a 4 and 4 will make a Hard 8, for example. Rolling a 6 and 2 is an Easy 8. A Hard Ways bet wins if any of the double numbers are rolled and will lose on either a 7 Out or if the Easy variant of the number is rolled.

Much like the Place Bets, you will be prompted to bet on the 4, 6, 8, and 10 in order, then you will get a confirmation on what you've bet before the game continues on. Enter 0 to clear a bet or not bet on any of the numbers.

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
<td>Horn Bet on 2, 12</td><td>30:1</td>
</tr>
<tr>
<td>Horn Bet on 3, 11</td><td>15:1</td>
</tr>
<tr>
<td>Hard 4 and 10</td><td>7:1</td>
</tr>
<tr>
<td>Hard 6 and 8</td><td>9:1</td>
</tr>
</table>