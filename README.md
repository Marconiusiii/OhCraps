# OhCraps! v.6.5
Python-based Craps game for Terminal.

## About

The game of Craps is one of the best table games you can play in a casino and contains a variety of bets that have some of the lowest house advantage percentages over you. This game is built to run within a Terminal environment and is accessible for blind players.

Craps is entirely based on the randomness of thrown dice. When the game starts, a bet on the Pass Line will win if a 7 or 11 is thrown with the first roll, also known as the Coming Out roll. A 2, 3, or 12 will lose on the first roll. Any other number thrown on the first roll becomes the Point number, and then the shooter continues to roll until they either roll the Point number or throw a 7. Hitting the Point number is a Pass Line win, the game resets and everything starts up again. Rolling a 7 on the other hand after a Point is established is a loss, and all bets on the table lose with the exception of Don't Pass/Don't Come bets and Any 7 proposition bets.

If you'd enjoy checking through some strategies to play, be sure to visit my [Oh Craps! Strategy Page.](https://www.marconius.com/craps/)

## How to Play

After downloading the OhCraps_Py3.command file, double-click or Open the file and it will open the Terminal app and run. Alternatively, with Terminal open, cd to the directory where the command file was downloaded and run:

$ python3 OhCraps_Py3.command

The game starts off asking you to set up a bankroll. Enter a numeric amount to start.

### Coming Out Roll

You've established your bankroll and are now ready to start betting. You have a few options for the very first roll, and all options are accessed by typing the bet code at the prompt and hitting Enter.

#### Bet Codes for Round 1 Betting

<table>
<caption>Come Out Roll Bet Codes</caption>
<thead>
<tr>
<th scope="col">Code</th>
<th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td>l</td><td>Line Bets: Pass and Don't Pass</td>
</tr>
<tr>
<td>p</td><td>Place Bets</td>
</tr>
<tr>
<td>ly</td><td>Lay Bets</td>
</tr>
<tr>
<td>f</td><td>Field Bet</td>
</tr>
<tr>
<td>hd</td><td>Hard Ways Bets</td>
</tr>
<tr>
<td>w</td><td>Toggle Working Bets On or Off</td>
</tr>
<tr>
<td>pr</td><td>Prop Bets</td>
</tr>
<tr>
<td>ats</td><td>All Tall Small</td>
</tr>
<tr>
<td>fire</td><td>Fire Bet</td>
</tr>
<tr>
<td>h</td><td>Show Help Menu for Bet Codes</td>
</tr>
<tr>
<td>a</td><td>Show all current bets</td>
</tr>
<tr>
<td>r</td><td>Roll the Dice!</td>
</tr>
<tr>
<td>q</td><td>Quit game</td>
</tr>
</tbody>
</table>

#### Line Bets

Bet on the Pass Line by typing 'p' and hitting Enter, then follow the prompt to put in a bet amount.  This bet will win if a 7 or 11 rolls on the Come out roll, loses if a 2, 3, or 12 rolls, and continues on to the point phase of the game if any other number rolls. If the shooter rolls that number again in the point phase, this bet will win. Rolling a 7 in the point phase will make this bet lose and the game resets.

Bet on the Don't Pass Line by typing 'd' and hitting Enter, then follow the prompts to place your bet. This bet wins if a 2 or 3 rolls on the Come Out roll. Rolling a 12 will push, so you will not lose nor win and the bet will be returned to you. This bet loses when rolling a 7 or 11 on the Come Out roll, and if any other number rolls that will become the point for the point phase of the game. If the shooter rolls a 7 in the Point phase of the game, the Don't Pass bet will win.

Once you've set your Line Bets, type 'x' and hit Enter to continue on with the game. Should your Line bets win in the come out phase, the bets will stay out on the table for you.

#### Place Bets

