# table.py

# Notes
# generalization - a raise is the same as a bet, functionally. Except that the first is a bet, proceeding are raises
# some table attributes are mutable some are immutable, some ints some lists mainly


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
        {'player'+str(i+1) : player.Player(stack_size=num_chips) for i in range(num_players)}
        
        self.plyr_dict['player1'].human = 1
        
        # seat_order[0] is dealer, seat_order[1] is SB
        # seat_order changes to reflect the dealer button being passed
        self.seat_order = [player for player in self.plyr_dict.keys()]
        shuffle(self.seat_order)
        
        self.round = 1
        self.min_bet = big_blind
        # Players in order of action, first to act is first element
        # is set during post_blinds(), first elem popped to back after each hand
        self.left_to_act = []
        # Players still in the current hand, but not necessarily left to act in the round
        self.in_hand = []
        self.cost_to_play = 0
        
    # ?maybe account for division of odd numbers / split chips?
    def post_blinds(self):
        if len(self.seat_order) == 2:
            # helper function, blind order is different for 2players
            self.post_blinds_2player()
            return
        else:
            # dealer+1 enough chips for SB
            if self.plyr_dict[self.seat_order[1]].stack_size >= self.big_blind/2:
                self.plyr_dict[self.seat_order[1]].contribute_chips(self.big_blind/2)
                self.pot += self.big_blind/2
            else: # dealer+1 not enough chips for SB
                self.pot += self.plyr_dict[self.seat_order[1]].stack_size
                self.plyr_dict[self.seat_order[1]].contribute_chips(\
                    self.plyr_dict[self.seat_order[1]].stack_size)
            # dealer+2 enough chips for BB
            if self.plyr_dict[self.seat_order[2]].stack_size >= self.big_blind:
                self.plyr_dict[self.seat_order[2]].contribute_chips(self.big_blind)
                self.pot += self.big_blind
            else: # dealer+2 not enough chips for BB
                self.pot += self.plyr_dict[self.seat_order[2]].stack_size
                self.plyr_dict[self.seat_order[2]].contribute_chips(\
                    self.plyr_dict[self.seat_order[2]].stack_size)
            # Set order of action, players in hand, cost_to_play
            if len(self.seat_order) == 3:
                self.left_to_act = self.seat_order[:]
            else:
                self.left_to_act = self.seat_order[3:] + self.seat_order[:3]
            self.in_hand = self.left_to_act[:]
            self.cost_to_play = self.big_blind
        
    # post_blinds for only 2 players
    def post_blinds_2player(self):
        # dealer enough for SB
        if self.plyr_dict[self.seat_order[0]].stack_size >= self.big_blind/2:
            self.plyr_dict[self.seat_order[0]].contribute_chips(self.big_blind/2)
            self.pot += self.big_blind/2
        else: # dealer not enough for SB
            self.pot += self.plyr_dict[self.seat_order[0]].stack_size
            self.plyr_dict[self.seat_order[0]].contribute_chips( \
                self.plyr_dict[self.seat_order[0]].stack_size)
        # dealer+1 enough for BB
        if self.plyr_dict[self.seat_order[1]].stack_size >= self.big_blind:
            self.plyr_dict[self.seat_order[1]].contribute_chips(self.big_blind)
            self.pot += self.big_blind
        else: # dealer+1 not enough for BB
            self.pot += self.plyr_dict[self.seat_order[1]].stack_size
            self.plyr_dict[self.seat_order[1]].contribute_chips( \
                self.plyr_dict[self.seat_order[1]].stack_size)
        # Set order of action, players in hand, cost_to_play
        self.left_to_act = self.seat_order[:]
        self.in_hand = self.left_to_act[:]
        self.cost_to_play = self.big_blind
        
    # At end of hand, if a player is all-in, run this
    # For each player in_hand and 'all-in', in order of ascending start_stack
    # Create a sidepot by contributing from each other player: max(player.start_stack, other_player.chips_in_pot)
    # The player or players whose equivalent start_stack values were used to create this sidepot...
    # are eligible for this pot and no further created pots
    # When all chips from table.pot are consumed, the current pot that finished consuming them is the 'main' pot
    # All remaining players are eligible for this and all previous pots
    # RETURN VALUE --> ([sidepot1,sidepot2,...,mainpot],[[players_elig_sidepot1],[players_elig_sidepot2],...,
    # [players_elig_mainpot]]
    # Call if at least one sidepot ncsry, at least one player is all-in/in_hand
    def create_sidepots(self):
        players_in_hand = self.in_hand[:]
        pot_chips = self.pot
        pots_w_elig_plyrs = []
        all_in = []
        for plyr in self.seat_order:
            if plyr in self.in_hand and self.plyr_dict[plyr].stack_size == 0:# if player is all-in
                all_in.append((self.plyr_dict[plyr].start_stack, plyr))
        all_in.sort()
        # all_in looks like: [(lowest_plyr.start_stack, lowest_plyr_str),...
        # just consume players that are all-in, only they need sidepots
        all_in_cpy = all_in[:]
        for stack_plyr_tup in all_in:
            sidepot = 0
            for plyr in self.seat_order:
                amount = min(self.plyr_dict[plyr].chips_in_pot, pot_chips)
                sidepot += amount
                pot_chips -= amount
                if pot_chips == 0:# pot is consumed, current sidepot is mainpot
                    pots_w_elig_players.append((sidepot, [players_in_hand]))
                    return pots_w_elig_players
            # remove players with equiv, least chips_in_pot from players_in_hand
            low_stack = all_in_copy[0][0]
            for player in self.in_hand:
                if self.plyr_dict[player].chips_in_pot == low_stack:
                    players_in_hand.remove(player)
                    all_in_copy = all_in_copy[1:] # modify object while looping on it

    def clean_table(self):
        self.pot = 0
        self.com_cards = []
        self.min_bet = self.big_blind
        self.round = 1
        self.left_to_act = []
        self.in_hand = []
        self.cost_to_play = 0
        for plyr in self.seat_order:
            self.plyr_dict[plyr].clean_player()

    # Starting from the plyr_str's index+1 in seat_order, if player is in_hand but not in left2act,
    # append player to left2act
    def repop_left_to_act(self, plyr_str):
        self.left_to_act = []
        players = self.seat_order[self.seat_order.index(plyr_str)+1:] + self.seat_order[:self.seat_order.index(plyr_str)]
        for plyr in players:
            if plyr in self.in_hand:
                self.left_to_act.append(plyr)

    def bet(self, plyr, amount):
        assert(amount >= self.min_bet)
        assert(amount <= self.plyr_dict[plyr].stack_size)
        self.plyr_dict[plyr].contribute_chips(amount)
        self.cost_to_play += amount
        self.min_bet = amount
        repop_left_to_act(plyr)
        
    
    def check(self, plyr):
        self.left_to_act.remove(plyr)
    
    def call(self, plyr, amount):
        assert(self.cost_to_play - self.plyr_dict[plyr].chips_this_round == amount)
        assert(amount <= self.plyr_dict[plyr].stack_size)
        self.pot += amount
        self.plyr_dict[plyr].contribute_chips(amount)
        self.left_to_act.remove(plyr)

    # raise/raze prevent name collision/reuse with raise python keyword
    def raze(self, plyr, amount):
        assert(amount >= self.min_bet)
        assert(amount <= self.plyr_dict[plyr].stack_size)
        self.plyr_dict[plyr].contribute_chips(amount)
        self.pot += amount
        self.cost_to_play += amount
        repop_left_to_act(plyr)
    
    def fold(self, plyr):
        self.left_to_act.remove(plyr)
        self.in_hand.remove(plyr)

    # Play-Hand Looping Function
    # Gets player action and steps through table states
    # Until only 1 player left in_hand or resolved with showdown function
    def play_hand_loop(self):
        sentinel = 1
        while(sentinel):
            plyr_str = self.left_to_act[0]
            # Prompt first player in left_to_act
            # bet/check/fold if table.cost_to_play == playerN.chips_this_round
            # call/raze/fold if table.cost_to_play > playerN.chips_this_round
            if self.plyr_dict[plyr_str].human == 1:# USER INPUT goes here
                act = input("test input without validation, input C for call c for check, b, r, f")
                amount = input("enter amount, if ncsry")
                action = (act, amount)
            else:#gethotbotaction , pass relevant table info, returns tuple like ('raise',100) or ('fold',0)
                action = self.plyr_dict[plyr_str].bot_action(self.cost_to_play, self.big_blind, self.min_bet)
            # apply action
            if action[0] == 'b':
                bet(plyr_str, action[1])
            elif action[0] == 'r':
                raze(plyr_str, action[1])
            elif action[0] == 'C':
                call(plyr_str, action[1])
            elif action[0] == 'f':
                fold(plyr_str)
            elif action[0] == 'c':
                self.check(plyr_str)
                
            # DEBUG
            print('left2act == ',self.left_to_act)
            # DEBUG
            # Check for end of round/hand
            if len(self.in_hand) == 1:
                # reward remaining player
                sentinel = 0
            elif self.left_to_act == [] and self.round == 4:
                # showdown()
                sentinel = 0
            # otherwise, advance round
            elif self.left_to_act == []:
                self.round += 1
                # reset players chips this round, BUT NOT chips_in_pot
                for plyr in self.seat_order:
                    self.plyr_dict[plyr].chips_this_round = 0
                self.left_to_act = self.seat_order[1:] + self.seat_order[:1]
                


####### TEST #######
# dependencies = num_players, num_chips, big_blind
# test_params = [[2,10,20],[3,100,20],[3,10,20]]
# for param in test_params:
#     table = Table(param[0],param[1],param[2])
# 
#     print(table.plyr_dict)
#     print(table.seat_order)
#     table.post_blinds()
#     for k in table.plyr_dict.keys():
#         print(table.plyr_dict[k].stack_size)
#     print(table.pot)

# TESTS for table.create_sidepots
# create mock data with AT LEAST one player all-in/in-hand

table = Table(4,200,20)
# set all players to human
for player in table.seat_order:
    table.plyr_dict[player].human = 1
table.post_blinds()
table.play_hand_loop()