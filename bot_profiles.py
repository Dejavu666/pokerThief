import player
from random import randrange
# extend Player class, override basic action getters
# currently mostly the same as 'random' bots
# just getting placeholder to adjust individual actions once instantiated correctly

# for all bots... rank_sum increases action, made_pairs incr action, draws to pot odds, adjust bet sizes rel to pot


# Stop n Go
# working on...'if check action: bet wide range, if call action: call wide range'
class Stop_n_Go(player.Player):
    def get_random_bot_action(self, p, table):
        rank_sum = table.pd[p].hand[0][0] + table.pd[p].hand[1][0]
        made_pair = 0
        if table.pd[p].hand[0][0] == table.pd[p].hand[1][0]:
            made_pair += table.pd[p].hand[0][0]
        if table.pd[p].stack == 0:
            return ('check',0)
        # bot big blind special option actions
        if len(table.seat_order) == 2 and table.round == 1 and p == table.seat_order[1] and table.cost_to_play == table.pd[p].chips_this_round:
            # 2 plyr bb options, check, bet
            choice = randrange(0,99)
            choice += rank_sum//2
            choice += made_pair
            if choice <= 45:
                return ('check',0)
            else:
                # if not enough for legal bet
                if table.min_bet >= table.pd[p].stack:
                    return ('all_in', table.pd[p].stack)
                else: # enough for legal bet
                    return ('raise', randrange(max(table.pot//3,table.min_bet), min(table.pot*2, table.pd[p].stack)+1))
        if len(table.seat_order) > 2 and table.round == 1 and table.cost_to_play == table.pd[p].chips_this_round:
            if table.seat_order[2] == p:
                # more than 2 plyr bb options, check, bet
                choice = randrange(0,99)
                if choice <= 25:
                    return ('check',0)
                else:
                    # if not enough for legal bet
                    if table.min_bet >= table.pd[p].stack:
                        return ('all_in', table.pd[p].stack)
                    else: # enough for legal bet
                        return ('raise', randrange(max(table.pot//3,table.min_bet), min(table.pot*2, table.pd[p].stack)+1))
        if table.cost_to_play == table.pd[p].chips_this_round:
            return self.get_random_check_action(p, table)
        else:
            return self.get_random_call_action(p, table)

    def get_random_check_action(self,p,table):
        print('rand check act table.min_bet ' + str(table.min_bet))
        if table.min_bet >= table.pd[p].stack:
            amount = table.pd[p].stack
        else:
            # empty range
            if max(table.pot//3,table.min_bet) >= min((2*table.pot),table.pd[p].stack)+1:
                amount = table.pd[p].stack
            else:
                amount = randrange(max(table.pot//3,table.min_bet), min((2*table.pot),table.pd[p].stack)+1)
        choice = randrange(0,100)
        rank_sum = table.pd[p].hand[0][0] + table.pd[p].hand[1][0]
        made_pairs = 0
        all_ranks = [table.pd[p].hand[0][0], table.pd[p].hand[1][0]]
        for card in table.com_cards:
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
        choice += rank_sum//2
        if choice <= 15:
            return ("check",0)
        else:
            return ('bet', amount)
    
    def get_random_call_action(self,p,table):
        true_cost = table.cost_to_play - table.pd[p].chips_this_round
        print('rand call act true_cost ' + str(true_cost))
        choice = randrange(0,100)
        rank_sum = table.pd[p].hand[0][0] + table.pd[p].hand[1][0]
        made_pairs = 0
        all_ranks = [table.pd[p].hand[0][0], table.pd[p].hand[1][0]]
        for card in table.com_cards:
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
        choice += rank_sum//2
        if choice <= 75:
            return ("fold",0)
        elif choice <= 95:
            return ("call", 0)
        else:
            # if not enough for legal raise
            if table.pd[p].stack <= (2 * true_cost):
                return ('all_in',table.pd[p].stack)
            else:
                if table.min_bet >= (table.pd[p].stack-true_cost+1):
                    return ('all_in', table.pd[p].stack)
                amount = randrange(table.min_bet, (table.pd[p].stack-true_cost+1))
                return ("raise", amount)
####################################################################################################################





# Loose Aggressive, currently same as 'random'
# change to 'if check action: bet wide range, if call action: raise wide range
class Loose_Aggressive(player.Player):
    def get_random_bot_action(self, p, table):
        rank_sum = table.pd[p].hand[0][0] + table.pd[p].hand[1][0]
        if table.pd[p].stack == 0:
            return ('check',0)
        # bot big blind special option actions
        elif len(table.seat_order) == 2 and table.round == 1 and p == table.seat_order[1] and table.cost_to_play == table.pd[p].chips_this_round:
            # 2 plyr bb options, check, bet
            choice = randrange(0,100)
            choice += rank_sum
            if choice < 60:
                return ('check',0)
            else:
                # if not enough for legal bet
                if table.min_bet >= table.pd[p].stack:
                    return ('all_in', table.pd[p].stack)
                else: # enough for legal bet, potential bug empty range
                    return ('raise', randrange(max(table.pot//3,table.min_bet), min(table.pot*2, table.pd[p].stack)+1))
        if len(table.seat_order) > 2 and table.round == 1 and table.cost_to_play == table.pd[p].chips_this_round:
            if table.seat_order[2] == p:
                # more than 2 plyr bb options, check, bet
                choice = randrange(0,100)
                choice += rank_sum
                if choice < 60:
                    return ('check',0)
                else:
                    # if not enough for legal bet
                    if table.min_bet >= table.pd[p].stack:
                        return ('all_in', table.pd[p].stack)
                    else: # enough for legal bet
                        return ('raise', randrange(max(table.pot//3,table.min_bet), min(table.pot*2, table.pd[p].stack)+1))
        if table.cost_to_play == table.pd[p].chips_this_round:
            return self.get_random_check_action(p, table)
        else:
            return self.get_random_call_action(p, table)

    def get_random_check_action(self,p,table):
        print('rand check act table.min_bet ' + str(table.min_bet))
        if table.min_bet >= table.pd[p].stack:
            amount = table.pd[p].stack
        else:
            amount = randrange(table.min_bet, table.pd[p].stack)
        return ("check",0) if randrange(0,2) else ("bet",amount)
    
    def get_random_call_action(self,p,table):
        true_cost = table.cost_to_play - table.pd[p].chips_this_round
        choice = randrange(0,3)
        if choice == 0:
            return ("fold",0)
        elif choice == 1:
            return ("call", 0)
        else:
            # if not enough for legal raise
            if table.pd[p].stack <= (2 * true_cost):
                return ('all_in',0)
            else:
                amount = randrange(table.min_bet, table.pd[p].stack-true_cost+1)
            return ("raise", amount)
#################################################################################################################
# TAG, currently same as 'random'
# change to 'if check: bet narrow range, if call: raise narrow range
class Tight_Aggressive(player.Player):
    def get_random_bot_action(self, p, table):
        if table.pd[p].stack == 0:
            return ('check',0)
        # bot big blind special option actions
        elif len(table.seat_order) == 2 and table.round == 1 and p == table.seat_order[1] and table.cost_to_play == table.pd[p].chips_this_round:
            # 2 plyr bb options, check, bet
            choice = randrange(0,2)
            if choice:
                return ('check',0)
            else:
                # if not enough for legal raise
                if table.min_bet >= table.pd[p].stack:
                    return ('all_in', 0)
                else: # enough for legal raise
                    return ('raise', randrange(table.min_bet, table.pd[p].stack+1))
        # bug here, can't reference seat_order[2] unless it exists
        if len(table.seat_order) > 2 and table.round == 1 and table.cost_to_play == table.pd[p].chips_this_round:
            if table.seat_order[2] == p:
                # more than 2 plyr bb options, check, bet
                choice = randrange(0,2)
                if choice:
                    return ('check',0)
                else:
                    # if not enough for legal raise
                    if table.min_bet >= table.pd[p].stack:
                        return ('all_in', 0)
                    else: # enough for legal raise
                        return ('raise', randrange(table.min_bet, table.pd[p].stack+1))
        if table.cost_to_play == table.pd[p].chips_this_round:
            return self.get_random_check_action(p, table)
        else:
            return self.get_random_call_action(p, table)

    def get_random_check_action(self,p,table):
        print('rand check act table.min_bet ' + str(table.min_bet))
        if table.min_bet >= table.pd[p].stack:
            amount = table.pd[p].stack
        else:
            amount = randrange(table.min_bet, table.pd[p].stack)
        return ("check",0) if randrange(0,2) else ("bet",amount)
    
    def get_random_call_action(self,p,table):
        true_cost = table.cost_to_play - table.pd[p].chips_this_round
        choice = randrange(0,3)
        if choice == 0:
            return ("fold",0)
        elif choice == 1:
            return ("call", 0)
        else:
            # if not enough for legal raise
            if table.pd[p].stack <= (2 * true_cost):
                return ('all_in',0)
            else:
                amount = randrange(table.min_bet, table.pd[p].stack-true_cost+1)
            return ("raise", amount)
#########################################################################################################
# Calling_Station, currently same as 'random' profile
# change to 'if check_action: check, if call_action: call
class Calling_Station(player.Player):
    def get_random_bot_action(self, p, table):
        if table.pd[p].stack == 0:
            return ('check',0)
        # bot big blind special option actions
        elif len(table.seat_order) == 2 and table.round == 1 and p == table.seat_order[1] and table.cost_to_play == table.pd[p].chips_this_round:
            # 2 plyr bb options, check, bet
            choice = randrange(0,2)
            if choice:
                return ('check',0)
            else:
                # if not enough for legal raise
                if table.min_bet >= table.pd[p].stack:
                    return ('all_in', 0)
                else: # enough for legal raise
                    return ('raise', randrange(table.min_bet, table.pd[p].stack+1))
        # bug here, can't reference seat_order[2] unless it exists
        if len(table.seat_order) > 2 and table.round == 1 and table.cost_to_play == table.pd[p].chips_this_round:
            if table.seat_order[2] == p:
                # more than 2 plyr bb options, check, bet
                choice = randrange(0,2)
                if choice:
                    return ('check',0)
                else:
                    # if not enough for legal raise
                    if table.min_bet >= table.pd[p].stack:
                        return ('all_in', 0)
                    else: # enough for legal raise
                        return ('raise', randrange(table.min_bet, table.pd[p].stack+1))
        if table.cost_to_play == table.pd[p].chips_this_round:
            return self.get_random_check_action(p, table)
        else:
            return self.get_random_call_action(p, table)

    def get_random_check_action(self,p,table):
        print('rand check act table.min_bet ' + str(table.min_bet))
        if table.min_bet >= table.pd[p].stack:
            amount = table.pd[p].stack
        else:
            amount = randrange(table.min_bet, table.pd[p].stack)
        return ("check",0) if randrange(0,2) else ("bet",amount)
    
    def get_random_call_action(self,p,table):
        true_cost = table.cost_to_play - table.pd[p].chips_this_round
        choice = randrange(0,3)
        if choice == 0:
            return ("fold",0)
        elif choice == 1:
            return ("call", 0)
        else:
            # if not enough for legal raise
            if table.pd[p].stack <= (2 * true_cost):
                return ('all_in',0)
            else:
                amount = randrange(table.min_bet, table.pd[p].stack-true_cost+1)
            return ("raise", amount)
            
if __name__ == '__main__':
    jim = Calling_Station()
    print(dir(jim))