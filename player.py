from random import randrange
class Player():
    def __init__(self, stack=0):
        self.stack = stack
        self.hand = []
        self.chips_this_round = 0
        self.begin_hand_chips = 0
        self.chips_in_pot = 0
        self.human = 1
        self.hand_rank = 0
        self.tie_break = []
        
    def str_hand(self):
        new_hand = []
        for card in self.hand:
            str_card = str(card[0]) + str(card[1])
            new_hand.append(str_card)
        return new_hand

    def draw_card(self,card):
        self.hand.append(card)
        
    def contribute_chips(self, amount):
        assert(amount <= self.stack)
        self.chips_in_pot += amount
        self.chips_this_round += amount
        self.stack -= amount
    
    def clean_player_after_hand(self):
        self.hand = []
        self.chips_this_round = 0
        self.chips_in_pot = 0
        self.begin_hand_chips = self.stack
    
    # bot needs all irreducible info, but start with:
    # stacksize, cost2play, com_cards,
    def bot_action(self, cost2play, bb, minbet):
        if self.chips_this_round == cost2play:# table is open
            # placeholder for testing
            # gets random bot action between possible actions
            randval = randrange(0,1)
            if randval == 0:
                amount = randrange(bb,self.stack)
                return ('bet',amount)
            elif randval == 1:
                return ('check',0)
        else:#table is bet
            assert(cost2play > self.chips_this_round)
            randval = randrange(0,2)
            if randval == 0:
                return ('call',min(self.stack, cost2play-self.chips_this_round))
            elif randval == 1:
                amount = randrange(min(minbet,self.stack), self.stack)
                return ('raise', amount)
            elif randval == 2:
                return ('fold',0)
#********* BOT STUFF ******************************************************************************
    def get_random_check_action(self,p,table):
        print('rand check act table.min_bet ' + str(table.min_bet))
        if table.min_bet >= table.plyr_dict[p].stack:
            amount = table.plyr_dict[p].stack
        else:
            amount = randrange(table.min_bet, table.plyr_dict[p].stack)
        return ("check",0) if randrange(0,2) else ("bet",amount)
    # fold, call, or raise
    
    def get_random_call_action(self,p,table):
        true_cost = table.cost_to_play - table.plyr_dict[p].chips_this_round
        # working here, bug BUG
        choice = randrange(0,3)
        if choice == 0:
            return ("fold",0)
        elif choice == 1:
            return ("call", 0)
        else:
            # if not enough for legal raise
            if table.plyr_dict[p].stack-true_cost <= table.plyr_dict[p].stack:
                return ('all_in',0)
            else:
                amount = randrange(true_cost, table.plyr_dict[p].stack-true_cost)
            return ("raise", amount)
# 
#     
#     def callingStationAction(self):
#         return "call" if randrange(0,1) else "check"