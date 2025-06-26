from dataclasses import dataclass
from constants import SUITS, VALUES
from random import shuffle

@dataclass
class CardType:
    name: str
    value: int
    
class Deck:
    def __init__(self, num_decks=1):
        self.cards = []
        self.num_decks = num_decks
        self.build()

    def build(self):
        self.cards = []
        for _ in range(self.num_decks):
            for value in VALUES:
                for suit in SUITS:
                    card_name = f"{value}{suit}"
                    card_value = 11 if value == "A" else 10 if value in "JQK" else int(value)
                    self.cards.append(CardType(name=card_name, value=card_value))

    def shuffle(self):
        shuffle(self.cards)
        
    def deal(self):
        if not self.cards:
            self.build()
            self.shuffle()
        return self.cards.pop()
        
class Hand:
    def __init__(self):
        self.cards = []
        self.card_img = []
        self.value = 0

    def add_card(self, card: CardType):
        self.cards.append(card)

    def calc_hand(self):
        self.value = 0
        non_aces = [c for c in self.cards if c.name[0] != 'A']
        aces = [c for c in self.cards if c.name[0] == 'A']

        for card in non_aces:
            self.value += card.value

        for card in aces:
            self.value += 11 if self.value <= 10 else 1
        return self.value
    

    def display_cards(self):
        for card in self.cards:
            if card.name not in self.card_img:
                self.card_img.append(card.name)
