import table
import tkinter as tk
from PIL import Image, ImageTk
import sys


class Player_window(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self,parent,bg='black',relief='ridge',bd=4)
        tmpImage = Image.open('res/placeholder.gif').resize((130,130))
        self.playerImage = ImageTk.PhotoImage(tmpImage)
        self.playerImg = tk.Label(self,image=self.playerImage,bg='black')
        self.playerImg.pack(side='left')
        self.plyrMsg = tk.Label(self,text='Welcome to Poker',bg='black',fg='maroon')
        self.plyrMsg.pack()
        self.card1 = tk.Label(self,image=None,bg='black')
        self.card1.pack(side='left')
        self.card2 = tk.Label(self,image=None,bg='black')
        self.card2.pack(side='left')
        
    # dispatch self.check(),self.bet(),self.fold()
    def create_check_buttons(self,plyr):
        self.b1 =  tk.Button(self,text='Check',highlightbackground='black',font=('Helvetica',16),command=lambda:self.check(plyr))
        self.b1.pack(side='left')
        self.b2 = tk.Button(self,text='Bet',highlightbackground='black',font=('Helvetica',16),command=lambda:self.bet(plyr))
        self.b2.pack(side='left')
        self.wagerEntry = tk.Scale(self,from_=min(room.table.playerDict[plyr].stackSize,room.table.minBet),to=room.table.playerDict[plyr].stackSize,orient='horizontal',resolution=10,bg='black',fg='wheat3')
        self.wagerEntry.pack(side='left')
        self.b3 = tk.Button(self,text='Fold',highlightbackground='black',font=('Helvetica',16),command=lambda:self.fold(plyr))
        self.b3.pack(side='left')
        
    # dispatch self.call(),self.Raise(),self.fold()
    def create_call_buttons(self,plyr):
        self.b1 = tk.Button(self,text='Call '+str(min(room.table.playerDict[plyr].stackSize,room.table.costToPlay-room.table.playerDict[plyr].inFront)),highlightbackground='black',font=('Helvetica',16),command=lambda:self.call(plyr))
        self.b1.pack(side='left')
        # player cannot raise if only enough to call, do not create the button
        if room.table.playerDict[plyr].stackSize > room.table.costToPlay-room.table.playerDict[plyr].inFront:
            self.b2 = tk.Button(self,text='Raise',highlightbackground='black',font=('Helvetica',16),command=lambda:self.Raise(plyr))
            self.b2.pack(side='left')
            self.wagerEntry = tk.Scale(self,from_=min(room.table.playerDict[plyr].stackSize-room.table.costToPlay+room.table.playerDict[plyr].inFront,room.table.minBet),to=min(room.table.playerDict[plyr].stackSize,room.table.playerDict[plyr].stackSize-room.table.costToPlay+room.table.playerDict[plyr].inFront),orient='horizontal',resolution=10,bg='black',fg='wheat3')
            self.wagerEntry.pack(side='left')
        self.b3 = tk.Button(self,text='Fold',highlightbackground='black',font=('Helvetica',16),command=lambda:self.fold(plyr))
        self.b3.pack(side='left')
        
    def create_currentplyr_image(self,plyr):
        self.plyrMsg.configure(text='What will '+plyr+' do?')
        self.cardimg1 = ImageTk.PhotoImage(Image.open('res/'+room.table.playerDict[plyr].hand[0]+'.gif'))
        self.card1.configure(image=self.cardimg1)
        self.cardimg2 = ImageTk.PhotoImage(Image.open('res/'+room.table.playerDict[plyr].hand[1]+'.gif'))
        self.card2.configure(image=self.cardimg2)
        
    # subsume into above
    def createBotPlayerImage(self,plyr):
        self.plyrMsg.configure(text='Robot '+plyr+' is thinking...')
        # WORKING HERE
        self.card1.configure(image=room.cardBack)
        self.card2.configure(image=room.cardBack)

