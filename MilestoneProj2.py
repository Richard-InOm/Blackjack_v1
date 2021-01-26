'''
Custom text based BlackJack Card game
'''
import random

#Global Variables to be used in Card Creation
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

#Global Variable Used to determine rounds
playing = True

#Define the Class Card
class Card:
    ''''
    Building block of playing cards
    '''
    #Initialize with the suit and rank
    #Calculate the value to be used later on in gameplay
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]
    
    def __str__(self):
        return f'{self.rank} of {self.suit}'

#Define a Class to be used to make a deck of 52 cards
class Deck:
    '''
    Deck of 52 Cards with methods for Shuffling and Dealing
    '''
    #Initialize the Deck with an empty list
    #Fill up the deck list with card instances of all the unique cards
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))
    
    def __str__(self):
        return f'There are {len(self.deck)} cards'

    #Use the random module imported to make a shuffle method
    def shuffle(self):
        random.shuffle(self.deck)
    
    #Use the pop method on the deck list to remove a card and deal it
    def deal(self):
        return self.deck.pop(0)

#Define a class to be used to represent the player and their hand
class PlayerHand:
    #Initialize the Class with the name of the player and the amount of money they're bringing to the 'casino'
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0   #Keep count of the number of aces for Ace optimization later
        self.rounds = 0 #Keep count of rounds won
        self.winnings = 0   #Keep count of total money won
        self.losses = 0 #Keep count of total money lost
    
    #Method to add a card to a player's Hand
    def add_card(self,card):
        self.cards.append(card)
        self.value += card.value
        if card.rank == 'Ace':
            self.aces += 1 #Keep track of Aces

    #Method for Ace optimization
    def adjust_for_aces(self):
        value = 0
        for card in self.cards:
            if card.rank != 'Ace':
                value += card.value
        if value > 10:
            for ace in range(self.aces):
                value += 1  #Aces count as 1 when preferable though originally are counted as 11
            self.value = value

    #Method to keep track of money available for betting
    def show_balance(self):
        print(f"{self.name} currently has ${self.balance}")
    
    #Method to display player stats 
    def stats(self):
        print(f"{self.name} rounds won: {self.rounds}")
        print(f"{self.name} total winnings: {self.winnings}")
        print(f"{self.name} total losses: {self.losses}")
        print(f"{self.name} current balance: {self.balance}")
    
    #Method to show how many cards a player has and the total value (was mostly used in testing lol)
    def __str__(self):
        return f'{self.name} has {len(self.cards)} cards with a total value of {self.value}'



#Function for the Hit Action
def hit(deck, hand):
    card = deck.deal()  #Pop a card from the deck
    hand.add_card(card) #Add the card to the Hand of the player
    hand.adjust_for_aces()  #Adjust the value of the player's Hand for Ace optimization (if necessary)

#Function to Show All the Player's Cards but keep one of the Dealer's hidden
def show_some(player, dealer):
    print(f"{player.name}'s Cards:")
    #Loop through the player's cards
    for card in player.cards:   
        print(card) #Print the cards
    print() #Leave a space for readerbility
    print(f"{dealer.name}'s Cards: ")
    print("Hidden Card")
    #Do the same for dealer but leave his first card out
    for card in dealer.cards[1:]:
        print(card)
    print()

#Function to show all the player and dealer cards, pretty identical to the previous one
def show_all(player, dealer):
    print(f"{player.name}'s Cards:")
    for card in player.cards:
        print(card)
    print()
    print("Al's Cards: ")
    for card in dealer.cards:
        print(card)
    print()

#Function to Take bets from players
def take_bet(player):
    #Initialize bet to a string
    bet = 'bet'
    #Loop until the user updates bet to an integer
    while bet.isdigit() == False:
        #Keep the user informed of how much money they have in the bank
        player.show_balance()
        #Ask the user for their bet
        bet = input(f"{player.name}, how much are you willing to bet this round(No cents): ")
        #Print an error message if they type in letters
        if bet.isalpha():
            print('Please type money in numbers')
        #Print an error message if they add decimals
        elif '.' in bet:
            print('No cents! Try again')
        #Print an error if they try to bet more than they currently have in the bank
        elif int(bet) > player.balance:
            print("Not enough cash, try again.")
            bet = 'bet'
    return bet

#Function to ask the user if they want to Hit or Stand
def hit_or_stand(deck, player):
    #Call the global variable playing
    global playing
    #Initialize act to a string
    act = 'act'
    #While the round is on
    while playing:
        #Loop until the player gives an appropriate action or busts
        while act not in ['H', 'S'] and player.value <= 21:
            #Inform them of their current Hand value
            print(f"Hand value currently at {player.value}")
            #Input the action
            act = input(f"{player.name}, Hit or Stand?(H/S) ")
        if act == 'H':
            hit(deck, player)
            act = 'act'
        elif act == 'S':
            print("Player Stands! Dealer's Turn...")
            print()
            playing = False
        if player.value > 21:
            playing = False

#Function for Player Bust Scenario
def player_bust(player, dealer, bet):
    print(f"{player.name}'s Hand had a value of {player.value}")    #Let the user know his Hand value
    print('Bust!')
    print('Al has won this round!')
    print() #Empty line for readerbility
    player.balance -= bet   #Update player balance
    player.losses += bet    #Update player losses
    dealer.balance += bet   #Update dealer balance (not important really)
    dealer.winnings += bet  #Update dealer winnings (also not important)
    dealer.rounds += 1  #Update dealer rounds won (unimportant)
    show_all(player, dealer)    #Show both player and dealer hands

