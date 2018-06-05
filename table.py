# the state is maintained by altering a Table instance,
# the Table calls a method like bet() which takes a player and an amount
# the order of play, pot, and bets are tracked by the Table instance

# DEFINE interface from this to visual element
# It needs to 
#   accept a Table state/object
#   prompt if active player is human else get action from Player instance
#   modify Table with received action
#   return Table object
from random import shuffle
import player, deck, hands

# do I need default values?
class Table():
    def __init__(self,bigBlind=0,pot=0,costToPlay=0,inHand=None,playerOrder=None,leftToAct=None,plyrDct=None,round='preflop',cardsInPlay=None):
        self.bigBlind = bigBlind
        if playerOrder == None:
            self.playerOrder = []
        self.deck = deck.Deck()
        self.pot = pot
        if inHand == None:
            self.inHand = []
        self.costToPlay = costToPlay
        if leftToAct == None:
            self.leftToAct = []
        if plyrDct == None:
            self.plyrDct = {}
        self.round = round # rounds are: 'preflop','flop','turn','river','showdown'
        if cardsInPlay == None:
            self.cardsInPlay = []
        self.sidepots = []
        self.sidepotsElig = []
        self.minBet = 0
         
    # takes the playerList and the stack_size, creates self.playOrder and self.plyrDct
    def seatPlayers(self,playerList,stack_size):
        shuffle(playerList)
        self.playerOrder = playerList[:]
        self.plyrDct = dict((name, player.Player(stack_size=stack_size)) for name in self.playerOrder)
        # set player1 to humanUser
        self.plyrDct['player1'].human = 1
        
    def dealCards(self):
        for plyr in self.playerOrder:
            self.plyrDct[plyr].draw_card(self.deck.draw_card())
        for plyr in self.playerOrder:
            self.plyrDct[plyr].draw_card(self.deck.draw_card())
        
    def postBlinds(self):
        for plyr in self.playerOrder:
            self.plyrDct[plyr].startStack = self.plyrDct[plyr].stack_size
        # more than 2 players post blinds
        if len(self.playerOrder) > 2:
            if self.plyrDct[self.playerOrder[2]].stack_size >= self.bigBlind:
                self.plyrDct[self.playerOrder[2]].stack_size -= self.bigBlind
                self.plyrDct[self.playerOrder[2]].in_front = self.bigBlind
                self.pot += self.bigBlind
            else:
                self.pot += self.plyrDct[self.playerOrder[2]].stack_size
                self.plyrDct[self.playerOrder[2]].in_front = self.plyrDct[self.playerOrder[2]].stack_size
                self.plyrDct[self.playerOrder[2]].stack_size = 0
            if self.plyrDct[self.playerOrder[1]].stack_size >= self.bigBlind/2:
                self.plyrDct[self.playerOrder[1]].stack_size -= self.bigBlind/2
                self.plyrDct[self.playerOrder[1]].in_front = self.bigBlind/2
                self.pot += self.bigBlind/2
            else:
                self.pot += self.plyrDct[self.playerOrder[1]].stack_size
                self.plyrDct[self.playerOrder[1]].in_front = self.plyrDct[self.playerOrder[1]].stack_size
                self.plyrDct[self.playerOrder[1]].stack_size = 0
        # only two players post blinds (order of play is different with only 2 players)
        elif len(self.playerOrder) == 2:
            if self.plyrDct[self.playerOrder[1]].stack_size >= self.bigBlind:
                self.plyrDct[self.playerOrder[1]].stack_size -= self.bigBlind
                self.plyrDct[self.playerOrder[1]].in_front = self.bigBlind
                self.pot += self.bigBlind
            else:
                self.pot += self.plyrDct[self.playerOrder[1]].stack_size
                self.plyrDct[self.playerOrder[1]].in_front = self.plyrDct[self.playerOrder[1]].stack_size
                self.plyrDct[self.playerOrder[1]].stack_size = 0
            if self.plyrDct[self.playerOrder[0]].stack_size >= self.bigBlind/2:
                self.plyrDct[self.playerOrder[0]].stack_size -= self.bigBlind/2
                self.plyrDct[self.playerOrder[0]].in_front = self.bigBlind/2
                self.pot += self.bigBlind/2
            else:
                self.pot += self.plyrDct[self.playerOrder[0]].stack_size
                self.plyrDct[self.playerOrder[0]].in_front = self.plyrDct[self.playerOrder[1]].stack_size
                self.plyrDct[self.playerOrder[0]].stack_size = 0
        # pot has been bet (blinds)
        self.costToPlay = self.bigBlind
        self.minBet = self.bigBlind
        # modify leftToAct, inHand here
        if len(self.playerOrder) > 3:
            self.leftToAct = self.playerOrder[3:]
            for plyr in self.playerOrder[:3]:
                self.leftToAct.append(plyr)
            self.inHand = [self.playerOrder[2]]
        elif len(self.playerOrder) == 3:
            self.leftToAct = []
            for plyr in self.playerOrder:
                self.leftToAct.append(plyr)
            self.inHand = [self.playerOrder[2]]
        elif len(self.playerOrder) < 3:
            self.leftToAct = self.playerOrder[:]
            self.inHand = [self.playerOrder[1]]
    
    # can pass in human player or bot
    def bet(self,plyr,amount):
        self.plyrDct[plyr].stack_size -= amount+self.costToPlay-self.plyrDct[plyr].in_front
        self.pot += amount+self.costToPlay-self.plyrDct[plyr].in_front
        self.plyrDct[plyr].in_front += amount+self.costToPlay-self.plyrDct[plyr].in_front
        self.costToPlay += amount
        self.minBet = amount
        if plyr in self.inHand:
            self.inHand.remove(plyr)
        self.inHand.append(plyr)
        for player in self.inHand:
            if player not in self.leftToAct:
                self.leftToAct.append(player)
        self.leftToAct.remove(plyr)
    
    def call(self,plyr):
        # if enough for a legal call
        if self.plyrDct[plyr].stack_size >= self.costToPlay-self.plyrDct[plyr].in_front:
            self.plyrDct[plyr].stack_size -= self.costToPlay-self.plyrDct[plyr].in_front
            self.pot += self.costToPlay-self.plyrDct[plyr].in_front
            self.plyrDct[plyr].in_front += self.costToPlay-self.plyrDct[plyr].in_front
        else: # call with what you have (less than legal)
            self.pot += self.plyrDct[plyr].stack_size
            self.plyrDct[plyr].in_front += self.plyrDct[plyr].stack_size
            self.plyrDct[plyr].stack_size = 0
        if plyr in self.inHand:
            self.inHand.remove(plyr)
        self.inHand.append(plyr)
        if len(self.leftToAct) == 1:
            self.leftToAct = []
        else:
            self.leftToAct = self.leftToAct[1:]
            
    def check(self,plyr):
        if plyr in self.inHand:
            self.inHand.remove(plyr)
        self.inHand.append(plyr)
        if len(self.leftToAct) == 1:
            self.leftToAct = []
        else:
            self.leftToAct = self.leftToAct[1:]
            
    def Raise(self,plyr,amount):
        # WORKING bug here, allows for raising more than stack_size
        # first branch here needs to account for reraising less than legal min
        if (amount+self.costToPlay-self.plyrDct[plyr].in_front) >= self.plyrDct[plyr].stack_size:
            amount = self.plyrDct[plyr].stack_size
            self.plyrDct[plyr].stack_size -= amount
            self.pot += amount
            self.plyrDct[plyr].in_front += amount+self.costToPlay-self.plyrDct[plyr].in_front
            self.costToPlay += amount
            self.minBet = amount
        else:
            self.plyrDct[plyr].stack_size -= amount+self.costToPlay-self.plyrDct[plyr].in_front
            self.pot += amount+self.costToPlay-self.plyrDct[plyr].in_front
            self.plyrDct[plyr].in_front += amount+self.costToPlay-self.plyrDct[plyr].in_front
            self.costToPlay += amount
            self.minBet = amount
        if plyr in self.inHand:
            self.inHand.remove(plyr)
        self.inHand.append(plyr)
        for player in self.inHand:
            if player not in self.leftToAct:
                self.leftToAct.append(player)
        for player in self.inHand:
            if player not in self.leftToAct:
                self.leftToAct.append(player)
        self.leftToAct.remove(plyr)
        
    def fold(self,plyr):
        if plyr in self.inHand:
            self.inHand.remove(plyr)
        self.plyrDct[plyr].hand = []
        if plyr in self.leftToAct:
            self.leftToAct.remove(plyr)
            
            
            
    # assumes players have hands, self.cardsInPlay is full (5 community cards).
    # Only assigns for players inHand
    def assignHandRanks(self):
        for player in self.inHand:
            final_hand = self.cardsInPlay + self.plyrDct[player].hand
            ranks = [x[0] for x in final_hand]
            suits = [x[1] for x in final_hand]
            #ints with Ace as 14 and 2 for straights
            straightranks = []
            #ints with Ace as 14 for pairs
            for rank in ranks:
                if rank == 'T':
                    straightranks.append(10)
                elif rank == 'J':
                    straightranks.append(11)
                elif rank == 'Q':
                    straightranks.append(12)
                elif rank == 'K':
                    straightranks.append(13)
                elif rank == 'A':
                    straightranks.append(1)
                    straightranks.append(14)
                else:
                    straightranks.append(int(rank))
            pairranks = [x for x in straightranks if x != 1]
            straightranks = sorted(list(set(straightranks)),reverse=True)
            if hands.straight_flush_finder(final_hand):
                 self.plyrDct[player].handRank = 9
                 self.plyrDct[player].tieBreak = hands.straight_flush_finder(final_hand)
            elif hands.four_of_a_kind_finder(pairranks):
                self.plyrDct[player].handRank = 8
                self.plyrDct[player].tieBreak = hands.four_of_a_kind_finder(pairranks)
            elif hands.fullhouse_finder(pairranks):
                self.plyrDct[player].handRank = 7
                self.plyrDct[player].tieBreak = hands.fullhouse_finder(pairranks)
            elif hands.flush_finder(final_hand):
                self.plyrDct[player].handRank = 6
                self.plyrDct[player].tieBreak = hands.flush_finder(final_hand)
            elif hands.straight_finder(straightranks):
                self.plyrDct[player].handRank = 5
                self.plyrDct[player].tieBreak = hands.straight_finder(straightranks)
            elif hands.three_of_a_kind_finder(pairranks):
                self.plyrDct[player].handRank = 4
                self.plyrDct[player].tieBreak = hands.three_of_a_kind_finder(pairranks)
            elif hands.two_pair_finder(pairranks):
                self.plyrDct[player].handRank = 3
                self.plyrDct[player].tieBreak = hands.two_pair_finder(pairranks)
            elif hands.one_pair_finder(pairranks):
                self.plyrDct[player].handRank = 2
                self.plyrDct[player].tieBreak = hands.one_pair_finder(pairranks)
            else:
                self.plyrDct[player].handRank = 1
                straightranks.sort(reverse=True)
                self.plyrDct[player].tieBreak = straightranks[:4]
                   
    # returns ([winners],amount, remainder) OR calls createSidePots()
    # should be called at end of hand, if more than 1 player is in inHand
    def showdown(self):
        self.assignHandRanks()
        # test to see if sidepots are necessary, if not then return winner(s) of pot
        sentinel = self.plyrDct[self.inHand[0]].contribute
        for plyr in self.inHand:
            if self.plyrDct[plyr].contribute == sentinel:
                continue
            else:
                break
        else:
            winners = self.bestHandAmong(self.inHand[:])
            for wnr in winners:
                self.plyrDct[wnr].stack_size += self.pot/len(winners)
            remainder = self.pot % len(winners)
            amount = self.pot/len(winners)
            self.pot = 0
            return amount,winners
        # else return sidepots and sidepotsElig
        return self.createSidePots()
        
    def createSidePots(self):
        # sidepots go here, make mainpot (sidepot[0])
        lowstack,lowman = self.findLowStack(self.inHand[:])
        self.sidepots.append(0)
        for plyr in self.playerOrder:
            self.sidepots[0] += min(self.plyrDct[lowman].startStack,self.plyrDct[plyr].contribute)
        self.sidepotsElig.append(self.inHand[:])
        firstPotWinners = self.bestHandAmong(self.sidepotsElig[0])
        if len(firstPotWinners) > 1:
            #split mainpot
            remainder = self.sidepots[0] % len(firstPotWinners)
            if remainder > 0:
                for wnr in firstPotWinners:
                    if remainder > 0:
                        self.plyrDct[wnr].stack_size += 1
                        remainder -= 1
            for wnr in firstPotWinners:
                self.plyrDct[wnr].stack_size += self.sidepots[0]/len(firstPotWinners)
        elif len(firstPotWinners) == 1:
            self.plyrDct[firstPotWinners[0]].stack_size += self.sidepots[0]
        for plyr in self.inHand[:]:
            if self.plyrDct[plyr].startStack == lowstack:
                self.inHand.remove(plyr)
        self.pot -= self.sidepots[0]
        ####### sidepot[0] done #######
        counter = 1
        while self.pot > 0:
            lowstack,lowman = self.findLowStack(self.inHand[:])
            self.sidepots.append(0)
            for plyr in self.playerOrder:
                self.sidepots[counter] += min(self.plyrDct[lowman].startStack,self.plyrDct[plyr].contribute)
            # right here subtract previous sidepots
            self.sidepots[counter] -= sum(self.sidepots[0:counter])
            self.sidepotsElig.append(self.inHand[:])
            potWinners = self.bestHandAmong(self.sidepotsElig[counter])
            for plyr in self.inHand[:]:
                if self.plyrDct[plyr].startStack == lowstack:
                    self.inHand.remove(plyr)
            self.pot -= self.sidepots[counter]
            counter += 1
        # reward for each other sidepot starting here
        eligTmp = self.sidepotsElig[1:]
        potsTmp = self.sidepots[1:]
        counter = 0
        for pot in potsTmp:
            winners = self.bestHandAmong(eligTmp[counter])
            if len(winners) > 1:
                #split pot, prematurely hands out odd chip
                remainder = potsTmp[counter] % len(winners)
                if remainder > 0:
                    for wnr in winners:
                        if remainder > 0:
                            self.plyrDct[wnr].stack_size += 1
                            remainder -= 1
                for wnr in winners:
                    self.plyrDct[wnr].stack_size += potsTmp[counter]/len(winners)
            elif len(winners) == 1:
                self.plyrDct[winners[0]].stack_size += potsTmp[counter]
            counter += 1
        return self.sidepots,self.sidepotsElig
            
            
            
    # takes a list of players with corresponding entries in plyrDct
    # returns lowstack(int) and lowman(string of player name)
    def findLowStack(self,players):
        lowstack = self.plyrDct[players[0]].startStack
        lowman = players[0]
        for plyr in players:
            if self.plyrDct[plyr].startStack < lowstack:
                lowstack = self.plyrDct[plyr].startStack
                lowman = plyr
        return lowstack,lowman
    
    # takes a list of players with corresponding entries in plyrDct
    # they need to have hands, and hand ranks been assigned
    # returns list of 1 or more players, more than 1 is absolute tie
    def bestHandAmong(self,players):
        tmpPlayers = []
        rankToBeat = 0
        for plyr in players:
            if self.plyrDct[plyr].handRank > rankToBeat:
                tmpPlayers = [plyr]
                rankToBeat = self.plyrDct[plyr].handRank
            elif self.plyrDct[plyr].handRank == rankToBeat:
                tmpPlayers.append(plyr)
        if len(tmpPlayers) > 1:
            tmpPlayers = hands.tieBreak(tmpPlayers,self.plyrDct)
        return tmpPlayers
            
    # !bad return value, two different formats of data could be returned!???
    # called after every round in a hand
    # ONLY returns something if ending the hand and more than one player remains
    def endRound(self):
        if self.round == 'preflop':
            self.costToPlay = 0
            self.minBet = self.bigBlind
            self.leftToAct = []
            tmp = self.playerOrder[1:]
            tmp.append(self.playerOrder[0])
            for plyr in tmp:
                self.plyrDct[plyr].contribute += self.plyrDct[plyr].in_front
                self.plyrDct[plyr].in_front = 0
                if plyr in self.inHand:
                    self.leftToAct.append(plyr)
            burnCard = self.deck.draw_card()
            for x in range(3):
                self.cardsInPlay.append(self.deck.draw_card())
            self.round = 'flop'
        elif self.round == 'flop':
            self.costToPlay = 0
            self.minBet = self.bigBlind
            self.leftToAct = []
            tmp = self.playerOrder[1:]
            tmp.append(self.playerOrder[0])
            for plyr in tmp:
                self.plyrDct[plyr].contribute += self.plyrDct[plyr].in_front
                self.plyrDct[plyr].in_front = 0
                if plyr in self.inHand:
                    self.leftToAct.append(plyr)
            burnCard = self.deck.draw_card()
            self.cardsInPlay.append(self.deck.draw_card())
            self.round = 'turn'
        elif self.round == 'turn':
            self.costToPlay = 0
            self.minBet = self.bigBlind
            self.leftToAct = []
            tmp = self.playerOrder[1:]
            tmp.append(self.playerOrder[0])
            for plyr in tmp:
                self.plyrDct[plyr].contribute += self.plyrDct[plyr].in_front
                self.plyrDct[plyr].in_front = 0
                if plyr in self.inHand:
                    self.leftToAct.append(plyr)
            burnCard = self.deck.draw_card()
            self.cardsInPlay.append(self.deck.draw_card())
            self.round = 'river'
        elif self.round == 'river':
            for plyr in self.playerOrder:
                self.plyrDct[plyr].contribute += self.plyrDct[plyr].in_front
            if len(self.inHand) > 1:
                self.round = 'showdown'
                # showdown() returns either 
                # int(amount), winners[list]
                # OR
                # [list of int amounts], [[lists],[of],[lists]]
                winners = self.showdown()
                return winners
            
    # if player is reduced to 0 chips after a hand, remove the player from the Table
    def deletePlayer(self,plyr):
        self.playerOrder.remove(plyr)
        if plyr in self.leftToAct:
            self.leftToAct.remove(plyr)
        if plyr in self.inHand:
            self.inHand.remove(plyr)
        del self.plyrDct[plyr]
            
    # resets the betting round to 'preflop', resets bet history, removes cardsInPlay, shuffle deck
    def clean(self):
        self.round = 'preflop'
        for plyr in self.playerOrder:
            self.plyrDct[plyr].in_front = 0
            self.plyrDct[plyr].handRank = 0
            self.plyrDct[plyr].hand = []
            self.plyrDct[plyr].contribute = 0
        self.minBet = self.bigBlind
        self.inHand = []
        self.leftToAct = []
        self.cardsInPlay = []
        self.costToPlay = 0
        self.sidepots = []
        self.sidepotsElig = []
        self.deck.renew()
    
    # move first(button) player to end of playerOrder
    def moveButton(self):
        tmp = self.playerOrder[0]
        self.playerOrder = self.playerOrder[1:]
        self.playerOrder.append(tmp)
            