# this populates the player area with current player info
# input is player string and repr of legal player options (
    def populate(self, plyr, options):
        plyr = room.table.leftToAct[0]
        # WORKING
        # IF PLAYER IS BOT
        if room.table.playerDict[plyr].human == 0:
            self.plyrMsg.configure(text='Robot '+plyr+' is thinking...')
            self.createBotPlayerImage(plyr)
            # If pot is open
            if room.table.playerDict[plyr].inFront == room.table.costToPlay:
                # do i need to pass the table object or can i refer to it from bot/player instance?
                botAction, maybeAmount = room.table.playerDict[plyr].getRandomCheckAction(plyr,room.table)
                if botAction == 'check':
                    self.check(plyr)
                else:
                    self.bet(plyr,maybeAmount)
            # pot is not open
            else:
                botAction, maybeAmount = room.table.playerDict[plyr].getRandomCallAction(plyr,room.table)
                if botAction == 'call':
                    self.call(plyr)
                elif botAction == 'raise':
                    self.Raise(plyr,maybeAmount)
                else:
                    self.fold(plyr)
        else:# actions for human user
            self.createCurrentPlayerImage(plyr)
            if room.table.playerDict[plyr].inFront == room.table.costToPlay:
                self.createCheckButtons(plyr)
            else:
                self.createCallButtons(plyr)
        
    def call(self,plyr):
        room.table.call(plyr)
        room.tableWindow.updateTableChips()
        self.destroyButtons()
        if room.table.leftToAct != []:
            self.nextPlayer()
        else:
            self.endRound()
        
    # note Raise instead of raise
    def Raise(self,plyr,amount=0):
        try:
            amount = self.wagerEntry.get()
        except:
            pass
        room.table.Raise(plyr,amount)
        room.tableWindow.updateTableChips()
        self.destroyButtons()
        if room.table.leftToAct != []:
            self.nextPlayer()
        else:
            self.endRound()
        
    def fold(self,plyr):
        room.table.fold(plyr)
        room.tableWindow.updateTableChips()
        room.imageList[currentPlyr].c1.configure(image=room.noCard)
        room.imageList[currentPlyr].c2.configure(image=room.noCard)
        self.destroyButtons()
        if room.table.leftToAct != []:
            self.nextPlayer()
        else:
            self.endRound()
        
    def bet(self,plyr,amount=0):
        try:
            amount = self.wagerEntry.get()
        except:
            pass
        room.table.bet(plyr,amount)
        room.tableWindow.updateTableChips()
        self.destroyButtons()
        if room.table.leftToAct != []:
            self.nextPlayer()
        else:
            self.endRound()
    
    def check(self,plyr):
        room.table.check(plyr)
        room.tableWindow.updateTableChips()
        self.destroyButtons()
        if room.table.leftToAct != []:
            self.nextPlayer()
        else:
            self.endRound()
            
    def destroyButtons(self):
        try:
            self.b1.destroy()
            self.b2.destroy()
            self.b3.destroy()
            self.wagerEntry.destroy()
            self.card1.configure(image=None)
            self.card2.configure(image=None)
        except:
            pass
    
    
