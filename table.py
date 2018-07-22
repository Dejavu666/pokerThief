# Work in progress, many shims until gui for testing

# Run with "python table.py"

# Table class instance holds dictionary with keys=='player_name_string' and value==Player_class_instance
# Table holds community objects and context of current play such as community cards and legal bet amounts
# Player instances hold attributes relevant to themselves like hole cards and stack

# Table needs num_players, num_chips, big_blind on init
# plyr_dict is populated
# call post_blinds()
# call play_hand_loop() to continue play until hand is resolved
# either reward player OR one or more showdowns with optional create_sidepots
# move button to next player with stack
# clean, remove players with no stack, prompt for optional next hand

# TO DO 

# If player runs out of chips remove from seat_order/in_hand AFTER hand is resolved

# take away illegal options, raise/bet with only enough chips to call
# Change first call of post_blinds() to inside play_hand_loop(), remove from showdown/resolution, maybe?
# Test create_sidepots() with edge cases
# fix remainder chips in showdown()
# some tie_break lens are 3, is this correct?
# division is changing ints to floats in player.stack or table.pot

# Could use entire decision path of winning hand as positively labeled data point
# Use losing paths as negatively labeled data points

# Should be provably correct with input validation
# Current command line parameter 'hints' become input validation
# (only range of hints is presented as possible input through sliders/buttons, no typed/entered input)
# This means the range of input is known and testable

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
            return
        else:
            # dealer+1 enough chips for SB
            if self.plyr_dict[self.seat_order[1]].stack >= self.big_blind/2:
                self.plyr_dict[self.seat_order[1]].contribute_chips(self.big_blind/2)
                self.pot += self.big_blind/2
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
        
    # post_blinds for only 2 players
    def post_blinds_2player(self):
        # dealer enough for SB
        if self.plyr_dict[self.seat_order[0]].stack >= self.big_blind/2:
            self.plyr_dict[self.seat_order[0]].contribute_chips(self.big_blind/2)
            self.pot += self.big_blind/2
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
        
    # At end of hand, if a player is all-in, run this
    # For each player in_hand and 'all-in', in order of ascending begin_hand_chips
    # Create a sidepot by contributing from each other player: max(player.begin_hand_chips, other_player.chips_in_pot)
    # The player or players whose equivalent begin_hand_chips values were used to create this sidepot...
    # are eligible for this pot and no further created pots
    # When all chips from table.pot are consumed, the current pot that finished consuming them is the 'main' pot
    # All remaining players are eligible for this and all previous pots
    # RETURN VALUE --> ([sidepot1,sidepot2,...,mainpot],[[players_elig_sidepot1],[players_elig_sidepot2],...,
    # [players_elig_mainpot]]
    # Call if at least one sidepot ncsry, at least one player is all-in/in_hand
    def create_sidepots(self):
        players_in_hand = self.in_hand[:]
        pot_chips = self.pot
        pots_w_elig_players = []
        all_in = []
        for plyr in self.seat_order:
            if plyr in self.in_hand and self.plyr_dict[plyr].stack == 0:# if player is all-in
                all_in.append((self.plyr_dict[plyr].begin_hand_chips, plyr))
        all_in.sort()
        # all_in looks like: [(lowest_plyr.begin_hand_chips, lowest_plyr_str),...
        # just consume players that are all-in, only they need sidepots
        all_in_cpy = all_in[:]
        for stack_plyr_tup in all_in:
            sidepot = 0
            for plyr in self.seat_order:
                amount = min(self.plyr_dict[plyr].chips_in_pot, pot_chips)
                sidepot += amount
                pot_chips -= amount
                if pot_chips == 0:# pot is consumed, current sidepot is mainpot
                    pots_w_elig_players.append((sidepot, players_in_hand))
                    return pots_w_elig_players
            # remove players with equiv, least chips_in_pot from players_in_hand
            low_stack = all_in_copy[0][0]
            for player in self.in_hand:
                if self.plyr_dict[player].chips_in_pot == low_stack:
                    players_in_hand.remove(player)
                    all_in_copy = all_in_copy[1:] # modify object while looping on it

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

    # raise/raze prevent name collision/reuse with raise python keyword
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

    # Play-Hand Looping Function
    def play_hand_loop(self):
