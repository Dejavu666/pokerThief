# what is a way to normalize the card representations ('AH','5C') so that no translation will be needed?
# these are called/controlled by assignHandRanks()

# Just pure functions here... I think...

# Take a string that is a Player name
def get_hand_rank(some_player_name):
    
    
    return rank



def straight_finder(ranks):
    ranks.sort(reverse=True)
    if len(ranks) < 5:
        return None
    elif (ranks[0]-ranks[4]) == 4:
        return [ranks[0]]
    else:
        return straight_finder(ranks[1:])

def four_of_a_kind_finder(ranks):
    for rank in ranks:
        if ranks.count(rank) == 4:
            highcards = [x for x in ranks if x != rank]
            return [rank,max(highcards)]
    else:
        return None

def fullhouse_finder(ranks):
    set3s = set()
    set2s = set()
    rnks = set(ranks)
    for rank in rnks:
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

def two_pair_finder(pairranks):
    pairs = set()
    highList = []
    for rank in pairranks:
        if pairranks.count(rank) == 2:
            pairs.add(rank)
        elif pairranks.count(rank) == 1:
            highList.append(rank)
    highCard = max(highList)
    if len(pairs) >= 2:
        overpair = max(pairs)
        pairs.remove(max(pairs))
        return [overpair,max(pairs),highCard]
    else:
        return None

def flush_finder(final_hand):
    newHand = []
    for card in final_hand:
        if card[0] == 'A':
            newHand.append('14'+card[1])
        elif card[0] == 'K':
            newHand.append('13'+card[1])
        elif card[0] == 'Q':
            newHand.append('12'+card[1])
        elif card[0] == 'J':
            newHand.append('11'+card[1])
        elif card[0] == 'T':
            newHand.append('10'+card[1])
        else:
            newHand.append(card)
    flushCards = [x[-1] for x in final_hand]
    hand = [x for x in newHand if flushCards.count(x[-1])>=5]
    if len(hand) >= 5:
        handRanks = [int(x[:-1]) for x in hand]
        suit = hand[0][-1]
        return sorted(handRanks,reverse=True)
    else:
        return None
        
def straight_flush_finder(final_hand):
    if flush_finder(final_hand):
        if straight_finder(flush_finder(final_hand)):
            return straight_finder(flush_finder(final_hand))
    return None

def three_of_a_kind_finder(pairranks):
    threes = []
    highcards = []
    for rank in pairranks:
        if pairranks.count(rank) == 3:
            threes.append(rank)
        else:
            highcards.append(rank)
    highcards.sort(reverse=True)
    if len(threes) >= 1:
        return [max(threes)]+highcards
    return None

def one_pair_finder(pairranks):
    highcards = []
    pairsof2 = []
    for rank in pairranks:
        if pairranks.count(rank) == 1:
            highcards.append(rank)
        elif pairranks.count(rank) == 2:
            pairsof2.append(rank)
    if len(pairsof2) >=1:
        return [max(pairsof2)]+sorted(highcards,reverse=True)
    else:
        return None

def highcard_finder(pairranks):
    highlist = sorted(pairranks,reverse=True)
    return highlist
    
# Takes a list of player names, ensures they all have the same hand_rank,
# Returns a list of player name(s) that all have true ties (same hand_rank and tie break value)
def tieBreak(playerList,plyrDct):
    winners = []
    while True:
        highVal = 0
        for plr in playerList:
            if plyrDct[plr].tieBreak[0] > highVal:
                winners = [plr]
                highVal = plyrDct[plr].tieBreak[0]
            elif plyrDct[plr].tieBreak[0] == highVal:
                winners.append(plr)
            plyrDct[plr].tieBreak.pop(0)
        if len(winners) == 1:
            return winners
        elif plyrDct[winners[0]].tieBreak == []:
            break
        playerList = winners[:]
    return winners
    