class Left_panel_buttons(tk.Frame):
    # creates buttons 
    def __init__(self,parent):
        tk.Frame.__init__(self,parent,bg='black',relief='ridge',bd=4)
        self.lpbg = Image.open('res/leftPanelbg.gif')
        self.img_copy= self.lpbg.copy()
        self.bgimg = ImageTk.PhotoImage(self.lpbg)
        self.bg = tk.Label(self,image=self.bgimg)
        self.bg.bind('<Configure>', self._resize_image)
        self.bg.pack(fill=tk.BOTH, expand=tk.YES)
        
        # Press to move dealer button, eliminates any busted players
        self.move_button_b = tk.Button(self.bg,takefocus=1, text='Move Button',highlightbackground='darkred',command=self.move_dlr_button)
        self.move_button_b.pack()
        
        # Press to deal 2 cards to all players
        self.deal_hole_b = tk.Button(self.bg,takefocus=1, text='Deal Cards',highlightbackground='darkred',command=self.deal_cards)
        self.deal_hole_b.pack()
        
        # Press to post blinds
        self.post_blinds_b = tk.Button(self.bg,takefocus=1, text='Post Blinds',highlightbackground='darkred',command=self.post_blinds)
        self.post_blinds_b.pack()
        
        # Press to start hand, get first action from player
        self.get_action_b = tk.Button(self.bg,takefocus=1,text='Get Action',highlightbackground='darkred',command=self.get_action)
        self.get_action_b.pack()
        
        # Press to reveal all hands
#         self.shwHands = tk.Button(self.bg,text='Show Hands',highlightbackground='darkred',command=self.showHands)
#         self.shwHands.pack()
        
        # Press to reset everything, should happen between hands
#         self.clnUp = tk.Button(self.bg,text='Clean',highlightbackground='darkred',command=self.cleanUp)
#         self.clnUp.pack()
        
    # move dealer button and eliminate busted players, called by self.move_button_b
    def move_dlr_button(self):
        room.table.move_button()
        room.imageList[room.table.playerOrder[-1]].dealerButton.configure(text='')
        room.imageList[room.table.playerOrder[0]].dealerButton.configure(text='Dealer')
        for plyr in room.table.playerOrder[:]:
            if room.table.playerDict[plyr].stackSize == 0:
                room.tableWindow.deletePlayer(plyr)
                
    # deals 2 cards to all players, called by self.deal button
    def deal_cards(self):
        room.table.deal_hole_cards()
        for plyr in room.table.player_order:
            room.imageList[plyr].c1.configure(image=room.cardBack)
            room.imageList[plyr].c2.configure(image=room.cardBack)
                
    # post blinds, called by self.pstBlinds button
    def post_blinds(self):
        room.table.post_blinds()
#         room.tableWindow.updateTableChips()
        
    # calls populate() to get the first action, called by self.gtActn button
    def get_action(self):
        options = room.table.get_legal_actions()
        print(options)
        if options == 'check_options':
            room.player_window.populate()
            room.player_window.create_check_buttons()
        elif options == 'call_options':
            room.player_window.create_call_buttons()
        elif options == 'bb_options':
            room.player_window.create_bb_option_buttons()
        room.player_window.populate()
        
    # reveal each player's hand, called by self.shwHands button
#     def showHands(self,event=None):
#         for plyr in room.table.playerOrder:
#             if room.table.playerDict[plyr].hand != []:
#                 room.imageList[plyr].img1 = ImageTk.PhotoImage(Image.open('cardImages/'+room.table.playerDict[plyr].hand[0]+'.gif'))
#                 room.imageList[plyr].c1.configure(image=room.imageList[plyr].img1)
#                 room.imageList[plyr].img2 = ImageTk.PhotoImage(Image.open('cardImages/'+room.table.playerDict[plyr].hand[1]+'.gif'))
#                 room.imageList[plyr].c2.configure(image=room.imageList[plyr].img2)
            
    # reset, called by self.clnUp button
#     def cleanUp(self):
#         room.tableWindow.clean()
        
    # resize background image on window resize
    def _resize_image(self,event):
        new_width = event.width # event.width is new window width
        new_height = event.height # event.height is new window height
        self.image = self.img_copy.resize((new_width, new_height)) # image becomes same size as window
        self.bgImg = ImageTk.PhotoImage(self.image) # change to ImageTk
        self.bg.configure(image = self.bgImg) 
            
            
            
