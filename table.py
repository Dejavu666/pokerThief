# 1) instantiate table object
# 2) should only interface with table object through get_legal_action(), apply_action() (eventually)

# TO DO

# scenario where player has more than call amount but less than legal raise (am i covering the parameters in 'call' correctly?)

# note, NOT provably correct because input parameters are derived from state (dynamic not static)

# If player runs out of chips remove from seat_order/in_hand AFTER hand is resolved
# Test create_sidepots() with edge cases
# fix remainder chips in showdown()
# some tie_break lens are 3, is this correct?
# division is changing ints to floats in player.stack or table.pot


import player, deck, hands, helpers
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
        
    # RETURN VALUE --> [(1stsidepot,[listofplyrselig,...]),...(mainpot,[listofeligplyrs])]
    # Call if at least one sidepot ncsry, at least one player is all-in/in_hand
    def create_sidepots(self):
        players_in_hand = self.in_hand[:]
        pot_chips = self.pot
        pots_w_elig_players = []
        all_in = []
        for plyr in self.in_hand:
            if self.plyr_dict[plyr].stack == 0:# if player is all-in
                all_in.append((self.plyr_dict[plyr].begin_hand_chips, plyr))
        all_in.sort()
        # keep only unique pot values in all_in
        stacks = [x[0] for x in all_in if x[0] not in stacks]
        # all_in looks like: [(lowest_plyr.begin_hand_chips, lowest_plyr_str),...
        # just consume players that are all-in, only they need sidepots
        for stack in stacks:# for each player that needs a sidepot
            sidepot = 0
            for plyr in self.seat_order:# build the sidepot
                amount = min(self.plyr_dict[plyr].chips_in_pot, stack, pot_chips)
                sidepot += amount
                pot_chips -= amount
                if pot_chips == 0:# pot is consumed, current (last) sidepot is mainpot
                    pots_w_elig_players.append((sidepot, players_in_hand))
                    return pots_w_elig_players
            pots_w_elig_players.append((sidepot, players_in_hand))
            # remove players with equiv, least chips_in_pot from players_in_hand
            for player in self.in_hand:
                if self.plyr_dict[player].chips_in_pot == stack:
                    players_in_hand.remove(player)

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

    def raze(self, plyr, raise_amount):
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
        if self.round == 1 and self.min_bet == self.big_blind:
            if len(self.seat_order)==2:# only 2 players
                if player == self.seat_order[1]:
                    return True
            else:# more than 2 players
                if player == self.seat_order[2]:
                    return True
        return False

    def skip_all_in_plyr(self):
        for p in self.seat_order:
            if self.plyr_dict[p].stack == 0 and p in self.left_to_act:
                self.left_to_act.remove(p)
    
    def sidepots_check(self):
        for p in self.in_hand:
            if self.plyr_dict[p].stack == 0:
                return True
        return False
    
    def is_round_or_hand_over(self):
        if len(self.in_hand) == 1: # only one player
            self.reward_only_player()
            return 'sentinel'
        elif self.left_to_act == []: # no players left to act
            if self.round == 4: # last round
                if self.sidepots_check() == True:
                    pots_plyrs_list = self.create_sidepots()
                    for pot_plyrs_tup in pots_plyrs_list:
                        self.showdown(pot_plyrs_tup)
                        return 'sentinel'
                else:
                    self.showdown((self.pot,self.in_hand[:]))
                    return 'sentinel'
                self.clean_table_after_hand()
            else:
                assert(self.round in [1,2,3])
                self.advance_round()
    
    # Returns legal actions of next player left to act
    # should maybe skip all-in here
    def get_legal_actions(self):
        if self.is_round_or_hand_over() == 'sentinel':
            # hand over, next hand
            print('hand over')
        plyr = self.left_to_act[0]
        # Special BB options
        if self.is_bb_option_avail(plyr) == True:
            return ('bb_options',('raise',min(self.plyr_dict[plyr].stack,self.min_bet),self.plyr_dict[plyr].stack),\
            ('check'),('fold'), plyr)
        # Check Bet Fold, table is open
        elif self.plyr_dict[plyr].chips_this_round == self.cost_to_play: # if table is open, bet/check/fold
            return ('check_options',('bet',min(self.plyr_dict[plyr].stack,self.min_bet),self.plyr_dict[plyr].stack),\
            ('check'), ('fold'), plyr)
        # Call Raise Fold, table is bet
        else:
            return ('call_options',('call',min(self.plyr_dict[plyr].stack,self.cost_to_play-self.plyr_dict[plyr].chips_this_round)),\
             ('raise',min(self.plyr_dict[plyr].stack,self.min_bet),self.plyr_dict[plyr].stack-self.cost_to_play+self.plyr_dict[plyr].chips_this_round),\
             ('fold'), plyr)
        
    def apply_action(self, player, action, amount=0):
        player = self.left_to_act[0]
        if action == 'raise':
            self.raze(player, amount)
        elif action == 'check':
            self.check(player)
        elif action == 'fold':
            self.fold(player)
        elif action == 'bet':
            self.bet(player, amount)
        elif action == 'call':
            self.call(player, amount)

    def reward_only_player(self):
        assert(len(self.in_hand)==1)
        self.plyr_dict[self.in_hand[0]].stack += self.pot
        self.pot = 0
        self.clean_table_after_hand()

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
        
    # input looks like: (800, [player1,player2,...])
    # one pot (side or main) and the list of players who are eligible to win all chips
    def showdown(self, pot_and_player_tuple):
        # Get highest hand_rank
        players = pot_and_player_tuple[1]
        pot = pot_and_player_tuple[0]
        max_rank = 0
        top_plyrs = []
        for plyr in players:
            self.assign_hand_rank(plyr)
            if self.plyr_dict[plyr].hand_rank > max_rank:
                top_plyrs = [plyr]
                max_rank = self.plyr_dict[plyr].hand_rank
            elif self.plyr_dict[plyr].hand_rank == max_rank:
                top_plyrs.append(plyr)
        # if one winner: award player
        if len(top_plyrs) == 1:
            # reward top_plyrs[0]
            self.plyr_dict[top_plyrs[0]].stack += pot
            self.pot -= pot
        else: # tie needs to be broken for this one pot, working bug, what about remainder here?
            winners = hands.break_ties(top_plyrs, self)
            amount = pot // len(winners)
            for p in winners:
                self.plyr_dict[p].stack += amount

    # Assigns hand_rank and tie_break values to the Player object
    # Only makes sense to call when Player has 2 cards and table.community has 5
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

######### in gui dispatch these ########
# deal_hole_cards()
# post_blinds()
# skip_all_in_plyr()
# if left2act: get_legal_actions(), present them, apply_action()
# if is_round_or_hand_over() returns 'sentinel': hand is over

############ TESTS #################
if __name__=='__main__':
    table = Table(2,1000,20)
    for p in table.seat_order:
        table.plyr_dict[p].human = 1
    while(1):
        table.deal_hole_cards()
        table.post_blinds()
        sentinel = 1
        while(sentinel):
            table.skip_all_in_plyr()
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
