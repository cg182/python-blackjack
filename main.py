# Blackjack attempt.
import random
from itertools import product
from time import sleep
from shutil import get_terminal_size
import os
from colorama import Fore, Back, Style
import sys

os.system('printf \'\e[8;50;160t\'')
os.system('clear')
width = get_terminal_size().columns
values, suits = ['Ace', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King'], ['Hearts', 'Diamonds', 'Clubs', 'Spades']
deck = []
dealer_cards = []
player_cards = []
dealer_pick = []
player_pick = []
results = [0, 0]
gameover = False
wins_losses = [0, 0]


print(Fore.LIGHTRED_EX + str.center("__        _______ _     ____ ___  __  __ _____   _____ ___    ______   _______ _   _  ___  _   _   ____  _        _    ____ _  __   _   _    ____ _  __ ", width))
print(str.center("\ \      / / ____| |   / ___/ _ \|  \/  | ____| |_   _/ _ \  |  _ \ \ / /_   _| | | |/ _ \| \ | | | __ )| |      / \  / ___| |/ /  | | / \  / ___| |/ / ", width))
print(str.center(" \ \ /\ / /|  _| | |  | |  | | | | |\/| |  _|     | || | | | | |_) \ V /  | | | |_| | | | |  \| | |  _ \| |     / _ \| |   | ' /_  | |/ _ \| |   | ' /  ", width))
print(str.center("  \ V  V / | |___| |__| |__| |_| | |  | | |___    | || |_| | |  __/ | |   | | |  _  | |_| | |\  | | |_) | |___ / ___ \ |___| . \ |_| / ___ \ |___| . \  ", width))
print(str.center("   \_/\_/  |_____|_____\____\___/|_|  |_|_____|   |_| \___/  |_|    |_|   |_| |_| |_|\___/|_| \_| |____/|_____/_/   \_\____|_|\_\___/_/   \_\____|_|\_\ ", width) + Style.RESET_ALL)


def main(player_name):
    if player_name == '':
        player_name = input('Please type your name and press Enter:\n')
    global gameover
    gameover = False
    for i in list(product(values, suits)):
        deck.append(i)
    results.insert(0, 0)
    results.insert(1, 0)
    dealer_cards.clear()
    player_cards.clear()
    dealer_pick.clear()
    player_pick.clear()
    deal()
    start(player_name)


def deal():
    while len(deck) > 0:
        pickcard()
        dealer_cards.append(pickcard())
        pickcard()
        player_cards.append(pickcard())
    dealer_pick.append(dealer_cards[0])
    for i in range(2):
        player_pick.append(player_cards[i])


def pickcard():
    pick = deck[random.randint(0, len(deck) - 1)]
    deck.remove(pick)
    return pick


def start(player_name):
    step = 0
    turn(0, None, player_name)
    while not gameover:
        action(step, player_name)
        step += 1


def turn(number, player_choice, player_name):
    dealer_total = results[0]
    player_total = results[1]
    if number == 0:
        dealer_total += count(dealer_pick[0][0], dealer_total)
        player_total += count(player_pick[0][0], player_total)
        player_total += count(player_pick[1][0], player_total)
        results.insert(0, dealer_total)
        results.insert(1, player_total)
        showcards(player_name)
    elif number > 0:
        if player_choice == 'H':
            player_pick.append(player_cards[number+1])
            player_total += count(player_pick[number+1][0], player_total)
            results.insert(0, dealer_total)
            results.insert(1, player_total)
            showcards(player_name)
        elif player_choice == 'S':
            global gameover
            gameover = True
            dealer_pick.append(dealer_cards[1])
            dealer_total += count(dealer_pick[1][0], dealer_total)
            results.insert(0, dealer_total)
            results.insert(1, player_total)
            showcards(player_name)
            for i in range(2, len(dealer_cards)):
                while dealer_total < 17:
                    print('\n' + str.center('Dealer Hits.', width) + '\n')
                    sleep(1)
                    dealer_pick.append(dealer_cards[i])
                    dealer_total += count(dealer_pick[i][0], dealer_total)
                    results.insert(0, dealer_total)
                    results.insert(1, player_total)
                    showcards(player_name)
            if dealer_total < player_total:
                print(str.center('Dealer Stands.', width) + '\n')
    game_result(player_name)


def count(card, player):
    if card == 'Ace':
        if player > 11:
            return 1
        elif player <= 11:
            return 10
    elif str(card) in ['Jack', 'Queen', 'King']:
        return 10
    else:
        return card


def action(step, player_name):
    turnnumber = step
    playerchoice = str.capitalize(input(str.center('Enter H to Hit or S to Stand. Press Enter to confirm.', width) + '\n'))
    if playerchoice in ['S', 'H']:
        turnnumber += 1
        turn(turnnumber, playerchoice, player_name)
    else:
        print('Incorrect Input.')
        action(turnnumber, player_name)


def showcards(playername):
    print('\n')
    print(str.rjust("Dealers Hand:", round(width*0.4)))
    for i in dealer_pick:
        if i[1] == 'Hearts':
            print(str.rjust(Fore.RED + Back.WHITE + '♥ ' + str(i[0]) + ' ♥', round(width*0.46)) + Style.RESET_ALL)
        if i[1] == 'Diamonds':
            print(str.rjust(Fore.RED + Back.WHITE + '♦ ' + str(i[0]) + ' ♦', round(width*0.46)) + Style.RESET_ALL)
        if i[1] == 'Clubs':
            print(str.rjust(Fore.BLACK + Back.WHITE + '♣ ' + str(i[0]) + ' ♣', round(width*0.46)) + Style.RESET_ALL)
        if i[1] == 'Spades':
            print(str.rjust(Fore.BLACK + Back.WHITE + '♠ ' + str(i[0]) + ' ♠', round(width*0.46)) + Style.RESET_ALL)
    print(str.rjust("Value: " + str(results[0]), round(width*0.4)))
    sleep(0.5)
    print(str.rjust(playername + "'s Hand:", round(width*0.66)))
    for i in player_pick:
        if i[1] == 'Hearts':
            print(str.rjust(Fore.RED + Back.WHITE + '♥ ' + str(i[0]) + ' ♥', round(width * 0.72)) + Style.RESET_ALL)
        if i[1] == 'Diamonds':
            print(str.rjust(Fore.RED + Back.WHITE + '♦ ' + str(i[0]) + ' ♦', round(width * 0.72)) + Style.RESET_ALL)
        if i[1] == 'Clubs':
            print(str.rjust(Fore.BLACK + Back.WHITE + '♣ ' + str(i[0]) + ' ♣', round(width * 0.72)) + Style.RESET_ALL)
        if i[1] == 'Spades':
            print(str.rjust(Fore.BLACK + Back.WHITE + '♠ ' + str(i[0]) + ' ♠', round(width * 0.72)) + Style.RESET_ALL)
    print(str.rjust("Value: " + str(results[1]) + "\n", round(width*0.66)))
    sleep(0.5)


def game_result(player_name):
    if results[1] == 21:
        wins_losses[0] += 1
        print(str.center('BLACKJACK! You Win!', width))
        gameend(player_name)
    if results[1] > 21:
        wins_losses[1] += 1
        print(str.center('Whoops! You went bust! Dealer Wins.', width))
        gameend(player_name)
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
        gameend(player_name)


def gameend(player_name):
    print(str.center('Wins: ' + str(wins_losses[0]) + ', Losses: ' + str(wins_losses[1]), width))
    playagain(player_name)


def playagain(player_name):
    sleep(0.5)
    if str.capitalize(input('\n' + str.center('Press Enter to play again or type Q to exit.', width) + '\n')) == 'Q':
        print(str.center('Thanks for playing!', width))
        sleep(1)
        sys.exit()
    else:
        main(player_name)


if input('\n' + str.center('Press Enter to start or type Q to quit!', width) + '\n') not in ['Q', 'q']:
    main('')
else:
    sys.exit()