################# SOME TESTS #################
        players_chips = 0
        for p in self.seat_order:
            players_chips += self.plyr_dict[p].stack
        begin_chips = self.num_chips*self.num_players
        # Check that chips are always subtracted and added at the same rate (total number of chips is same)
        # Does not ncsrly mean that they are added and subtracted appropriately, only correctly
        # For example: a raise may subtract an amount equal to the amount added to pot, but the raise amounts
        # COULD be illegal (shouldnt be as of writing this)
        assert(self.pot+players_chips==begin_chips)
################# END TESTS ############
################# BEGIN LOOP #################
        sentinel = 1
        new_hand = 1
        while(sentinel):
            if new_hand:
                self.deal_hole_cards()
                self.post_blinds()
                new_hand = 0
            plyr_str = self.left_to_act[0]
            # Skip player input if player is all-in (player 'checks')
            if self.plyr_dict[plyr_str].stack == 0:
                act = 'c'
            # Otherwise, prompt the player for input
            elif self.plyr_dict[plyr_str].human == 1:# USER INPUT goes here
                #### Print Console Info, temp until GUI
                print(plyr_str)
                print('players left to act this round == ', self.left_to_act)
                print('players still in the hand == ' , self.in_hand)
                print('round is ', self.round)
                print('community cards == ', self.com_cards)
                print('your hole cards == ', self.plyr_dict[plyr_str].hand)
                print('your stack == ', self.plyr_dict[plyr_str].stack)
                print('your chips this round == ', self.plyr_dict[plyr_str].chips_this_round)
                print('your chips in the pot == ', self.plyr_dict[plyr_str].chips_in_pot)
                print('the pot == ', self.pot)
                print('cost_to_play == ', self.cost_to_play)
                print('cost to you is ', self.cost_to_play - self.plyr_dict[plyr_str].chips_this_round)
################ Begin Input Logic, constraints become input validation in GUI
                # IF ONLY 2 PLAYERS:
                if len(self.seat_order) == 2:
                    # if round1 and plyr is D+1 and cost_to_play has not changed:
                    if self.round == 1 and plyr_str == self.seat_order[1] and self.cost_to_play == self.big_blind:
                        # present bb option check/raise/fold
                        act = input('c for check, r for raise, f for fold')
                        if act == 'r':
                            amount = input('raise how much? Between '+str(min(self.plyr_dict[plyr_str].stack,self.min_bet))+' and '+str(self.plyr_dict[plyr_str].stack-self.cost_to_play+self.plyr_dict[plyr_str].chips_this_round))
                    # elif table not open:
                    elif self.cost_to_play-self.plyr_dict[plyr_str].chips_this_round > 0:
                        # present call/raise/fold
                        act = input('c for call, r for raise, f for fold')
                        if act == 'c':
                            act = 'C'
                            amount = min(self.plyr_dict[plyr_str].stack, self.cost_to_play-self.plyr_dict[plyr_str].chips_this_round)
                        elif act == 'r':
                            amount = input('How much to raise? Between '+str(min(self.plyr_dict[plyr_str].stack, self.min_bet))+' and '+str(self.plyr_dict[plyr_str].stack-self.cost_to_play+self.plyr_dict[plyr_str].chips_this_round))
                    # elif table is open:
                    elif self.cost_to_play-self.plyr_dict[plyr_str].chips_this_round == 0:
                        # present bet/check/fold
                        act = input('b for bet, c for check, f for fold')
                        if act == 'b':
                            amount = input('How much to bet? Between '+str(min(self.plyr_dict[plyr_str].stack,self.min_bet))+' and '+str(self.plyr_dict[plyr_str].stack))