#Function to play the dealer's hand
def play_dealer(player, dealer, deck):
    #Dealer Hits until he either beats the player or exceeds 21
    while True:
        if dealer.value < player.value and dealer.value < 21:
            hit(deck, dealer)
        else:
            break

#Function for dealer bust scenario
def dealer_bust(player, dealer, bet):
    print(f"Al's Hand had a value of {dealer.value}")
    print("Bust!")
    print(f"{player.name} has wone this round!")
    print()
    #Run updates on stats
    player.balance += bet
    player.winnings += bet
    player.rounds += 1
    dealer.balance -= bet
    dealer.losses += bet
    show_all(player, dealer)

#Function for player win, no busts scenario
def player_win(player, dealer, bet):
    print(f"{player.name}'s Hand had a value of {player.value}")
    print(f"Al's Hand had a value of {dealer.value}")
    print(f"{player.name} has wone this round!")
    print()
    #Update stats
    player.balance += bet
    player.winnings += bet
    player.rounds += 1
    dealer.balance -= bet
    dealer.losses += bet
    show_all(player, dealer)

#Function for dealer win, no busts scenario
def dealer_win(player, dealer, bet):
    print(f"{player.name}'s Hand had a value of {player.value}")
    print(f"Al's hand had a value of {dealer.value}")
    print('Al has won this round!')
    print()
    #Update Stats
    player.balance -= bet
    player.losses += bet
    dealer.balance += bet
    dealer.winnings += bet
    dealer.rounds += 1
    show_all(player, dealer)

#Function to ask if player wants to play another round
def replay():
    rep = 'rep'
    while rep not in ['Y','N']:
        rep = input("Want to play another round?(Y/N)")
    return rep == 'Y'

#Function to reset gameplay components
def reset(deck, player, dealer):
    #Restock deck to 52 cards
    deck = Deck()
    #Empty out player and dealer hands
    player.cards = []
    player.value = 0
    player.aces = 0
    dealer.cards = []
    dealer.value = 0
    dealer.aces = 0

#Yay! Gameplay finally starts
while True:
    #Oops, not yet gotta set up first
    #Set the game to be on
    gameon = True
    #Print a welcome message
    print('Welcome to BlackJack!')
    #Initialize the deck
    gamedeck = Deck()
    #Shuffle the deck
    gamedeck.shuffle()
    #Ask for player name
    name = input("Player, what is your name? ")
    #Initialize player bank to a string
    balance = 'balance'
    #Loop until user gives appropriate response
    while balance.isdigit() == False:
        #Ask for bank
        balance = input(f"{name}, how much money are you playing with(No cents): ")
        #Error message for text
        if balance.isalpha():
            print('Please type money in numbers')
        #Error message for decimals
        elif '.' in balance:
            print('No cents! Try again')
    
    #Initialize the Player and Dealer
    player = PlayerHand(name, int(balance))
    al = PlayerHand('Al', int(balance)) #I chose to call my dealer Al because I was getting tired and dealer is long and I like Al
    #Loop until user decides to stop playing
    while gameon:
        #Deal two cards to the player and dealer (or al in my case)
        for num in range(2):
            hit(gamedeck, player)
            hit(gamedeck, al)
        #Take the player's bet
        bet = int(take_bet(player))
        #Show some of the cards
        show_some(player, al)
        #Loop until the round ends
        while playing:
            #Player's turn
            hit_or_stand(gamedeck, player)
            #Show some cards
            show_some(player, al)
            #If player busts during their turn, no need for dealer to play
            if player.value > 21:
                player_bust(player, al, bet)
                break   #End the round
            #If player doesn't bust, dealer's turn
            play_dealer(player, al, gamedeck)
            #If dealer busts
            if al.value > 21:
                dealer_bust(player, al, bet)
                break
            #If no bust, check for player win
            if player.value > al.value:
                player_win(player, al, bet)
                break
            #If no bust, check for dealer win
            if player.value < al.value:
                dealer_win(player, al, bet)
                break
            #If no bust and no win, must be tie but check anyway
            if player.value == al.value:
                print('Draw!')
                show_all(player, al)
                break
            #Round ends anyway
        #Remind player of their current stats
        player.stats()
        #Ask player if they want to play again
        rep = replay()
        #If they want to play and still have money in the bank
        if rep and player.balance > 0:
            playing = True  #Set the round to be true
            reset(gamedeck, player, al) #Reset the gamplay components
            continue    #Skip to top of game loop
        #If they still want to play but don't have enough cash in the bank
        elif rep and player.balance <= 0:
            print("Sorry, you're out of cash!")
            print("Input some more and start over")
            break   #Restart the game
        #They don't want to play again, end game
        else:
            break
    #Remind them of stats
    print()
    print("Here are your stats again: ")
    player.stats()
    print("Thanks for playing!")
    print()
    #If they chose to play again but ran out of cash, restart the whole game
    if rep:
        playing = True
        continue    #Skip to top of game including set up
    #Prevent infinite loop and allow game exit
    break