# import dependencies
import threading
import mttkinter.mtTkinter as tK
from PIL import ImageTk, Image
import random
from itertools import product
#set fixed card width and heights
cardwidth = 68
cardheight = 95
# Initialise list with card values and suits.
values, suits = ['ace', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'jack', 'queen', 'king'], ['hearts', 'diamonds', 'clubs', 'spades']
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
# initialise turn counter
turn_counter = 0

# define play function
def play():
    # if wins_losses has any non-zero values then game has been played before, so previous cards need to be removed.
    if wins_losses != [0,0]:
        # delete previous roud message.
        message.grid_forget()
        # remove cards 3 and beyond from player and dealer.
        for i in range(3, len(dealer_pick)+1):
            name = "dealer_card_" + str(i)
            globals()[name].grid_forget()
        for i in range(3, len(player_pick)+1):
            name = "player_card_" + str(i)
            globals()[name].grid_forget()
    # remove start button
    start_button.destroy()
    # forget play_again_button
    play_again_button.grid_forget()
    # display dealer and player labels, as well as hit and stand buttons and scoreboard.
    dealer_label.grid(row=1, column=1)
    player_label.grid(row=2, column=1)
    hit_button.grid(row=3, column=3)
    stand_button.grid(row=3, column=5)
    scoreboard.grid(row=3, column=1)
    # setup next round
    setup_round()

def buttonpressed(value):
    global turn_counter
    choice = str(value)
    # When player presses Hit or Stand then pass their choice to the turn() function along with the turn number; increment turncounter by 1.
    turn_counter +=1
    turn(turn_counter, choice)

def setup_round():
    # reset global gameover variable to False and turn counter to 0.
    global gameover
    global turn_counter
    gameover = False
    turn_counter = 0
    # reset results list indexes to 0, clear dealers and players cards, dealer and player aces, and dealers and players visible cards.
    results.insert(0, 0)
    results.insert(1, 0)
    dealer_aces.clear()
    player_aces.clear()
    dealer_cards.clear()
    player_cards.clear()
    dealer_pick.clear()
    player_pick.clear()
    deal()
    # take first turn, no player choice at this stage so pass None.
    turn(0, None)

