
# TO DO

# Bug with continual raising with odd amounts of chips, where sb becomes odd

# Need to separate 'public' and 'private' methods of Table class
# gui should only call get_actions(), apply_action(), 

# divide by zero error?

# scenario where player has more than call amount but less than legal raise (am i covering the parameters in 'call' correctly?)


# If player runs out of chips remove from seat_order/in_hand AFTER hand is resolved
# division is changing ints to floats in player.stack or table.pot


import player, deck, hands
from random import shuffle

class Table():
    def __init__(self, num_players, num_chips, big_blind):
        self.num_players = num_players
        self.num_chips = num_chips
        self.big_blind = big_blind
        
        self.deck = deck.Deck()
        self.com_cards = []
        self.pot = 0
        
        self.plyr_dict = \
        {'player'+str(i+1) : player.Player(stack=num_chips) for i in range(num_players)}
        
        self.plyr_dict['player1'].human = 1
        
        self.seat_order = [player for player in self.plyr_dict.keys()]
        shuffle(self.seat_order)
        
        self.round = 1
        self.min_bet = big_blind
        self.left_to_act = []
        self.in_hand = []
        self.cost_to_play = 0
        
        self.deal_hole_cards()
        self.post_blinds()
        
    def deal_hole_cards(self):
        for p in self.seat_order:
            self.plyr_dict[p].draw_card(self.deck.draw_card())
        for p in self.seat_order:
            self.plyr_dict[p].draw_card(self.deck.draw_card())
    
    # ?maybe account for division of odd numbers / split chips?
    def post_blinds(self):
        if len(self.seat_order) == 2:
            # helper function, blind order is different for 2players
            self.post_blinds_2player()
        else:
            # dealer+1 enough chips for SB
            if self.plyr_dict[self.seat_order[1]].stack >= self.big_blind//2:
                self.plyr_dict[self.seat_order[1]].contribute_chips(self.big_blind//2)
                self.pot += self.big_blind//2
            else: # dealer+1 not enough chips for SB
                self.pot += self.plyr_dict[self.seat_order[1]].stack
                self.plyr_dict[self.seat_order[1]].contribute_chips(\
                    self.plyr_dict[self.seat_order[1]].stack)
            # dealer+2 enough chips for BB
            if self.plyr_dict[self.seat_order[2]].stack >= self.big_blind:
                self.plyr_dict[self.seat_order[2]].contribute_chips(self.big_blind)
                self.pot += self.big_blind
            else: # dealer+2 not enough chips for BB
                self.pot += self.plyr_dict[self.seat_order[2]].stack
                self.plyr_dict[self.seat_order[2]].contribute_chips(\
                    self.plyr_dict[self.seat_order[2]].stack)
            # Set order of action, players in hand, cost_to_play
            if len(self.seat_order) == 3:
                self.left_to_act = self.seat_order[:]
            else:
                self.left_to_act = self.seat_order[3:] + self.seat_order[:3]
            self.in_hand = self.seat_order[:]
            self.cost_to_play = self.big_blind
        
    # post_blinds for only 2 players, helper func called by post_blinds()
    def post_blinds_2player(self):
        # dealer enough for SB
        if self.plyr_dict[self.seat_order[0]].stack >= self.big_blind//2:
            self.plyr_dict[self.seat_order[0]].contribute_chips(self.big_blind//2)
            self.pot += self.big_blind//2
        else: # dealer not enough for SB
            self.pot += self.plyr_dict[self.seat_order[0]].stack
            self.plyr_dict[self.seat_order[0]].contribute_chips( \
                self.plyr_dict[self.seat_order[0]].stack)
        # dealer+1 enough for BB
        if self.plyr_dict[self.seat_order[1]].stack >= self.big_blind:
            self.plyr_dict[self.seat_order[1]].contribute_chips(self.big_blind)
            self.pot += self.big_blind
        else: # dealer+1 not enough for BB
            self.pot += self.plyr_dict[self.seat_order[1]].stack
            self.plyr_dict[self.seat_order[1]].contribute_chips( \
                self.plyr_dict[self.seat_order[1]].stack)
        # Set order of action, players in hand, cost_to_play
        self.left_to_act = self.seat_order[:]
        self.in_hand = self.seat_order[:]
        self.cost_to_play = self.big_blind
        
    # Creates input for showdown() from table state at end of hand
    # RETURN VALUE --> [(1stsidepot,[listofplyrselig,...]),...(mainpot,[listofeligplyrs])]
    def create_pots(self):
        all_in = [p for p in self.in_hand if self.plyr_dict[p].stack == 0]
        if len(all_in) == 0:
            return [(self.pot, self.in_hand[:])]
        small_stacks = sorted(set([self.plyr_dict[p].begin_hand_chips for p in all_in]))
        pots_plyrs = []
        all_plyrs = self.in_hand[:]
        for n in small_stacks:
            pot = 0
            plyrs = self.all_plyrs[:]
            for p in plyrs:
                amount = min(n, self.pot)
                pot += amount
                self.pot -= amount
                if self.pot == 0:
                    pots_plyrs.append((pot, plyrs))
                    return pots_plyrs
            pots_plyrs.append((pot, plyrs))
            for p in self.in_hand[:]:
                if self.plyr_dict[p].begin_hand_chips == n:
                    # BUG here destructing in_hand which is used later
                    all_plyrs.remove(p)
        pots_plyrs.append((self.pot, all_plyrs))
        return pots_plyrs

    def clean_table_after_hand(self):
        self.pot = 0
        self.com_cards = []
        self.min_bet = self.big_blind
        self.round = 1
        self.left_to_act = []
        self.in_hand = []
        self.cost_to_play = 0
        for plyr in self.seat_order:
            self.plyr_dict[plyr].clean_player_after_hand()

    def repop_left_to_act(self, plyr_str):
        self.left_to_act = []
        players = self.seat_order[self.seat_order.index(plyr_str)+1:] + self.seat_order[:self.seat_order.index(plyr_str)]
        for plyr in players:
            if plyr in self.in_hand:
                self.left_to_act.append(plyr)

    def bet(self, plyr, amount):
        assert(amount >= self.min_bet)
        assert(amount <= self.plyr_dict[plyr].stack)
        self.pot += amount
        self.plyr_dict[plyr].contribute_chips(amount)
        self.cost_to_play = amount
        self.min_bet = amount
        self.repop_left_to_act(plyr)
        
    def check(self, plyr):
        self.left_to_act.remove(plyr)
    
    def call(self, plyr, amount):
        assert(self.cost_to_play - self.plyr_dict[plyr].chips_this_round == amount)
        assert(amount <= self.plyr_dict[plyr].stack)
        self.pot += amount
        self.plyr_dict[plyr].contribute_chips(amount)
        self.left_to_act.remove(plyr)

    def _raise(self, plyr, raise_amount):
        assert(raise_amount >= self.min_bet)
        true_cost = self.cost_to_play-self.plyr_dict[plyr].chips_this_round
        assert(raise_amount + true_cost <= self.plyr_dict[plyr].stack)
        self.pot += raise_amount+true_cost
        self.plyr_dict[plyr].contribute_chips(raise_amount+true_cost)
        self.cost_to_play += raise_amount
        self.min_bet = raise_amount
        self.repop_left_to_act(plyr)
    
    def fold(self, plyr):
        self.left_to_act.remove(plyr)
        self.in_hand.remove(plyr)

    def is_bb_option_avail(self, player):
        if self.round == 1 and self.cost_to_play == self.big_blind:
            if len(self.seat_order)==2:# only 2 players
                if player == self.seat_order[1]:
                    return True
            else:# more than 2 players
                if player == self.seat_order[2]:
                    return True
        return False
                
    def is_round_or_hand_over(self):
        if len(self.in_hand) == 1: # only one player
            dict = self.reward(self.pot, self.in_hand[0])
            return ['hand over', dict]
        elif self.left_to_act == []: # no players left to act
            if self.round == 4: # last round
                pots_plyrs = self.create_pots()
                dict = self.showdown(pots_plyrs)
                return ['hand over', dict]
            else:
                assert(self.round in [1,2,3])
                self.advance_round()
    
    # Returns legal actions of next player left to act
    # should maybe skip all-in here
    def get_actions(self):
        p = self.left_to_act[0]
        if self.plyr_dict[p].stack == 0:
            return ('all-in',('check'))
        # Special BB options
        if self.is_bb_option_avail(p) == True:
            return ('bb_options',('raise',min(self.plyr_dict[p].stack,self.min_bet),self.plyr_dict[p].stack),\
            ('check'),('fold'), p)
        # Check Bet Fold, table is open
        elif self.plyr_dict[p].chips_this_round == self.cost_to_play: # if table is open, bet/check/fold
            return ('check_options',('bet',min(self.plyr_dict[p].stack,self.min_bet),self.plyr_dict[p].stack),\
            ('check'), ('fold'), p)
        # Call Raise Fold, table is bet
        else:
            return ('call_options',('call',min(self.plyr_dict[p].stack,self.cost_to_play-self.plyr_dict[p].chips_this_round)),\
             ('raise',min(self.plyr_dict[p].stack,self.min_bet),self.plyr_dict[p].stack-self.cost_to_play+self.plyr_dict[p].chips_this_round),\
             ('fold'), p)
        
    def apply_action(self, plyr, action, amount=0):
        if action == 'raise':
            self._raise(plyr, amount)
        elif action == 'check':
            self.check(plyr)
        elif action == 'fold':
            self.fold(plyr)
        elif action == 'bet':
            self.bet(plyr, amount)
        elif action == 'call':
            self.call(plyr, amount)
        maybe_winner_info = self.is_round_or_hand_over()
        if maybe_winner_info:
            return maybe_winner_info

    def advance_round(self):
        if self.round == 1:# preflop to flop, deal 3 com_cards
            self.com_cards.append(self.deck.draw_card())
            self.com_cards.append(self.deck.draw_card())
            self.com_cards.append(self.deck.draw_card())
        elif self.round == 2:# flop to turn, deal 1 com_card
            self.com_cards.append(self.deck.draw_card())
        elif self.round == 3:# turn to river, deal 1 com_card
            self.com_cards.append(self.deck.draw_card())
        # advance round
        self.round += 1
        # reset cost_to_play, min_bet
        self.cost_to_play = 0
        self.min_bet = self.big_blind
        # reset players chips this round, BUT NOT chips_in_pot
        for plyr in self.seat_order:
            self.plyr_dict[plyr].chips_this_round = 0
            # Reset left_to_act
            if plyr in self.in_hand:
                self.left_to_act.append(plyr)

    def move_button_remove_chipless_players(self):
        new_seats = []
        for plyr in self.seat_order[1:] + self.seat_order[0:1]:
            if self.plyr_dict[plyr].stack > 0:
                new_seats.append(plyr)
        self.seat_order = new_seats[:]
        
    # called by showdown(), break ties among same hand_rank
    def break_ties(self, plyrs):
        while(True):
            if self.plyr_dict[plyrs[0]].tie_break == []:
                return plyrs
            max = self.plyr_dict[plyrs[0]].tie_break[0]
            for p in plyrs[:]:
                if self.plyr_dict[p].tie_break[0] < max:
                    if p in plyrs:
                        plyrs.remove(p)
                self.plyr_dict[p].tie_break = self.plyr_dict[p].tie_break[1:]
            if len(plyrs) == 1:
                return plyrs
    
    def reward(self, pot, plyrs):
        winner_info = dict((plyr, 0) for plyr in plyrs)
        remainder = pot % len(plyrs)
        pot -= remainder
        for p in plyrs:
            winner_info[p] += (pot//len(plyrs))
            self.plyr_dict[p].stack += (pot//len(plyrs))
        while(remainder):
            for p in self.in_hand[1:]+[self.in_hand[0]]:
                if remainder > 0:
                    self.plyr_dict[p].stack += 1
                    winner_info[p] += 1
                    remainder -= 1
        return winner_info
    
    # Takes the 'pots_plyrs' output from create_pots()
    # Ends the hand, rewards players
    # Should prompt for next_hand with this
    def showdown(self, pots_plyrs_tup):
        main_dict = {}
        for p in self.in_hand:
            self.assign_hand_rank(p)
            print(self.plyr_dict[p].hand_rank)
        for pot_plyr in pots_plyrs_tup:
            high = max([self.plyr_dict[p].hand_rank for p in self.in_hand])
            pot = pot_plyr[0]
            plyrs = pot_plyr[1]
            dict = self.reward(pot, self.break_ties([p for p in plyrs if self.plyr_dict[p].hand_rank == high]))
            for k in dict.keys():
                if k not in main_dict.keys():
                    main_dict[k] = dict[k]
                else:
                    main_dict[k] += dict[k]
        return main_dict
        

    
    # Assigns hand_rank and tie_break values to the Player object
    def assign_hand_rank(self, plyr):
        hand = self.plyr_dict[plyr].hand + self.com_cards
        handranks_w_ace_as_one = []
        for card in hand:
            if card[0] == 14:
                handranks_w_ace_as_one.append(1)
                handranks_w_ace_as_one.append(14)
            else:
                handranks_w_ace_as_one.append(card[0])
        handranks_w_ace_as_one.sort(reverse=True)
        if hands.straight_flush_finder(hand):
            self.plyr_dict[plyr].hand_rank = 9
            self.plyr_dict[plyr].tie_break = hands.straight_flush_finder(hand)
        elif hands.four_of_a_kind_finder(hand):
            self.plyr_dict[plyr].hand_rank = 8
            self.plyr_dict[plyr].tie_break = hands.four_of_a_kind_finder(hand)
        elif hands.fullhouse_finder(hand):
            self.plyr_dict[plyr].hand_rank = 7
            self.plyr_dict[plyr].tie_break = hands.fullhouse_finder(hand)
        elif hands.flush_finder(hand):
            self.plyr_dict[plyr].hand_rank = 6
            self.plyr_dict[plyr].tie_break = hands.flush_finder(hand)
        elif hands.straight_finder(handranks_w_ace_as_one):
            self.plyr_dict[plyr].hand_rank = 5
            self.plyr_dict[plyr].tie_break = hands.straight_finder(handranks_w_ace_as_one)
        elif hands.three_of_a_kind_finder(hand):
            self.plyr_dict[plyr].hand_rank = 4
            self.plyr_dict[plyr].tie_break = hands.three_of_a_kind_finder(hand)
        elif hands.two_pair_finder(hand):
            self.plyr_dict[plyr].hand_rank = 3
            self.plyr_dict[plyr].tie_break = hands.two_pair_finder(hand)
        elif hands.one_pair_finder(hand):
            self.plyr_dict[plyr].hand_rank = 2
            self.plyr_dict[plyr].tie_break = hands.one_pair_finder(hand)
        else:
            self.plyr_dict[plyr].hand_rank = 1
            self.plyr_dict[plyr].tie_break = hands.highcard_finder(hand)

#     def next_hand(self)

############ TESTS #################
if __name__=='__main__':
    table = Table(2,1000,20)
    for p in table.seat_order:
        table.plyr_dict[p].human = 1
    while(1):
        sentinel = 1
        while(sentinel):
            #table.skip_all_in_plyr()
            if len(table.left_to_act) > 0:
                plyr = table.left_to_act[0]
                print(table.get_legal_actions())
                action = input('input action bet, check, fold, call, raise ')
                amount = int(input('optional input amount '))
                table.apply_action(plyr,action,amount)
            if table.is_round_or_hand_over() == 'sentinel':
                sentinel = 0
    table.move_button_remove_chipless_players()
# next_hand()