Typing 'p' and hitting Enter in the Place Your Bets prompt will take you through the Place Bet flow, asking you for a bet on each of the place numbers (4, 5, 6, 8, 9, 10). Enter a 0 if you want to keep the bet clear, otherwise enter your bet to Place the number. Typing Enter will bypass the current Place Number and leave the bet alone and move you to the next number. Once you enter a bet or pass the Place 10, you'll be brought back to the Place Bets prompt.

If the Place Bet number is rolled, you'll be prompted to Press your Bet. Hit Enter to decline, or enter 'y' to edit the Place Bet. Enter 0 to remove it.

Additionally, at the "Change your bet?" prompt, you can type "p" to perform a full press, "hp" for a half-press, or "u" to press up one unit. A Full Press doubles the bet you currently have on the box number, a half-press presses up exactly half of what you have currently bet, and going up a unit will press your bet up $5 on the 4, 5, 9, and 10, and up $6 on the 6 or 8.

Emulating how Craps works in Las Vegas, Placing the 4 or 10 for $10 or more will automatically buy those bets, and the 5% commission is factored into what you win if they hit. For example, Buying the Place 4 for $25 will win 2 for 1, so you pay a $1 vig to win $50, and will end up collecting $49. The vig will round up to the nearest dollar for bets under $20, and will round down to the nearest dollar for everything else.

In the Place Bet prompt, if you type 'd' instead of 'y' and hit Enter, this will take down all your bets. A quick and simple way to 0 them all out. This works both in the Come Out phase and also after a Point has been established.

After a Point has been established, when you are prompted with the Place Bet option, typing 'o' and hitting Enter will toggle your Place Bets Off for the next roll. This means that hitting any of the numbers or a 7 Out will not affect your bets and you will not get paid. The bets stay Off for only this one roll, so you'll need to turn them off after each roll if you want them to stay off for an extended period of rolls. When still in the prompt, entering 'o' again and hitting Enter will toggle the bets back On.

You can automatically place bets across all the numbers or bet inside using keywords on the Place Bet prompt. Typing 'a' and hitting Enter will activate the Across mode, where you will be prompted how many units you want to bet on each Place number. When using Across mode after a Point has been established, you'll be prompted on whether you'd like to include the Point number or not.

On the Place Bet prompt, typing 'i' and hitting Enter will activate Inside mode, where the Place 4 and 10 will be taken down and you'll be prompted for how many units you'd like to place on the 5, 6, 8, and 9.

Typing 'c' and hitting Enter will activate the center betting mode, where you'll be asked how many units you'd like to place on the 6 and 8 together. So typing '2' will place the 6 and 8 for 2 units, or $12, each.

These options provide a quick way to make common Place bets without having to jump through each individual number. 1 Unit is equal to $5, with the 6 and 8 automatically adjusting for the $6 bets required for them.

Typing 'h' in the Place Bets prompt and hitting Enter will open the help menu that displays the various codes for Place Betting.

Finish your Place Betting by typing 'x' and hitting Enter. You will be returned to the Place Your Bets prompt.

Common Across/Inside Bets:
* 1 Unit - $32 Across - $22 Inside
* 2 Units - $64 Across - $44 Inside
* 3 Units - $96 Across - $66 Inside
* 4 Units - $128 Across - $88 Inside
* 5 Units - $160 Across - $110 Inside 

Once a Point has been established, typing 'm' at the Place Bet prompt will automatically move your Place bet to an open place number if it is not already placed. The bet will automatically adjust to the closest amount if going from the 6 and 8 to the other numbers, and vice versa.

Typing 'p' and hitting Enter on the Place Prompt after the point has been established will take down only the Point number if it is placed. This works if you have already bet all the numbers across and just want to quickly take it down without going through every number in the Place Prompt bet flow.

#### Lay Bets

Lay Bets are the opposite of Place Bets. You will be wagering money that the 7 rolls before the number you are betting on hits. This functionality works the same way as the Place Betting system, where you will be asked how much you'd like to Lay against each number. Enter a 0 or just hit Enter to leave the bet alone.

Lay bets are always working on the Come Out roll.

At the Lay Bet prompt, typing 'd' and hitting Enter will take down all your Lay Bets.

Also at the prompt, typing 'a' and hitting enter will allow you to make Lay bets across all of the numbers. Enter a unit amount and it will multiply by 5 and lay that amount on each of the box numbers.

After a point has been established, you'll be able to turn your Lay bets Off when prompted for the Lay Bets. Type 'o' and hit Enter to turn your Lay Bets Off for the next roll. Just like the Place Bets, they will only be Off for the very next roll. With the Lay bets Off, they will not be affected by a 7 out or by rolling the Lay number.

Check the Pay Table to see how each of the Lay Bets pays out. There is a 5% commission/vig paid back to the House based on your winnings when a Lay bet wins. When your Lay Bets win, they will stay up until you take them down or they lose.

Type 'h' and hit Enter to show the Lay Betting codes.

Type 'x' and hit Enter to finish Lay Betting and return to the Place Your Bets prompt.

#### Field Bet

The Field Bet is a bet on the numbers 2, 3, 4, 9, 10, 11, and 12. If a 2 is rolled, you win double your bet, and if a 12 is rolled, you will win triple your bet. All other numbers win even money. A 5, 6, 7, or 8 will lose.

This is a one-roll bet, so this bet is always working for the next roll.

Type 'y' if you'd like to bet on the Field, otherwise hit Enter to bypass it. Follow the prompts to place your bet.

Field Bets stay up on the table after winning. To take down a Field Bet, type 'd' or 'td' at the Field Bet prompt and hit Enter. You can also go into the prompt and enter a Field Bet of $0.

#### Hard Ways

The Hard Ways bets are Proposition Bets that are not Single-Roll bets. These are bets that a 4, 6, 8, or 10 are rolled  the Hard Way, or with double numbers. Rolling a 4 and 4 will make a Hard 8, for example. Rolling a 6 and 2 is an Easy 8. A Hard Ways bet wins if any of the double numbers are rolled and will lose on either a 7 Out or if the Easy variant of the number is rolled. If you win a Hard Way bet, you'll be prompted to change your bet. Hit Enter to leave your current bet alone as is, type a number to change the bet, or enter 0 to take the bet down. Alternatively, if you lose the Hard Way bet, you'll be prompted to go back up on the bet; enter a number to bet again on that Hard Way number, or hit Enter to bypass the bet and leave it blank.

Rather than going through each individual bet, typing 'a' and hitting Enter at the Hard Ways prompt will allow you to automatically bet units across all of the Hard Ways at the same time. For this prompt, units are $1, so entering 5 will put $5 on each of the Hard Ways, etc.

At the Hard Ways prompt, you can bet a random amount spread across all the hard ways going high on one number by entering 'h4,' 'h6,' 'h8', or 'h10' and hitting Enter for the 4, 6, 8, or 10 respectively. When prompted, entering any amount here will automatically break down the bet to spread across the hard ways, with your chosen number receiving double the bet.

For example, typing 'h4' and hitting Enter will prompt you for your bets going high on the Hard 4; then entering $25 will put $5 bets on the Hard 6, 8, and 10 and $10 on the Hard 4. This will work with any whole number, give it a go! Much better to try it here than at a live game since it annoys the dealers.

At any point, entering 'd' or 'td' at the Hard Ways bet prompt and hitting Enter will take down all your Hard Ways bets.

After a Point has been established, you can turn your Hard Ways bets Off by typing 'o' or 'off' and hitting Enter when you are in the Hard Ways Betting menu. This will take your bets out of action for the next roll. Hitting a Hard Way number, and Easy number, or a 7 Out will not affect your bets when they are Off.

Much like the Place Bets, you will be prompted to bet on the 4, 6, 8, and 10 in order, then you will get a confirmation on what you've bet before the game continues on. Enter 0 to clear a bet or not bet on any of the numbers.

Enter 'h' in the hard Ways betting prompt to display the bet codes.

Type 'x' and hit Enter to exit Hard Ways Betting mode and return to the Place Your Bets prompt.