def turn(number, player_choice):
    # set dealer and player total values.
    dealer_total = results[0]
    player_total = results[1]
    # Initial turn after setup.
    if number == 0:
        # Count value of currently shown cards for dealer and player and insert them into the results list.
        dealer_total += count(dealer_pick[0][0], dealer_total)
        player_total += count(player_pick[0][0], player_total)
        player_total += count(player_pick[1][0], player_total)
        results.insert(0, dealer_total)
        results.insert(1, player_total)
        # Display cards in GUI
        dealer_card_1 = str(dealer_pick[0][0]) + '_' + dealer_pick[0][1]
        dealer_card_1 = tK.Label(width=cardwidth, height=cardheight, borderwidth=1, relief="solid", image=globals()[dealer_card_1])
        dealer_card_2 = tK.Label(width=cardwidth, height=cardheight, borderwidth=1, relief="solid", image=back)
        dealer_card_1.grid(row=1, column=2)
        dealer_card_2.grid(row=1, column=3)
        player_card_1 = str(player_pick[0][0]) + '_' + player_pick[0][1]
        player_card_2 = str(player_pick[1][0]) + '_' + player_pick[1][1]
        player_card_1 = tK.Label(width=cardwidth, height=cardheight, borderwidth=1, relief="solid", image=globals()[player_card_1])
        player_card_2 = tK.Label(width=cardwidth, height=cardheight, borderwidth=1, relief="solid", image=globals()[player_card_2])
        player_card_1.grid(row=2, column=2)
        player_card_2.grid(row=2, column=3)
    # Subsequent turns
    elif number > 0:
        # If player chooses to hit, reveals another player card and total hand value.
        if player_choice == 'H':
            player_pick.append(player_cards[number+1])
            # If card is an Ace, append the value it was assigned to the player aces list.
            if player_pick[number+1][0] == 'ace':
                player_aces.append(count(player_pick[number + 1][0], player_total))
            # find and display correct image for the picked card and display next to current cards
            player_card_number = "player_card_" + str(number+2)
            player_card = str(player_pick[number+1][0]) + '_' + player_pick[number+1][1]
            globals()[player_card_number] = tK.Label(width=cardwidth, height=cardheight, borderwidth=1, relief="solid",
                                                     image=globals()[player_card])
            col = number + 3
            globals()[player_card_number].grid(row=2, column=col)
            player_total += count(player_pick[number + 1][0], player_total)
            # Check if previous cards contain Aces, if so, check if player has gone bust, if so remove 10 so Ace becomes worth 1 instead of 11.
            for i in range(len(player_aces)):
                if player_aces[i] == 11 and player_total > 21:
                    player_aces[i] = 1
                    player_total -= 10
            #insert new totals as results.
            results.insert(0, dealer_total)
            results.insert(1, player_total)

        # If player chooses to stand, gameover is set to True, and dealer takes action based on Blackjack rules, revealing hand after each action.
        elif player_choice == 'S':
            global gameover
            gameover = True
            # find and display correct image for the picked card and display next to current cards
            dealer_pick.append(dealer_cards[1])
            dealer_card_2 = str(dealer_pick[1][0]) + '_' + dealer_pick[1][1]
            dealer_card_2 = tK.Label(width=cardwidth, height=cardheight, borderwidth=1, relief="solid", image=globals()[dealer_card_2])
            dealer_card_2.grid(row=1, column=3)
            # If card is an Ace, append the value it was assigned to the dealer aces list.
            if dealer_pick[1][0] == 'ace':
                dealer_aces.append(11)
            dealer_total += count(dealer_pick[1][0], dealer_total)
            # insert new totals as results.
            results.insert(0, dealer_total)
            results.insert(1, player_total)
            # If dealers hand is less than 17, dealer will hit and take another card. This repeats until the hand is equal to or over 17.
            while dealer_total < 17:
                for i in range(2, len(dealer_cards) - 1):
                    # exit while loop and continue once dealer_total is 17 or over.
                    if dealer_total >= 17:
                        continue
                    dealer_pick.append(dealer_cards[i])
                    # find and display correct image for the picked card and display next to current cards
                    dealer_card_number = "dealer_card_" + str(i+1)
                    dealer_card = str(dealer_pick[i][0]) + '_' + dealer_pick[i][1]
                    globals()[dealer_card_number] = tK.Label(width=cardwidth, height=cardheight, borderwidth=1, relief="solid",
                                             image=globals()[dealer_card])
                    col = i+2
                    globals()[dealer_card_number].grid(row=1, column=col)
                    if dealer_pick[i][0] == 'ace':
                        player_aces.append(count(dealer_pick[i][0], player_total))
                    dealer_total += count(dealer_pick[i][0], dealer_total)
                    # Check if previous cards contain Aces, if so, check if Dealer has gone bust, if so remove 10 so Ace becomes worth 1 instead of 11.
                    for ace in range(len(dealer_aces)):
                        if dealer_aces[ace] == 11 and dealer_total > 21:
                            dealer_aces[ace] = 1
                            dealer_total -= 10
                    results.insert(0, dealer_total)
                    results.insert(1, player_total)
    # show card values
    dealer_label.configure(text="Dealer\n" + str(results[0]))
    player_label.configure(text="Player\n" + str(results[1]))
    # Check results after each turn
    game_result()

# determine outcome of game by comparing player and dealer results. Print result then end round. Track overall wins/losses within wins_losses list
def game_result():
    global turn_counter
    global gameover
    # If player gets blackjack on first turn or goes bust prior to dealer card reveals, print result immediately. Dealer does not take turn and gameover variable remains False.
    if not gameover:
        if results[1] == 21:
            wins_losses[0] += 1
            if turn_counter == 0:
                message.configure(text='BLACKJACK!\nYou Win!')
                gameend()
            else:
                turn_counter +=1
                turn(turn_counter, 'S')
                gameover = True
        if results[1] > 21:
            wins_losses[1] += 1
            message.configure(text='You went bust!\nDealer Wins.')
            gameend()
    # Player does not achieve blackjack or go bust, dealer takes turn(s) and gameover variable is set to True. Calculate outcome and print result.
    if gameover:
        if results[0] == 21:
            wins_losses[1] += 1
            message.configure(text='BLACKJACK!\nDealer Wins!')
        elif results[0] > 21:
            wins_losses[0] += 1
            message.configure(text='Dealer goes bust!\nYou Win!')
        elif results[0] >= results[1]:
            wins_losses[1] += 1
            message.configure(text='Dealer Wins!\nBetter Luck Next Time!')
        elif results[0] <= results[1]:
            wins_losses[0] += 1
            message.configure(text='Congratulations!\nYou Win!')
        # End round.
        gameend()