class Start_game_bar(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self,parent,bg='black',relief='ridge',bd=4)
        self.b=tk.Button(self,takefocus=1,text="Start Game!",highlightbackground='black',command=self.startGameEntries)
        self.b.pack(side='left')
        self.quitButton = tk.Button(self,takefocus=1,text='Quit',highlightbackground='black',command=self.areYouSureQuit)
        self.quitButton.pack(side='left')
    
    def areYouSureQuit(self):
        self.quitGamePopup = QuitGamePopup(self)
        
    def startGameEntries(self):
        self.startGamePopup = StartGamePopup(self)
        self.wait_window(self.startGamePopup.top)
    
    
# holds all gui elements in middle window ("table" area), images for each player, community cards, chips
class Table_window(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self,parent,relief='ridge',bd=4)
        self.image = Image.open("res/background.gif") # open image as instance of self
        self.img_copy= self.image.copy() # copy made for later resizing
        self.background_image = ImageTk.PhotoImage(self.image) # changed to ImageTk
        self.background = tk.Label(self, image=self.background_image) # label as background
        self.background.bind('<Configure>', self._resize_image) # bind to resize window
        self.background.pack(fill=tk.BOTH, expand=tk.YES)
        
    # initialize pot and community cards gui area
    def createChipImages(self):
        self.chipFrame = tk.Frame(self.background,bg='black',relief='groove',bd=4)
        self.numFrame = tk.Frame(self.chipFrame,bg='black',relief='raised',bd=3)
        self.chips = tk.Label(self.numFrame,text=0,font=('Helvetica',22),bg='black',fg='wheat3')
        self.chips.pack(side='top')
        self.chipImage = tk.Label(self.numFrame,image=room.chips,bg='black')
        self.chipImage.pack(side='top')
        self.numFrame.pack(side='left')
        self.chipFrame.grid(row=2,column=1,columnspan=2)
        self.card1 = tk.Label(self.chipFrame,image=room.noCard,bg='black')
        self.card1.pack(side='left')
        self.card2 = tk.Label(self.chipFrame,image=room.noCard,bg='black')
        self.card2.pack(side='left')
        self.card3 = tk.Label(self.chipFrame,image=room.noCard,bg='black')
        self.card3.pack(side='left')
        self.card4 = tk.Label(self.chipFrame,image=room.noCard,bg='black')
        self.card4.pack(side='left')
        self.card5 = tk.Label(self.chipFrame,image=room.noCard,bg='black')
        self.card5.pack(side='left')
        
    # called after player decisions, update all player chips and pot chip amount
    def updateTableChips(self):
        self.chips.configure(text=room.table.pot)
        for plyr in room.table.playerOrder:
            room.imageList[plyr].stack.configure(text=room.table.playerDict[plyr].stackSize)
        
    # get and reveal gui images of dealt cards
    def dealFlop(self):
        self.card1img = ImageTk.PhotoImage(Image.open('cardImages/'+room.table.cardsInPlay[0]+'.gif'))
        self.card1.configure(image=self.card1img)
        self.card2img = ImageTk.PhotoImage(Image.open('cardImages/'+room.table.cardsInPlay[1]+'.gif'))
        self.card2.configure(image=self.card2img)
        self.card3img = ImageTk.PhotoImage(Image.open('cardImages/'+room.table.cardsInPlay[2]+'.gif'))
        self.card3.configure(image=self.card3img)
        
    def dealTurn(self):
        self.card4img = ImageTk.PhotoImage(Image.open('cardImages/'+room.table.cardsInPlay[3]+'.gif'))
        self.card4.configure(image=self.card4img)
        
    def dealRiver(self):
        self.card5img = ImageTk.PhotoImage(Image.open('cardImages/'+room.table.cardsInPlay[4]+'.gif'))
        self.card5.configure(image=self.card5img)
        
    # create room.imagelist dictionary, places images in seating order
    # reference the IMAGES on each players window like so:
    # room.imageList['player1'].stack, .c1 (card1), .c2 (card2)
    # create grid layout depending on number of players
    def createPlayerImages(self,plyrOrder):
        room.imageList = {}
        row = 1
        column = 1
        counter = 1
        for plyr in plyrOrder:
            self.w = tk.Frame(self.background,relief='ridge',bd=4,background='black')
            self.w.info = tk.Frame(self.w,relief='ridge',bd=3,background='black')
            self.w.plyrImg = ImageTk.PhotoImage(Image.open('cardImages/playerImage.gif').resize((60,50)))
            self.w.pic = tk.Label(self.w.info,image=self.w.plyrImg,bg='black')
            self.w.pic.pack(side='left')
            self.w.player = tk.Label(self.w.info,text=plyr,fg='wheat3',bg='black')
            self.w.player.pack(side='top')
            self.w.stack = tk.Label(self.w.info,text=room.table.playerDict[plyr].stackSize,bg='black',fg='wheat3')
            self.w.stack.pack(side='top')
            self.w.dealerButton = tk.Label(self.w.info,text = '',fg='wheat3',bg='black')
            self.w.dealerButton.pack(side='top')
            self.w.info.pack(side='top')
            self.w.c1 = tk.Label(self.w,image=room.noCard,background='black')
            self.w.c1.pack(side='left')
            self.w.c2 = tk.Label(self.w,image=room.noCard,background='black')
            self.w.c2.pack(side='left')
            self.w.grid(row=row,column=column,padx=25,pady=4)
            room.imageList[plyr] = self.w
            counter += 1
            # uses tkinter grid layout
            if counter < 5:
                column += 1
            elif counter == 5:
                column = 4
                row = 2
            elif counter == 6:
                column = 4
                row = 3
            elif counter == 7:
                column = 3
                row = 3
            elif counter == 8:
                column = 2
                row = 3
            elif counter == 9:
                column = 1
                row = 3
        room.imageList[room.table.playerOrder[0]].dealerButton.configure(text='Dealer')
            
    def deletePlayer(self,plyr):
        room.table.deletePlayer(plyr)
        room.imageList[plyr].destroy()
            
    # clean all gui elements for next hand, calls underlying table clean
    def clean(self):
        room.table.clean()
        for plyr in room.table.playerOrder:
            room.imageList[plyr].c1.configure(image=room.noCard)
            room.imageList[plyr].c2.configure(image=room.noCard)
        self.card1.configure(image=room.noCard)
        self.card2.configure(image=room.noCard)
        self.card3.configure(image=room.noCard)
        self.card4.configure(image=room.noCard)
        self.card5.configure(image=room.noCard)
        self.updateTableChips()
        room.playerWindow.card1.configure(image=room.noCard)
        room.playerWindow.card2.configure(image=room.noCard)
        room.playerWindow.plyrMsg.configure(text='')
        room.playerWindow.b1.destroy()
        room.playerWindow.b2.destroy()
        room.playerWindow.b3.destroy()
        room.playerWindow.wagerEntry.destroy()
        
    # resize background image
    def _resize_image(self,event):
        new_width = event.width # event.width is new window width
        new_height = event.height # event.height is new window height
        self.image = self.img_copy.resize((new_width, new_height)) # image becomes same size as window
        self.background_image = ImageTk.PhotoImage(self.image) # change to ImageTk
        self.background.configure(image =  self.background_image) 