#### Working  Bets

If you've made Place Bets, Lay Bets, or Hard Ways bets, you can have them Working on the Come Out roll. Generally, when you make a Place Bet or Hard Ways bet before a Point is established, the bets are Off by default, meaning they will not be affected by the roll of the dice. Having your bets "Working" means that you are turning them on and they will be affected by the next roll of the dice.

If you've made Come or Don't Come bets in a previous hand and they are still on the table during the Come Out roll, the Come or Don't Come bets will always be working, but any odds that have been bet will automatically be off by default. Toggling Working bets on in this case will turn the Odds or Lay Odds back on for those bets.

If you've Placed, Laid, or made Hard Ways  or Come/Don't Come Bets, typing 'w' in the Place Your Bets prompt and hitting Enter will set them all to be Working on the Come Out Roll. You can toggle this on and off by typing 'w' again.

#### Proposition Bets

These bets are all single-roll bets. If they do not come up on the very next roll, they will lose. When you activate the Prop Bet Mode by typing "pr", another text prompt will come up asking you for which specific bet you'd like to add. Type in the bet code and hit Enter to bring up the betting prompt for your choice. After you've entered your bet, you'll be returned to the Prop Bet prompt. Type in another code to make another bet, type "all" to see all the bets you've made, type 'help' to see a list of all commands, or type 'x' and hit Enter to finish up and move onwards with the game.

1. Any 7 - Bet on any 7 to come up.
	• Bet Code: '7', 'a7', 's'
2. Any Craps - Bet on a 2, 3, or 12 to come up.
	• Bet Code: 'c'
3. C & E - Bet on a 2, 3, 11, or 12 to come up.
	• Bet Code: 'ce'
4. Snake Eyes - Bet that a 2 comes up.
	• Bet Code: '2', 's'
5. Acey-Deucey - Bet on a 3 to come up.
	• Bet Code: '3', 'ad'
6. Boxcars - Bet that a 12 comes up.
	• Bet Code: '12', 'b'
7. Horn - Bet that a 2, 3, 11, or 12 comes up.
	• Bet Code: 'h'
	Horn High Deuce:
	• Code: 'hh2'
	Horn High Ace-Deuce:
	• Code: 'hh3'
	Horn High Yo
	• Code: 'hhy', 'hh11'
	Horn High 12
	• Code: 'hhb', 'hhm', 'hh12'
8. Yo - Betting that an Eleven will be the next roll outcome.
	• BetCodes: '11', 'e'
9. Hop Bets - Betting on specific outcomes of the dice; hopping the 4s is betting that the dice roll 3, 1 or 2, 2, etc.
	• Bet Codes: 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10'
	• 'h6e' and 'h8e' will allow you to hop only the easy outcomes for the 6 and 8.
10. Hop the Easies - Placing a bet on all the easy way Hop Bets.
	• Bet Code: 'hez'
11. Hop the Hard Ways - Hopping all the numbers that can come out with equal dice amounts, or specifically on one outcome.
	• Bet Codes: 'hh', 'hh4', 'hh6', 'hh8', 'hh10'
12. World - Also known as the Whirl Bet, this places a bet across the Horn and the Any 7.
	• Code: 'w', 'world', 'wh'
13. Buffalo - A bet that contains Any 7 along with the Hard Ways hopping.
	• Code: 'bf', 'buff', 'buffalo'
14. Buffalo Yo - Hard Ways hopping with the Eleven rather than the Any 7.
	• Code: 'bf11', 'by'
15. Hi-Lo, betting evenly on the 2 and 12.
	• Code: 'hl'
16. All - See all prop bets you've placed.
	• Code: 'a', 'all'
17. Help - See a list of all Prop Bet commands.
	• Code: 'help'
18. Exit Prop betting and return to the game.
	• Code: x

##### Hop Bets

Hop Bets are where you can bet that a specific number will appear on the next roll. Hopping the number places a unit on each of the outcomes possible for that number. For example, hopping the 6 places a bet on the dice rolling as 3 and 3, 4 and 2, or5 and 1 on the next roll. If one of those outcomes hits, you get paid for that but lose the other bets on the other outcomes for the number. Hard Way hop bets pay 30:1, while all the other bets pay 15:1. You will be prompted to make a correct bet amount for the specific number you bet on. There are 3 ways to make a 6, so any Hop 6 bets must be made in multiples of 3, and so on.

The Hop the Easies bet, or 'hez' as the bet code, places a single unit on all 15 easy way outcomes for the dice.

The Hop the Hard Ways bets allows you to bet on all the Hard outcomes at once, or on any of the values that have equal dice amounts, so 2, 4, 6, 8, 10, and 12. The 'hh' code allows you to bet on all of these numbers at once with a bet that is a multiple of 6, and while Snake Eyes is the "Hard Way" bet for 2 and Boxcars is for 12, the 4, 6, 8. and 10 can be individually hopped with 'hh4', 'hh6', 'hh8', and 'hh10' respectively.

The Buffalo Prop bet places bets across the Hard Ways Hop bets and either the Any 7 or Eleven. 

Check the Pay Table section to understand the various payouts for all these bets.

#### All Tall Small

The All Tall Small bet is an interesting persistent bet where you are betting that a set of numbers will all appear before the 7. Small means you are betting that the 2, 3, 4, 5, and 6 will appear before the 7; Tall means you are betting that the 8. 9. 10, 11, and 12 will appear; All is a bet that both the small and tall numbers will all appear before the 7.

This bet is made at the Come Out roll and will not appear again until a 7 out. The game will keep track of your rolls and display them each time you roll the dice. You will only lose this bet on a 7 Out or a 7 on the Come Out roll.

#### Fire Bet

This is the bet for players who think they can hit a hot streak of Point numbers before a 7 out. Like the All Tall Small, the Fire Bet is a persistent bet made in the Come Out phase. This is a bet on how many Point numbers the shooter hits before a 7. For example, if the shooter rolls a Point of 5 in the Come Out roll, and then rolls a 5 and wins the Point, the 5 is marked in the Fire Bet and it now counts as 1 Point Hit. Then if the shooter rolls a 4 on the Come Out, then wins the hand by rolling the Point 4 again, the 4 gets marked in the Fire Bet, counting as 2 Points won. If a Point number is rolled again, such as the shooter rolling a 5 after all of this, that Point will not count if the shooter wins. 

Once a shooter wins 4 Points, the Fire Bet will pay out on the next 7 Out. If the shooter 7s Out while 3 or less points have been hit in the Fire Bet, you lose the Fire Bet and have to start over. This is a risky bet, but can pay off big with just a $1 bet and a lot of luck. If the shooter rolls 4 Points and then 7s out, you win 24:1. If the shooter rolls 5 points and then 7s out, you win 249:1, and if the Fire Bet is at the maximum of 6 points rolled, you will win 999:1!

### Point Phase

If a 4, 5, 6, 8, 9, or 10 is rolled on the Coming Out roll, that number becomes the Point. Roll the dice until the Point is hit to win on the Pass Line and reset the game, or until a 7 is rolled, clearing all the bets in a loss and returning to the Come Out roll.

New betting modes appear in the Point phase, and are accessed through the following codes.

#### Point Phase Bet Codes

<table>
<caption>Point Phase Bet Codes</caption>
<thead>
<tr>
<th scope="col">Code</th><th scope="col">Description</th>
</tr>
</thead>
<tbody>
<tr>
<td>o</td><td>Line Odds for Pass and Don't Pass bets.</td>
</tr>
<tr>
<td>c</td><td>Come Bets, opens prompt for Come and Don't Come bets.</td>
</tr>
<tr>
<td>dp</td><td>Take down Don't Pass bet and Odds.</td>
</tr>
<tr>
<td>co</td><td>Change Come or Don't Come Bet Odds.</td>
</tr>
<tr>
<td>dcd</td><td>Take down Don't Come and Odds</td>
</tr>
<tr>
<td>hd</td><td>Hard Ways betting mode</td>
</tr>
<tr>
<td>pr</td><td>Prop Bets mode</td>
</tr>
<tr>
<td>h</td><td>Help Menu for Bet Codes</td>
</tr>
<tr>
<td>q</td><td>Quit game</td>
</tr>
</tbody>
</table>

