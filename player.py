from random import randrange
# Players are instantiated in a dict belonging to a Table object
# keys are the Player's name, values are the Player instance
class Player():
    def __init__(self, stack_size=0):
        self.stack_size = stack_size
        self.hand = []
        # tracks how many chips have been bet by a player this round, reset every round
        self.chips_this_round = 0
        # tracks how many chips a player has at the begin of a hand
        self.start_stack = 0
        # tracks how much player has contributed to a pot, reset every hand
        self.chips_in_pot = 0
        # signify if instance is human or computer
        self.human = 0

    def discard_hand(self):
        self.hand = []

    def draw_card(self,card):
        self.hand.append(card)
        
    def contribute_chips(self, amount):
        assert(amount <= self.stack_size)
        self.chips_in_pot += amount
        self.chips_this_round += amount
        self.stack_size -= amount
    
    # bot needs all irreducible info, but start with:
    # stacksize, cost2play, com_cards,
    def bot_action(self, cost2play, bb, minbet):
        if self.chips_this_round == cost2play:# table is open
            # placeholder for testing
            # gets random bot action between possible actions
            # AI INTERFACE GOES HERE
            randval = randrange(0,1)
            if randval == 0:
                amount = randrange(bb,self.stack_size)
                return ('bet',amount)
            elif randval == 1:
                return ('check',0)
        else:#table is bet
            assert(cost2play > self.chips_this_round)
            randval = randrange(0,2)
            if randval == 0:
                return ('call',min(self.stack_size, cost2play-self.chips_this_round))
            elif randval == 1:
                amount = randrange(min(minbet,self.stack_size), self.stack_size)
                return ('raise', amount)
            elif randval == 2:
                return ('fold',0)



#********* BOT STUFF ******************************************************************************
# from random import randrange
    # check or bet
#     def getRandomCheckAction(self,plyr,table):
#         if table.minBet >= table.plyrDct[plyr].stack_size:
#             amount = table.plyrDct[plyr].stack_size
#         else:
#             amount = randrange(table.minBet, table.plyrDct[plyr].stack_size)
#         return ("check",0) if randrange(0,2) else ("bet",amount)
#     # fold, call, or raise
#     def getRandomCallAction(self,plyr,table):
#         choice = randrange(0,3)
#         if choice == 0:
#             return ("fold",0)
#         elif choice == 1:
#             return ("call",0)
#         else:
#             if table.costToPlay >= table.plyrDct[plyr].stack_size:
#                 amount = table.plyrDct[plyr].stack_size
#             else:
#                 amount = randrange(table.costToPlay, table.plyrDct[plyr].stack_size)
#             return ("raise",amount)
# 
#     
#     def callingStationAction(self):
#         return "call" if randrange(0,1) else "check"