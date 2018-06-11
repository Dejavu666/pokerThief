from random import shuffle

# Deck is a list of 'cards' (tuples)
# (2,'H') is 2 of hearts, (14,'S') is ace of spades

class Deck():
    def __init__(self):
        self.reset_shuffle()
        
    def draw_card(self):
        x = self.cards.pop()
        return x
        
    def reset_shuffle(self):
        self.cards = []
        for rank in [2,3,4,5,6,7,8,9,10,11,12,13,14]:
            for suit in ['H','S','D','C']:
                self.cards.append((rank,suit))
        shuffle(self.cards)