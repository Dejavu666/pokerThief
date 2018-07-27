# GUI layer

# Pull apart table object so no loop is ncsry
# table instance exists, each action by a player (input, func dispatched by gui widget)
# updates player and table amounts and returns nothing
# Actions that need to be dispatched to underlying table object:
# -get dependencies for instantiation from gui, istantiate object
# -seat players
# -hand actions
#   -deal_cards
#   -post_blinds
#   -check for 'skip all-in player'
#   -determine legal actions and parameter range, present to user/gui
#   -get player action and apply (update player attrs, table attrs) (alter left_to_act, in_hand, etc...)
#   -check for only one remaining player
#   -check for end of hand, if so check for ncsry create_sidepots(), showdown()
#   -after showdown(), should completely return, not be in any stacks besides gui mainloop
#   -if no return from 'one-remain-player' or 'showdown', advance round 


# Old gui uses root tk object with multiple frames dividing screen as children of root
# change to just dispatch actions from gui instead of so much logic
# currently, the player_window frame calls populate() on itself which presents legal player actions
# any of these actions call nextPlayer() which updates some info and calls populate() again to replenish the
# window with the next player information
# The above should be changed so that the first populate()(heretofore, get_action()(to be called after post_blinds() at the begin of a new hand, is a signal sent to table object
# table object should rotate to active player position (first player in left_to_act, table skips all-in players)
# and return a signal to present either bot-thinking or player-option window (returned with the player-option
# are the legal player actions and parameters, bot-window returns chosen bot action

# ... how to resolve end of hand checks...can put either at end of applied actions (bet/call/check)
# OR at the begin of populate()?...

# either bot-window.after(), or player input sends signal back to table of action to apply
# table applies action to itself...

# tkinter reference
# http://effbot.org/tkinterbook/
# https://docs.python.org/3/library/tkinter.html#a-simple-hello-world-program



import table
import tkinter as tk


class Player_window(tk.Frame):
    pass
class Left_panel_buttons(tk.Frame):
    pass
class Start_game_bar(tk.Frame):
    pass
class Table_window(tk.Frame):
    pass

