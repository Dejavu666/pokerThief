# table.py
import player, deck, hands
from random import shuffle

class Table():
    def __init__(self, num_players, start_stack, big_blind):
        self.num_players = num_players
        self.start_stack = start_stack
        self.big_blind = big_blind
        
        self.deck = deck.Deck()
        self.com_cards = []
        self.pot = 0
        
        self.plyr_dict = \
        {'player'+str(i+1) : player.Player(stack_size=start_stack) for i in range(num_players-1)}
        
        self.plyr_dict['player1'].human = 1
        
        # seat_order[0] is dealer, seat_order[1] is SB
        self.seat_order = [k for k in self.plyr_dict.keys()]
        shuffle(self.seat_order)
        
        self.round = 'preflop' # 'flop' | 'turn' | 'river'
        self.cost_to_play = 0
        self.min_bet = 0
        
    # Subtract blind amounts from SB BB and add them to pot
    # Account for less than legal stack sizes
    def post_blinds(self):
        # dealer+1 enough for SB
        if self.plyr_dict[self.seat_order[1]].stack_size >= (self.big_blind/2):
            self.plyr_dict[self.seat_order[1]].contribute_chips(self.big_blind/2)
            self.pot += (self.big_blind/2)





####### TEST #######
table = Table(6, 1000, 20)

print(table.plyr_dict)
print(table.seat_order)