################## else (MORE THAN 2 PLAYER):
                elif len(self.seat_order) > 2:
                    # if round1 and plyr is D+2 and cost_to_play has not changed:
                    if self.round == 1 and plyr_str == self.seat_order[2] and self.cost_to_play == self.big_blind:
                        # present bb option check/raise/fold
                        act = input('c for check, r for raise, f for fold')
                        if act == 'r':
                            amount = input('How much to raise? Between '+str(min(self.plyr_dict[plyr_str].stack,self.min_bet))+' and '+str(self.plyr_dict[plyr_str].stack-self.cost_to_play+self.plyr_dict[plyr_str].chips_this_round))
                    # elif table not open:
                    elif self.cost_to_play - self.plyr_dict[plyr_str].chips_this_round > 0:
                        # present call/raise/fold
                        act = input('c for call, r for raise, f for fold')
                        if act == 'c':
                            act = 'C'
                            amount = min(self.plyr_dict[plyr_str].stack,self.cost_to_play-self.plyr_dict[plyr_str].chips_this_round)
                        elif act == 'r':
                            amount = input('How much to raise? Between '+str(min(self.plyr_dict[plyr_str].stack,self.min_bet))+' and '+str(self.plyr_dict[plyr_str].stack-self.cost_to_play+self.plyr_dict[plyr_str].chips_this_round))
                    # elif table open:
                    elif self.cost_to_play-self.plyr_dict[plyr_str].chips_this_round == 0:
                        # present bet/check/fold
                        act = input('b for bet, c for check, f for fold')
                        if act == 'b':
                            amount = input('How much to bet? Between'+str(min(self.plyr_dict[plyr_str].stack,self.min_bet))+' and '+str(self.plyr_dict[plyr_str].stack))
######################################### END USER INPUT / BEGIN BOT ACTION
########### Pass relevant table info, returns tuple like ('r',100) or ('f',0) for raise 100 or fold
            else:
                action = self.plyr_dict[plyr_str].bot_action(self.cost_to_play, self.big_blind, self.min_bet)
######################################### END BOT ACTION
            # Apply Input Action to table/player
            # Action potentially modifies table attributes and attributes of current player only
            # (player action does not change attributes of other player objects)
            action = (act,int(amount))
            if action[0] == 'b':
                self.bet(plyr_str, action[1])
            elif action[0] == 'r':
                self.raze(plyr_str, action[1])
            elif action[0] == 'C':
                self.call(plyr_str, action[1])
            elif action[0] == 'f':
                self.fold(plyr_str)
            elif action[0] == 'c':
                self.check(plyr_str)
######################################### END APPLY INPUT ACTION / BEGIN END_ROUND
            # skip to here if player is all-in, having skipped input
            # By here, player's action will have removed them from self.left_to_act (from in_hand if fold)
            # Check if only one player remains in hand
            if len(self.in_hand) == 1:
                # reward remaining player
                print('!!! winner of '+str(self.pot)+' chips!!!')
                self.plyr_dict[self.in_hand[0]].stack += self.pot
                print('your stack is '+str(self.plyr_dict[self.in_hand[0]].stack))
                self.pot = 0
############### TESTS ####
                x = 0
                for p in self.seat_order:
                    x += self.plyr_dict[p].stack
                assert(x==self.num_chips*self.num_players)
