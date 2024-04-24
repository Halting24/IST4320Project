import tkinter as tk
from tkinter import messagebox
import random

# Define the card class
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = self._set_value(rank)
    
    def _set_value(self, rank):
        if rank in ['Jack', 'Queen', 'King']:
            return 10
        elif rank == 'Ace':
            return 11
        else:
            return int(rank)
    
    def __repr__(self):
        return f"{self.rank} of {self.suit}"

# Define the deck class
class Deck:
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in self.suits for rank in self.ranks]
        random.shuffle(self.cards)
    
    def deal(self):
        if len(self.cards) > 0:
            return self.cards.pop()
        else:
            return None

# Define the hand class
class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += card.value
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

    def get_value(self):
        self.adjust_for_ace()
        return self.value

    def __repr__(self):
        return ', '.join(str(card) for card in self.cards)

# Define the Blackjack game class
class BlackjackGame:
    def __init__(self, root):
        self.root = root
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()

        self.player_hand.add_card(self.deck.deal())
        self.player_hand.add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())

        self.player_label = tk.Label(root, text=f"Player's Hand: {self.player_hand}")
        self.player_label.pack()

        self.dealer_label = tk.Label(root, text=f"Dealer's Hand: {self.dealer_hand}")
        self.dealer_label.pack()

        self.hit_button = tk.Button(root, text='Hit', command=self.player_hit)
        self.hit_button.pack()

        self.stand_button = tk.Button(root, text='Stand', command=self.player_stand)
        self.stand_button.pack()

        self.update_ui()

    def player_hit(self):
        self.player_hand.add_card(self.deck.deal())
        self.update_ui()

        if self.player_hand.get_value() > 21:
            messagebox.showinfo('Busted!', 'You busted! Dealer wins.')
            self.reset_game()

    def player_stand(self):
        while self.dealer_hand.get_value() < 17:
            self.dealer_hand.add_card(self.deck.deal())

        self.update_ui()

        player_score = self.player_hand.get_value()
        dealer_score = self.dealer_hand.get_value()

        if dealer_score > 21 or player_score > dealer_score:
            messagebox.showinfo('You Win!', 'You beat the dealer!')
        elif player_score < dealer_score:
            messagebox.showinfo('Dealer Wins!', 'Dealer beats you!')
        else:
            messagebox.showinfo('Push!', 'It\'s a push, nobody wins.')

        self.reset_game()

    def update_ui(self):
        self.player_label.config(text=f"Player's Hand: {self.player_hand} (Value: {self.player_hand.get_value()})")
        self.dealer_label.config(text=f"Dealer's Hand: {self.dealer_hand} (Value: {self.dealer_hand.get_value()})")

    def reset_game(self):
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.player_hand.add_card(self.deck.deal())
        self.player_hand.add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())
        self.update_ui()

# Create the main window
root = tk.Tk()
root.title("Blackjack Game")

game = BlackjackGame(root)

root.mainloop()

