# Simple text-based 1-player game of Blackjack.
# Import required modules.
import random
import sys
import os
from itertools import product
from time import sleep
from colorama import Fore, Back, Style

# Resize and clear terminal window. Set width variable to allow for layout of content.
os.system('printf \'\e[8;50;160t\'')
os.system('clear')
width = 160
# Initialise list with card values and suits.
values, suits = ['Ace', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King'], ['Hearts', 'Diamonds', 'Clubs', 'Spades']
# Initialise empty lists to contain card deck, dealer and player cards, and currently visible cards for each player.
deck = []
dealer_cards = []
player_cards = []
dealer_pick = []
player_pick = []
# Initialise list to contain and track Aces values.
player_aces = []
dealer_aces = []
# Initialise results list, list item 0 is dealer result, list item 1 is player result.
results = [0, 0]
# Initialise global variable to track game progress.
gameover = False
# Initialise list to track wins and losses.
wins_losses = [0, 0]

# ASCII art welcome message.
print(Fore.LIGHTRED_EX + str.center(
    "__        _______ _     ____ ___  __  __ _____   _____ ___    ______   _______ _   _  ___  _   _   ____  _        _    ____ _  __   _   _    ____ _  __ ",
    width))
print(str.center(
    "\ \      / / ____| |   / ___/ _ \|  \/  | ____| |_   _/ _ \  |  _ \ \ / /_   _| | | |/ _ \| \ | | | __ )| |      / \  / ___| |/ /  | | / \  / ___| |/ / ",
    width))
print(str.center(
    " \ \ /\ / /|  _| | |  | |  | | | | |\/| |  _|     | || | | | | |_) \ V /  | | | |_| | | | |  \| | |  _ \| |     / _ \| |   | ' /_  | |/ _ \| |   | ' /  ",
    width))
print(str.center(
    "  \ V  V / | |___| |__| |__| |_| | |  | | |___    | || |_| | |  __/ | |   | | |  _  | |_| | |\  | | |_) | |___ / ___ \ |___| . \ |_| / ___ \ |___| . \  ",
    width))
print(str.center(
    "   \_/\_/  |_____|_____\____\___/|_|  |_|_____|   |_| \___/  |_|    |_|   |_| |_| |_|\___/|_| \_| |____/|_____/_/   \_\____|_|\_\___/_/   \_\____|_|\_\ ",
    width) + Style.RESET_ALL)


# Define main loop, takes player_name as condition to enable player name to persist between rounds.
def main(player_name):
    # Prompt for player name if one is not currently set
    if player_name == '':
        player_name = input('Please type your name and press Enter:\n')
    # reset global gameover variable to False.
    global gameover
    gameover = False
    # populate card deck with all cards.
    for i in list(product(values, suits)):
        deck.append(i)
    # reset results list indexes to 0, clear dealers and players cards, dealer and player aces, and dealers and players visible cards.
    results.insert(0, 0)
    results.insert(1, 0)
    dealer_aces.clear()
    player_aces.clear()
    dealer_cards.clear()
    player_cards.clear()
    dealer_pick.clear()
    player_pick.clear()
    # deal cards then start game with player_name condition.
    deal()
    start(player_name)


# Deal function picks cards one by one, removing them from the deck, and adding them to dealer_cards and player_cards lists until the deck is empty.
def deal():
    while len(deck) > 0:
        dealer_cards.append(pickcard())
        player_cards.append(pickcard())
    dealer_pick.append(dealer_cards[0])
    # If card is an Ace, append the value it was assigned to the dealer aces list.
    if dealer_cards[0][0] == 'Ace':
        dealer_aces.append(11)
    for i in range(2):
        player_pick.append(player_cards[i])
        # If card is an Ace, append the value it was assigned to the player aces list.
        if player_cards[i][0] == 'Ace':
            player_aces.append(11)


# pickcard() function picks cards at random and returns the picked card.
def pickcard():
    pick = deck[random.randint(0, len(deck) - 1)]
    deck.remove(pick)
    return pick


# start(player_name) takes the player name passed from the main() function and starts the game.
def start(player_name):
    # step variable counts turns taken and is passed to the turn() and action() functions as a condition with the player name
    step = 0
    # take first turn. At this point no player action has been prompted so the second condition for player_choice is None.
    turn(0, None, player_name)
    # keep taking turns until the game is over
    while not gameover:
        # trigger action() and increment turn counter by 1
        action(step, player_name)
        step += 1


def turn(number, player_choice, player_name):
    dealer_total = results[0]
    player_total = results[1]
    # Initial turn after setup.
    if number == 0:
        # Count value of currently shown cards for dealer and player and insert them into the results list.
        dealer_total += count(dealer_pick[0][0], dealer_total)
        player_total += count(player_pick[0][0], player_total)
        player_total += count(player_pick[1][0], player_total)
        player_total = 21
        results.insert(0, dealer_total)
        results.insert(1, player_total)
        # Show dealer and player cards and hand values.
        showcards(player_name)
        # If player has natural Blackjack then instant win.
        if player_total == 21:
            game_result(player_name)
    # Subsequent turns
    elif number > 0:
        # If player chooses to hit, reveals another player card and total hand value.
        if player_choice == 'H':
            player_pick.append(player_cards[number + 1])
            # If card is an Ace, append the value it was assigned to the player aces list.
            if player_pick[number + 1][0] == 'Ace':
                player_aces.append(count(player_pick[number+1][0], player_total))
            player_total += count(player_pick[number + 1][0], player_total)
            # Check if previous cards contain Aces, if so, check if player has gone bust, if so remove 10 so Ace becomes worth 1 instead of 11.
            for i in range(len(player_aces)):
                if player_aces[i] == 11 and player_total > 21:
                    player_aces[i] = 1
                    player_total -= 10
            results.insert(0, dealer_total)
            results.insert(1, player_total)
            showcards(player_name)
        # If player chooses to stand, gameover is set to True, and dealer takes action based on Blackjack rules, revealing hand after each action.
        elif player_choice == 'S':
            global gameover
            gameover = True
            dealer_pick.append(dealer_cards[1])
            # If card is an Ace, append the value it was assigned to the dealer aces list.
            if dealer_pick[1][0] == 'Ace':
                dealer_aces.append(11)
            dealer_total += count(dealer_pick[1][0], dealer_total)
            results.insert(0, dealer_total)
            results.insert(1, player_total)
            showcards(player_name)
            # If total is over 17 end game.
            if dealer_total >= 17:
                game_result(player_name)
            # If dealers hand is less than 17, dealer will hit and take another card. This repeats until the hand is over 17.
            elif dealer_total < 17:
                for i in range(2, len(dealer_cards)-1):
                    print('\n' + str.center('Dealer Hits.', width) + '\n')
                    sleep(1)
                    dealer_pick.append(dealer_cards[i])
                    if dealer_pick[i][0] == 'Ace':
                        player_aces.append(count(dealer_pick[i][0], player_total))
                    dealer_total += count(dealer_pick[i][0], dealer_total)
                    # Check if previous cards contain Aces, if so, check if Dealer has gone bust, if so remove 10 so Ace becomes worth 1 instead of 11.
                    for ace in range(len(dealer_aces)):
                        if dealer_aces[ace] == 11 and dealer_total > 21:
                            dealer_aces[ace] = 1
                            dealer_total -= 10
                    results.insert(0, dealer_total)
                    results.insert(1, player_total)
                    showcards(player_name)
                    if dealer_total >= 17:
                        # Show game results.
                        game_result(player_name)


# Determine card value and return this.
def count(card, player):
    if card == 'Ace':
        if player > 10:
            return 1
        elif player <= 10:
            return 11
    elif str(card) in ['Jack', 'Queen', 'King']:
        return 10
    else:
        return card


def action(step, player_name):
    # Prompt player to Hit or Stand then pass their choice to the turn() function along with the turn number; if input is a valid choice increment turncounter by 1, otherwise display feedback and prompt for input again.
    turnnumber = step
    playerchoice = str.capitalize(
        input(str.center('Enter H to Hit or S to Stand. Press Enter to confirm.', width) + '\n'))
    if playerchoice in ['S', 'H']:
        turnnumber += 1
        turn(turnnumber, playerchoice, player_name)
    else:
        print('Incorrect Input.')
        action(turnnumber, player_name)


# function to show current hands for dealer and player, stylized to match colours of each suit.
def showcards(playername):
    # new line separator
    print('\n')
    # print all cards currently visible in dealers hand
    print(str.rjust("Dealers Hand:", round(width * 0.4)))
    for i in dealer_pick:
        if i[1] == 'Hearts':
            print(str.rjust(Fore.RED + Back.WHITE + '♥ ' + str(i[0]) + ' ♥', round(width * 0.46)) + Style.RESET_ALL)
        if i[1] == 'Diamonds':
            print(str.rjust(Fore.RED + Back.WHITE + '♦ ' + str(i[0]) + ' ♦', round(width * 0.46)) + Style.RESET_ALL)
        if i[1] == 'Clubs':
            print(str.rjust(Fore.BLACK + Back.WHITE + '♣ ' + str(i[0]) + ' ♣', round(width * 0.46)) + Style.RESET_ALL)
        if i[1] == 'Spades':
            print(str.rjust(Fore.BLACK + Back.WHITE + '♠ ' + str(i[0]) + ' ♠', round(width * 0.46)) + Style.RESET_ALL)
    # print total value of visible cards in dealers hand
    print(str.rjust("Value: " + str(results[0]), round(width * 0.4)))
    sleep(0.5)
    # print all cards currently visible in players hand
    print(str.rjust(playername + "'s Hand:", round(width * 0.66)))
    for i in player_pick:
        if i[1] == 'Hearts':
            print(str.rjust(Fore.RED + Back.WHITE + '♥ ' + str(i[0]) + ' ♥', round(width * 0.72)) + Style.RESET_ALL)
        if i[1] == 'Diamonds':
            print(str.rjust(Fore.RED + Back.WHITE + '♦ ' + str(i[0]) + ' ♦', round(width * 0.72)) + Style.RESET_ALL)
        if i[1] == 'Clubs':
            print(str.rjust(Fore.BLACK + Back.WHITE + '♣ ' + str(i[0]) + ' ♣', round(width * 0.72)) + Style.RESET_ALL)
        if i[1] == 'Spades':
            print(str.rjust(Fore.BLACK + Back.WHITE + '♠ ' + str(i[0]) + ' ♠', round(width * 0.72)) + Style.RESET_ALL)
    # print total value of visible cards in players hand
    print(str.rjust("Value: " + str(results[1]) + "\n", round(width * 0.66)))
    sleep(0.5)


# determine outcome of game by comparing player and dealer results. Print result then end round. Track overall wins/losses within wins_losses list
def game_result(player_name):
    # If player gets blackjack or goes bust prior to dealer card reveals, print result immediately. Dealer does not take turn and gameover variable remains False.
    if results[1] == 21:
        wins_losses[0] += 1
        print(str.center('BLACKJACK! You Win!', width))
        gameend(player_name)
    if results[1] > 21:
        wins_losses[1] += 1
        print(str.center('Whoops! You went bust! Dealer Wins.', width))
        gameend(player_name)
    # Player does not achieve blackjack or go bust, dealer takes turn(s) and gameover variable is set to True. Calculate outcome and print result.
    if gameover:
        if results[0] == 21:
            wins_losses[1] += 1
            print(str.center('BLACKJACK! Dealer Wins!', width))
        elif results[0] > 21:
            wins_losses[0] += 1
            print(str.center('Dealer goes bust! You Win!', width))
        elif results[0] >= results[1]:
            wins_losses[1] += 1
            print(str.center('Dealer Wins! Better Luck Next Time!', width))
        elif results[0] <= results[1]:
            wins_losses[0] += 1
            print(str.center('Congratulations! You Win!', width))
        # End round.
        gameend(player_name)


# Ends current round, presents current wins and losses stats and triggers playagain() function with the current player name.
def gameend(player_name):
    print(str.center('Wins: ' + str(wins_losses[0]) + ', Losses: ' + str(wins_losses[1]), width))
    playagain(player_name)


# Prompts user to play again, if they choose to do so, passes their name to the main function so that it does not need to be entered again. If they wish to quit, ends execution.
def playagain(player_name):
    sleep(0.5)
    if str.capitalize(input('\n' + str.center('Press Enter to play again or type Q to exit.', width) + '\n')) == 'Q':
        print(str.center('Thanks for playing!', width))
        sleep(1)
        sys.exit()
    else:
        main(player_name)


# Initial input request to start script after showing welcome banner.
if input('\n' + str.center('Press Enter to start or type Q to quit!', width) + '\n') not in ['Q', 'q']:
    main('')
else:
    sys.exit()