def gameend():
    #update scoreboard
    scoreboard.configure(text="Wins: " + str(wins_losses[0]) + "\nLosses: " + str(wins_losses[1]))
    # show play again button and hide other buttons.
    play_again_button.grid(row=3, column=4)
    hit_button.grid_forget()
    stand_button.grid_forget()
    # show result message
    message.grid(row=1, rowspan=2, column=3, columnspan=3)


# Determine card value and return this.
def count(card, player):
    if card == 'ace':
        if player > 10:
            return 1
        elif player <= 10:
            return 11
    elif str(card) in ['jack', 'queen', 'king']:
        return 10
    else:
        return card


def card_setup():
    # populate card deck with all cards.
    for i in list(product(values, suits)):
        deck.append(i)
    for suit in suits:
        for card in values:
            # create cardname variable to match image naming conventions.
            cardname = str(card) + "_" + suit
            # assign all card images as global variables
            globals()[cardname] = Image.open("card_images/" + cardname + ".jpg")
            globals()[cardname] = globals()[cardname].resize((72, 100), Image.ANTIALIAS)
            globals()[cardname] = ImageTk.PhotoImage(globals()[cardname])
    #assign card back image as global variable.
    global back
    back = ImageTk.PhotoImage(Image.open("card_images/back.jpg").resize((72, 100), Image.ANTIALIAS))

# Deal function picks cards one by one, removing them from the deck, and adding them to dealer_cards and player_cards lists until the deck is empty.
def deal():
    card_setup()
    while len(deck) > 0:
        dealer_cards.append(pickcard())
        player_cards.append(pickcard())
    dealer_pick.append(dealer_cards[0])
    # If card is an Ace, append the value it was assigned to the dealer aces list.
    if dealer_cards[0][0] == 'ace':
        dealer_aces.append(11)
    for i in range(2):
        player_pick.append(player_cards[i])
        # If card is an Ace, append the value it was assigned to the player aces list.
        if player_cards[i][0] == 'ace':
            player_aces.append(11)

# pickcard() function picks cards at random and returns the picked card.
def pickcard():
    pick = deck[random.randint(0, len(deck) - 1)]
    deck.remove(pick)
    return pick

window = tK.Tk()
window.title("Python BlackJack")
window.geometry("750x600")
window.grid_columnconfigure((0,1,2,3,4,5,6,7,8), minsize=82)
window.grid_rowconfigure((0,1,2,3), minsize=150)
icon1=tK.Label(text="♥")
icon1.config(font=("Arial Bold", 80), fg="Red")
icon2=tK.Label(text="♠")
icon2.config(font=("Arial Bold", 80))
icon3=tK.Label(text="♣")
icon3.config(font=("Arial Bold", 80))
icon4=tK.Label(text="♦")
icon4.config(font=("Arial Bold", 80), fg="Red")
title=tK.Label(text="BlackJack")
title.config(font=("Arial Bold", 46))
icon1.grid(row=0, column=1)
icon2.grid(row=0, column=2)
title.grid(row=0, column=3, columnspan=3)
icon3.grid(row=0, column=6)
icon4.grid(row=0, column=7)
start_button = tK.Button(text="Start Game", command=play)
start_button.config(font=("Arial Bold", 50))
start_button.grid(row=1, rowspan=2, column=3, columnspan=3)
dealer_label = tK.Label(text="Dealer")
dealer_label.config(font=("Arial Bold", 16))
player_label = tK.Label(text="Player")
player_label.config(font=("Arial Bold", 16))
hit_button = tK.Button(text="Hit", width=8, command=lambda : buttonpressed('H'))
stand_button = tK.Button(text="Stand", width=8, command=lambda : buttonpressed('S'))
hit_button.config(font=("Arial Bold", 16))
stand_button.config(font=("Arial Bold", 16))
play_again_button = tK.Button(text="Play Again", command=play)
play_again_button.config(font=("Arial Bold", 16))
scoreboard = tK.Label(text="Wins: " + str(wins_losses[0]) + "\nLosses: " + str(wins_losses[1]))
dealer_label = tK.Label(text="Dealer")
dealer_label.config(font=("Arial Bold", 16))
player_label = tK.Label(text="Player")
player_label.config(font=("Arial Bold", 16))
message = tK.Label(text="")
message.config(font=("Arial Bold", 14))
window.mainloop()