class QuitGamePopup(object):
    def __init__(self,parent):
        self.top = tk.Toplevel(parent,bg='black',relief='ridge',bd=4)
        self.top.minsize(420,120)
        self.top.maxsize(420,120)
        self.players = tk.Label(self.top,text="Would You Like To Quit?",fg='burlywood1',bg='black',font=("Courier bold", 28))
        self.players.pack()
        self.yes = tk.Button(self.top,text='Yes',takefocus=1,font=("Gothic", 16),highlightbackground='black',command=self.getMeOutOfHere)
        self.yes.pack()
        self.no = tk.Button(self.top,takefocus=1,text="No, don't quit",font=("Gothic", 16),highlightbackground='black', command=self.top.destroy)
        self.no.pack()
        
    def getMeOutOfHere(self):
        self.top.destroy()
        sys.exit()

# still need to round down to closest factor of 20
# gets input from user numPlayers,stackSize,bigBlind 
# stored as room.numberOfPlayers,room.stackSize,room.bigBlindSize
class StartGamePopup(object):
    def __init__(self,root):
        self.top = tk.Toplevel(root,bg='black',relief='ridge',bd=4)
        self.top.geometry('700x360')
        self.top.grab_set()
        self.players = tk.Label(self.top,bg='black',fg='maroon',text="How Many players?\n2-9",font=('Courier bold',26))
        self.players.pack()
        self.playersEntry = tk.Scale(self.top,relief='raised',from_=2,to=9,orient='horizontal',bg='black',fg='red')
        self.playersEntry.pack()
        self.stackSize = tk.Label(self.top,bg='black',fg='maroon',text="What is the starting stack size?\nIncrements of 10, at least 100",font=('Courier bold',26))
        self.stackSize.pack()
        self.stackSizeEntry = tk.Scale(self.top,relief='raised',from_=200,to=10000,length=300,orient='horizontal',bg='black',fg='red',resolution=10,command=lambda x: self.bigBlindEntry.config(to=(self.stackSizeEntry.get()//10)))#need to round down to factor20 here
        self.stackSizeEntry.pack() 
        self.bigBlind = tk.Label(self.top,bg='black',fg='maroon',text="What is the big blind value?\nIncrements of 20,\n at most, ten percent of stack size",font=('Courier bold',26))
        self.bigBlind.pack()
        self.bigBlindEntry = tk.Scale(self.top,relief='raised',from_=20,to=self.stackSizeEntry.get(),resolution=20,orient='horizontal',fg='red',bg='black')
        self.bigBlindEntry.pack()
        self.b=tk.Button(self.top,bg='black',highlightbackground='maroon',relief='raised',text='Ok',fg='maroon',font=("Helvetica bold italic",26)\
       ,takefocus=1,command=self.start_game)
        self.b.pack()
    
    # When 'OK' is pressed after 'Start Game'
    def start_game(self):
        room.numberOfPlayers = self.playersEntry.get()
        room.stackSize = self.stackSizeEntry.get()
        room.bigBlindSize = self.bigBlindEntry.get()
        room.table = table.Table(big_blind=room.bigBlindSize,num_players=room.numberOfPlayers,num_chips=room.stackSize)
        plyrList = []
        for x in range(room.numberOfPlayers):
            plyrList.append('player'+str(x+1))
        self.top.destroy()
#         room.tableWindow.createPlayerImages(room.table.playerOrder)
#         room.tableWindow.createChipImages()
        

# just a geometry organizer for other classes
class Main_application(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        # 4 child widgets
        self.player_window = Player_window(self)
        self.left_panel_buttons = Left_panel_buttons(self)
        self.start_game_bar = Start_game_bar(self)
        self.table_window = Table_window(self)
        # geometry packer
        self.player_window.pack(side="bottom", fill="x")
        self.left_panel_buttons.pack(side="left", fill="y")
        self.start_game_bar.pack(side="top", fill="x")
        self.table_window.pack(side="right", fill="both", expand=True)
        # constant image references held in class that inherits from TK root
#         self.cardBack = ImageTk.PhotoImage(Image.open('cardImages/cardBack.gif'))
#         self.noCard = ImageTk.PhotoImage(Image.open('cardImages/noCard.gif'))
#         self.chips = ImageTk.PhotoImage(Image.open('cardImages/chips.gif'))
        

root = tk.Tk()
root.geometry('1000x700')

room = Main_application(root)
room.pack(fill=tk.BOTH, expand=tk.YES)

# table = table.Table(4,1000,20)
# table.post_blinds()

root.mainloop()