#### Line Odds

When a point is established, you'll have the ability to add Pass Line Odds or a Lay Bet to your initial Line Bet. If you bet on the Pass Line before the Coming Out roll, typing 'o' and hitting Enter in the Place Your Bets prompt will open the Odds Betting mode. You'll be able to set Pass Line Odds and Lay Odds for Don't Pass bets.

This game uses a standard 3x4x5x Odds limit. Odds on the 4 and 10 are limited to 3x your initial Line bet, odds on the 5 and 9 are limited to 4x your bet, and odds on the 6 and 8 are limited to 5x your bet. All Don't Pass lay odds are limited to 10x your Don't Pass bet.

When at the Line Bet Odds prompt, typing 'p' and hitting Enter will take down your Pass Line Odds bet. Typing 'd' and hitting Enter will take down your Don't Pass Lay Odds. Typing 'a' and hitting Enter will take down both Pass and Don't Pass Odds if you have them set.

#### Take Down Don't Pass Bet and Odds

Due to the overall low House edge that Don't Pass bets have in casinos, the Don't Pass Bet and Don't Pass Odds can actually be taken down at any point of game play. It is not a contractual bet like the Pass Line, which has to stay up until a Point is hit or a 7 out. Type 'dp' at the Place Your Bets prompt and hit Enter and your Don't Pass Bet along with your Odds will be returned to you, and you will not be able to make another Don't Pass bet until the next Come Out roll.

#### Come and Don't Come

The Come and Don't Come Fields act like additional Pass Line Bets after a Point has been established. Placing these bets is only possible after the Point Phase has started. Enter 'c' if you want to bet on these fields when prompted, then Enter a 'c' for Come or a 'd' for Don't Come.

##### Come Bet
A Come Bet will win if a 7 or 11 is rolled, and lose with a 2, 3, or 12. If any other number is rolled, the Come Bet moves to that number, and you will be prompted for Come Bet Odds.  If that Come Bet number is rolled before a 7, you will win. If a 7 is rolled before any of the Come Bet numbers are hit, all Come bets are cleared and you lose.

If you still have Come Bets up with odds in the Come Out phase, such as if you made Come Bets and then the Point was hit, rolling a 7 at this stage will result in all Come Bets losing but all Odds returned to you. If you happen to roll a Come Bet number as the Point in the come out phase, you will win the flat bet, but the odds once again will be returned to you since they are off during the come out phase unless you've turned Working on.

##### Don't Come Bet
The Don't Come is the opposite of the Come. A bet here wins on a 2, 3 or 12 and loses with a 7 or 11. If any other number is rolled, the Don't Come moves to that number and you are prompted to add Odds, which are always optional. Should a 7 roll before the Don't Come number is rolled, you win on all Don't Come bets. If the Don't Come number is rolled before a 7, you lose that bet.

If Come or Don't Come bets are up during the Coming Out roll, all Come and Don't Come Odds bets are Off, or are not counted on the Coming Out Roll unless Working has been turned on. If a 7 is rolled for the Coming Out roll, Come bets will lose, but the Odds will be ignored, while a Don't Come bet will win but will also have the Odds ignored until a Point is established. If Working is Off, the Odds will be returned to your bankroll.

#### going Off on your bets

As mentioned in the Place Lay, and Hard Ways sections, you can take these bets Off for the next roll by typing 'o' or 'off' and hitting Enter when you are in those betting modes. After the very next roll, those bets will turn back On.

#### Field and Proposition Bets

These bets are available at all times. If there is a bet on the Field, the Field Bet prompt will announce it.

## Pay Table

