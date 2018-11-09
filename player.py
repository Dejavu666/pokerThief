from random import randrange
class Player():
    def __init__(self, stack=0):
        self.stack = stack
        self.hand = []
        self.chips_this_round = 0
        self.begin_hand_chips = 0
        self.chips_in_pot = 0
        self.human = 0
        self.hand_rank = 0
        self.tie_break = []
        
        # of 'random', 'calling_station', 'tight_aggressive', 'loose_aggressive', 'stop_n_go'
        self.bot_profile = 'random'
        
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
    
#********* BOT STUFF ******************************************************************************

    def get_random_bot_action(self, p, table):
        if table.plyr_dict[p].stack == 0:
            return ('check',0)
        # bot big blind special option actions
        elif len(table.seat_order) == 2 and table.round == 1 and p == table.seat_order[1] and table.cost_to_play == table.plyr_dict[p].chips_this_round:
            # 2 plyr bb options, check, bet
            choice = randrange(0,2)
            if choice:
                return ('check',0)
            else:
                # if not enough for legal raise
                if table.min_bet >= table.plyr_dict[p].stack:
                    return ('all_in', 0)
                else: # enough for legal raise
                    return ('raise', randrange(table.min_bet, table.plyr_dict[p].stack+1))
        # bug here, can't reference seat_order[2] unless it exists
        if len(table.seat_order) > 2 and table.round == 1 and table.cost_to_play == table.plyr_dict[p].chips_this_round:
            if table.seat_order[2] == p:
                # more than 2 plyr bb options, check, bet
                choice = randrange(0,2)
                if choice:
                    return ('check',0)
                else:
                    # if not enough for legal raise
                    if table.min_bet >= table.plyr_dict[p].stack:
                        return ('all_in', 0)
                    else: # enough for legal raise
                        return ('raise', randrange(table.min_bet, table.plyr_dict[p].stack+1))
        if table.cost_to_play == table.plyr_dict[p].chips_this_round:
            return self.get_random_check_action(p, table)
        else:
            return self.get_random_call_action(p, table)

    def get_random_check_action(self,p,table):
        print('rand check act table.min_bet ' + str(table.min_bet))
        if table.min_bet >= table.plyr_dict[p].stack:
            amount = table.plyr_dict[p].stack
        else:
            amount = randrange(table.min_bet, table.plyr_dict[p].stack)
        return ("check",0) if randrange(0,2) else ("bet",amount)
    
    def get_random_call_action(self,p,table):
        true_cost = table.cost_to_play - table.plyr_dict[p].chips_this_round
        choice = randrange(0,3)
        if choice == 0:
            return ("fold",0)
        elif choice == 1:
            return ("call", 0)
        else:
            # if not enough for legal raise
            if table.plyr_dict[p].stack <= (2 * true_cost):
                return ('all_in',0)
            # working here, bug BUG
            # what about not enough for even legal call?, see error at top of gui page
            else:
                amount = randrange(table.min_bet, table.plyr_dict[p].stack-true_cost+1)
            return ("raise", amount)
# 
#     
#     def callingStationAction(self):
#         return "call" if randrange(0,1) else "check"