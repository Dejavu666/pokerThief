# hands.py has functions that evaluate player hands for type and resolves ties among them
# Only call 'break_ties()' and 'assign_hand_rank()'
# Other functions must be controlled by 'assign_hand_rank()'

# NEED TO: Test that straight_flush is found when having higher flush cards, middle straight

def straight_finder(ranks):
    ranks = list(set(ranks))
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
    ranks = [card[0] for card in hand]
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
        
# needs to not rely on sub-functions
# find all flush cards, at least 5
# find a straight among those flush cards, you have straight_flush
# only transform ace if ace is among flush cards
def straight_flush_finder(hand):
    # get only cards if suit count is >=5
    flushCards = [card[1] for card in hand]
    hand = [card for card in hand if flushCards.count(card[1])>=5]
    if len(hand)<5:
        return None
    # if ace exists, add 'one' value, feed flush cards to straight_finder
    ranks = []
    for card in hand:
        if card[0] == 14:
            ranks.append(1)
            ranks.append(14)
        else:
            ranks.append(card[0])
    return straight_finder(ranks)

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

# working here
# BUG tie_break for one-pair not working
# Too many tie_break vals being added to plyr.tie_break
def one_pair_finder(hand):
    ranks = [card[0] for card in hand]
    highcards = []
    pairsof2 = []
    for rank in ranks:
        if ranks.count(rank) == 1:
            highcards.append(rank)
        elif ranks.count(rank) == 2:
            pairsof2.append(rank)
    highcards = sorted(highcards, reverse=True)
    if len(pairsof2) >= 1:
        return [max(pairsof2)]+highcards[:4]
    else:
        return None

def highcard_finder(hand):
    ranks = [card[0] for card in hand]
    highlist = sorted(ranks,reverse=True)
    return highlist