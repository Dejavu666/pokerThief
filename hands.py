# hands.py has functions that evaluate player hands for type and resolves ties among them
# Only call 'break_ties()' and 'assign_hand_rank()'
# Other functions must be controlled by 'assign_hand_rank()'

# NEED TO: Test that straight_flush is found when having higher flush cards, middle straight

# Takes a list of player names, ensures they all have the same hand_rank,
# Returns a list of player name(s) that have true ties (same hand_rank and tie_break value)
def break_ties(plyr_list):
    winners = []
    while True:
        highVal = 0
        for plr in plyr_list:
            if table.plyr_dict[plr].tie_break[0] > highVal:
                winners = [plr]
                highVal = plyr_dict[plr].tie_break[0]
            elif plyr_dict[plr].tie_break[0] == highVal:
                winners.append(plr)
            plyr_dict[plr].tie_break.pop(0)
        if len(winners) == 1:
            return winners
        # if players have exhausted tie_break values
        elif plyr_dict[winners[0]].tie_break == []:
            break
    return winners

# Take a string that is a Player name
# Assigns hand_rank and tie_break values to the Player object
# Only makes sense to call when Player has 2 cards and table.community has 5
def assign_hand_rank(name):
    hand = plyr_dict[name].hand + table.community_cards
    if straight_flush_finder(hand):
        plyr_dict[name].hand_rank = 9
        plyr_dict[name].tie_break = straight_flush_finder(hand)
    elif four_of_a_kind_finder(hand):
        plyr_dict[name].hand_rank = 8
        plyr_dict[name].tie_break = four_of_a_kind_finder(hand)
    elif fullhouse_finder(hand):
        plyr_dict[name].hand_rank = 7
        plyr_dict[name].tie_break = fullhouse_finder(hand)
    elif flush_finder(hand):
        plyr_dict[name].hand_rank = 6
        plyr_dict[name].tie_break = flush_finder(hand)
    elif straight_finder(hand):
        plyr_dict[name].hand_rank = 5
        plyr_dict[name].tie_break = straight_finder(hand)
    elif three_of_a_kind_finder(hand):
        plyr_dict[name].hand_rank = 4
        plyr_dict[name].tie_break = three_of_a_kind_finder(hand)
    elif two_pair_finder(hand):
        plyr_dict[name].hand_rank = 3
        plyr_dict[name].tie_break = two_pair_finder(hand)
    elif one_pair_finder(hand):
        plyr_dict[name].hand_rank = 2
        plyr_dict[name].tie_break = one_pair_finder(hand)
    else:
        plyr_dict[name].hand_rank = 1
        plyr_dict[name].tie_break = highcard_finder(hand)



def straight_finder(hand):
    ranks = []
    for card in hand:
        if card[0] == 14:
            ranks.append(1)
        else:
            ranks.append(card[0])
    ranks.sort(reverse=True)
    if len(ranks) < 5:
        return None
    elif (ranks[0]-ranks[4]) == 4:
        return [ranks[0]]
    else:
        return straight_finder(ranks[1:])

def four_of_a_kind_finder(hand):
    ranks = [card[0] for card in hand]
    for rank in ranks:
        if ranks.count(rank) == 4:
            highcards = [x for x in ranks if x != rank]
            return [rank,max(highcards)]
    else:
        return None

def fullhouse_finder(hand):
    ranks = set([card[0] for card in hand])
    set3s = set()
    set2s = set()
    for rank in ranks:
        if ranks.count(rank) == 3:
            set3s.add(rank)
        elif ranks.count(rank) == 2:
            set2s.add(rank)
    if len(set3s) == 2:
        set2s.add(min(set3s))
        set3s.remove(min(set3s))
    if len(set3s) == 1 and len(set2s) >= 1:
        return [set3s.pop(),max(set2s)]
    else:
        return None

def two_pair_finder(hand):
    ranks = [card[0] for card in hand]
    pairs = set()
    highList = []
    for rank in ranks:
        if ranks.count(rank) == 2:
            pairs.add(rank)
        elif ranks.count(rank) == 1:
            highList.append(rank)
    highCard = max(highList)
    if len(pairs) >= 2:
        overpair = max(pairs)
        pairs.remove(max(pairs))
        return [overpair,max(pairs),highCard]
    else:
        return None

def flush_finder(hand):
    flushCards = [card[1] for card in hand]
    hand = [card for card in hand if flushCards.count(card[1])>=5]
    if len(hand) >= 5:
        ranks = [card[0] for card in hand]
        return sorted(ranks,reverse=True)
    else:
        return None
        
def straight_flush_finder(hand):
    if flush_finder(hand):
        if straight_finder(flush_finder(hand)):
            return straight_finder(flush_finder(hand))
    return None

def three_of_a_kind_finder(hand):
    ranks = [card[0] for card in hand]
    threes = []
    highcards = []
    for rank in ranks:
        if ranks.count(rank) == 3:
            threes.append(rank)
        else:
            highcards.append(rank)
    highcards.sort(reverse=True)
    if len(threes) >= 1:
        return [max(threes)]+highcards
    return None

def one_pair_finder(hand):
    ranks = [card[0] for card in hand]
    highcards = []
    pairsof2 = []
    for rank in ranks:
        if ranks.count(rank) == 1:
            highcards.append(rank)
        elif ranks.count(rank) == 2:
            pairsof2.append(rank)
    if len(pairsof2) >=1:
        return [max(pairsof2)]+sorted(highcards,reverse=True)
    else:
        return None

def highcard_finder(hand):
    ranks = [card[0] for card in hand]
    highlist = sorted(ranks,reverse=True)
    return highlist