# just a geometry organizer for other classes
class Main_application(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        # 4 child widgets
        self.player_window = Player_window()
        self.left_panel_buttons = Left_panel_buttons()
        self.start_game_bar = Start_game_bar()
        self.table_window = Table_window()
        # geometry packer
        self.player_window.pack(side="bottom", fill="x")
        self.start_game_bar.pack(side="top", fill="x")
        self.left_panel_buttons.pack(side="left", fill="y")
        self.table_window.pack(side="right", fill="both", expand=True)
        # constant image references held in class that inherits from TK root
#         self.cardBack = ImageTk.PhotoImage(Image.open('cardImages/cardBack.gif'))
#         self.noCard = ImageTk.PhotoImage(Image.open('cardImages/noCard.gif'))
#         self.chips = ImageTk.PhotoImage(Image.open('cardImages/chips.gif'))
        

root = tk.Tk()
root.geometry('1000x700')

room = Main_application(root)
room.pack(fill=tk.BOTH, expand=tk.YES)

root.mainloop()





# table = table.Table(4,1000,20)
# table.post_blinds()
# table.play_hand_loop()

# OLD GUI, too much tied to underlying layers
# should dispatch actions from gui, but all the logic should be in underlying object

import Tkinter as tk
import sys, deck, player, table
from PIL import Image, ImageTk


# NICE TO HAVE
# fit window and children to various screen-size
# revealing showdown hands in order from dealer's left
# bind hotkeys to player options (check,raise,call,bet,fold), change args to event=None, operate on room.table.leftToAct[0]
# when player(s) win, should tell what the hand is/show winning cards (the 5 of 7 used)

'''
Poker---
 startGameBar gets user input
 leftPanelButtons dispatch action
 tableWindow is visual "table area", shows community info
 playerWindow is visual "active player area" (bottom of screen), shows active player decisions
 
 important vars == room.numberOfPlayers, room.stackSize, room.bigBlindSize
 room.table, room.table.playerOrder, room.table.playerDict, room.table.leftToAct, room.table.inHand
 room.table.costToPlay, 
 room.imageList holds frames with visual player info, list is in same order as room.table.playerOrder
 dict room.imageList['player1'].c1 is the visual representation of room.playerDict['player1'].hand[0], ie first card
room.cardBack, room.noCard
'''
# 
# root = tk.Tk() 
# root.title("Poker")
# root.geometry("1025x720")
# root.configure(background="black")
# root.minsize(1025,720)
# 
# 
# # Press these buttons to walk through play
# class LeftPanelButtons(tk.Frame):
#     # creates buttons 
#     def __init__(self,parent):
#         tk.Frame.__init__(self,parent,bg='black',relief='ridge',bd=4)
#         self.lpbg = Image.open('cardImages/leftPanelbg.gif')
#         self.img_copy= self.lpbg.copy()
#         self.bgimg = ImageTk.PhotoImage(self.lpbg)
#         self.bg = tk.Label(self,image=self.bgimg)
#         self.bg.bind('<Configure>', self._resize_image)
#         self.bg.pack(fill=tk.BOTH, expand=tk.YES)
#         
#         # Press to move dealer button, eliminates any busted players
#         self.moveButton = tk.Button(self.bg,takefocus=1, text='Move Button',highlightbackground='darkred',command=self.moveButton)
#         self.moveButton.pack()
#         
#         # Press to deal 2 cards to all players
#         self.deal = tk.Button(self.bg,takefocus=1, text='Deal Cards',highlightbackground='darkred',command=self.dealCards)
#         self.deal.pack()
#         
#         # Press to post blinds
#         self.pstBlnds = tk.Button(self.bg,takefocus=1, text='Post Blinds',highlightbackground='darkred',command=self.postBlinds)
#         self.pstBlnds.pack()
#         
#         # Press to start hand, get first action from player
#         self.gtActn = tk.Button(self.bg,takefocus=1,text='Get Action',highlightbackground='darkred',command=self.getAction)
#         self.gtActn.pack()
#         
#         # Press to reveal all hands
#         self.shwHands = tk.Button(self.bg,text='Show Hands',highlightbackground='darkred',command=self.showHands)
#         self.shwHands.pack()
#         
#         # Press to reset everything, should happen between hands
#         self.clnUp = tk.Button(self.bg,text='Clean',highlightbackground='darkred',command=self.cleanUp)
#         self.clnUp.pack()
#         
#     # move dealer button and eliminate busted players, called by self.moveButton button
#     def moveButton(self):
#         room.table.moveButton()
#         room.imageList[room.table.playerOrder[-1]].dealerButton.configure(text='')
#         room.imageList[room.table.playerOrder[0]].dealerButton.configure(text='Dealer')
#         for plyr in room.table.playerOrder[:]:
#             if room.table.playerDict[plyr].stackSize == 0:
#                 room.tableWindow.deletePlayer(plyr)
#                 
#     # deals 2 cards to all players, called by self.deal button
#     def dealCards(self):
#         room.table.dealCards()
#         for plyr in room.table.playerOrder:
#             room.imageList[plyr].c1.configure(image=room.cardBack)
#             room.imageList[plyr].c2.configure(image=room.cardBack)
#                 
#     # post blinds, called by self.pstBlinds button
#     def postBlinds(self):
#         room.table.postBlinds()
#         room.tableWindow.updateTableChips()
#         
#     # calls populate() to get the first action, called by self.gtActn button
#     def getAction(self):
#         room.playerWindow.populate()
#         
#     # reveal each player's hand, called by self.shwHands button
#     def showHands(self,event=None):
#         for plyr in room.table.playerOrder:
#             if room.table.playerDict[plyr].hand != []:
#                 room.imageList[plyr].img1 = ImageTk.PhotoImage(Image.open('cardImages/'+room.table.playerDict[plyr].hand[0]+'.gif'))
#                 room.imageList[plyr].c1.configure(image=room.imageList[plyr].img1)
#                 room.imageList[plyr].img2 = ImageTk.PhotoImage(Image.open('cardImages/'+room.table.playerDict[plyr].hand[1]+'.gif'))
#                 room.imageList[plyr].c2.configure(image=room.imageList[plyr].img2)
#             
#     # reset, called by self.clnUp button
#     def cleanUp(self):
#         room.tableWindow.clean()
#         
#     # resize background image on window resize
#     def _resize_image(self,event):
#         new_width = event.width # event.width is new window width
#         new_height = event.height # event.height is new window height
#         self.image = self.img_copy.resize((new_width, new_height)) # image becomes same size as window
#         self.bgImg = ImageTk.PhotoImage(self.image) # change to ImageTk
#         self.bg.configure(image = self.bgImg) 
#             
# # active player's actions are chosen here (bottom window), actions are dispatched to underlying table Class
# # working here, gui tieBreak displays wrong number of chips awarded, actual amount is correct
# class PlayerWindow(tk.Frame):
#     def __init__(self,parent):
#         tk.Frame.__init__(self,parent,bg='black',relief='ridge',bd=4)
#         tmpImage = Image.open('cardImages/placeholder.gif').resize((130,130))
#         self.playerImage = ImageTk.PhotoImage(tmpImage)
#         self.playerImg = tk.Label(self,image=self.playerImage,bg='black')
#         self.playerImg.pack(side='left')
#         self.plyrMsg = tk.Label(self,text='Welcome to Poker',bg='black',fg='wheat3')
#         self.plyrMsg.pack()
#         self.card1 = tk.Label(self,image=None,bg='black')
#         self.card1.pack(side='left')
#         self.card2 = tk.Label(self,image=None,bg='black')
#         self.card2.pack(side='left')
#         
#     # dispatch self.check(),self.bet(),self.fold()
#     def createCheckButtons(self,plyr):
#         self.b1 =  tk.Button(self,text='Check',highlightbackground='black',font=('Helvetica',16),command=lambda:self.check(plyr))
#         self.b1.pack(side='left')
#         self.b2 = tk.Button(self,text='Bet',highlightbackground='black',font=('Helvetica',16),command=lambda:self.bet(plyr))
#         self.b2.pack(side='left')
#         self.wagerEntry = tk.Scale(self,from_=min(room.table.playerDict[plyr].stackSize,room.table.minBet),to=room.table.playerDict[plyr].stackSize,orient='horizontal',resolution=10,bg='black',fg='wheat3')
#         self.wagerEntry.pack(side='left')
#         self.b3 = tk.Button(self,text='Fold',highlightbackground='black',font=('Helvetica',16),command=lambda:self.fold(plyr))
#         self.b3.pack(side='left')
#         
#     # dispatch self.call(),self.Raise(),self.fold()
#     def createCallButtons(self,plyr):
#         self.b1 = tk.Button(self,text='Call '+str(min(room.table.playerDict[plyr].stackSize,room.table.costToPlay-room.table.playerDict[plyr].inFront)),highlightbackground='black',font=('Helvetica',16),command=lambda:self.call(plyr))
#         self.b1.pack(side='left')
#         # player cannot raise if only enough to call, do not create the button
#         if room.table.playerDict[plyr].stackSize > room.table.costToPlay-room.table.playerDict[plyr].inFront:
#             self.b2 = tk.Button(self,text='Raise',highlightbackground='black',font=('Helvetica',16),command=lambda:self.Raise(plyr))
#             self.b2.pack(side='left')
#             self.wagerEntry = tk.Scale(self,from_=min(room.table.playerDict[plyr].stackSize-room.table.costToPlay+room.table.playerDict[plyr].inFront,room.table.minBet),to=min(room.table.playerDict[plyr].stackSize,room.table.playerDict[plyr].stackSize-room.table.costToPlay+room.table.playerDict[plyr].inFront),orient='horizontal',resolution=10,bg='black',fg='wheat3')
#             self.wagerEntry.pack(side='left')
#         self.b3 = tk.Button(self,text='Fold',highlightbackground='black',font=('Helvetica',16),command=lambda:self.fold(plyr))
#         self.b3.pack(side='left')
#         
#     def createCurrentPlayerImage(self,plyr):
#         self.plyrMsg.configure(text='What will '+plyr+' do?')
#         self.cardimg1 = ImageTk.PhotoImage(Image.open('cardImages/'+room.table.playerDict[plyr].hand[0]+'.gif'))
#         self.card1.configure(image=self.cardimg1)
#         self.cardimg2 = ImageTk.PhotoImage(Image.open('cardImages/'+room.table.playerDict[plyr].hand[1]+'.gif'))
#         self.card2.configure(image=self.cardimg2)
#         
#     def createBotPlayerImage(self,plyr):
#         self.plyrMsg.configure(text='Robot '+plyr+' is thinking...')
#         # WORKING HERE
#         self.card1.configure(image=room.cardBack)
#         self.card2.configure(image=room.cardBack)
# 
# # this populates the player area with current player info
#     def populate(self):
#         # skip player if all-in
#         # WORKING HERE list index out of range error
#         print(room.table.playerDict, ' is playerDict')
#         print(room.table.leftToAct, ' is leftToAct')
#         if room.table.leftToAct != []:
#             if room.table.playerDict[room.table.leftToAct[0]].stackSize == 0:
#                 room.table.leftToAct.remove(room.table.leftToAct[0])
#                 if room.table.leftToAct == []:
#                     self.endRound()
#                 else:
#                     # memory leak? nextPlayer calls populate until?
#                     self.nextPlayer()
#         # end skip player if all in
#         plyr = room.table.leftToAct[0]
#         # WORKING
#         # IF PLAYER IS BOT
#         if room.table.playerDict[plyr].human == 0:
#             self.plyrMsg.configure(text='Robot '+plyr+' is thinking...')
#             self.createBotPlayerImage(plyr)
#             # If pot is open
#             if room.table.playerDict[plyr].inFront == room.table.costToPlay:
#                 # do i need to pass the table object or can i refer to it from bot/player instance?
#                 botAction, maybeAmount = room.table.playerDict[plyr].getRandomCheckAction(plyr,room.table)
#                 if botAction == 'check':
#                     self.check(plyr)
#                 else:
#                     self.bet(plyr,maybeAmount)
#             # pot is not open
#             else:
#                 botAction, maybeAmount = room.table.playerDict[plyr].getRandomCallAction(plyr,room.table)
#                 if botAction == 'call':
#                     self.call(plyr)
#                 elif botAction == 'raise':
#                     self.Raise(plyr,maybeAmount)
#                 else:
#                     self.fold(plyr)
#         else:# actions for human user
#             self.createCurrentPlayerImage(plyr)
#             if room.table.playerDict[plyr].inFront == room.table.costToPlay:
#                 self.createCheckButtons(plyr)
#             else:
#                 self.createCallButtons(plyr)
#         
#     # these call underlying table methods
#     # then nextPlayer()|endRound()
#     
#     def call(self,currentPlyr):
#         room.table.call(currentPlyr)
#         room.tableWindow.updateTableChips()
#         self.destroyButtons()
#         if room.table.leftToAct != []:
#             self.nextPlayer()
#         else:
#             self.endRound()
#         
#     # note Raise instead of raise
#     def Raise(self,currentPlyr,amount=0):
#         try:
#             amount = self.wagerEntry.get()
#         except:
#             pass
#         room.table.Raise(currentPlyr,amount)
#         room.tableWindow.updateTableChips()
#         self.destroyButtons()
#         if room.table.leftToAct != []:
#             self.nextPlayer()
#         else:
#             self.endRound()
#         
#     def fold(self,currentPlyr):
#         room.table.fold(currentPlyr)
#         room.tableWindow.updateTableChips()
#         room.imageList[currentPlyr].c1.configure(image=room.noCard)
#         room.imageList[currentPlyr].c2.configure(image=room.noCard)
#         self.destroyButtons()
#         if room.table.leftToAct != []:
#             self.nextPlayer()
#         else:
#             self.endRound()
#         
#     def bet(self,currentPlyr,amount=0):
#         try:
#             amount = self.wagerEntry.get()
#         except:
#             pass
#         room.table.bet(currentPlyr,amount)
#         room.tableWindow.updateTableChips()
#         self.destroyButtons()
#         if room.table.leftToAct != []:
#             self.nextPlayer()
#         else:
#             self.endRound()
#     
#     def check(self,currentPlyr):
#         room.table.check(currentPlyr)
#         room.tableWindow.updateTableChips()
#         self.destroyButtons()
#         if room.table.leftToAct != []:
#             self.nextPlayer()
#         else:
#             self.endRound()
#         
#         
#         # remove this, and other logic from gui
#     # nextPlayer is only called when leftToAct has at least one remaining player
#     def nextPlayer(self):
#         # check if folded around to last player, regardless of last player all-in status
#         if len(room.table.leftToAct) == 1 and len(room.table.inHand) == 1:
#             tmp = room.table.pot
#             room.table.playerDict[room.table.leftToAct[0]].stackSize += room.table.pot
#             room.table.pot = 0
#             room.tableWindow.updateTableChips()
#             self.plyrMsg.configure(text=room.table.leftToAct[0]+' Wins '+str(tmp)+' chips!')
#         else:
#             self.populate()
#     
#     def endRound(self):
#         tmpPot = room.table.pot
#         # WORKING HERE BUG1
#         # if folded around to player, reward last player and return
#         if room.table.leftToAct == [] and len(room.table.inHand) == 1: 
#             tmp = room.table.pot
#             room.table.playerDict[room.table.inHand[0]].stackSize += room.table.pot
#             room.table.pot = 0
#             room.tableWindow.updateTableChips()
#             self.plyrMsg.configure(text=room.table.inHand[0]+' Wins '+str(tmp)+' chips!')
#             return
#         winners = room.table.endRound()
#         if winners:
#             # pots is either an int in the case of 'no sidepots', or a list of ints
#             pots = winners[0]
#             # potsElig is either a list of players in the case of 'no sidepots', or a list of lists of players
#             potsElig = winners[1]
#         room.tableWindow.updateTableChips()
#         if room.table.round == 'flop':
#             room.tableWindow.dealFlop()
#             room.playerWindow.populate()
#         elif room.table.round == 'turn':
#             room.tableWindow.dealTurn()
#             room.playerWindow.populate()
#         elif room.table.round == 'river':
#             room.tableWindow.dealRiver()
#             room.playerWindow.populate()
#         elif room.table.round == 'showdown':
#             if winners:
#                 print winners
#                 # check for 'no sidepots' or 'sidepots in showWinners
#                 self.showWinners(pots,potsElig)
#             
#     def destroyButtons(self):
#         try:
#             self.b1.destroy()
#             self.b2.destroy()
#             self.b3.destroy()
#             self.wagerEntry.destroy()
#             self.card1.configure(image=None)
#             self.card2.configure(image=None)
#         except:
#             pass
#     # pots is either int or list of ints, eligPlayers is either list of players or list of lists of players
#     # no sidepots: eligPlayers == ['player1','player2'],pots == 500
#     # sidepots: eligPlayers == [['player1','player2','player3'],['player2','player3']], pots == [180,100,100]
#     def showWinners(self,pots,eligPlayers):
#         plyrs = eligPlayers
#         # check if sidepots happened
#         if type(pots) == int: # no sidepots happened/sidepots would be type list
#             self.plyrMsg.configure(text=plyrs[0]+' Wins '+str(pots)+' chips!')
#             self.cardimg1 = ImageTk.PhotoImage(Image.open('cardImages/'+room.table.playerDict[plyrs[0]].hand[0]+'.gif'))
#             self.card1.configure(image=self.cardimg1)
#             self.cardimg2 = ImageTk.PhotoImage(Image.open('cardImages/'+room.table.playerDict[plyrs[0]].hand[1]+'.gif'))
#             self.card2.configure(image=self.cardimg2)
#             room.imageList[plyrs[0]].c1.configure(image=self.cardimg1)
#             room.imageList[plyrs[0]].c2.configure(image=self.cardimg2)
#             if len(plyrs) > 1:
#                 plyrs = plyrs[1:]
#                 self.after(3300,self.showWinners,pots,plyrs)
#         else:
#             # sidepots happened
#             # delays showing of players in gui
#             if pots != []:
#                 self.after(3300,self.showSidepotWinners,pots[0],plyrs[0])
#                 pots.remove(pots[0])
#                 plyrs.remove(plyrs[0])
#                 self.after(3300,self.showWinners,pots,plyrs)
#                 
#     # should pass in one pot and list of eligible players?
#     # need to find bestHandAmong the eligible players
#     def showSidepotWinners(self,pots,plyrs):
#         # plyrs is a list of one or more players
#         plyrs = room.table.bestHandAmong(plyrs)
#         self.plyrMsg.configure(text=plyrs[0]+' Wins '+str(pots/len(plyrs))+' chips!')
#         self.cardimg1 = ImageTk.PhotoImage(Image.open('cardImages/'+room.table.playerDict[plyrs[0]].hand[0]+'.gif'))
#         self.card1.configure(image=self.cardimg1)
#         self.cardimg2 = ImageTk.PhotoImage(Image.open('cardImages/'+room.table.playerDict[plyrs[0]].hand[1]+'.gif'))
#         self.card2.configure(image=self.cardimg2)
#         # imageList saves the images so not gc'ed
#         room.imageList[plyrs[0]].c1.configure(image=self.cardimg1)
#         room.imageList[plyrs[0]].c2.configure(image=self.cardimg2)
#         if len(plyrs) > 1:
#             pots -= pots/len(plyrs)
#             plyrs = plyrs[1:]
#             self.after(2300,self.showSidepotWinners,pots,plyrs)
#         
#             
# # holds all gui elements in middle window ("table" area), images for each player, community cards, chips
# class TableWindow(tk.Frame):
#     def __init__(self,parent):
#         tk.Frame.__init__(self,parent,relief='ridge',bd=4)
#         self.image = Image.open("background.gif") # open image as instance of self
#         self.img_copy= self.image.copy() # copy made for later resizing
#         self.background_image = ImageTk.PhotoImage(self.image) # changed to ImageTk
#         self.background = tk.Label(self, image=self.background_image) # label as background
#         self.background.bind('<Configure>', self._resize_image) # bind to resize window
#         self.background.pack(fill=tk.BOTH, expand=tk.YES)
#         
#     # initialize pot and community cards gui area
#     def createChipImages(self):
#         self.chipFrame = tk.Frame(self.background,bg='black',relief='groove',bd=4)
#         self.numFrame = tk.Frame(self.chipFrame,bg='black',relief='raised',bd=3)
#         self.chips = tk.Label(self.numFrame,text=0,font=('Helvetica',22),bg='black',fg='wheat3')
#         self.chips.pack(side='top')
#         self.chipImage = tk.Label(self.numFrame,image=room.chips,bg='black')
#         self.chipImage.pack(side='top')
#         self.numFrame.pack(side='left')
#         self.chipFrame.grid(row=2,column=1,columnspan=2)
#         self.card1 = tk.Label(self.chipFrame,image=room.noCard,bg='black')
#         self.card1.pack(side='left')
#         self.card2 = tk.Label(self.chipFrame,image=room.noCard,bg='black')
#         self.card2.pack(side='left')
#         self.card3 = tk.Label(self.chipFrame,image=room.noCard,bg='black')
#         self.card3.pack(side='left')
#         self.card4 = tk.Label(self.chipFrame,image=room.noCard,bg='black')
#         self.card4.pack(side='left')
#         self.card5 = tk.Label(self.chipFrame,image=room.noCard,bg='black')
#         self.card5.pack(side='left')
#         
#     # called after player decisions, update all player chips and pot chip amount
#     def updateTableChips(self):
#         self.chips.configure(text=room.table.pot)
#         for plyr in room.table.playerOrder:
#             room.imageList[plyr].stack.configure(text=room.table.playerDict[plyr].stackSize)
#         
#     # get and reveal gui images of dealt cards
#     def dealFlop(self):
#         self.card1img = ImageTk.PhotoImage(Image.open('cardImages/'+room.table.cardsInPlay[0]+'.gif'))
#         self.card1.configure(image=self.card1img)
#         self.card2img = ImageTk.PhotoImage(Image.open('cardImages/'+room.table.cardsInPlay[1]+'.gif'))
#         self.card2.configure(image=self.card2img)
#         self.card3img = ImageTk.PhotoImage(Image.open('cardImages/'+room.table.cardsInPlay[2]+'.gif'))
#         self.card3.configure(image=self.card3img)
#         
#     def dealTurn(self):
#         self.card4img = ImageTk.PhotoImage(Image.open('cardImages/'+room.table.cardsInPlay[3]+'.gif'))
#         self.card4.configure(image=self.card4img)
#         
#     def dealRiver(self):
#         self.card5img = ImageTk.PhotoImage(Image.open('cardImages/'+room.table.cardsInPlay[4]+'.gif'))
#         self.card5.configure(image=self.card5img)
#         
#     # create room.imagelist dictionary, places images in seating order
#     # reference the IMAGES on each players window like so:
#     # room.imageList['player1'].stack, .c1 (card1), .c2 (card2)
#     # create grid layout depending on number of players
#     def createPlayerImages(self,plyrOrder):
#         room.imageList = {}
#         row = 1
#         column = 1
#         counter = 1
#         for plyr in plyrOrder:
#             self.w = tk.Frame(self.background,relief='ridge',bd=4,background='black')
#             self.w.info = tk.Frame(self.w,relief='ridge',bd=3,background='black')
#             self.w.plyrImg = ImageTk.PhotoImage(Image.open('cardImages/playerImage.gif').resize((60,50)))
#             self.w.pic = tk.Label(self.w.info,image=self.w.plyrImg,bg='black')
#             self.w.pic.pack(side='left')
#             self.w.player = tk.Label(self.w.info,text=plyr,fg='wheat3',bg='black')
#             self.w.player.pack(side='top')
#             self.w.stack = tk.Label(self.w.info,text=room.table.playerDict[plyr].stackSize,bg='black',fg='wheat3')
#             self.w.stack.pack(side='top')
#             self.w.dealerButton = tk.Label(self.w.info,text = '',fg='wheat3',bg='black')
#             self.w.dealerButton.pack(side='top')
#             self.w.info.pack(side='top')
#             self.w.c1 = tk.Label(self.w,image=room.noCard,background='black')
#             self.w.c1.pack(side='left')
#             self.w.c2 = tk.Label(self.w,image=room.noCard,background='black')
#             self.w.c2.pack(side='left')
#             self.w.grid(row=row,column=column,padx=25,pady=4)
#             room.imageList[plyr] = self.w
#             counter += 1
#             # uses tkinter grid layout
#             if counter < 5:
#                 column += 1
#             elif counter == 5:
#                 column = 4
#                 row = 2
#             elif counter == 6:
#                 column = 4
#                 row = 3
#             elif counter == 7:
#                 column = 3
#                 row = 3
#             elif counter == 8:
#                 column = 2
#                 row = 3
#             elif counter == 9:
#                 column = 1
#                 row = 3
#         room.imageList[room.table.playerOrder[0]].dealerButton.configure(text='Dealer')
#             
#     def deletePlayer(self,plyr):
#         room.table.deletePlayer(plyr)
#         room.imageList[plyr].destroy()
#             
#     # clean all gui elements for next hand, calls underlying table clean
#     def clean(self):
#         room.table.clean()
#         for plyr in room.table.playerOrder:
#             room.imageList[plyr].c1.configure(image=room.noCard)
#             room.imageList[plyr].c2.configure(image=room.noCard)
#         self.card1.configure(image=room.noCard)
#         self.card2.configure(image=room.noCard)
#         self.card3.configure(image=room.noCard)
#         self.card4.configure(image=room.noCard)
#         self.card5.configure(image=room.noCard)
#         self.updateTableChips()
#         room.playerWindow.card1.configure(image=room.noCard)
#         room.playerWindow.card2.configure(image=room.noCard)
#         room.playerWindow.plyrMsg.configure(text='')
#         room.playerWindow.b1.destroy()
#         room.playerWindow.b2.destroy()
#         room.playerWindow.b3.destroy()
#         room.playerWindow.wagerEntry.destroy()
#         
#     # resize background image
#     def _resize_image(self,event):
#         new_width = event.width # event.width is new window width
#         new_height = event.height # event.height is new window height
#         self.image = self.img_copy.resize((new_width, new_height)) # image becomes same size as window
#         self.background_image = ImageTk.PhotoImage(self.image) # change to ImageTk
#         self.background.configure(image =  self.background_image) 
#         
# # bar across top of window
# # summons StartGamePopup, "seats" players, summons QuitGamePopup
# # gets initial values, ie room.numberOfPlayers, room.stackSize, room.bigBlindSize
# class StartGameBar(tk.Frame):
#     def __init__(self,parent):
#         tk.Frame.__init__(self,parent,bg='black',relief='ridge',bd=4)
#         self.b=tk.Button(self,takefocus=1,text="Start Game!",highlightbackground='black',command=self.startGameEntries)
#         self.b.pack(side='left')
#         self.seatPlayerButton = tk.Button(self,state='disabled',takefocus=1,text='Seat Players',highlightbackground='black',command=self.seatPlayers)
#         self.seatPlayerButton.pack(side='left')
#         self.quitButton = tk.Button(self,takefocus=1,text='Quit',highlightbackground='black',command=self.areYouSureQuit)
#         self.quitButton.pack(side='left')
#     
#     def seatPlayers(self):
#         self.seatPlayerButton.configure(state='disabled')
#         room.table = table.Table(bigBlind=room.bigBlindSize)
#         plyrList = []
#         for x in range(room.numberOfPlayers):
#             plyrList.append('player'+str(x+1))
#         room.table.seatPlayers(plyrList,room.stackSize)
#         room.tableWindow.createPlayerImages(room.table.playerOrder)
#         room.tableWindow.createChipImages()
#         
#     def areYouSureQuit(self):
#         self.quitGamePopup = QuitGamePopup(self)
#         
#     def startGameEntries(self):
#         self.startGamePopup = StartGamePopup(self)
#         self.wait_window(self.startGamePopup.top)
#         
# # gets input from user numPlayers,stackSize,bigBlind 
# # stored as room.numberOfPlayers,room.stackSize,room.bigBlindSize
# class StartGamePopup(object):
#     def __init__(self,root):
#         self.top = tk.Toplevel(root,bg='black',relief='ridge',bd=4)
#         self.top.geometry('700x330')
#         self.top.grab_set()
#         self.players = tk.Label(self.top,bg='black',fg='burlywood1',text="How Many players?\n2-9",font=('Courier bold',26))
#         self.players.pack()
#         self.playersEntry = tk.Entry(self.top,relief='raised')
#         self.playersEntry.pack()
#         self.stackSize = tk.Label(self.top,bg='black',fg='burlywood1',text="What is the starting stack size?\nIncrements of 10, at least 100",font=('Courier bold',26))
#         self.stackSize.pack()
#         self.stackSizeEntry = tk.Entry(self.top,relief='raised')
#         self.stackSizeEntry.pack() 
#         self.bigBlind = tk.Label(self.top,bg='black',fg='burlywood1',text="What is the big blind value?\nIncrements of 20,\n at most, ten percent of stack size",font=('Courier bold',26))
#         self.bigBlind.pack()
#         self.bigBlindEntry = tk.Entry(self.top,relief='raised')
#         self.bigBlindEntry.pack()
#         self.b=tk.Button(self.top,relief='raised',text='Ok',fg='blue2',font=("Helvetica bold italic",26)\
#        ,takefocus=1,command=self.verify)
#         self.b.pack()
#     
#     # verify that number of players, starting stack and blinds are valid values
#     def verify(self):
#         room.numberOfPlayers = self.playersEntry.get()
#         room.stackSize = self.stackSizeEntry.get()
#         room.bigBlindSize = self.bigBlindEntry.get()
#         try:
#             room.numberOfPlayers = int(room.numberOfPlayers)
#             if room.numberOfPlayers < 2 or room.numberOfPlayers > 9:
#                 raise
#             room.stackSize = int(room.stackSize)
#             if room.stackSize % 10 != 0 or room.stackSize < 100:
#                 raise
#             room.bigBlindSize = int(room.bigBlindSize)
#             if room.bigBlindSize % 20 != 0 or room.stackSize/10 < room.bigBlindSize:
#                 raise
#             self.top.destroy()
#         except:
#             pass
#         room.startGameBar.seatPlayerButton.configure(state='normal')
#         
# class QuitGamePopup(object):
#     def __init__(self,parent):
#         self.top = tk.Toplevel(parent,bg='black',relief='ridge',bd=4)
#         self.top.minsize(420,120)
#         self.top.maxsize(420,120)
#         self.players = tk.Label(self.top,text="Would You Like To Quit?",fg='burlywood1',bg='black',font=("Courier bold", 28))
#         self.players.pack()
#         self.yes = tk.Button(self.top,text='Yes',takefocus=1,font=("Gothic", 16),highlightbackground='black',command=self.getMeOutOfHere)
#         self.yes.pack()
#         self.no = tk.Button(self.top,takefocus=1,text="No, don't quit",font=("Gothic", 16),highlightbackground='black', command=self.top.destroy)
#         self.no.pack()
#         
#     def getMeOutOfHere(self):
#         self.top.destroy()
#         sys.exit()
#         
# # just a geometry organizer for other classes
# class MainApplication(tk.Frame):
#     def __init__(self, parent):
#         tk.Frame.__init__(self, parent)
#         # 4 child widgets
#         self.playerWindow = PlayerWindow(self)
#         self.leftPanelButtons = LeftPanelButtons(self)
#         self.startGameBar = StartGameBar(self)
#         self.tableWindow = TableWindow(self)
#         # geometry packer
#         self.playerWindow.pack(side="bottom", fill="x")
#         self.startGameBar.pack(side="top", fill="x")
#         self.leftPanelButtons.pack(side="left", fill="y")
#         self.tableWindow.pack(side="right", fill="both", expand=True)
#         # constant image references held in class that inherits from TK root
#         self.cardBack = ImageTk.PhotoImage(Image.open('cardImages/cardBack.gif'))
#         self.noCard = ImageTk.PhotoImage(Image.open('cardImages/noCard.gif'))
#         self.chips = ImageTk.PhotoImage(Image.open('cardImages/chips.gif'))
#         
# if __name__ == "__main__":
#     room = MainApplication(root)
#     room.pack(fill=tk.BOTH, expand=tk.YES)
#     # keyboard shortcuts
#     #root.bind("c",room.leftPanelButtons.showHands)
#     root.mainloop()