############### END TESTS #####
                # clean table, also cleans players, maintains player stacks and table.seat_order
                self.clean_table_after_hand()
                value = input('Another hand? y for yes, n for no')
                if value == 'y':
                    self.move_button_remove_chipless_players()
                    self.post_blinds()
                    sentinel = 1
                else:
                    sentinel = 0
            # CHECK FOR END OF FINAL ROUND, SHOWDOWN RESOLUTION
            elif self.left_to_act == [] and self.round == 4:
                # Check if sidepots are ncsry, if one or more players are all-in
                for p in self.in_hand:
                    assert(self.plyr_dict[p].stack >= 0)
                    if self.plyr_dict[p].stack == 0:
                        # return type of create_sidepots is list of 2-tuples, 1st elem is pot/int, 2nd is list of
                        # player strings (players that are eligible for the pot)
                        pots_w_elig_plyrs = self.create_sidepots()
                        for pot_n_plyrs in pots_w_elig_plyrs:
                            print(pot_n_plyrs)
                            self.showdown(pot_n_plyrs)
                        break
                else: # for/else loop, if no player is all-in, go to here, just resolve one showdown()
                    pot_and_plyrs = (self.pot, self.in_hand[:])
                    self.showdown(pot_and_plyrs)
                # Showdowns complete, players rewarded
                # Prompt whether to end loop or not
                value = input('Another hand? y for yes, n for no')
                self.clean_table_after_hand()
                if value == 'y':
                    self.move_button_remove_chipless_players()
                    new_hand = 1
                    sentinel = 1
                else: # exit program
                    sentinel = 0
###################### END SHOWDOWN RESOLUTION ###########
###################### OTHERWISE ADVANCE TO NEXT ROUND ###########
            elif len(self.left_to_act) == 0:
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
                #### CONTINUE LOOP ####


    # rotates seating position so that dealer button is on next player with chips
    # (skips players who have just been reduced to zero stack, so as not to skip player's chance at dealer position)
    # Rebuilds self.seat_order with players that have > 0 stack remaining
    # Maintains previous seating order
    def move_button_remove_chipless_players(self):
        new_seats = []
        for plyr in self.seat_order[1:] + self.seat_order[0:1]:
            if self.plyr_dict[plyr].stack > 0:
                new_seats.append(plyr)
        return new_seats
        

    def showdown(self, pot_and_player_tuple):
        # Get highest hand_rank
        players = pot_and_player_tuple[1]
        print(players)
        pot = pot_and_player_tuple[0]
        max_rank = 0
        top_plyrs = []
        for plyr in players:
            hands.assign_hand_rank(plyr, self)
            if self.plyr_dict[plyr].hand_rank > max_rank:
                top_plyrs = [plyr]
                max_rank = self.plyr_dict[plyr].hand_rank
            elif self.plyr_dict[plyr].hand_rank == max_rank:
                top_plyrs.append(plyr)
        # if one winner: award player
        if len(top_plyrs) == 1:
            # reward top_plyrs[0]
            print(top_plyrs[0]+' wins '+str(pot))
            self.plyr_dict[top_plyrs[0]].stack += pot
            self.pot -= pot
        else: # tie needs to be broken for this one pot, working bug, what about remainder here?
            winners = hands.break_ties(top_plyrs, self)
            amount = pot / len(winners)
            for p in winners:
                self.plyr_dict[p].stack += amount
                print(p+' wins DEBUG '+str(pot))


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
#         print(table.plyr_dict[k].stack)
#     print(table.pot)

# TESTS for table.create_sidepots
# create mock data with AT LEAST one player all-in/in-hand

table = Table(4,200,20)
for p in table.seat_order:
    table.plyr_dict[p].human = 1
table.play_hand_loop()



# table.com_cards.append(table.deck.draw_card())
# table.com_cards.append(table.deck.draw_card())
# table.com_cards.append(table.deck.draw_card())
# table.com_cards.append(table.deck.draw_card())
# table.com_cards.append(table.deck.draw_card())
# # set all players to human
# for p in table.seat_order:
#     table.plyr_dict[p].human = 1
#     table.plyr_dict[p].hand.append(table.deck.draw_card())
#     table.plyr_dict[p].hand.append(table.deck.draw_card())
#     hands.assign_hand_rank(p, table)
#     print(table.plyr_dict[p].hand+table.com_cards)
#     print(table.plyr_dict[p].hand_rank)
#     print(table.plyr_dict[p].tie_break)

