# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
player_score = ""
dealer_score = "Unknown"
outcomes = ['Player Wins', 'Dealer Wins', 'You have busted', 'Dealer Busts']

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        card_string = ""
        for card in self.cards:
            card_string += card.__str__() + " "
        return "Hand contains " + card_string

    def add_card(self, card):
        self.cards.append(card)	# add a card object to a hand

    def get_value(self):
        value = 0
        ranks = []  
        for card in self.cards:
            rank = card.get_rank()
            ranks.append(rank)
            value += VALUES[rank]
        if ranks.count('A') > 0 and value <= 11:
            value += 10
        
        return value
        
    def draw(self, canvas, pos):
        for i in range(len(self.cards)): 
            card = self.cards[i]
            card.draw(canvas, [pos[0] + i*40, pos[1]])

        
# define deck class 
class Deck:
    def __init__(self):
        self.deck = [Card(suit, rank) for suit in SUITS for rank in RANKS]
        
    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()
    
    def __str__(self):
        card_string = ""
        for card in self.deck:
            card_string += card.__str__() + " "
        return "Deck contains " + card_string



#define event handlers for buttons
def deal():
    global outcome, message, in_play, deck, dealer_hand, player_hand, score, player_score,dealer_score
    if in_play:
        score -= 1
    dealer_score = "Unknown"
    message = ""
    deck = Deck()
    deck.shuffle()
    dealer_hand = Hand()
    player_hand = Hand()
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    
    outcome = "Hit or stand?"
    player_score = player_hand.get_value()
    
    in_play = True

def hit():
    global in_play, message, player_hand, deck, outcome, score, player_score, dealer_score
    
    # if the user busted, prevent them from being able to hit again
    if outcomes.count(outcome) == 0:
        player_hand.add_card(deck.deal_card())
        # if busted, assign a message to outcome, update in_play and score
        if player_hand.get_value() > 21:
            outcome = 'You have busted'
            in_play = False
            score -= 1
            message = "New Deal?"
        player_score = player_hand.get_value()
        
        if outcome == 'You have busted':
            dealer_score = dealer_hand.get_value()
    
def stand():
    global in_play, message, dealer_deck, deck, player_hand, outcome, player_score, dealer_score, score
    if in_play:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
            
        if dealer_hand.get_value() > 21:
            outcome = 'Dealer Busts'
            score += 1
        elif dealer_hand.get_value() >= player_hand.get_value():
            outcome = 'Dealer Wins'
            score -= 1
        else:
            outcome = 'Player Wins'
            score += 1
        message = "New Deal?"
    in_play = False
    
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    card = Card("S", "A")
    canvas.draw_text("Blackjack", [10, 50], 50, 'Purple')
    canvas.draw_text("Dealer Hand: "+ str(dealer_score), [170, 140], 30, 'White')
    canvas.draw_text("Player Hand: "+ str(player_score), [170, 550], 30, 'White')
    canvas.draw_text(outcome, [300, 350], 25, "Black")
    canvas.draw_text(message, [300, 370], 25, "Black")
    canvas.draw_text("Score " + str(score), [450, 100], 25, "Black")
    # if player hand is in play, show only one dealer card
    canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE,
                      [10 + CARD_BACK_SIZE[0], 100 + CARD_BACK_SIZE[1]],
                      CARD_SIZE)
    
    if in_play:
        dealer_hand.draw(canvas, [200, 170])
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE,
                      [200 + 38*2, 218],
                      CARD_SIZE)
    else:
    #dealer_hand.draw(canvas, [60 + CARD_CENTER[0], 170 + CARD_CENTER[1]])
        dealer_hand.draw(canvas, [200, 170])
    player_hand.draw(canvas, [200, 425])
    
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric