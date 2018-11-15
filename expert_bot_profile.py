from random import randrange
import player




# need to encapsulate 'choice' increasing function, takes p,t,hole+com ; returns val of some range
# representing hand strength given the table state


# normalize hand_rank_sum between -k and k, subtract from 'choice' for below par hands

# bots need a sense of how big POT versus STACK versus BET SIZE

# need to know when has 'TOP PAIR' esp for heads up postflop

class Expert_Bot(player.Player):
    def get_random_bot_action(self, p, t):
        if t.pd[p].stack == 0:
            return ('check',0)
        choice = randrange(0,100)
        # BIG BLIND special options ONLY 2 PLAYER
        if len(t.seat_order) == 2 and t.round == 1 and p == t.seat_order[1] and t.cost_to_play == t.pd[p].chips_this_round:
            hand_eval_sum = self.eval_hole_cards_PREFLOP_2plyrs(p, t)
            choice += hand_eval_sum
            # BB bot still has check/raise option
            if choice <= 60:
                return ('check',0)
            else:# TRY TO RAISE from BB
                if t.min_bet >= t.pd[p].stack: # not enough for legal RAISE
                    return ('all_in', t.pd[p].stack)
                else: # enough for legal RAISE, 2plyr BB last2act preflop, 1st2act postflop, pot is always 2*minbet
                    # only consideration: is stack small enough to warrant thinking about full commit versus fold
                    # otherwise, at least build pot
                    return ('raise', randrange(max(t.pot//3,t.min_bet)//10*10, min(t.pot*2, t.pd[p].stack)+1,10))
        # END 2 PLAYER BIG BLIND SPECIAL OPTIONS
        # BOT BIG BLIND special option actions MORE THAN 2 PLAYER
        if len(t.seat_order) > 2 and t.round == 1 and t.cost_to_play == t.pd[p].chips_this_round:
            if t.seat_order[2] == p:
                # more than 2 plyr bb options, check, bet
                if choice <= 55:
                    return ('check',0)
                else:
                    # if not enough for legal bet
                    if t.min_bet >= t.pd[p].stack:
                        return ('all_in', t.pd[p].stack)
                    else: # enough for legal bet
                        return ('raise', randrange(max(t.pot//3,t.min_bet)//10*10, min(t.pot*2, t.pd[p].stack)+1,10))
        if t.cost_to_play == t.pd[p].chips_this_round:
            return self.get_random_check_action(p, t)
        else:
            return self.get_random_call_action(p, t)
            
            
    def eval_hole_cards_postflop_Kplyrs(self, p, t):
        pass
    # takes a player 'p' and table state 't', evaluates player's hole cards in terms of table state considering
    # that other hole cards are unknown, num_opp is variable, stack relative to pot/bet size is variable,
    # players previous actions this round and players left to act are variable
    # most basically just returns value (1-100?) of two hole cards among possible two hole card hands
    # could just hardcode rating of hand combinations, but their relative value sometimes changes drastically
    # based on number of players
    # for instance, pocket 2s has better than 50% win percentage against any unpaired set of overcards (nonpairs)
    # with one player, but 2 players both with unpaired overcards drop win percentage of pocket2s in half
    def eval_hole_cards_PREFLOP_2plyrs(self, p, t):
        hole = t.pd[p].hand
        value = 0
        left_act = t.left_to_act[:]
        # Rank Value each card, AK preflop branch leads apx 50% any other hand,
        # rank_sum average value == 15, sub avg, then incr by some constant
        # range created is -11 to 13, rly range does not include pocket_pairs
        rank_sum = hole[0][0] + hole[1][0] - 15
        value += rank_sum
        # Pocket Pair Rank value
        p_pair_rank = 0
        if hole[0][0] == hole[1][0]:
            p_pair_rank += hole[0][0]
        pass

    def eval_hole_cards_POSTFLOP_2plyrs(self, p, t):
        pass
    # this will be preflop, discriminate between if you are first or last to act
    def eval_hole_cards_preflop_Kplyrs(self, p, t):
        # when this is called will p be equal to t.left_to_act[0]?
        pass

    # input is the player 'p' and the table state 't'
    # returns an int value added to random 'choice' for determining bot action
    # should eval the hand+state at dif points (preflop(only hole cards), final board state with no draws left
    def eval_hand_sum(self, p, t):
        hole = t.pd[p].hand
        hand = t.pd[p].hand + t.com_cards
        rank_sum = hole[0][0] + hole[1][0]
        p_pair_rank = 0
        if hand[0][0] == hand[1][0]:
            p_pair_rank += hand[0][0]
        # suited
        suited = 0
        if hand[0][1] == hand[1][1]: # am suited
            suited += 3
        # connected, must account for Ace as both one and 14
        connected = 0
        if abs(hand[0][0] - hand[1][0]) == 1: # am connected, should discr between middle and end connected pairs
            connected += 2
        elif hand[0][0] == 14 or hand[1][0] == 14:
            if hand[0][0] == 2 or hand[1][0] == 2: # connected with Ace and 2
                connected += 2
        choice += connected
        # draws to straight | flush
        ranks = [x[0] for x in hand]
        sd_sum = self.straight_draws_sum(hand+t.com_cards)
        choice += sd_sum
        # made straight | made flush
        
        # num opponent
        
        # position
        
        # true cost compared to pot value
        
        # opp bet patterns, vpip versus passivity 
        
        # detect likely made hands, guess range
        
        # trap with nuts, detect top possible hands versus likely hands

    # input is list, output is int (arbitrary sum value representing equity in straight draws)
    # just do, for every seq that starts with each char, is there one val that completes the str?
    def straight_draws_sum(self, hand_com_cards):
        ranks = [x[0] for x in hand_com_cards]
        # add ace as 1, also need to account for Ace outs as 1 and 14
        for rank in ranks[:]:
            if rank == 14:
                ranks.append(1)
        ranks = list(set(ranks))
        seqs = []
        strs = []
        outs = []
        for i,rank in enumerate(ranks[:]): # what i want here is all sorted permutes of len4
            for j,k in enumerate(ranks):
                if len(ranks[i:j+1]) == 4: # seq must be exactly len4
                    seqs.append(ranks[i:j+1])
        for seq in seqs:
            # if there is one int val 1-14 added to set that satisfies 'abs(seq[0]-seq[4]) == 4'
            for val in range(1,15):
                ns = sorted(seq + [val])
                if abs(ns[0] - ns[4]) == 4:
                    strs.append(ns)
                    if val not in ranks:
                        outs.append(val)
        outs = list(set(outs))
        if len(outs) == 1:
            return 2
        elif len(outs) == 2:
            return 5
        elif len(outs) > 2:
            return 7
        else:
            return 0

    def get_random_check_action(self,p,t):
        print('rand check act t.min_bet ' + str(t.min_bet))
        hand = t.pd[p].hand # hand is list of two tuples with int for rank and str for suit [(13,'H'),(12,'S')]
        choice = randrange(0,100)
        # rank of cards in hand sum
        rank_sum = hand[0][0] + hand[1][0]
        p_pair_rank = 0
        if hand[0][0] == hand[1][0]:
            p_pair_rank += hand[0][0]
        choice += rank_sum
        choice += p_pair_rank
        # suited
        suited = 0
        if hand[0][1] == hand[1][1]: # am suited
            suited += 3
        choice += suited
        # connected, must account for Ace as both one and 14
        connected = 0
        if abs(hand[0][0] - hand[1][0]) == 1: # am connected, should discr between middle and end connected pairs
            connected += 2
        elif hand[0][0] == 14 or hand[1][0] == 14:
            if hand[0][0] == 2 or hand[1][0] == 2: # connected with Ace and 2
                connected += 2
        choice += connected
        # draws to straight | flush
        ranks = [x[0] for x in hand]
        sd_sum = self.straight_draws_sum(hand+t.com_cards)
        choice += sd_sum
        # made straight | made flush
        
        # num opponent
        
        # position
        
        # true cost compared to pot value
        
        # opp bet patterns, vpip versus passivity 
        
        # detect likely made hands, guess range
        
        # trap with nuts, detect top possible hands versus likely hands
        
        # set BET AMOUNT
        if t.min_bet >= t.pd[p].stack: # not enough for min_bet, if bet amt is stack
            amount = t.pd[p].stack
        else:
            # empty range
            if max(t.pot//3,t.min_bet) >= min((2*t.pot),t.pd[p].stack)+1:
                amount = t.pd[p].stack
            else:
                amount = randrange(max(t.pot//3,t.min_bet)//10*10, min((2*t.pot),t.pd[p].stack)+1,10)
                
        all_ranks = [t.pd[p].hand[0][0], t.pd[p].hand[1][0]]
        for card in t.com_cards:
            all_ranks.append(card[0])
        quads = []
        trips = []
        pairs = []
        for rank in all_ranks:
            if all_ranks.count(rank) == 4:
                quads.append(rank)
            elif all_ranks.count(rank) == 3:
                trips.append(rank)
            elif all_ranks.count(rank) == 2:
                pairs.append(rank)
        if quads != []:
            choice += 3*max(quads)
        if trips != []:
            choice += 2*max(trips)
        if pairs != []:
            choice += max(pairs)
        if choice <= 50:
            return ("check",0)
        else:
            return ('bet', amount)



    def get_random_call_action(self,p,t):
        hand = t.pd[p].hand
        true_cost = t.cost_to_play - t.pd[p].chips_this_round
        print('rand call act true_cost ' + str(true_cost))
        choice = randrange(0,100)
        rank_sum = hand[0][0] + hand[1][0]
        choice += rank_sum
        made_pairs = 0
        # suited
        suited = 0
        if hand[0][1] == hand[1][1]: # am suited
            suited += 3
        choice += suited
        # connected, must account for Ace as both one and 14
        connected = 0
        if abs(hand[0][0] - hand[1][0]) == 1: # am connected, should discr between middle and end connected pairs
            connected += 2
        elif hand[0][0] == 14 or hand[1][0] == 14:
            if hand[0][0] == 2 or hand[1][0] == 2: # connected with Ace and 2
                connected += 2
        choice += connected
        # draws to straight | flush
        ranks = [x[0] for x in hand]
        sd_sum = self.straight_draws_sum(hand+t.com_cards)
        choice += sd_sum
        all_ranks = [t.pd[p].hand[0][0], t.pd[p].hand[1][0]]
        for card in t.com_cards:
            all_ranks.append(card[0])
        quads = []
        trips = []
        pairs = []
        for rank in all_ranks:
            if all_ranks.count(rank) == 4:
                quads.append(rank)
            elif all_ranks.count(rank) == 3:
                trips.append(rank)
            elif all_ranks.count(rank) == 2:
                pairs.append(rank)
        if quads != []:
            choice += 3*max(quads)
        if trips != []:
            choice += 2*max(trips)
        if pairs != []:
            choice += max(pairs)
        if choice <= 85:
            return ("fold",0)
        elif choice <= 100:
            return ("call", 0)
        else:
            # if not enough for legal raise
            if t.pd[p].stack <= (2 * true_cost):
                return ('all_in',t.pd[p].stack)
            elif t.min_bet//10*10 >= (t.pd[p].stack-true_cost)+1:
                return ('all_in', t.pd[p].stack)
            else:
                if t.min_bet >= (t.pd[p].stack-true_cost+1):
                    return ('all_in', t.pd[p].stack)
                # this is in call_action, trying to reraise some amount, change max to...
                # min(t.pd[p].stack-true_cost, 3*t.min_bet)
                amount = randrange(t.min_bet//10*10, min(t.pd[p].stack-true_cost, 3*t.min_bet)+1,10)
                return ("raise", amount)
                
                
###########################################

# TESTS

###########################################

if __name__ == '__main__':
    
    
    # make just take list of ranks
    # test straight_draws_sum(ranks)
    p = Stop_n_Go()
    hand = [(13,'H'), (12,'H'), (11,'H'), (9,'H'), (8,'H'), (7,'H'), (6,'H')] # outs should be 6, 10
    print(p.straight_draws_sum(hand))