from random import shuffle

class Deck():
    def __init__(self):
        self.reset_shuffle()
        
    def draw_card(self):
        x = self.cards.pop()
        return x
        
    def reset_shuffle(self):
        self.cards = []
        for rank in ['A','2','3','4','5','6','7','8','9','T','J','Q','K']:
            for suit in ['H','S','D','C']:
                self.cards.append(rank+suit)
        shuffle(self.cards)