<table>
<caption>Line, Field, and Come Payouts</caption>
<thead>
<tr>
<th scope="col">Bet</th>
<th scope="col">Payout</th>
</tr>
</thead>
<tbody>
<tr>
<th scope="row">Pass/Don't Pass Line</th><td>1:1</td>
</tr>
<tr>
<th scope="row">Pass Line Odds 4 and 10</th><td>2:1</td>
</tr>
<tr>
<th scope="row">Pass Line Odds 5 and 9</th><td>3:2</td>
</tr>
<tr>
<th scope="row">Pass Line Odds 6 and 8</th><td>6:5</td>
</tr>
<tr>
<th scope="row">Field Bet</th><td>1:1</td>
</tr>
<tr>
<th scope="row">Field Bet 2</th><td>2:1</td>
</tr>
<tr>
<th scope="row">Field Bet 12</th><td>3:1</td>
</tr>
<tr>
<th scope="row">Place 4 and 10</th><td>9:5</td>
</tr>
<tr>
<th scope="row">Place 5 and 9</th><td>7:5</td>
</tr>
<tr>
<th scope="row">Place 6 and 8</th><td>7:6</td>
</tr>
<tr>
<th scope="row">Come/Don't Come Bet</th><td>1:1</td>
</tr>
<tr>
<th scope="row">Come Odds 4 and 10</th><td>2:1</td>
</tr>
<tr>
<th scope="row">Come Odds 5 and 9</th><td>3:2</td>
</tr>
<tr>
<th scope="row">Come Odds 6 and 8</th><td>6:5</td>
</tr>
<tr>
<th scope="row">Lay/DC Odds 4, 10</th><td>1:2</td>
</tr>
<tr>
<th scope="row">Lay/DC Odds 5, 9</th><td>2:3</td>
</tr>
<tr>
<th scope="row">Lay/DC Odds 6, 8</th><td>5:6</td>
</tr>
</tbody>
</table>

<table>
<caption>Proposition Bet Payouts</caption>
<thead>
<tr>
<th scope="col">Bet</th><th scope="col">Payout</th>
</tr>
</thead>
<tbody>
<tr>
<th scope="row">Any 7</th><td>4:1</td>
</tr>
<tr>
<th scope="row">Any Craps</th><td>7:1</td>
</tr>
<tr>
<th scope="row">C & E with Craps</th><td>3:1</td>
</tr>
<tr>
<th scope="row">C&E with 11</th><td>7:1</td>
</tr>
<tr>
<th scope="row">Snake Eyes/Aces</th><td>30:1</td>
</tr>
<tr>
<th scope="row">Acey-Deucey</th><td>15:1</td>
</tr>
<tr>
<th scope="row">Boxcars</th><td>30:1</td>
</tr>
<tr>
<th scope="row">Horn Bet on 2, 12</th><td>30:1 - 3/4 of initial bet</td>
</tr>
<tr>
<th scope="row">Horn Bet on 3, 11</th><td>15:1 - 3/4 of initial bet</td>
</tr>
<tr>
<th scope="row">Yo Eleven</th>
<td>15:1</td>
</tr>
<tr>
<th scope="row">Hard 4 and 10</th><td>7:1</td>
</tr>
<tr>
<th scope="row">Hard 6 and 8</th><td>9:1</td>
</tr>
<tr>
<th scope="row">Hop easy way/6-8 Easies</th><td>15:1</td>
</tr>
<tr>
<th scope="row">Hop hard number</th><td>30:1</td>
</tr>
<tr>
<th scope="row">Small and Tall</th><td>34:1</td>
</tr>
<tr>
<th scope="row">The All</th><td>175:1</td>
</tr>
<tr>
<th scope="row">4 Fire Bet Points</th><td>24:1</td>
</tr>
<tr>
<th scope="row">5 Fire Bet Points</th><td>249:1</td>
</tr>
<tr>
<th scope="row">6 Fire Bet Points</th><td>999:1</td>
</tr>
</tbody>
</table>
